import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from package_sync_projection import TranslationNeedsReview
from package_sync_tree import Blob, merge_trees, translate_tree

PROFILE = {'packageIds': {'com.deucarian.common': 'com.simultria.common'},
           'namespaceOverrides': {'Deucarian.Common': 'Simultria.Common'}, 'repositories': {}}


def blob(text, mode='100644'):
    return Blob(mode, text.encode() if isinstance(text, str) else text)


class TreeTests(unittest.TestCase):
    def test_change_preserves_original_path_and_product_names(self):
        original = {'Deucarian.Common.cs': blob('namespace Deucarian.Common { string name = "Simultria"; int value = 1; }')}
        baseline = {'Simultria.Common.cs': blob('namespace Simultria.Common { string name = "Simultria"; int value = 1; }')}
        incoming = {'Simultria.Common.cs': blob(baseline['Simultria.Common.cs'].data.replace(b'value = 1', b'value = 2'))}
        result, changed = translate_tree(original, baseline, incoming, PROFILE)
        self.assertEqual(['Deucarian.Common.cs'], changed)
        self.assertEqual(original['Deucarian.Common.cs'].data.replace(b'value = 1', b'value = 2'), result[changed[0]].data)

    def test_github_workflow_cannot_be_replaced_from_bitbucket(self):
        original = {'.github/workflows/run.yml': blob('trusted')}
        result, changed = translate_tree(original, {}, {'.github/workflows/run.yml': blob('untrusted')}, PROFILE)
        self.assertEqual(original, result)
        self.assertFalse(changed)

    def test_excluded_game_file_survives(self):
        original = {'game.json': blob('keep'), 'file.cs': blob('value = 1;')}
        baseline = {'file.cs': original['file.cs']}
        result, _ = translate_tree(original, baseline, {'file.cs': blob('value = 2;')}, PROFILE)
        self.assertEqual(original['game.json'], result['game.json'])

    def test_new_file_known_namespace_translates(self):
        result, _ = translate_tree({}, {}, {'Feature.cs': blob('namespace Simultria.Common { }')}, PROFILE)
        self.assertEqual(blob('namespace Deucarian.Common { }'), result['Feature.cs'])

    def test_new_ambiguous_brand_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            translate_tree({}, {}, {'Feature.cs': blob('string product = "Simultria";')}, PROFILE)

    def test_host_only_code_edit_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            translate_tree({}, {'Private.cs': blob('one')}, {'Private.cs': blob('two')}, PROFILE)

    def test_unmodified_binary_can_be_updated(self):
        old = {'file.bin': blob(b'\0one')}
        new = {'file.bin': blob(b'\0two')}
        result, _ = translate_tree(old, old, new, PROFILE)
        self.assertEqual(new, result)

    def test_conflicting_binary_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            merge_trees({'file': blob(b'\0local')}, {'file': blob(b'\0base')}, {'file': blob(b'\0incoming')})

    def test_source_deletion_is_translated(self):
        original = {'Deucarian.Common.cs': blob('namespace Deucarian.Common { }')}
        baseline = {'Simultria.Common.cs': blob('namespace Simultria.Common { }')}
        result, _ = translate_tree(original, baseline, {}, PROFILE)
        self.assertFalse(result)

    def test_deletion_of_host_overlay_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            translate_tree({'file': blob('local host')}, {'file': blob('remote host')}, {}, PROFILE)

    def test_symlink_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            translate_tree({}, {}, {'file': blob('../../secret', '120000')}, PROFILE)

    def test_traversal_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            translate_tree({}, {}, {'../escape': blob('source')}, PROFILE)

    def test_independent_local_edits_survive(self):
        baseline = {'file': blob('first = 1\na\nb\nc\nlast = 1\n')}
        local = {'file': blob('first = 2\na\nb\nc\nlast = 1\n')}
        incoming = {'file': blob('first = 1\na\nb\nc\nlast = 2\n')}
        result = merge_trees(local, baseline, incoming)
        self.assertEqual(blob('first = 2\na\nb\nc\nlast = 2\n'), result['file'])

    def test_delete_modify_conflict_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            merge_trees({'file': blob('local')}, {'file': blob('base')}, {})


if __name__ == '__main__':
    unittest.main()
