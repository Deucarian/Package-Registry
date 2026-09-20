"""Pull a private Bitbucket package into its GitHub counterpart through reviewed PRs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from package_sync_projection import TranslationNeedsReview
from package_sync_tree import Blob, merge_trees, translate_tree, validate_path

STATE = '.github/package-sync/state.json'
MAX_TREE_BYTES = 128 * 1024 * 1024


def git(root, *args, data=None, env=None):
    result = subprocess.run(['git', '-C', str(root), '-c', 'core.hooksPath=/dev/null', *args],
                            input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env={**os.environ, 'GIT_TERMINAL_PROMPT': '0', **(env or {})}, timeout=180)
    if result.returncode:
        # Never print credential-bearing command arguments or HTTP headers.
        raise RuntimeError(f'Git {args[0]} failed with exit code {result.returncode}')
    return result.stdout


def text_git(root, *args, **kwargs):
    return git(root, *args, **kwargs).decode().strip()


def read_tree(root, revision):
    rows = git(root, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0')
    entries = []
    for row in filter(None, rows):
        header, name = row.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        path = name.decode('utf-8')
        validate_path(path)
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise TranslationNeedsReview(f'{path}: unsupported tree entry')
        entries.append((path, mode, oid))
    if not entries:
        return {}
    sizes = git(root, 'cat-file', '--batch-check=%(objectsize)',
                data=('\n'.join(oid for _, _, oid in entries) + '\n').encode())
    if sum(map(int, sizes.split())) > MAX_TREE_BYTES:
        raise TranslationNeedsReview('Repository exceeds the reviewed synchronization size limit')
    payload = git(root, 'cat-file', '--batch', data=('\n'.join(oid for _, _, oid in entries) + '\n').encode())
    result, offset = {}, 0
    for name, mode, oid in entries:
        end = payload.index(b'\n', offset)
        actual, kind, size = payload[offset:end].decode().split()
        if actual != oid or kind != 'blob':
            raise RuntimeError('Unexpected Git object')
        offset = end + 1
        result[name] = Blob(mode, payload[offset:offset + int(size)])
        offset += int(size) + 1
    return result


def write_tree(root, tree):
    with tempfile.TemporaryDirectory(prefix='package-sync-index-') as temporary:
        environment = {'GIT_INDEX_FILE': str(Path(temporary) / 'index')}
        git(root, 'read-tree', '--empty', env=environment)
        rows = []
        blobs = {}
        if text_git(root, 'rev-parse', '--show-object-format') != 'sha1':
            raise RuntimeError('Unsupported Git object format')
        for name, blob in sorted(tree.items()):
            validate_path(name)
            if blob.mode not in ('100644', '100755'):
                raise TranslationNeedsReview('Unsupported file mode')
            digest = hashlib.sha1()
            digest.update(f'blob {len(blob.data)}\0'.encode())
            digest.update(blob.data)
            oid = digest.hexdigest()
            blobs[oid] = blob.data
            rows.append(f'{blob.mode} {oid}\t{name}\0'.encode())
        if blobs:
            objects = git(root, 'cat-file', '--batch-check=%(objectname) %(objecttype)',
                          data=('\n'.join(blobs) + '\n').encode()).decode().splitlines()
            for row in objects:
                oid, kind = row.split()
                if kind == 'missing':
                    actual = text_git(root, 'hash-object', '-w', '--stdin', data=blobs[oid])
                    if actual != oid:
                        raise RuntimeError('Git object digest mismatch')
                elif kind != 'blob':
                    raise RuntimeError('Unexpected existing Git object type')
        git(root, 'update-index', '-z', '--index-info', data=b''.join(rows), env=environment)
        return text_git(root, 'write-tree', env=environment)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise RuntimeError('Unexpected GitHub API redirect')


class GitHub:
    def __init__(self, repository, token):
        if not re.fullmatch(r'Deucarian/[A-Za-z0-9_.-]+', repository):
            raise ValueError('Unexpected GitHub owner or repository')
        self.repository, self.token = repository, token
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, endpoint, method='GET', body=None):
        if not endpoint.startswith('/') or '..' in endpoint:
            raise ValueError('Invalid API endpoint')
        request = urllib.request.Request('https://api.github.com/repos/' + self.repository + endpoint,
            data=json.dumps(body).encode() if body is not None else None, method=method,
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28'})
        try:
            with self.opener.open(request, timeout=60) as response:
                data = response.read()
                return json.loads(data) if data else None
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'GitHub {method} {endpoint.split("?")[0]} returned HTTP {error.code}') from None


def commit(root, tree, parent, message, identity):
    return text_git(root, 'commit-tree', write_tree(root, tree), *(['-p', parent] if parent else []),
                    data=(message + '\n').encode(), env=identity)


def maintain_schedule_activity(root, configuration, now=None):
    """Keep quiet public repositories active without touching either release branch."""
    if not configuration.get('keepScheduleActive', False):
        return
    now = now or datetime.now(timezone.utc)
    branch = 'sync/schedule-activity'
    try:
        previous = text_git(root, 'rev-parse', '--verify', 'refs/remotes/origin/' + branch)
    except RuntimeError:
        previous = None
    if previous:
        updated = datetime.fromtimestamp(int(text_git(root, 'show', '-s', '--format=%ct', previous)), timezone.utc)
        if (now - updated).total_seconds() < 28 * 24 * 60 * 60:
            return
    owner = configuration['committer']
    identity = {f'GIT_{role}_{field}': value for role in ('AUTHOR', 'COMMITTER')
                for field, value in (('NAME', owner['name']), ('EMAIL', owner['email']), ('DATE', now.isoformat()))}
    tree = {'schedule-activity.json': Blob('100644', (json.dumps({'checkedAt': now.isoformat()}, indent=2) + '\n').encode())}
    revision = commit(root, tree, previous, 'Maintain scheduled package synchronization', identity)
    git(root, 'push', 'origin', revision + ':refs/heads/' + branch)
    print('Recorded monthly synchronization activity on its separate bookkeeping branch')


def pending_pull(github, channel):
    pulls = github.request('/pulls?state=open&base=' + channel + '&per_page=100')
    prefix = f'chore/bitbucket-sync-{channel}-'
    return [pull for pull in pulls if pull['head']['ref'].startswith(prefix)
            and pull['head']['repo']['full_name'] == github.repository]


def dispatch_validation(github, ref, workflow):
    github.request('/actions/workflows/' + urllib.parse.quote(workflow, safe='') + '/dispatches',
                   'POST', {'ref': ref})


def finish_pending(github, pull, configuration):
    detail = github.request('/pulls/' + str(pull['number']))
    if detail['draft'] or detail.get('requested_reviewers') or detail.get('requested_teams'):
        print('Awaiting requested review: ' + detail['html_url'])
        return
    if not configuration.get('mergeAfterValidation', False):
        print('Awaiting review: ' + detail['html_url'])
        return
    revision = detail['head']['sha']
    checks = github.request('/commits/' + revision + '/check-runs?per_page=100')['check_runs']
    if not checks:
        dispatch_validation(github, detail['head']['ref'], configuration['validationWorkflow'])
        print('Requested validation for synchronization pull request')
        return
    required = set(configuration['requiredChecks'])
    successful = {check['name'] for check in checks if check['status'] == 'completed'
                  and check['conclusion'] == 'success'}
    if not required or not required.issubset(successful):
        print('Awaiting successful required checks: ' + detail['html_url'])
        return
    if any(check['status'] != 'completed' or check['conclusion'] not in ('success', 'neutral', 'skipped')
           for check in checks):
        print('Additional checks need attention: ' + detail['html_url'])
        return
    reviews = github.request('/pulls/' + str(pull['number']) + '/reviews?per_page=100')
    latest_reviews = {}
    for review in reviews:
        if review['state'] in ('APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'):
            latest_reviews[review['user']['login']] = review['state']
    if 'CHANGES_REQUESTED' in latest_reviews.values():
        print('Changes requested by a reviewer: ' + detail['html_url'])
        return
    if detail['mergeable_state'] == 'behind':
        github.request('/pulls/' + str(pull['number']) + '/update-branch', 'PUT', {'expected_head_sha': revision})
        dispatch_validation(github, detail['head']['ref'], configuration['validationWorkflow'])
        print('Updated synchronization branch; fresh validation required')
        return
    if detail['mergeable_state'] != 'clean':
        print('Merge remains blocked or pending: ' + detail['html_url'])
        return
    merge_method = configuration.get('mergeMethod', 'rebase')
    if merge_method not in ('rebase', 'squash', 'merge'):
        raise RuntimeError('Invalid configured merge method')
    result = github.request('/pulls/' + str(pull['number']) + '/merge', 'PUT', {
        'sha': revision, 'merge_method': merge_method})
    if not result.get('merged'):
        raise RuntimeError('GitHub did not merge the validated synchronization pull request')
    print('Merged validated synchronization: ' + detail['html_url'])


def sync_channel(root, upstream, profile, configuration, channel, github, publish):
    ref = 'refs/remotes/origin/' + channel
    target = text_git(root, 'rev-parse', ref)
    current = read_tree(root, target)
    state = json.loads(current[STATE].data)
    pair = state['channels'][channel]
    if any(not re.fullmatch('[0-9a-f]{40}', pair[key]) for key in ('githubBaseline', 'bitbucketCommit')):
        raise TranslationNeedsReview('Invalid synchronization baseline')
    incoming_ref = text_git(upstream, 'rev-parse', 'refs/heads/' + channel)
    if incoming_ref == pair['bitbucketCommit']:
        print(channel + ': already synchronized')
        return
    if github:
        pending = pending_pull(github, channel)
        if pending:
            finish_pending(github, pending[0], configuration)
            return
    baseline = read_tree(root, pair['githubBaseline'])
    git(upstream, 'merge-base', '--is-ancestor', pair['bitbucketCommit'], incoming_ref)
    old_upstream = read_tree(upstream, pair['bitbucketCommit'])
    new_upstream = read_tree(upstream, incoming_ref)
    canonical, changed = translate_tree(baseline, old_upstream, new_upstream, profile)
    merged = merge_trees(current, baseline, canonical)
    name, email, timestamp = text_git(upstream, 'show', '-s', '--format=%an%n%ae%n%aI', incoming_ref).splitlines()
    identity = {'GIT_AUTHOR_NAME': name, 'GIT_AUTHOR_EMAIL': email, 'GIT_AUTHOR_DATE': timestamp,
                'GIT_COMMITTER_NAME': configuration['committer']['name'],
                'GIT_COMMITTER_EMAIL': configuration['committer']['email'], 'GIT_COMMITTER_DATE': timestamp}
    canonical_commit = commit(root, canonical, pair['githubBaseline'],
                              f'Apply shared package changes through {incoming_ref[:12]}', identity)
    state['channels'][channel] = {'bitbucketCommit': incoming_ref, 'githubBaseline': canonical_commit}
    merged[STATE] = Blob('100644', (json.dumps(state, indent=2) + '\n').encode())
    branch = f'chore/bitbucket-sync-{channel}-{incoming_ref[:12]}'
    proposed = commit(root, merged, target, 'Synchronize shared package changes from Bitbucket', identity)
    print(f'{channel}: {len(changed)} shared files prepared; revision {proposed}')
    if not publish:
        return
    baseline_branch = f'sync/bitbucket-baseline-{channel}-{incoming_ref[:12]}'
    # No force push, no main/develop mutation, and no Bitbucket writes.
    git(root, 'push', 'origin', f'{canonical_commit}:refs/heads/{baseline_branch}',
        f'{proposed}:refs/heads/{branch}')
    body = (f'Applies shared changes from the Simultria package through `{incoming_ref}`. '
            'Preserves Deucarian package identifiers, GitHub configuration, and independent local changes.\n\n'
            f'Translation and three-way merge completed without conflicts for {len(changed)} shared files. '
            'The package validation workflow must pass before merging.')
    pull = github.request('/pulls', 'POST', {'head': branch, 'base': channel,
        'title': 'Synchronize shared package changes from Bitbucket', 'body': body})
    dispatch_validation(github, branch, configuration['validationWorkflow'])
    print('Prepared ' + pull['html_url'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root', type=Path, required=True)
    parser.add_argument('--bitbucket-root', type=Path, required=True)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    configuration = json.loads((args.repository_root / '.github/package-sync/config.json').read_text())
    profile = json.loads(args.profile.read_text())
    github = GitHub(configuration['githubRepository'], os.environ['GH_TOKEN']) if args.publish else None
    if args.publish:
        maintain_schedule_activity(args.repository_root, configuration)
    failures = []
    channels = configuration.get('channels', ['main', 'develop'])
    if not channels or len(set(channels)) != len(channels) or any(channel not in ('main', 'develop') for channel in channels):
        raise SystemExit('Invalid synchronization channel configuration')
    for channel in channels:
        try:
            sync_channel(args.repository_root, args.bitbucket_root, profile, configuration, channel,
                         github, args.publish)
        except (TranslationNeedsReview, RuntimeError) as error:
            failures.append(f'{channel}: {error}')
    if failures:
        raise SystemExit('\n'.join(failures))


if __name__ == '__main__':
    main()
