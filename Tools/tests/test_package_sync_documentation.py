import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from package_sync_documentation import align_host_documentation
from package_sync_projection import TranslationNeedsReview
from package_sync_tree import Blob


REVISION = '1234567890abcdef1234567890abcdef12345678'
SOURCE = 'https://bitbucket.org/simultria/api.git'


def blob(text, mode='100644'):
    return Blob(mode, text.encode() if isinstance(text, str) else text)


def package_tree(readme=None, changelog=None, version='2.2.0'):
    tree = {'package.json': blob(json.dumps({'name': 'com.deucarian.api', 'version': version}))}
    if readme is not None:
        tree['README.md'] = blob(readme)
    if changelog is not None:
        tree['CHANGELOG.md'] = blob(changelog)
    return tree


class DocumentationTests(unittest.TestCase):
    def align(self, tree, revision=REVISION, url=SOURCE):
        return align_host_documentation(tree, revision, url)

    def test_api_release_metadata_aligns_without_rewriting_history_or_examples(self):
        readme = '# API\nCurrent package version: `2.1.1`.\nExample URL: https://host/2.1.1\n'
        history = '## 2.1.1 - Unreleased\n\n- Existing local documentation.\n\n## [2.1.0] - 2026-09-01\n'
        tree = package_tree(readme, '# Changelog\n\n' + history)
        tree['Documentation~/Overview.md'] = blob('Keep 2.1.1 and Simultria product references.')
        original = dict(tree)
        result, changed = self.align(tree)
        self.assertEqual(['README.md', 'CHANGELOG.md'], changed)
        self.assertEqual(readme.replace('`2.1.1`', '`2.2.0`').encode(), result['README.md'].data)
        self.assertIn(b'## [2.2.0] - Upstream synchronization', result['CHANGELOG.md'].data)
        self.assertIn(f'https://bitbucket.org/simultria/api/commits/{REVISION}'.encode(),
                      result['CHANGELOG.md'].data)
        self.assertTrue(result['CHANGELOG.md'].data.endswith(history.encode()))
        self.assertEqual(tree['Documentation~/Overview.md'], result['Documentation~/Overview.md'])
        self.assertEqual(original, tree)

    def test_repeated_sync_is_byte_identical_and_adds_no_duplicate_entry(self):
        tree = package_tree('Current package version: `2.1.1`.\n', '# Changelog\n\n## [2.1.1]\nNotes.\n')
        once, _ = self.align(tree)
        twice, changed = self.align(once, revision='f' * 40)
        self.assertEqual(once, twice)
        self.assertEqual([], changed)

    def test_supported_readme_declarations_keep_table_and_inline_formatting(self):
        for declaration in ('| Package version | `2.1.1` |', '| Version | 2.1.1 |',
                            '- Current package version: 2.1.1.', 'current package VERSION | `2.1.1`.',
                            'Current package version: `2.1.1`', 'Current package version: 2.1.1'):
            with self.subTest(declaration=declaration):
                result, changed = self.align(package_tree(declaration + '\n'))
                self.assertEqual(['README.md'], changed)
                self.assertEqual((declaration.replace('2.1.1', '2.2.0') + '\n').encode(),
                                 result['README.md'].data)

    def test_consistent_multiple_declarations_align_together(self):
        text = 'Current package version: `2.1.1`.\n| Version | 2.1.1 |\n'
        result, _ = self.align(package_tree(text))
        self.assertEqual(text.replace('2.1.1', '2.2.0').encode(), result['README.md'].data)

    def test_conflicting_declarations_require_review(self):
        with self.assertRaisesRegex(TranslationNeedsReview, 'conflicting'):
            self.align(package_tree('Current package version: 2.1.1.\n| Version | 1.0.0 |\n'))

    def test_unrecognized_version_values_are_not_rewritten(self):
        for value in ('latest', '2.1', '2.1.1-preview.1', '2.1.10oops'):
            with self.subTest(value=value), self.assertRaisesRegex(TranslationNeedsReview, 'unsupported'):
                self.align(package_tree(f'Current package version: `{value}`.\n'))

    def test_fenced_examples_and_readme_without_declaration_are_unchanged(self):
        for fence in ('```', '~~~'):
            tree = package_tree(f'# API\n{fence}markdown\nCurrent package version: `1.0.0`.\n{fence}\n')
            result, changed = self.align(tree)
            self.assertEqual(tree, result)
            self.assertEqual([], changed)

    def test_missing_manifest_or_optional_documentation_is_preserved(self):
        for tree in ({}, {'README.md': blob('Host documentation')}, package_tree()):
            with self.subTest(tree=tree):
                result, changed = self.align(tree)
                self.assertEqual(tree, result)
                self.assertEqual([], changed)

    def test_existing_current_changelog_notes_are_not_replaced(self):
        tree = package_tree(changelog='# Changelog\n\n## 2.2.0 - Unreleased\n\n- Handwritten release notes.\n')
        result, changed = self.align(tree)
        self.assertEqual(tree, result)
        self.assertEqual([], changed)

    def test_unreleased_section_and_preamble_are_preserved_before_new_release(self):
        prefix = '# Changelog\n\nIntroduction.\n\n## [Unreleased]\n\n- Pending local work.\n\n'
        history = '## [2.1.1] - 2026-09-01\n\n- Previous release.\n'
        result, _ = self.align(package_tree(changelog=prefix + history))
        text = result['CHANGELOG.md'].data.decode()
        self.assertTrue(text.startswith(prefix + '## [2.2.0]'))
        self.assertTrue(text.endswith(history))

    def test_encoding_line_endings_and_file_mode_survive(self):
        tree = package_tree('Current package version: `2.1.1`.\r\n', '# Changelog\r\n\r\n## 2.1.1\r\n')
        for name in ('README.md', 'CHANGELOG.md'):
            tree[name] = Blob('100755', b'\xef\xbb\xbf' + tree[name].data)
        result, _ = self.align(tree)
        for name in ('README.md', 'CHANGELOG.md'):
            self.assertEqual('100755', result[name].mode)
            self.assertTrue(result[name].data.startswith(b'\xef\xbb\xbf'))
            self.assertNotIn(b'\n', result[name].data.replace(b'\r\n', b''))

    def test_unsupported_changelog_requires_review(self):
        for text in ('# Changelog\n', '# Changelog\n\n## Next release\n\nNotes.\n',
                     '# Changelog\n\n## [2.1.1\n', '# Changelog\n\n## 2.1.1-preview.1\n\n## 1.0.0\n'):
            with self.subTest(text=text), self.assertRaisesRegex(TranslationNeedsReview, 'release heading'):
                self.align(package_tree(changelog=text))

    def test_existing_older_target_entry_is_not_duplicated_or_reordered(self):
        with self.assertRaisesRegex(TranslationNeedsReview, 'already exists'):
            self.align(package_tree(changelog='# Changelog\n\n## 3.0.0\n\n## 2.2.0\n'))

    def test_exempt_changelog_is_preserved(self):
        tree = package_tree(changelog='# Host-specific changelog\n')
        tree['deucarian-package.json'] = blob('{"changelogVersionExempt": true}')
        result, changed = self.align(tree)
        self.assertEqual(tree, result)
        self.assertEqual([], changed)

    def test_malformed_or_unsupported_manifest_requires_review(self):
        for contents in ('{', '[]', '{}', '{"version": 2}', '{"version": "2.2.0-beta.1"}'):
            with self.subTest(contents=contents), self.assertRaises(TranslationNeedsReview):
                self.align({'package.json': blob(contents)})

    def test_binary_symlink_and_invalid_text_documentation_are_rejected(self):
        for invalid in (blob(b'\xff'), blob(b'\0binary'), blob('somewhere', '120000')):
            tree = package_tree()
            tree['README.md'] = invalid
            with self.subTest(invalid=invalid), self.assertRaises(TranslationNeedsReview):
                self.align(tree)

    def test_source_reference_has_full_revision_and_optional_github_link(self):
        tree = package_tree(changelog='# Changelog\n\n## 2.1.1\n')
        result, _ = self.align(tree, url=None)
        self.assertIn(f'upstream commit `{REVISION}`'.encode(), result['CHANGELOG.md'].data)
        result, _ = self.align(tree, url='https://github.com/example/package/')
        self.assertIn(f'https://github.com/example/package/commit/{REVISION}'.encode(),
                      result['CHANGELOG.md'].data)

    def test_invalid_revision_or_credential_bearing_url_cannot_enter_documentation(self):
        tree = package_tree(changelog='# Changelog\n\n## 2.1.1\n')
        for url in ('https://user:secret@bitbucket.org/simultria/api', 'http://bitbucket.org/simultria/api',
                    'https://bitbucket.org/simultria/api?token=secret', 'https://example.com/org/repo',
                    'https://bitbucket.org/simultria/api#fragment'):
            with self.subTest(url=url), self.assertRaises(TranslationNeedsReview):
                self.align(tree, url=url)
        with self.assertRaises(TranslationNeedsReview):
            self.align(tree, revision='short-sha')


if __name__ == '__main__':
    unittest.main()
