import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync import STATE, commit, git, read_tree, sync_channel, text_git, write_tree
from package_sync_tree import Blob

IDENTITY = {'GIT_AUTHOR_NAME': 'Fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
            'GIT_COMMITTER_NAME': 'Fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid',
            'GIT_AUTHOR_DATE': '2026-01-01T00:00:00+00:00', 'GIT_COMMITTER_DATE': '2026-01-01T00:00:00+00:00'}
PROFILE = {'packageIds': {}, 'namespaceOverrides': {'Deucarian.Common': 'Simultria.Common'}, 'repositories': {}}


class GitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='package-sync-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        git(self.root, 'init', '--initial-branch=main')
        self.empty = text_git(self.root, 'commit-tree', write_tree(self.root, {}), data=b'Fixture\n', env=IDENTITY)

    def test_git_tree_round_trip_preserves_binary_modes_and_paths(self):
        tree = {'source with spaces/file.cs': Blob('100644', b'\xef\xbb\xbfsource\r\n'),
                'script': Blob('100755', b'line one\nline two\n'), 'asset': Blob('100644', b'\x00\xffasset')}
        revision = commit(self.root, tree, self.empty, 'Fixture', IDENTITY)
        self.assertEqual(tree, read_tree(self.root, revision))

    def test_empty_tree_round_trip(self):
        self.assertEqual({}, read_tree(self.root, self.empty))

    def test_commit_is_deterministic_with_preserved_identity(self):
        first = commit(self.root, {'file': Blob('100644', b'content')}, self.empty, 'Fixture', IDENTITY)
        second = commit(self.root, {'file': Blob('100644', b'content')}, self.empty, 'Fixture', IDENTITY)
        self.assertEqual(first, second)
        self.assertEqual('Fixture\nfixture@example.invalid', text_git(self.root, 'show', '-s', '--format=%an%n%ae', first))

    def test_dry_run_prepares_real_commit_without_changing_target_or_remote(self):
        github_tree = {'file.cs': Blob('100644', b'namespace Deucarian.Common { int value = 1; }')}
        upstream_tree = {'file.cs': Blob('100644', b'namespace Simultria.Common { int value = 1; }')}
        baseline = commit(self.root, github_tree, self.empty, 'GitHub source', IDENTITY)
        old_upstream = commit(self.root, upstream_tree, self.empty, 'Bitbucket source', IDENTITY)
        upstream_tree['file.cs'] = Blob('100644', b'namespace Simultria.Common { int value = 2; }')
        new_upstream = commit(self.root, upstream_tree, old_upstream, 'Shared fix', IDENTITY)
        state = {'channels': {'main': {'githubBaseline': baseline, 'bitbucketCommit': old_upstream}}}
        github_tree[STATE] = Blob('100644', json.dumps(state).encode())
        target = commit(self.root, github_tree, baseline, 'Sync configuration', IDENTITY)
        git(self.root, 'update-ref', 'refs/remotes/origin/main', target)
        git(self.root, 'update-ref', 'refs/heads/main', new_upstream)
        output = io.StringIO()
        config = {'committer': {'name': 'Fixture', 'email': 'fixture@example.invalid'}}
        with contextlib.redirect_stdout(output):
            sync_channel(self.root, self.root, PROFILE, config, 'main', None, False)
        proposed = output.getvalue().strip().split()[-1]
        actual = read_tree(self.root, proposed)
        self.assertEqual(b'namespace Deucarian.Common { int value = 2; }', actual['file.cs'].data)
        self.assertEqual(target, text_git(self.root, 'rev-parse', 'refs/remotes/origin/main'))
        advanced = json.loads(actual[STATE].data)['channels']['main']
        self.assertEqual(new_upstream, advanced['bitbucketCommit'])
        self.assertEqual(actual['file.cs'], read_tree(self.root, advanced['githubBaseline'])['file.cs'])


if __name__ == '__main__':
    unittest.main()
