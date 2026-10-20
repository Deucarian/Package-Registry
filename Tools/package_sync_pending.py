"""Finish synchronization PRs without bypassing review or workflow approval."""

from dataclasses import dataclass
from enum import Enum
import re
from urllib.parse import quote


class PendingStatus(str, Enum):
    MERGED = 'merged'
    CLOSED = 'closed'
    VALIDATION_REQUESTED = 'validation_requested'
    VALIDATION_PENDING = 'validation_pending'
    BRANCH_UPDATED = 'branch_updated'
    REVIEW_REQUIRED = 'review_required'
    APPROVAL_REQUIRED = 'approval_required'
    VALIDATION_FAILED = 'validation_failed'
    CHECKS_MISSING = 'checks_missing'
    MERGE_BLOCKED = 'merge_blocked'
    HEAD_CHANGED = 'head_changed'


@dataclass(frozen=True)
class PendingResult:
    status: PendingStatus
    message: str
    url: str
    revision: str

    @property
    def needs_attention(self):
        return self.status in {
            PendingStatus.REVIEW_REQUIRED, PendingStatus.APPROVAL_REQUIRED,
            PendingStatus.VALIDATION_FAILED, PendingStatus.CHECKS_MISSING,
            PendingStatus.MERGE_BLOCKED,
        }


def _pages(github, endpoint, key=None):
    """Use bounded pagination so large check/review histories cannot hide blockers."""
    separator = '&' if '?' in endpoint else '?'
    items = []
    for page in range(1, 101):
        response = github.request(f'{endpoint}{separator}per_page=100&page={page}')
        batch = response[key] if key else response
        if not isinstance(batch, list):
            raise RuntimeError('Unexpected GitHub collection response')
        items.extend(batch)
        if len(batch) < 100:
            return items
    raise RuntimeError('GitHub history exceeded the safe pagination limit')


def _latest(items, identity, order=lambda item: (item['id'],)):
    latest = {}
    for item in items:
        key = identity(item)
        # IDs increase when a newer run is created, including jobs of rerun attempts.
        if key not in latest or order(item) > order(latest[key]):
            latest[key] = item
    return list(latest.values())


def dispatch_validation(github, ref, workflow):
    github.request('/actions/workflows/' + quote(workflow, safe='') + '/dispatches',
                   'POST', {'ref': ref})


def _workflow_runs(github, revision, number):
    runs = _pages(github, '/actions/runs?head_sha=' + revision, 'workflow_runs')
    relevant = []
    for run in runs:
        if run.get('head_sha') != revision:
            continue
        pulls = run.get('pull_requests', [])
        if run.get('event') == 'pull_request' and pulls:
            if not any(pull.get('number') == number for pull in pulls):
                continue
        relevant.append(run)
    # A successful manual dispatch does not supersede a PR workflow awaiting approval.
    latest = _latest(relevant, lambda run: (run['workflow_id'], run.get('event')),
                     lambda run: (run.get('run_started_at') or run.get('created_at') or '',
                                  run['id'], run.get('run_attempt', 1)))
    return latest, relevant


def _current_checks(github, checks, runs, history):
    active_ids = set()
    run_checks = {}
    for run in runs:
        jobs = _pages(github, '/actions/runs/' + str(run['id']) + '/jobs?filter=latest', 'jobs')
        identifiers = set()
        for job in jobs:
            match = re.search(r'/check-runs/(\d+)$', job.get('check_run_url') or '')
            if not match:
                raise RuntimeError('GitHub validation job has no check-run identity')
            identifiers.add(int(match.group(1)))
        run_checks[run['id']] = identifiers
        active_ids.update(identifiers)
    known_runs = {run['id'] for run in history}
    known_suites = {run['check_suite_id'] for run in history if run.get('check_suite_id')}
    current = []
    for check in checks:
        actions = check.get('app', {}).get('id') == 15368
        match = re.fullmatch(r'https://github\.com/' + re.escape(github.repository)
                             + r'/actions/runs/(\d+)/job/\d+', check.get('details_url') or '')
        known = ((match and int(match.group(1)) in known_runs)
                 or check.get('check_suite', {}).get('id') in known_suites)
        if actions and known and check['id'] not in active_ids:
            continue
        current.append(check)
    owners = {identifier: run_id for run_id, identifiers in run_checks.items() for identifier in identifiers}
    return _latest(current, lambda check: (check['name'], check.get('app', {}).get('id'),
                                          owners.get(check['id']))), run_checks


