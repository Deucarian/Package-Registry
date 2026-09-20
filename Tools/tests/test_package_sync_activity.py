import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_sync import git, maintain_schedule_activity, read_tree, text_git


class ScheduleActivityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='sync-activity-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.local = self.root / 'local'
        self.remote = self.root / 'remote'
        self.local.mkdir()
        self.remote.mkdir()
        git(self.remote, 'init', '--bare')
        git(self.local, 'init')
        git(self.local, 'remote', 'add', 'origin', str(self.remote))
        self.configuration = {'keepScheduleActive': True,
                              'committer': {'name': 'Fixture', 'email': 'fixture@example.invalid'}}
        self.now = datetime(2026, 9, 1, tzinfo=timezone.utc)

    def revision(self):
        return text_git(self.remote, 'rev-parse', 'refs/heads/sync/schedule-activity')

    def test_only_bookkeeping_branch_is_created_with_configured_identity(self):
        maintain_schedule_activity(self.local, self.configuration, self.now)
        revision = self.revision()
        self.assertEqual(['schedule-activity.json'], list(read_tree(self.remote, revision)))
        self.assertEqual(self.now.isoformat(), json.loads(read_tree(self.remote, revision)['schedule-activity.json'].data)['checkedAt'])
        self.assertEqual('Fixture\nfixture@example.invalid', text_git(self.remote, 'show', '-s', '--format=%an%n%ae', revision))
        self.assertEqual('refs/heads/sync/schedule-activity', text_git(self.remote, 'for-each-ref', '--format=%(refname)'))

    def test_recent_activity_is_not_rewritten_and_old_activity_fast_forwards(self):
        maintain_schedule_activity(self.local, self.configuration, self.now)
        first = self.revision()
        maintain_schedule_activity(self.local, self.configuration, self.now + timedelta(days=27))
        self.assertEqual(first, self.revision())
        maintain_schedule_activity(self.local, self.configuration, self.now + timedelta(days=29))
        second = self.revision()
        self.assertNotEqual(first, second)
        self.assertEqual(first, text_git(self.remote, 'rev-parse', second + '^'))

    def test_disabled_setting_makes_no_remote_changes(self):
        self.configuration['keepScheduleActive'] = False
        maintain_schedule_activity(self.local, self.configuration, self.now)
        self.assertEqual('', text_git(self.remote, 'for-each-ref', '--format=%(refname)'))
