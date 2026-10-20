import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync import finish_pending
from package_sync_pending import PendingStatus
from test_package_sync_pending import CONFIG, REVISION, GitHubFixture, check


class MergeTests(unittest.TestCase):
    def fixture(self, conclusion='success', state='clean', reviews=None):
        client = GitHubFixture()
        client.detail['mergeable_state'] = state
        client.checks = [check(conclusion=conclusion)]
        client.reviews = reviews or []
        return client, {'number': 1}, dict(CONFIG)

    def test_successful_checks_merge_only_the_validated_revision(self):
        client, pull, config = self.fixture()
        result = finish_pending(client, pull, config)
        self.assertEqual(PendingStatus.MERGED, result.status)
        self.assertEqual([('/pulls/1/merge', 'PUT', {'sha': REVISION, 'merge_method': 'rebase'})],
                         client.mutations)

    def test_failed_validation_cannot_merge(self):
        client, pull, config = self.fixture(conclusion='failure')
        result = finish_pending(client, pull, config)
        self.assertEqual(PendingStatus.VALIDATION_FAILED, result.status)
        self.assertTrue(result.needs_attention)
        self.assertEqual([], client.mutations)

    def test_squash_only_repository_policy_is_respected(self):
        client, pull, config = self.fixture()
        config['mergeMethod'] = 'squash'
        finish_pending(client, pull, config)
        self.assertEqual('squash', client.mutations[-1][2]['merge_method'])

    def test_invalid_merge_method_cannot_publish(self):
        client, pull, config = self.fixture()
        config['mergeMethod'] = 'invalid'
        with self.assertRaisesRegex(RuntimeError, 'merge method'):
            finish_pending(client, pull, config)
        self.assertEqual([], client.mutations)

    def test_review_objection_blocks_automatic_merge(self):
        client, pull, config = self.fixture(reviews=[
            {'id': 1, 'state': 'CHANGES_REQUESTED', 'user': {'login': 'reviewer'}}])
        result = finish_pending(client, pull, config)
        self.assertEqual(PendingStatus.REVIEW_REQUIRED, result.status)
        self.assertEqual([], client.mutations)

    def test_behind_branch_defers_validation_until_asynchronous_update_finishes(self):
        client, pull, config = self.fixture(state='behind')
        result = finish_pending(client, pull, config)
        self.assertEqual(PendingStatus.BRANCH_UPDATED, result.status)
        self.assertEqual([('/pulls/1/update-branch', 'PUT', {'expected_head_sha': REVISION})],
                         client.mutations)


if __name__ == '__main__':
    unittest.main()
