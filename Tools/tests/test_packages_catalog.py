import json
import unittest
from pathlib import Path


class PackagesCatalogTests(unittest.TestCase):
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
