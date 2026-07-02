import json
import unittest
from pathlib import Path


class PackagesCatalogTests(unittest.TestCase):
    def test_idle_auto_defense_template_declares_editor_and_authoring_dependencies(self):
        registry_root = Path(__file__).resolve().parents[2]
        packages = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))["packages"]
        template = next(
            package
            for package in packages
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
