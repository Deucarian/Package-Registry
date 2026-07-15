import json
import unittest
from pathlib import Path


RESERVED_PRODUCT_PACKAGE_IDS = {
    "com.deucarian.camera-navigation",
    "com.deucarian.theming",
    "com.deucarian.ui",
    "com.deucarian.xr-ui",
    "com.deucarian.xr-ui.theming-integration",
}
RELATIONSHIP_FIELDS = (
    "dependencies",
    "optionalCompanions",
    "optionalIntegrations",
    "integrationTargets",
    "recommendedWith",
    "suiteMembers",
)


class PackagesCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry_root = Path(__file__).resolve().parents[2]
        cls.registry = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))
        cls.packages = cls.registry["packages"]

    def test_public_catalog_contains_only_38_open_foundation_packages(self):
        package_ids = {package["id"] for package in self.packages}

        self.assertEqual(38, len(self.packages))
        self.assertTrue(RESERVED_PRODUCT_PACKAGE_IDS.isdisjoint(package_ids))

    def test_all_relationships_remain_inside_public_catalog(self):
        package_ids = {package["id"] for package in self.packages}

        for package in self.packages:
            for field in RELATIONSHIP_FIELDS:
                for target in package.get(field, []):
                    with self.subTest(package=package["id"], field=field, target=target):
                        self.assertIn(target, package_ids)
                        self.assertNotIn(target, RESERVED_PRODUCT_PACKAGE_IDS)

    def test_public_git_channels_preserve_main_and_develop_contract(self):
        for package in self.packages:
            with self.subTest(package=package["id"], channel="stable"):
                self.assertTrue(package["stableUrl"].endswith(".git#main"))
            with self.subTest(package=package["id"], channel="development"):
                self.assertTrue(package["developmentUrl"].endswith(".git#develop"))

    def test_idle_auto_defense_template_declares_editor_and_authoring_dependencies(self):
        template = next(
            package
            for package in self.packages
            if package["id"] == "com.deucarian.template.game.idle-auto-defense"
        )

        self.assertEqual(
            [
                "com.deucarian.auto-defense-suite",
                "com.deucarian.editor",
                "com.deucarian.game-content-authoring",
                "com.deucarian.gameplay-foundation",
                "com.deucarian.monetization",
            ],
            template["dependencies"],
        )


if __name__ == "__main__":
    unittest.main()
