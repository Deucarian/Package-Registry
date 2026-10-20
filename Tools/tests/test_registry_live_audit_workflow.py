"""Guard the live audit's blocking policy checks and failure evidence."""

from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github/workflows/package-registry-validation.yml"
).read_text(encoding="utf-8")


def step(name: str) -> str:
    match = re.search(
        rf"^      - name: {re.escape(name)}\n(.*?)(?=^      - name: |\Z)",
        WORKFLOW,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"Missing audit step: {name}")
    return match.group(1)


class RegistryLiveAuditWorkflowTests(unittest.TestCase):
    def test_authoritative_policy_check_reuses_provisioned_snapshot(self):
        body = step("Provision organization snapshots and validate live audit")
        commands = re.findall(
            r"python Tools/Generate-DeucarianAudit\.py\s+(.*?)(?=\n          python|\Z)",
            body,
            re.DOTALL,
        )
        self.assertEqual(2, len(commands))
        self.assertIn("--provision", commands[0])
        self.assertIn("--write", commands[0])
        self.assertNotIn("--provision", commands[1])
        self.assertIn("--check", commands[1])
        for command in commands:
            self.assertIn("--authoritative", command)
            self.assertIn('--audit-root "$RUNNER_TEMP/deucarian-org-audit"', command)
            self.assertIn('--output-root "$RUNNER_TEMP/deucarian-live-audit"', command)
        self.assertNotIn("continue-on-error", WORKFLOW)
        self.assertNotIn("|| true", WORKFLOW)

    def test_all_three_audits_validate_generated_reports(self):
        for name in (
            "Check organization AOT safety inventory",
            "Check compact Deucarian menu governance",
        ):
            body = step(name)
            self.assertIn("--check", body)
            self.assertEqual(2, body.count('--output-root "$RUNNER_TEMP/deucarian-live-audit"'))
            self.assertNotIn("--output-root .", body)
            self.assertIn("if: ${{ !cancelled() }}", body)

    def test_stable_and_scheduled_development_sources_remain_distinct(self):
        for name in (
            "Provision organization snapshots and validate live audit",
            "Check organization AOT safety inventory",
        ):
            body = step(name)
            self.assertIn("github.event_name == 'schedule' && 'develop'", body)
            self.assertIn("github.base_ref == 'main'", body)
            self.assertIn("&& 'main' || 'develop'", body)

    def test_failure_evidence_cannot_be_copied_committed_reports(self):
        preparation = step("Prepare isolated live audit reports")
        self.assertIn("audit.OUTPUT_FILES", preparation)
        self.assertIn("(output / name).unlink(missing_ok=True)", preparation)
        self.assertIn('"AOT_SAFETY_AUDIT.json"', preparation)
        self.assertIn('"MENU_AUDIT.json"', preparation)
        for name in ("Summarize report changes", "Upload organization audit reports"):
            self.assertIn("if: ${{ !cancelled() }}", step(name))
        self.assertIn("actions/upload-artifact@", step("Upload organization audit reports"))

    def run_summary(self, root: Path) -> str:
        source = textwrap.dedent(step("Summarize report changes").split("        run: |\n", 1)[1])
        summary = root / "summary.md"
        result = subprocess.run(
            [sys.executable, "-c", source],
            cwd=Path(__file__).resolve().parents[2],
            env={**os.environ, "RUNNER_TEMP": str(root), "GITHUB_STEP_SUMMARY": str(summary)},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return summary.read_text(encoding="utf-8")

    def test_summary_reports_missing_evidence_after_generation_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            summary = self.run_summary(Path(temporary))
        self.assertIn("Generated 0 of 19 reports", summary)
        self.assertIn("Audit generation is incomplete", summary)
        self.assertIn("Policy and deterministic-generation failures remain blocking", summary)

    def test_live_drift_is_advisory_and_does_not_change_committed_snapshot(self):
        committed = Path(__file__).resolve().parents[2] / "DUPLICATION_REPORT.json"
        original = committed.read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            generated = root / "deucarian-live-audit"
            generated.mkdir()
            (generated / committed.name).write_text('{"new": "live report"}\n', encoding="utf-8")
            summary = self.run_summary(root)
        self.assertIn("`DUPLICATION_REPORT.json` changed", summary)
        self.assertIn("Changes since the committed snapshot are advisory", summary)
        self.assertEqual(original, committed.read_bytes())


if __name__ == "__main__":
    unittest.main()
