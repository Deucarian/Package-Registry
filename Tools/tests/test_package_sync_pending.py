import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync_pending import PendingStatus, finish_pending


REVISION = 'a' * 40
CONFIG = {'mergeAfterValidation': True, 'requiredChecks': ['Required'],
          'validationWorkflow': 'validation.yml'}


def check(identifier=10, conclusion='success', name='Required', revision=REVISION):
    return {'id': identifier, 'name': name, 'head_sha': revision, 'status': 'completed',
            'conclusion': conclusion, 'app': {'id': 15368}}


def run(identifier=10, conclusion='success', event='workflow_dispatch', revision=REVISION):
    return {'id': identifier, 'workflow_id': 1, 'name': 'Validation', 'head_sha': revision,
            'status': 'completed', 'conclusion': conclusion, 'event': event,
            'path': '.github/workflows/validation.yml', 'pull_requests': [{'number': 1}]}


class GitHubFixture:
    def __init__(self):
        self.repository = 'Deucarian/Fixture'
        self.detail = {'number': 1, 'draft': False, 'state': 'open',
                       'html_url': 'https://github.com/Deucarian/Fixture/pull/1',
                       'head': {'sha': REVISION, 'ref': 'sync-fixture'}, 'mergeable_state': 'clean'}
        self.refreshed = None
        self.checks = [check()]
        self.runs = [run()]
        self.reviews = []
        self.jobs = {10: [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/10'}]}
        self.calls = []

    def request(self, endpoint, method='GET', body=None):
        self.calls.append((endpoint, method, body))
        if endpoint == '/pulls/1':
            detail_calls = sum(call[0] == endpoint for call in self.calls)
            return copy.deepcopy(self.refreshed if self.refreshed and detail_calls > 1 else self.detail)
        if '/check-runs?' in endpoint:
            return {'check_runs': self.page(self.checks, endpoint)}
        if endpoint.startswith('/actions/runs?'):
            return {'workflow_runs': self.page(self.runs, endpoint)}
        if endpoint.startswith('/actions/runs/') and '/jobs?' in endpoint:
            identifier = int(endpoint.split('/')[3])
            jobs = self.jobs.get(identifier, [])
            return {'jobs': self.page(jobs, endpoint)}
        if endpoint.startswith('/pulls/1/reviews?'):
            return self.page(self.reviews, endpoint)
        if endpoint == '/pulls/1/merge' and method == 'PUT':
            return {'merged': True}
        if endpoint == '/pulls/1/update-branch' and method == 'PUT':
            return {'message': 'Updating pull request branch.'}
        if endpoint == '/actions/workflows/validation.yml/dispatches' and method == 'POST':
            return None
        raise AssertionError('Unexpected API request: ' + endpoint)

    @staticmethod
    def page(values, endpoint):
        page = int(endpoint.rsplit('page=', 1)[1])
        return values[(page - 1) * 100:page * 100]

    @property
    def mutations(self):
        return [call for call in self.calls if call[1] != 'GET']


class PendingTests(unittest.TestCase):
    def setUp(self):
        self.github = GitHubFixture()

    def finish(self, **configuration):
        return finish_pending(self.github, {'number': 1}, dict(CONFIG, **configuration))

    def test_success_merges_only_the_checked_revision(self):
        result = self.finish()
        self.assertEqual(PendingStatus.MERGED, result.status)
        self.assertFalse(result.needs_attention)
        self.assertEqual([('/pulls/1/merge', 'PUT', {'sha': REVISION, 'merge_method': 'rebase'})],
                         self.github.mutations)

    def test_newer_failed_check_cannot_be_hidden_by_older_success(self):
        self.github.checks = [check(12, 'failure'), check(10)]
        result = self.finish()
        self.assertEqual(PendingStatus.VALIDATION_FAILED, result.status)
        self.assertTrue(result.needs_attention)
        self.assertEqual([], self.github.mutations)

    def test_successful_rerun_supersedes_previous_failed_check(self):
        self.github.checks = [
            dict(check(10, 'failure'), details_url='https://github.com/Deucarian/Fixture/actions/runs/10/job/10'),
            dict(check(12), details_url='https://github.com/Deucarian/Fixture/actions/runs/12/job/12'),
        ]
        self.github.runs = [run(10, 'failure'), run(12)]
        self.github.jobs[12] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/12'}]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_foreign_app_success_with_same_name_cannot_replace_validation_workflow(self):
        self.github.runs = []
        self.github.checks = [dict(check(), app={'id': 123})]
        result = self.finish()
        self.assertEqual(PendingStatus.VALIDATION_REQUESTED, result.status)
        self.assertEqual([('/actions/workflows/validation.yml/dispatches', 'POST', {'ref': 'sync-fixture'})],
                         self.github.mutations)

    def test_foreign_app_success_cannot_satisfy_trusted_workflow_job(self):
        self.github.checks = [dict(check(), app={'id': 123})]
        self.assertEqual(PendingStatus.CHECKS_MISSING, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_unrelated_workflow_success_with_same_name_cannot_replace_validation(self):
        self.github.runs[0]['path'] = '.github/workflows/unrelated.yml'
        self.assertEqual(PendingStatus.VALIDATION_REQUESTED, self.finish().status)
        self.assertFalse(any(path == '/pulls/1/merge' for path, _, _ in self.github.mutations))

    def test_unrelated_successful_check_does_not_prevent_first_validation_dispatch(self):
        self.github.checks = [check(name='Unrelated lint')]
        self.github.runs[0]['path'] = '.github/workflows/lint.yml'
        self.assertEqual(PendingStatus.VALIDATION_REQUESTED, self.finish().status)
        self.assertEqual([('/actions/workflows/validation.yml/dispatches', 'POST', {'ref': 'sync-fixture'})],
                         self.github.mutations)

    def test_required_name_must_match_a_job_of_configured_successful_workflow(self):
        self.github.jobs[10] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/11'}]
        self.github.runs += [dict(run(12), workflow_id=2, path='.github/workflows/unrelated.yml')]
        self.github.jobs[12] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/10'}]
        self.assertEqual(PendingStatus.CHECKS_MISSING, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_unrelated_same_name_success_does_not_hide_valid_configured_workflow_job(self):
        self.github.checks += [check(12)]
        self.github.runs += [dict(run(12), workflow_id=2, path='.github/workflows/unrelated.yml')]
        self.github.jobs[12] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/12'}]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_skipped_configured_workflow_cannot_reuse_success_from_another_workflow(self):
        self.github.runs[0]['conclusion'] = 'skipped'
        self.assertEqual(PendingStatus.CHECKS_MISSING, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_pr_approval_is_not_satisfied_by_successful_dispatch(self):
        self.github.runs += [run(11, 'action_required', event='pull_request')]
        result = self.finish()
        self.assertEqual(PendingStatus.APPROVAL_REQUIRED, result.status)
        self.assertIn('maintainer approval', result.message)
        self.assertTrue(result.needs_attention)
        self.assertEqual([], self.github.mutations)

    def test_approval_only_run_without_jobs_does_not_dispatch(self):
        self.github.checks = []
        self.github.runs = [run(conclusion='action_required', event='pull_request')]
        self.assertEqual(PendingStatus.APPROVAL_REQUIRED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_pending_check_does_not_merge_or_dispatch(self):
        self.github.checks[0].update(status='queued', conclusion=None)
        self.assertEqual(PendingStatus.VALIDATION_PENDING, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_latest_running_workflow_supersedes_previous_failure(self):
        self.github.runs = [run(10, 'failure'), dict(run(12), status='in_progress', conclusion=None)]
        self.assertEqual(PendingStatus.VALIDATION_PENDING, self.finish().status)

    def test_later_rerun_of_older_workflow_id_is_latest_execution(self):
        self.github.runs = [
            dict(run(12, 'failure'), run_started_at='2026-10-20T10:00:00Z', run_attempt=1),
            dict(run(10), run_started_at='2026-10-20T11:00:00Z', run_attempt=2),
        ]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_failed_later_rerun_cannot_use_earlier_successful_workflow(self):
        self.github.runs = [
            dict(run(12), run_started_at='2026-10-20T10:00:00Z', run_attempt=1),
            dict(run(10, 'failure'), run_started_at='2026-10-20T11:00:00Z', run_attempt=2),
        ]
        self.assertEqual(PendingStatus.VALIDATION_FAILED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_old_failed_job_name_is_removed_after_successful_workflow_rerun(self):
        self.github.checks = [
            dict(check(9, 'failure', 'Former validation'),
                 details_url='https://github.com/Deucarian/Fixture/actions/runs/10/job/9'),
            dict(check(12), details_url='https://github.com/Deucarian/Fixture/actions/runs/10/job/12'),
        ]
        self.github.runs = [dict(run(10), run_attempt=2)]
        self.github.jobs[10] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/12'}]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_superseded_workflow_jobs_cannot_block_successful_new_execution(self):
        self.github.checks = [
            dict(check(9, 'failure', 'Former validation'),
                 details_url='https://github.com/Deucarian/Fixture/actions/runs/8/job/9'),
            dict(check(12), details_url='https://github.com/Deucarian/Fixture/actions/runs/10/job/12'),
        ]
        self.github.runs = [run(8, 'failure'), run(10)]
        self.github.jobs[10] = [{'check_run_url': 'https://api.github.com/repos/Deucarian/Fixture/check-runs/12'}]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_external_app_failure_is_not_discarded_with_github_actions_jobs(self):
        self.github.checks += [dict(check(9, 'failure', 'External'), app={'id': 123},
                                   details_url='https://github.com/Deucarian/Fixture/actions/runs/10/job/9')]
        self.assertEqual(PendingStatus.VALIDATION_FAILED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_no_checks_or_validation_attempt_dispatches_once(self):
        self.github.checks = []
        self.github.runs = []
        self.assertEqual(PendingStatus.VALIDATION_REQUESTED, self.finish().status)
        self.assertEqual([('/actions/workflows/validation.yml/dispatches', 'POST', {'ref': 'sync-fixture'})],
                         self.github.mutations)

    def test_existing_failed_run_without_jobs_is_not_redispatched(self):
        self.github.checks = []
        self.github.runs = [run(conclusion='failure')]
        self.assertEqual(PendingStatus.VALIDATION_FAILED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_completed_attempt_missing_check_requires_attention(self):
        self.github.checks = []
        result = self.finish()
        self.assertEqual(PendingStatus.CHECKS_MISSING, result.status)
        self.assertTrue(result.needs_attention)
        self.assertEqual([], self.github.mutations)

    def test_success_from_other_revision_does_not_satisfy_required_check(self):
        self.github.checks = [check(revision='b' * 40)]
        self.assertEqual(PendingStatus.CHECKS_MISSING, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_old_head_approval_cannot_block_current_head(self):
        self.github.runs += [run(12, 'action_required', 'pull_request', 'b' * 40)]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_different_pull_request_workflow_is_not_current_approval(self):
        self.github.runs += [dict(run(12, 'action_required', 'pull_request'), pull_requests=[{'number': 2}])]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_failure_on_second_page_of_checks_is_not_ignored(self):
        self.github.checks = [check(index, name=f'Job {index}') for index in range(100)]
        self.github.checks += [check(101), check(102, 'failure', name='Additional')]
        self.assertEqual(PendingStatus.VALIDATION_FAILED, self.finish().status)
        self.assertTrue(any('/check-runs?' in path and 'page=2' in path for path, _, _ in self.github.calls))
        self.assertEqual([], self.github.mutations)

    def test_approval_on_second_page_of_runs_is_not_ignored(self):
        self.github.runs = [dict(run(index), workflow_id=index) for index in range(100)]
        self.github.runs += [run(101, 'action_required', 'pull_request')]
        self.assertEqual(PendingStatus.APPROVAL_REQUIRED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_reviewer_objection_on_second_page_blocks_merge(self):
        self.github.reviews = [{'id': index, 'state': 'COMMENTED', 'user': {'login': 'reader'}}
                               for index in range(100)]
        self.github.reviews += [{'id': 101, 'state': 'CHANGES_REQUESTED', 'user': {'login': 'reviewer'}}]
        self.assertEqual(PendingStatus.REVIEW_REQUIRED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_newer_approval_supersedes_same_reviewers_objection(self):
        self.github.reviews = [{'id': 12, 'state': 'APPROVED', 'user': {'login': 'reviewer'}},
                               {'id': 10, 'state': 'CHANGES_REQUESTED', 'user': {'login': 'reviewer'}}]
        self.assertEqual(PendingStatus.MERGED, self.finish().status)

    def test_behind_branch_update_does_not_dispatch_before_async_update_finishes(self):
        self.github.detail['mergeable_state'] = 'behind'
        self.assertEqual(PendingStatus.BRANCH_UPDATED, self.finish().status)
        self.assertEqual([('/pulls/1/update-branch', 'PUT', {'expected_head_sha': REVISION})],
                         self.github.mutations)

    def test_head_change_during_checks_prevents_merge(self):
        self.github.refreshed = copy.deepcopy(self.github.detail)
        self.github.refreshed['head']['sha'] = 'b' * 40
        self.assertEqual(PendingStatus.HEAD_CHANGED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_new_review_request_during_checks_prevents_merge(self):
        self.github.refreshed = dict(self.github.detail, requested_reviewers=[{'login': 'reviewer'}])
        self.assertEqual(PendingStatus.REVIEW_REQUIRED, self.finish().status)
        self.assertEqual([], self.github.mutations)

    def test_github_blocked_state_is_never_bypassed(self):
        self.github.detail['mergeable_state'] = 'blocked'
        result = self.finish()
        self.assertEqual(PendingStatus.MERGE_BLOCKED, result.status)
        self.assertTrue(result.needs_attention)
        self.assertEqual([], self.github.mutations)

    def test_manual_merge_policy_is_respected(self):
        self.assertEqual(PendingStatus.REVIEW_REQUIRED, self.finish(mergeAfterValidation=False).status)
        self.assertEqual([], self.github.mutations)

    def test_empty_required_checks_cannot_merge(self):
        self.assertEqual(PendingStatus.CHECKS_MISSING, self.finish(requiredChecks=[]).status)
        self.assertEqual([], self.github.mutations)

    def test_squash_method_is_respected(self):
        self.finish(mergeMethod='squash')
        self.assertEqual('squash', self.github.mutations[-1][2]['merge_method'])

    def test_invalid_merge_method_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'merge method'):
            self.finish(mergeMethod='invalid')
        self.assertEqual([], self.github.mutations)


if __name__ == '__main__':
    unittest.main()
