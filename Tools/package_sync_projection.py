"""Conservative source translation; contains no remote or publication code.

An incoming change is applied to the source that produced the translated baseline.
Unchanged brand text is restored from that source, not guessed by global replacement.
Only explicitly mapped identifiers may be introduced automatically in the reverse direction.
"""
from __future__ import annotations

import difflib
import re
import subprocess
import tempfile
from pathlib import Path


class TranslationNeedsReview(ValueError):
    pass


class Projection:
    def __init__(self, forward_rules: dict[str, str], reverse_identifier_rules: dict[str, str],
                 ambiguous_identifiers=(), reverse_exact_rules: dict[str, str] | None = None,
                 ambiguous_exact_identifiers=()):
        self.rules = forward_rules
        self.pattern = self.compile(forward_rules)
        self.reverse_rules = reverse_identifier_rules
        self.reverse_pattern = self.compile(reverse_identifier_rules)
        self.ambiguous_pattern = self.compile(dict.fromkeys(ambiguous_identifiers, ''))
        self.reverse_exact_rules = reverse_exact_rules or {}
        self.ambiguous_exact_identifiers = set(ambiguous_exact_identifiers)
        self.compile(self.reverse_exact_rules)
        self.compile(dict.fromkeys(self.ambiguous_exact_identifiers, ''))
        self.target_pattern = self.compile({value: '' for value in forward_rules.values() if value})

    @staticmethod
    def compile(rules):
        if any(not key for key in rules):
            raise ValueError('Empty translation key')
        return re.compile('|'.join(re.escape(key) for key in sorted(rules, key=len, reverse=True)) or r'(?!)')

    def _exact_tokens(self, text, allow_unquoted=True):
        identities = self.reverse_exact_rules.keys() | self.ambiguous_exact_identifiers
        if not identities:
            return
        if allow_unquoted and text in identities:
            yield 0, len(text), text, '', ''
            return
        # Consume whole quoted values, including escaped and C# verbatim quotes.
        # A resource-looking substring inside a longer value is never a load-path identity.
        quoted = r'''(?<!\\)(?:@"(?:[^"]|"")*"|"(?:\\.|[^"\\\r\n])*"|'(?:\\.|[^'\\\r\n])*')'''
        for match in re.finditer(quoted, text):
            token = match.group()
            prefix = '@"' if token.startswith('@"') else token[0]
            identity = token[len(prefix):-1]
            if identity in identities:
                yield match.start(), match.end(), identity, prefix, token[-1]

    def forward(self, source: str):
        return self.pattern.sub(lambda match: self.rules[match.group()], source)

    def mapped_baseline(self, source):
        """Map translated text boundaries back to their unambiguous source boundaries."""
        result = []
        boundaries = [0]
        cursor = 0
        for match in self.pattern.finditer(source):
            result.append(source[cursor:match.start()])
            boundaries.extend(range(cursor + 1, match.start() + 1))
            replacement = self.rules[match.group()]
            if not replacement:
                raise TranslationNeedsReview('Deleting a branding token requires review')
            result.append(replacement)
            boundaries.extend([None] * (len(replacement) - 1))
            boundaries.append(match.end())
            cursor = match.end()
        result.append(source[cursor:])
        boundaries.extend(range(cursor + 1, len(source) + 1))
        text = ''.join(result)
        assert len(boundaries) == len(text) + 1
        return text, boundaries

    def reverse_insert(self, inserted, *, allow_unquoted_exact=True):
        if self.ambiguous_pattern.search(inserted):
            raise TranslationNeedsReview('Identifier has multiple source mappings')
        parts = []
        cursor = 0
        for start, end, identity, prefix, suffix in self._exact_tokens(inserted, allow_unquoted_exact):
            if identity in self.ambiguous_exact_identifiers:
                raise TranslationNeedsReview('Identifier has multiple source mappings')
            parts.append(self._reverse_identifiers(inserted[cursor:start]))
            parts.append(prefix + self.reverse_exact_rules[identity] + suffix)
            cursor = end
        parts.append(self._reverse_identifiers(inserted[cursor:]))
        return ''.join(parts)

    def _reverse_identifiers(self, inserted):
        # Protect only approved, complete identifiers/qualified prefixes. Bare product names
        # are ambiguous: Simultria can be original business terminology or translated branding.
        parts = []
        cursor = 0
        for match in self.reverse_pattern.finditer(inserted):
            if re.search(r'Simultria|simultria|SIMULTRIA', inserted[cursor:match.start()]):
                raise TranslationNeedsReview('New brand text has no explicit inverse mapping')
            parts.append(inserted[cursor:match.start()])
            parts.append(self.reverse_rules[match.group()])
            cursor = match.end()
        if re.search(r'Simultria|simultria|SIMULTRIA', inserted[cursor:]):
            raise TranslationNeedsReview('New brand text has no explicit inverse mapping')
        parts.append(inserted[cursor:])
        return ''.join(parts)

    def _target_tokens(self, text):
        """Keep known translated tokens indivisible, with original character offsets."""
        tokens = []
        cursor = 0
        for match in self.target_pattern.finditer(text):
            tokens.extend(text[cursor:match.start()])
            tokens.append(match.group())
            cursor = match.end()
        tokens.extend(text[cursor:])
        offsets = [0]
        for token in tokens:
            offsets.append(offsets[-1] + len(token))
        return tokens, offsets

    def _change_opcodes(self, baseline, incoming, boundaries):
        opcodes = difflib.SequenceMatcher(None, baseline, incoming, autojunk=False).get_opcodes()
        split_changes = [(start, end) for operation, start, end, _, _ in opcodes
                         if operation != 'equal' and (boundaries[start] is None or boundaries[end] is None)]
        if not split_changes:
            return opcodes
        before, before_offsets = self._target_tokens(baseline)
        after, after_offsets = self._target_tokens(incoming)
        result = []
        for operation, start, end, new_start, new_end in difflib.SequenceMatcher(
                None, before, after, autojunk=False).get_opcodes():
            start, end = before_offsets[start], before_offsets[end]
            new_start, new_end = after_offsets[new_start], after_offsets[new_end]
            if (operation not in ('equal', 'delete')
                    and any(start <= split_start <= split_end <= end for split_start, split_end in split_changes)
                    and not self.reverse_pattern.search(incoming[new_start:new_end])
                    and not any(self._exact_tokens(incoming[new_start:new_end]))):
                # Expanding a partial typo into a whole-token replacement must
                # not make an unknown renamed identity silently acceptable.
                raise TranslationNeedsReview('Change overlaps the interior of a renamed identifier')
            result.append((operation, start, end, new_start, new_end))
        return result

    def reverse_change(self, github_baseline: str, bitbucket_changed: str, bitbucket_baseline: str | None = None):
        translated, boundaries = self.mapped_baseline(github_baseline)
        baseline = translated if bitbucket_baseline is None else bitbucket_baseline
        overlay_positions = set()
        if baseline != translated:
            mapped = [None] * (len(baseline) + 1)
            for operation, start, end, new_start, new_end in difflib.SequenceMatcher(
                    None, translated, baseline, autojunk=False).get_opcodes():
                if operation == 'equal':
                    mapped[new_start:new_end + 1] = boundaries[start:end + 1]
                else:
                    overlay_positions.update(range(new_start, new_end + 1))
            boundaries = mapped
        edits = []
        exact_value_spans = {
            (start + len(prefix), end - len(suffix))
            for start, end, _, prefix, suffix in self._exact_tokens(bitbucket_changed)
        }
        for operation, start, end, new_start, new_end in self._change_opcodes(
                baseline, bitbucket_changed, boundaries):
            if operation == 'equal':
                continue
            before, after = boundaries[start], boundaries[end]
            if any(position in overlay_positions for position in range(start, end + 1)):
                raise TranslationNeedsReview('Change overlaps a host-specific baseline difference')
            if before is None or after is None:
                raise TranslationNeedsReview('Change overlaps the interior of a renamed identifier')
            replacement = self.reverse_insert(
                bitbucket_changed[new_start:new_end],
                allow_unquoted_exact=(new_start, new_end) in exact_value_spans,
            )
            edits.append((before, after, replacement))
        result = github_baseline
        for start, end, replacement in reversed(edits):
            result = result[:start] + replacement + result[end:]
        expected = self.forward(result)
        if baseline != translated:
            expected = merge_independent_changes(baseline.encode(), translated.encode(), expected.encode()).decode()
        if expected != bitbucket_changed:
            raise TranslationNeedsReview('Translation failed the exact forward projection check')
        return result


def merge_independent_changes(current: bytes, baseline: bytes, incoming: bytes):
    """Return a clean three-way merge; never use the result of a conflicting merge."""
    with tempfile.TemporaryDirectory(prefix='package-sync-') as directory:
        paths = [Path(directory) / name for name in ('current', 'baseline', 'incoming')]
        for path, value in zip(paths, (current, baseline, incoming)):
            path.write_bytes(value)
        result = subprocess.run(['git', 'merge-file', '-p', *(str(path) for path in paths)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise TranslationNeedsReview('Both versions changed overlapping source; manual merge required')
    return result.stdout
