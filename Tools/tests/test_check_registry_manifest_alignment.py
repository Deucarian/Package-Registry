from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "check_registry_manifest_alignment.py"
SPEC = importlib.util.spec_from_file_location("check_registry_manifest_alignment", SCRIPT_PATH)
alignment = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = alignment
SPEC.loader.exec_module(alignment)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class AlignmentFixture:
    def __init__(self, root: Path):
        self.root = root
        self.registry = root / "Package-Registry"
        self.audit_root = root
        self.registry.mkdir()
        self.write_registry()
        self.write_package("Alpha", "com.deucarian.alpha", "Deucarian Alpha", {"com.deucarian.logging": "1.0.0"})
        self.write_package("Logging", "com.deucarian.logging", "Deucarian Logging", {})

    def write_registry(self) -> None:
        write_json(
            self.registry / "packages.json",
            {
                "packages": [
                    {
                        "id": "com.deucarian.alpha",
                        "displayName": "Deucarian Alpha",
                        "stableUrl": "https://github.com/Deucarian/Alpha.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Alpha.git#develop",
                        "dependencies": ["com.deucarian.logging"],
                    },
                    {
                        "id": "com.deucarian.logging",
                        "displayName": "Deucarian Logging",
                        "stableUrl": "https://github.com/Deucarian/Logging.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Logging.git#develop",
                        "dependencies": [],
                    },
                    {
                        "id": "com.deucarian.missing",
                        "displayName": "Deucarian Missing",
                        "stableUrl": "https://github.com/Deucarian/Missing.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Missing.git#develop",
                        "dependencies": [],
                    },
                ]
            },
        )

    def write_package(
        self,
        repo: str,
        package_id: str,
        display_name: str,
        dependencies: dict[str, str],
        *,
        version: str = "1.0.0",
        unity: str = "2021.3",
    ) -> None:
        write_json(
            self.root / repo / "package.json",
            {
                "name": package_id,
                "displayName": display_name,
                "version": version,
                "unity": unity,
                "repository": {"type": "git", "url": f"git+https://github.com/Deucarian/{repo}.git"},
                "dependencies": dependencies,
            },
        )

    def report(self, require_checkouts: bool = False) -> dict:
        return alignment.AlignmentChecker(self.registry, self.audit_root, require_checkouts).build_report()


class RegistryManifestAlignmentTests(unittest.TestCase):
    def test_repo_name_parser_accepts_git_remote_line_tokens(self) -> None:
        self.assertEqual(
            "Package-Installer",
            alignment.repo_name_from_url("https://github.com/Deucarian/Package-Installer.git (fetch)"),
        )

    def test_matching_manifests_pass_and_missing_checkouts_warn(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))

            report = fixture.report()

            self.assertTrue(report["ok"], report)
            self.assertEqual(2, report["checkedPackages"])
            self.assertEqual(["com.deucarian.missing"], [item["packageId"] for item in report["missingCheckouts"]])
            self.assertTrue(report["warnings"])

    def test_dependency_mismatch_is_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))
            fixture.write_package("Alpha", "com.deucarian.alpha", "Deucarian Alpha", {})

            report = fixture.report()

            self.assertFalse(report["ok"], report)
            self.assertEqual("dependencies", report["findings"][0]["field"])
            self.assertEqual(["com.deucarian.logging"], report["findings"][0]["registry"])
            self.assertEqual([], report["findings"][0]["manifest"])

    def test_require_checkouts_promotes_missing_checkout_to_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))

            report = fixture.report(require_checkouts=True)

            self.assertFalse(report["ok"], report)
            self.assertIn("checkout", {finding["field"] for finding in report["findings"]})

    def test_manifest_identity_mismatches_are_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))
            fixture.write_package("Alpha", "com.deucarian.wrong", "Wrong Alpha", {"com.deucarian.logging": "1.0.0"})

            report = fixture.report()

            fields = {finding["field"] for finding in report["findings"]}
            self.assertIn("name", fields)
            self.assertIn("displayName", fields)

    def test_dependency_versions_must_match_dependency_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))
            fixture.write_package("Logging", "com.deucarian.logging", "Deucarian Logging", {}, version="1.1.0")

            report = fixture.report()

            self.assertFalse(report["ok"], report)
            self.assertIn("dependencyVersion:com.deucarian.logging", {item["field"] for item in report["findings"]})

    def test_dependency_unity_floor_cannot_exceed_package_floor(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = AlignmentFixture(Path(temp))
            fixture.write_package("Logging", "com.deucarian.logging", "Deucarian Logging", {}, unity="2022.3")

            report = fixture.report()

            self.assertFalse(report["ok"], report)
            self.assertIn("unityFloor:com.deucarian.logging", {item["field"] for item in report["findings"]})


if __name__ == "__main__":
    unittest.main()
