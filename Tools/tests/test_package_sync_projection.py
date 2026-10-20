import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync_projection import Projection, TranslationNeedsReview, merge_independent_changes


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.projection = Projection({'Deucarian.Common': 'Simultria.Common',
                                      'DeucarianEasing': 'SimultriaEasing',
                                      'Deucarian': 'Simultria'},
                                     {'Simultria.Common': 'Deucarian.Common',
                                      'SimultriaEasing': 'DeucarianEasing'})

    def test_unchanged_native_product_names_are_preserved(self):
        original = 'namespace Deucarian.Common { string product = "Simultria"; int speed = 1; }'
        incoming = self.projection.forward(original).replace('speed = 1', 'speed = 2')
        self.assertEqual(original.replace('speed = 1', 'speed = 2'),
                         self.projection.reverse_change(original, incoming))

    def test_known_new_identifier_is_translated(self):
        original = 'namespace Deucarian.Common {\n}\n'
        incoming = 'namespace Simultria.Common {\n  SimultriaEasing value;\n}\n'
        expected = 'namespace Deucarian.Common {\n  DeucarianEasing value;\n}\n'
        self.assertEqual(expected, self.projection.reverse_change(original, incoming))

    def test_ambiguous_new_branding_requires_review(self):
        original = 'namespace Deucarian.Common {\n}\n'
        incoming = 'namespace Simultria.Common {\n  string product = "Simultria";\n}\n'
        with self.assertRaises(TranslationNeedsReview):
            self.projection.reverse_change(original, incoming)

    def test_partial_brand_rename_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            self.projection.reverse_change('Deucarian.Common', 'Simultrio.Common')

    def test_replacing_known_namespaces_does_not_split_translated_identity(self):
        projection = Projection(
            {'Deucarian.SimultriaViewerIntegration': 'Simultria.ViewerConnection',
             'Deucarian.Simultria.API': 'Simultria.Backend.API'},
            {'Simultria.ViewerConnection': 'Deucarian.SimultriaViewerIntegration',
             'Simultria.Backend.API': 'Deucarian.Simultria.API'})
        original = 'using Deucarian.SimultriaViewerIntegration;'
        incoming = 'using Simultria.Backend.API.Models;'
        result = projection.reverse_change(original, incoming)
        self.assertEqual('using Deucarian.Simultria.API.Models;', result)
        self.assertEqual(incoming, projection.forward(result))

    def test_multiple_import_edits_translate_whole_longest_tokens(self):
        projection = Projection(
            {'Deucarian.SimultriaViewerIntegration': 'Simultria.ViewerConnection',
             'Deucarian.Simultria.API': 'Simultria.Backend.API',
             'Deucarian': 'Simultria'},
            {'Simultria.ViewerConnection': 'Deucarian.SimultriaViewerIntegration',
             'Simultria.Backend.API': 'Deucarian.Simultria.API'})
        original = ('using Deucarian.Simultria.API.Services;\n'
                    'using Deucarian.SimultriaViewerIntegration;\n')
        incoming = ('using Simultria.Backend.API;\nusing Simultria.Backend.API.Generated;\n'
                    'using Simultria.Backend.API.Models;\n')
        expected = ('using Deucarian.Simultria.API;\nusing Deucarian.Simultria.API.Generated;\n'
                    'using Deucarian.Simultria.API.Models;\n')
        self.assertEqual(expected, projection.reverse_change(original, incoming))

    def test_token_replacement_preserves_separate_host_overlay_and_native_product_name(self):
        original = ('Deucarian.Common service;\nline2;\nline3;\nline4;\n'
                    'string host = "github";\nstring product = "Simultria";\n')
        baseline = self.projection.forward(original).replace('"github"', '"bitbucket"')
        incoming = baseline.replace('Simultria.Common service', 'SimultriaEasing curve')
        expected = original.replace('Deucarian.Common service', 'DeucarianEasing curve')
        self.assertEqual(expected, self.projection.reverse_change(original, incoming, baseline))

    def test_atomic_token_diff_does_not_allow_host_overlay_to_be_replaced(self):
        original = 'Deucarian.Common service;\n'
        baseline = self.projection.forward(original).replace('Simultria.Common', 'Simultria.HostOnly')
        incoming = 'SimultriaEasing service;\n'
        with self.assertRaises(TranslationNeedsReview):
            self.projection.reverse_change(original, incoming, baseline)

    def test_unmapped_token_replacement_still_requires_review(self):
        with self.assertRaises(TranslationNeedsReview):
            self.projection.reverse_change('Deucarian.Common value;', 'Simultria.Unknown value;')

    def test_replay_is_idempotent(self):
        original = 'namespace Deucarian.Common { int value = 1; }'
        self.assertEqual(original, self.projection.reverse_change(original, self.projection.forward(original)))

    def test_host_specific_metadata_is_preserved_while_shared_code_changes(self):
        original = 'namespace Deucarian.Common\n{\n  int first = 1;\n  int second = 2;\n  int third = 3;\n  string host = "github";\n}\n'
        baseline = self.projection.forward(original).replace('"github"', '"bitbucket"')
        incoming = baseline.replace('first = 1', 'first = 9')
        self.assertEqual(original.replace('first = 1', 'first = 9'),
                         self.projection.reverse_change(original, incoming, baseline))

    def test_game_rows_absent_from_bitbucket_are_not_deleted_from_github(self):
        original = 'shared-a = 1;\nline-b;\nline-c;\nline-d;\ngame-only = retained;\nend;\n'
        baseline = original.replace('game-only = retained;\n', '')
        incoming = baseline.replace('shared-a = 1', 'shared-a = 2')
        self.assertEqual(original.replace('shared-a = 1', 'shared-a = 2'),
                         self.projection.reverse_change(original, incoming, baseline))

    def test_editing_a_host_specific_overlay_requires_review(self):
        original = 'namespace Deucarian.Common { string host = "github"; }'
        baseline = self.projection.forward(original).replace('"github"', '"bitbucket"')
        with self.assertRaises(TranslationNeedsReview):
            self.projection.reverse_change(original, baseline.replace('"bitbucket"', '"changed"'), baseline)

    def test_overlapping_changes_are_not_silently_overwritten(self):
        with self.assertRaises(TranslationNeedsReview):
            merge_independent_changes(b'value = 2;\n', b'value = 1;\n', b'value = 3;\n')

    def test_independent_changes_merge(self):
        baseline = b'first = 1;\na\nb\nc\nlast = 1;\n'
        current = baseline.replace(b'first = 1', b'first = 2')
        incoming = baseline.replace(b'last = 1', b'last = 2')
        self.assertEqual(current.replace(b'last = 1', b'last = 2'),
                         merge_independent_changes(current, baseline, incoming))


if __name__ == '__main__':
    unittest.main()
