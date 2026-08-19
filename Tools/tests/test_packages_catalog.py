import json
import unittest
from pathlib import Path


class PackagesCatalogTests(unittest.TestCase):
    def test_web_viewer_ecosystem_catalog_dependencies_match_direct_contracts(self):
        registry_root = Path(__file__).resolve().parents[2]
        packages = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))["packages"]
        packages_by_id = {package["id"]: package for package in packages}
        expected_dependencies = {
            "com.deucarian.api": [
                "com.deucarian.editor",
                "com.deucarian.logging",
            ],
            "com.deucarian.viewer-navigation": [
                "com.deucarian.camera-navigation",
                "com.deucarian.camera-navigation.input-system-integration",
                "com.deucarian.common",
                "com.deucarian.diagnostics",
                "com.deucarian.editor",
                "com.deucarian.logging",
                "com.deucarian.pointer-capture",
                "com.deucarian.theming",
                "com.deucarian.ui",
            ],
            "com.deucarian.command-routing.webgl-integration": [
                "com.deucarian.command-routing",
                "com.deucarian.diagnostics",
                "com.deucarian.editor",
                "com.deucarian.logging",
            ],
            "com.deucarian.activity-visualization": [
                "com.deucarian.diagnostics",
                "com.deucarian.logging",
            ],
            "com.deucarian.viewer-rendering": [
                "com.deucarian.common",
                "com.deucarian.diagnostics",
                "com.deucarian.logging",
                "com.deucarian.theming",
            ],
            "com.deucarian.viewer-shell": [
                "com.deucarian.common",
                "com.deucarian.theming",
                "com.deucarian.ui",
                "com.deucarian.viewer-rendering",
            ],
            "com.deucarian.viewer-authentication": [
                "com.deucarian.api",
                "com.deucarian.command-routing",
                "com.deucarian.editor",
                "com.deucarian.session",
                "com.deucarian.session.api-integration",
            ],
            "com.deucarian.simultria-api": [
                "com.deucarian.api",
                "com.deucarian.editor",
                "com.deucarian.session",
                "com.deucarian.session.api-integration",
                "com.deucarian.viewer-authentication",
            ],
            "com.deucarian.simultria-viewer-connection": [
                "com.deucarian.api",
                "com.deucarian.command-routing",
                "com.deucarian.editor",
                "com.deucarian.logging",
                "com.deucarian.simultria-api",
                "com.deucarian.viewer-authentication",
            ],
            "com.deucarian.web-viewer-suite": [
                "com.deucarian.api",
                "com.deucarian.build-pipeline",
                "com.deucarian.camera-navigation",
                "com.deucarian.camera-navigation.input-system-integration",
                "com.deucarian.command-routing",
                "com.deucarian.command-routing.webgl-integration",
                "com.deucarian.diagnostics",
                "com.deucarian.object-loading",
                "com.deucarian.object-loading.api-integration",
                "com.deucarian.pointer-capture",
                "com.deucarian.session",
                "com.deucarian.session.api-integration",
                "com.deucarian.theming",
                "com.deucarian.ui",
                "com.deucarian.viewer-navigation",
                "com.deucarian.viewer-rendering",
                "com.deucarian.viewer-shell",
                "com.deucarian.viewer-authentication",
            ],
            "com.deucarian.template.viewer.web": [
                "com.deucarian.api",
                "com.deucarian.build-pipeline",
                "com.deucarian.camera-navigation",
                "com.deucarian.command-routing",
                "com.deucarian.command-routing.webgl-integration",
                "com.deucarian.diagnostics",
                "com.deucarian.logging",
                "com.deucarian.object-loading",
                "com.deucarian.object-loading.api-integration",
                "com.deucarian.session",
                "com.deucarian.session.api-integration",
                "com.deucarian.theming",
                "com.deucarian.ui",
                "com.deucarian.viewer-navigation",
                "com.deucarian.viewer-rendering",
                "com.deucarian.viewer-shell",
                "com.deucarian.viewer-authentication",
                "com.deucarian.web-viewer-suite",
            ],
        }

        for package_id, dependencies in expected_dependencies.items():
            with self.subTest(package_id=package_id):
                self.assertEqual(dependencies, packages_by_id[package_id]["dependencies"])

        suite = packages_by_id["com.deucarian.web-viewer-suite"]
        self.assertEqual(suite["dependencies"], suite["suiteMembers"])

        template = packages_by_id["com.deucarian.template.viewer.web"]
        self.assertEqual(
            ["com.deucarian.template.viewer.web"],
            packages_by_id["com.deucarian.simultria-api"]["recommendedWith"],
        )
        self.assertEqual(
            ["com.deucarian.template.viewer.web"],
            packages_by_id["com.deucarian.simultria-viewer-connection"]["recommendedWith"],
        )
        self.assertEqual(
            ["core", "authenticated", "simultria"],
            [preset["id"] for preset in template["compositionPresets"]],
        )
        self.assertEqual(
            ["com.deucarian.simultria-viewer-connection"],
            template["compositionPresets"][2]["packageIds"],
        )

    def test_idle_auto_defense_template_declares_every_direct_assembly_dependency(self):
        registry_root = Path(__file__).resolve().parents[2]
        packages = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))["packages"]
        template = next(
            package
            for package in packages
            if package["id"] == "com.deucarian.template.game.idle-auto-defense"
        )

        self.assertEqual(
            [
                "com.deucarian.attacks",
                "com.deucarian.auto-defense",
                "com.deucarian.auto-defense-suite",
                "com.deucarian.combat",
                "com.deucarian.common",
                "com.deucarian.defense-games",
                "com.deucarian.editor",
                "com.deucarian.encounters",
                "com.deucarian.game-content-authoring",
                "com.deucarian.gameplay-foundation",
                "com.deucarian.idle-progression",
                "com.deucarian.monetization",
                "com.deucarian.persistence",
                "com.deucarian.progression",
                "com.deucarian.projectiles",
                "com.deucarian.run-upgrades",
                "com.deucarian.weapon-systems",
                "com.deucarian.world-navigation",
                "com.deucarian.world-spawning",
            ],
            template["dependencies"],
        )

    def test_attacks_catalog_dependencies_match_its_direct_package_contract(self):
        registry_root = Path(__file__).resolve().parents[2]
        packages = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))["packages"]
        attacks = next(package for package in packages if package["id"] == "com.deucarian.attacks")

        self.assertEqual(
            [
                "com.deucarian.gameplay-foundation",
                "com.deucarian.combat",
                "com.deucarian.editor",
                "com.deucarian.game-content-authoring",
            ],
            attacks["dependencies"],
        )


if __name__ == "__main__":
    unittest.main()
