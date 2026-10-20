"""Align host-owned release metadata without importing upstream Markdown."""
from __future__ import annotations

import json
import re
from urllib.parse import urlsplit

from package_sync_projection import TranslationNeedsReview
from package_sync_tree import Blob


VERSION = r'\d+\.\d+\.\d+'
README_DECLARATION = re.compile(
    r'(?im)^(?:[ \t]*[-*][ \t]+)?[ \t]*Current package version[ \t]*[:|][ \t]*'
    r'|^[ \t]*\|[ \t]*(?:Package version|Version)[ \t]*\|[ \t]*'
)
README_VALUE = re.compile(
    rf'(?P<quote>`)?(?P<version>{VERSION})(?(quote)`)'
    r'(?=[ \t]*(?:\.(?:[ \t]|\r?$)|\||\r?$))', re.M
)
RELEASE_HEADING = re.compile(
    rf'(?m)^##[ \t]+(?P<bracket>\[)?(?P<version>{VERSION})(?(bracket)\])'
    r'(?=(?:[ \t]+-[ \t]+|[ \t]*\r?$))'
)


def _text(name: str, blob: Blob) -> str:
    if blob.mode not in ('100644', '100755'):
        raise TranslationNeedsReview(f'{name}: documentation must be a regular file')
    try:
        text = blob.data.decode('utf-8-sig')
    except UnicodeDecodeError as error:
        raise TranslationNeedsReview(f'{name}: expected UTF-8 text') from error
    if '\0' in text:
        raise TranslationNeedsReview(f'{name}: expected text, found binary data')
    return text


def _replace_blob(original: Blob, text: str) -> Blob:
    prefix = b'\xef\xbb\xbf' if original.data.startswith(b'\xef\xbb\xbf') else b''
    return Blob(original.mode, prefix + text.encode('utf-8'))


def _json_document(name: str, blob: Blob) -> dict:
    try:
        value = json.loads(_text(name, blob))
    except json.JSONDecodeError as error:
        raise TranslationNeedsReview(f'{name}: invalid JSON') from error
    if not isinstance(value, dict):
        raise TranslationNeedsReview(f'{name}: expected a JSON object')
    return value


def _without_fences(text: str) -> str:
    """Mask fenced examples while retaining exact offsets in the original text."""
    fence = None
    lines = []
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^[ \t]{0,3}(`{3,}|~{3,})', line)
        inside = fence is not None
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
                inside = True
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        lines.append(re.sub(r'[^\r\n]', ' ', line) if inside else line)
    return ''.join(lines)


def _align_readme(text: str, version: str) -> str:
    matches = []
    visible = _without_fences(text)
    for declaration in README_DECLARATION.finditer(visible):
        value = README_VALUE.match(visible, declaration.end())
        if value is None:
            raise TranslationNeedsReview('README.md: unsupported package version declaration')
        matches.append(value)
    if len({match.group('version') for match in matches}) > 1:
        raise TranslationNeedsReview('README.md: conflicting package version declarations')
    for match in reversed(matches):
        start, end = match.span('version')
        text = text[:start] + version + text[end:]
    return text


def _commit_reference(revision: str, repository_url: str | None) -> str:
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise TranslationNeedsReview('Documentation synchronization requires a full upstream commit SHA')
    if repository_url is None:
        return f'upstream commit `{revision}`'
    parsed = urlsplit(repository_url)
    if (parsed.scheme != 'https' or parsed.netloc not in ('bitbucket.org', 'github.com')
            or not re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?', parsed.path)
            or parsed.query or parsed.fragment):
        raise TranslationNeedsReview('Documentation source URL must be a credential-free repository HTTPS URL')
    base = repository_url.rstrip('/')
    if base.endswith('.git'):
        base = base[:-4]
    segment = 'commits' if parsed.netloc == 'bitbucket.org' else 'commit'
    return f'[upstream commit `{revision}`]({base}/{segment}/{revision})'


def _align_changelog(text: str, version: str, reference: str) -> str:
    visible = _without_fences(text)
    releases = list(RELEASE_HEADING.finditer(visible))
    starts = {match.start() for match in releases}
    if any(match.start() not in starts for match in re.finditer(r'(?m)^##[ \t]+\[?\d', visible)):
        raise TranslationNeedsReview('CHANGELOG.md: unsupported release heading')
    if releases and releases[0].group('version') == version:
        return text
    if any(match.group('version') == version for match in releases):
        raise TranslationNeedsReview('CHANGELOG.md: incoming version already exists below the latest entry')
    if not releases:
        raise TranslationNeedsReview('CHANGELOG.md: no supported release heading; preserve it for manual review')
    newline = '\r\n' if '\r\n' in text else '\n'
    entry = newline.join([
        f'## [{version}] - Upstream synchronization', '',
        f'- Synchronize package version {version} from {reference}.', '', '',
    ])
    position = releases[0].start()
    return text[:position] + entry + text[position:]


def align_host_documentation(
        tree: dict[str, Blob], source_revision: str,
        source_repository_url: str | None = None) -> tuple[dict[str, Blob], list[str]]:
    """Return a copy with only explicit README version and changelog metadata aligned.

    Call after translating and merging package code, using the incoming upstream
    revision and its repository URL. Existing Markdown, history, absent files,
    and documentation without a README version declaration remain host-owned.
    No new release entry is added when the latest entry already has this version.
    Unsupported or conflicting release metadata requires review rather than a guess.
    """
    result = dict(tree)
    if 'package.json' not in tree:
        return result, []
    manifest = _json_document('package.json', tree['package.json'])
    version = manifest.get('version')
    if not isinstance(version, str) or not re.fullmatch(VERSION, version):
        raise TranslationNeedsReview('package.json: documentation alignment requires a stable x.y.z version')
    config = (_json_document('deucarian-package.json', tree['deucarian-package.json'])
              if 'deucarian-package.json' in tree else {})
    changed = []
    for name in ('README.md', 'CHANGELOG.md'):
        if name not in tree or (name == 'CHANGELOG.md' and config.get('changelogVersionExempt', False)):
            continue
        original = tree[name]
        text = _text(name, original)
        if name == 'README.md':
            updated = _align_readme(text, version)
        else:
            updated = _align_changelog(text, version, _commit_reference(source_revision, source_repository_url))
        if updated != text:
            result[name] = _replace_blob(original, updated)
            changed.append(name)
    return result, changed
