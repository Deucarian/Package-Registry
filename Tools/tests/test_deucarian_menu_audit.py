from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "deucarian_menu_audit.py"
SPEC = importlib.util.spec_from_file_location("deucarian_menu_audit", SCRIPT)
menu_audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = menu_audit
SPEC.loader.exec_module(menu_audit)


class MenuAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.policy = {
            "schemaVersion": 1,
            "root": "Tools/Deucarian",
            "approvedPaths": {
                "Tools/Deucarian/Control Center...": "com.deucarian.editor",
                "Tools/Deucarian/Package Installer...": "com.deucarian.package-installer",
            },
            "knownConstants": {
                "ExternalMenu.MenuRoot": "Tools/Deucarian",
            },
            "prohibitedFragments": ["Infrastructure", "Tools and Quality"],
            "permittedCrossPackageMenuBridges": [],
            "staleProjectSetupExclusions": ["Tests/", "CHANGELOG.md"],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def repo(self, name: str, package_id: str, source: str) -> Path:
        repo = self.root / name
        (repo / "Editor").mkdir(parents=True)
        (repo / "package.json").write_text(
            json.dumps({"name": package_id}), encoding="utf-8"
        )
        (repo / "Editor" / "Menu.cs").write_text(source, encoding="utf-8")
        return repo

    def test_accepts_owned_approved_constant_path(self) -> None:
        self.repo(
            "Editor",
            "com.deucarian.editor",
            'const string Path = "Tools/Deucarian/" + "Control Center...";\n'
            "[MenuItem(Path)] static void Open() {}",
        )
        report = menu_audit.audit(self.root, self.policy)
        self.assertTrue(report["summary"]["ok"], report["findings"])
        self.assertEqual(1, report["summary"]["entryCount"])

    def test_resolves_repository_and_known_external_constants(self) -> None:
        repo = self.repo(
            "Editor",
            "com.deucarian.editor",
            "[MenuItem(MenuPaths.ControlCenter)] static void Open() {}",
        )
        (repo / "Editor" / "MenuPaths.cs").write_text(
            "const string ControlCenter = "
            'ExternalMenu.MenuRoot + "/Control Center...";',
            encoding="utf-8",
        )

        report = menu_audit.audit(self.root, self.policy)
        self.assertTrue(report["summary"]["ok"], report["findings"])
        self.assertEqual(1, report["summary"]["entryCount"])

    def test_rejects_unauthorized_technical_duplicate_and_stale_paths(self) -> None:
        source = (
            '[MenuItem("Tools/Deucarian/Tools and Quality/Debug")] static void A() {}\n'
            '[MenuItem("Tools/Deucarian/Tools and Quality/Debug")] static void B() {}\n'
            'const string Old = "Tools/Deucarian/Project Setup";'
        )
        self.repo("Alpha", "com.deucarian.alpha", source)
        report = menu_audit.audit(self.root, self.policy)
        codes = {item["code"] for item in report["findings"]}
        self.assertTrue(
            {"UnauthorizedPath", "TechnicalTaxonomy", "DuplicatePath", "StaleProjectSetup"}
            <= codes
        )

    def test_rejects_cross_package_literal_navigation(self) -> None:
        self.repo(
            "Alpha",
            "com.deucarian.alpha",
            'static void Open() { Menu.ExecuteMenuItem("Tools/Deucarian/Package Installer..."); }',
        )
        report = menu_audit.audit(self.root, self.policy)
        self.assertIn(
            "CrossPackageMenuContract",
            {item["code"] for item in report["findings"]},
        )

    def test_rejects_editorapplication_cross_package_literal_navigation(self) -> None:
        self.repo(
            "Alpha",
            "com.deucarian.alpha",
            'static void Open() { EditorApplication.ExecuteMenuItem('
            '"Tools/Deucarian/Package Installer..."); }',
        )
        report = menu_audit.audit(self.root, self.policy)
        self.assertIn(
            "CrossPackageMenuContract",
            {item["code"] for item in report["findings"]},
        )

    def test_permits_audited_bootstrap_bridge(self) -> None:
        self.policy["permittedCrossPackageMenuBridges"] = [
            {
                "callerPackageId": "com.deucarian.bootstrap",
                "path": "Tools/Deucarian/Package Installer...",
            }
        ]
        self.repo(
            "Bootstrap",
            "com.deucarian.bootstrap",
            'static void Open() { EditorApplication.ExecuteMenuItem('
            '"Tools/Deucarian/Package Installer..."); }',
        )
        report = menu_audit.audit(self.root, self.policy)
        self.assertTrue(report["summary"]["ok"], report["findings"])

    def test_stale_project_setup_scans_text_and_respects_exclusions(self) -> None:
        repo = self.repo("Alpha", "com.deucarian.alpha", "static class Menu {}")
        (repo / "README.md").write_text(
            "Open Tools/Deucarian/Project Setup to continue.", encoding="utf-8"
        )
        (repo / "Editor" / "Legacy.uxml").write_text(
            '<Label text="Tools/Deucarian/Project Setup" />', encoding="utf-8"
        )
        (repo / "CHANGELOG.md").write_text(
            "Migrated Tools/Deucarian/Project Setup.", encoding="utf-8"
        )
        (repo / "Tests").mkdir()
        (repo / "Tests" / "Legacy.json").write_text(
            '"Tools/Deucarian/Project Setup"', encoding="utf-8"
        )

        report = menu_audit.audit(self.root, self.policy)
        stale = [
            item for item in report["findings"]
            if item["code"] == "StaleProjectSetup"
        ]
        self.assertEqual(
            ["Editor/Legacy.uxml", "README.md"],
            [item["file"] for item in stale],
        )

    def test_write_then_check_is_deterministic(self) -> None:
        self.repo(
            "Editor",
            "com.deucarian.editor",
            '[MenuItem("Tools/Deucarian/Control Center...")] static void Open() {}',
        )
        report = menu_audit.audit(self.root, self.policy)
        self.assertEqual(".", report["auditRoot"])
        output = self.root / "output"
        self.assertTrue(menu_audit.write_or_check(output, report, False))
        self.assertTrue(menu_audit.write_or_check(output, report, True))


if __name__ == "__main__":
    unittest.main()
