import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from package_sync_projection import TranslationNeedsReview
from package_sync_tree import Blob, merge_trees, projection_for, translate_tree

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

    def test_domain_adapter_preserves_new_business_identifiers(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        manifest = blob(json.dumps({'name': 'com.deucarian.simultria-api'}))
        original = {'package.json': manifest}
        incoming = {**original, 'Generated/SimultriaApiClient.contract.json': blob(
            '{"client":"SimultriaApiClient","namespace":"Simultria.Common"}')}
        result, changed = translate_tree(original, original, incoming, profile)
        self.assertEqual(['Generated/SimultriaApiClient.contract.json'], changed)
        self.assertEqual(blob('{"client":"SimultriaApiClient","namespace":"Deucarian.Common"}'),
                         result[changed[0]])

    def test_native_brand_policy_does_not_apply_to_generic_packages(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.common"}')}
        with self.assertRaises(TranslationNeedsReview):
            translate_tree(original, original, {**original, 'SimultriaNew.cs': blob('new')}, profile)

    def test_native_policy_keeps_existing_infrastructure_translation(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                    'Helper.cs': blob('class DeucarianHelper {}')}
        baseline = {**original, 'Helper.cs': blob('class SimultriaHelper {}')}
        incoming = {**baseline, 'Feature.cs': blob('SimultriaHelper helper; SimultriaApi api;')}
        result, _ = translate_tree(original, baseline, incoming, profile)
        self.assertEqual(blob('DeucarianHelper helper; SimultriaApi api;'), result['Feature.cs'])

    def test_native_policy_cannot_hide_colliding_mappings(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api'],
                   'namespaceOverrides': {'Deucarian.One': 'Simultria.Shared',
                                          'Deucarian.Two': 'Simultria.Shared'}}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}')}
        with self.assertRaisesRegex(TranslationNeedsReview, 'multiple source mappings'):
            translate_tree(original, original, {**original, 'File.cs': blob('Simultria.Shared value;')}, profile)

    def test_new_resource_load_retains_existing_host_asset_path(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                    'Runtime/Resources/Deucarian/Simultria/API/Catalog.asset': blob('asset')}
        baseline = {'package.json': original['package.json'],
                    'Runtime/Resources/Simultria/Simultria/API/Catalog.asset': blob('asset')}
        incoming = {**baseline, 'Load.cs': blob('Resources.Load("Simultria/Simultria/API/Catalog");')}
        result, _ = translate_tree(original, baseline, incoming, profile)
        self.assertEqual(blob('Resources.Load("Deucarian/Simultria/API/Catalog");'), result['Load.cs'])
        self.assertEqual(original['Runtime/Resources/Deucarian/Simultria/API/Catalog.asset'],
                         result['Runtime/Resources/Deucarian/Simultria/API/Catalog.asset'])

    def test_unknown_generic_resource_load_still_requires_review(self):
        original = {'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset')}
        baseline = {'Runtime/Resources/Simultria/Common/Known.asset': blob('asset')}
        with self.assertRaises(TranslationNeedsReview):
            translate_tree(original, baseline, {
                **baseline, 'Load.cs': blob('Resources.Load("Simultria/Common/Unknown");')}, PROFILE)

    def test_resource_identity_collision_requires_review(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                    'Runtime/Resources/Deucarian/Common/Known.asset': blob('one'),
                    'Other/Resources/Simultria/Common/Known.asset': blob('two')}
        with self.assertRaisesRegex(TranslationNeedsReview, 'multiple source mappings'):
            translate_tree(original, original, {
                **original, 'Load.cs': blob('Resources.Load("Simultria/Common/Known");')}, profile)

    def test_resource_load_mapping_accepts_only_complete_quoted_or_full_paths(self):
        original = {'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset')}
        projection = projection_for(PROFILE, original)
        for value in ('Simultria/Common/Known', '"Simultria/Common/Known"',
                      "'Simultria/Common/Known'", '@"Simultria/Common/Known"',
                      'Resources.Load("Simultria/Common/Known");',
                      '{"path":"Simultria/Common/Known"}',
                      '// Package\'s catalog.\nResources.Load("Simultria/Common/Known");\n// Caller\'s resource.'):
            with self.subTest(value=value):
                self.assertEqual(value.replace('Simultria/Common/Known', 'Deucarian/Common/Known'),
                                 projection.reverse_insert(value))

    def test_generic_resource_prefix_suffix_or_child_does_not_authorize_unknown_paths(self):
        original = {'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset')}
        baseline = {'Runtime/Resources/Simultria/Common/Known.asset': blob('asset')}
        for value in ('Simultria/Common/KnownExtra', 'prefixSimultria/Common/Known',
                      'Simultria/Common/Known/Child', 'prefix Simultria/Common/Known',
                      'Simultria/Common/Known suffix', ' Simultria/Common/Known',
                      'Simultria/Common/Known '):
            with self.subTest(value=value), self.assertRaises(TranslationNeedsReview):
                translate_tree(original, baseline, {
                    **baseline, 'Load.cs': blob(f'Resources.Load("{value}");')}, PROFILE)

    def test_native_resource_like_substrings_remain_unchanged(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                    'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset')}
        baseline = {'package.json': original['package.json'],
                    'Runtime/Resources/Simultria/Common/Known.asset': blob('asset')}
        for source in ('Resources.Load("Simultria/Common/KnownExtra");',
                       'Resources.Load("prefixSimultria/Common/Known");',
                       'Resources.Load("Simultria/Common/Known/Child");',
                       'Resources.Load("prefix Simultria/Common/Known suffix");',
                       r'var text = "prefix \"Simultria/Common/Known\" suffix";',
                       'var text = @"prefix ""Simultria/Common/Known"" suffix";',
                       '''var text = 'prefix "Simultria/Common/Known" suffix';'''):
            with self.subTest(source=source):
                result, _ = translate_tree(original, baseline, {**baseline, 'Load.cs': blob(source)}, profile)
                self.assertEqual(blob(source), result['Load.cs'])

    def test_ambiguous_exact_resource_path_does_not_claim_unknown_native_descendant(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                    'Runtime/Resources/Deucarian/Common/Known.asset': blob('one'),
                    'Other/Resources/Simultria/Common/Known.asset': blob('two')}
        projection = projection_for(profile, original)
        for value in ('"Simultria/Common/Known/Child"', '"prefix Simultria/Common/Known"'):
            self.assertEqual(value, projection.reverse_insert(value))
        with self.assertRaisesRegex(TranslationNeedsReview, 'multiple source mappings'):
            projection.reverse_insert('"Simultria/Common/Known"')

    def test_inserted_path_fragment_in_existing_native_literal_remains_unchanged(self):
        profile = {**PROFILE, 'nativeBrandPackages': ['com.deucarian.simultria-api']}
        for before, after in (
                ('prefix', 'prefixSimultria/Common/Known'),
                ('/Child', 'Simultria/Common/Known/Child'),
                ('prefix suffix', 'prefix Simultria/Common/Known suffix')):
            with self.subTest(after=after):
                original = {'package.json': blob('{"name":"com.deucarian.simultria-api"}'),
                            'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset'),
                            'Load.cs': blob(f'Resources.Load("{before}");')}
                baseline = {'package.json': original['package.json'],
                            'Runtime/Resources/Simultria/Common/Known.asset': blob('asset'),
                            'Load.cs': original['Load.cs']}
                incoming = {**baseline, 'Load.cs': blob(f'Resources.Load("{after}");')}
                result, _ = translate_tree(original, baseline, incoming, profile)
                self.assertEqual(incoming['Load.cs'], result['Load.cs'])

    def test_complete_path_inserted_in_existing_literal_still_maps(self):
        original = {'Runtime/Resources/Deucarian/Common/Known.asset': blob('asset'),
                    'Load.cs': blob('Resources.Load("");')}
        baseline = {'Runtime/Resources/Simultria/Common/Known.asset': blob('asset'),
                    'Load.cs': original['Load.cs']}
        incoming = {**baseline, 'Load.cs': blob('Resources.Load("Simultria/Common/Known");')}
        result, _ = translate_tree(original, baseline, incoming, PROFILE)
        self.assertEqual(blob('Resources.Load("Deucarian/Common/Known");'), result['Load.cs'])

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