def finish_pending(github, pull, configuration):
    """Return an explicit outcome; only ordinary GitHub merges are permitted."""
    number = pull['number']
    endpoint = '/pulls/' + str(number)
    detail = github.request(endpoint)
    revision = detail['head']['sha']
    url = detail['html_url']

    def result(status, message):
        return PendingResult(status, message, url, revision)

    if detail.get('state') == 'closed':
        return result(PendingStatus.CLOSED, 'Synchronization pull request is already closed.')
    if detail['draft'] or detail.get('requested_reviewers') or detail.get('requested_teams'):
        return result(PendingStatus.REVIEW_REQUIRED, 'Synchronization awaits the requested review.')
    if not configuration.get('mergeAfterValidation', False):
        return result(PendingStatus.REVIEW_REQUIRED, 'Automatic synchronization merging is disabled.')
    required = set(configuration['requiredChecks'])
    if not required:
        return result(PendingStatus.CHECKS_MISSING, 'No required synchronization checks are configured.')

    checks = _pages(github, '/commits/' + revision + '/check-runs?filter=all', 'check_runs')
    checks = [check for check in checks if check.get('head_sha') == revision]
    runs, history = _workflow_runs(github, revision, number)
    checks, run_checks = _current_checks(github, checks, runs, history)
    failed = [check['name'] for check in checks if check['status'] == 'completed'
              and check.get('conclusion') not in ('success', 'neutral', 'skipped', 'action_required')]
    failed.extend(run['name'] for run in runs if run['status'] == 'completed'
                  and run.get('conclusion') not in ('success', 'neutral', 'skipped', 'action_required'))
    if failed:
        return result(PendingStatus.VALIDATION_FAILED,
                      'Synchronization validation failed: ' + ', '.join(sorted(set(failed)))
                      + '. Fix the failure and rerun validation; it will not be repeatedly redispatched.')
    approvals = [run for run in runs if run.get('conclusion') == 'action_required']
    if approvals or any(check.get('conclusion') == 'action_required' for check in checks):
        return result(PendingStatus.APPROVAL_REQUIRED,
                      'GitHub requires maintainer approval for the PR workflows. Review and approve them '
                      'on the pull request. For unattended future PRs, configure the dedicated '
                      'synchronization GitHub App token; no approval or protection will be bypassed.')
    if any(item['status'] != 'completed' for item in checks + runs):
        return result(PendingStatus.VALIDATION_PENDING, 'Synchronization validation is still running.')

    validation = configuration['validationWorkflow']
    validation_runs = [run for run in runs
                       if run.get('path', '').split('@', 1)[0].rsplit('/', 1)[-1] == validation]
    if not validation_runs:
        dispatch_validation(github, detail['head']['ref'], validation)
        return result(PendingStatus.VALIDATION_REQUESTED, 'Requested synchronization validation.')
    validated_jobs = set()
    for run in validation_runs:
        if run['status'] == 'completed' and run.get('conclusion') == 'success':
            validated_jobs.update(run_checks[run['id']])
    successful = {check['name'] for check in checks if check.get('conclusion') == 'success'
                  and check.get('app', {}).get('id') == 15368 and check['id'] in validated_jobs}
    missing = required - successful
    if missing:
        return result(PendingStatus.CHECKS_MISSING,
                      'Required successful GitHub Actions jobs from the configured validation workflow '
                      'are missing on the current revision: '
                      + ', '.join(sorted(missing)) + '. Inspect the validation workflow before retrying.')

    reviews = _pages(github, endpoint + '/reviews')
    latest_reviews = {}
    for review in sorted(reviews, key=lambda value: value['id']):
        if review['state'] in ('APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'):
            latest_reviews[review['user']['login']] = review['state']
    if 'CHANGES_REQUESTED' in latest_reviews.values():
        return result(PendingStatus.REVIEW_REQUIRED, 'A reviewer requested changes to this synchronization.')

    # Refresh after remote reads; neither merge nor update a head other than the one checked.
    current = github.request(endpoint)
    if current['head']['sha'] != revision:
        return result(PendingStatus.HEAD_CHANGED, 'The synchronization revision changed; inspect it next run.')
    if current.get('state') == 'closed':
        return result(PendingStatus.CLOSED, 'Synchronization pull request closed while checking validation.')
    if current['draft'] or current.get('requested_reviewers') or current.get('requested_teams'):
        return result(PendingStatus.REVIEW_REQUIRED, 'Synchronization now awaits the requested review.')
    state = current.get('mergeable_state')
    if state == 'behind':
        github.request(endpoint + '/update-branch', 'PUT', {'expected_head_sha': revision})
        # GitHub's update is asynchronous. Dispatch on the next run after inspecting its new SHA.
        return result(PendingStatus.BRANCH_UPDATED, 'Requested branch update; the new revision needs validation.')
    if state != 'clean':
        return result(PendingStatus.MERGE_BLOCKED,
                      'GitHub reports the synchronization merge as ' + str(state)
                      + '. Resolve its PR checks, conflicts, or protection requirements.')
    merge_method = configuration.get('mergeMethod', 'rebase')
    if merge_method not in ('rebase', 'squash', 'merge'):
        raise RuntimeError('Invalid configured merge method')
    merged = github.request(endpoint + '/merge', 'PUT', {'sha': revision, 'merge_method': merge_method})
    if not merged.get('merged'):
        raise RuntimeError('GitHub did not merge the validated synchronization pull request')
    return result(PendingStatus.MERGED, 'Merged the validated synchronization revision.')
