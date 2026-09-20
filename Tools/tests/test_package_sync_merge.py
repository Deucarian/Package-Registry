import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync import finish_pending


class MergeTests(unittest.TestCase):
    def fixture(self, conclusion='success', state='clean', reviews=None):
        client = Mock()
        detail = {'draft': False, 'number': 1, 'html_url': 'https://example.invalid/pull/1',
                  'head': {'sha': 'a' * 40, 'ref': 'chore/bitbucket-sync-main-fixture'}, 'mergeable_state': state}
        client.request.side_effect = [detail, {'check_runs': [
            {'name': 'Required', 'status': 'completed', 'conclusion': conclusion}]}, reviews or [], {'merged': True}, None]
        return client, {'number': 1}, {'mergeAfterValidation': True, 'requiredChecks': ['Required'],
                                     'validationWorkflow': 'validation.yml'}

    def test_successful_checks_merge_only_the_validated_revision(self):
        client, pull, config = self.fixture()
        finish_pending(client, pull, config)
        self.assertEqual('/pulls/1/merge', client.request.call_args.args[0])
        self.assertEqual('a' * 40, client.request.call_args.args[2]['sha'])
        self.assertEqual('rebase', client.request.call_args.args[2]['merge_method'])

    def test_failed_validation_cannot_merge(self):
        client, pull, config = self.fixture(conclusion='failure')
        finish_pending(client, pull, config)
        self.assertEqual(2, client.request.call_count)

    def test_squash_only_repository_policy_is_respected(self):
        client, pull, config = self.fixture()
        config['mergeMethod'] = 'squash'
        finish_pending(client, pull, config)
        self.assertEqual('squash', client.request.call_args.args[2]['merge_method'])

    def test_invalid_merge_method_cannot_publish(self):
        client, pull, config = self.fixture()
        config['mergeMethod'] = 'invalid'
        with self.assertRaisesRegex(RuntimeError, 'merge method'):
            finish_pending(client, pull, config)
        self.assertEqual(3, client.request.call_count)

    def test_review_objection_blocks_automatic_merge(self):
        client, pull, config = self.fixture(reviews=[{'state': 'CHANGES_REQUESTED', 'user': {'login': 'reviewer'}}])
        finish_pending(client, pull, config)
        self.assertEqual(3, client.request.call_count)

    def test_behind_branch_is_updated_and_revalidated_not_merged(self):
        client, pull, config = self.fixture(state='behind')
        finish_pending(client, pull, config)
        paths = [call.args[0] for call in client.request.call_args_list]
        self.assertIn('/pulls/1/update-branch', paths)
        self.assertIn('/actions/workflows/validation.yml/dispatches', paths)
        self.assertNotIn('/pulls/1/merge', paths)


if __name__ == '__main__':
    unittest.main()
