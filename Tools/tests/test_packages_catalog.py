import json
import unittest
from pathlib import Path


class PackagesCatalogTests(unittest.TestCase):
    def test_every_package_has_complete_public_catalog_metadata(self):
        registry_root = Path(__file__).resolve().parents[2]
        catalog = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))

        self.assertEqual(44, len(catalog["packages"]))
        for package in catalog["packages"]:
            with self.subTest(package=package["id"]):
                self.assertTrue(package["displayName"].startswith("Deucarian "))
                self.assertTrue(package["description"].strip())
                public = package["public"]
                self.assertEqual("active", public["status"])
                self.assertEqual("upm-git", public["installMethod"])
                self.assertRegex(public["unity"], r"^\d{4}\.\d+$")
                repository_url = package["stableUrl"].removesuffix(".git#main")
                self.assertEqual(f"{repository_url}/blob/main/README.md", public["documentationUrl"])
                self.assertEqual(f"{repository_url}/blob/main/LICENSE.md", public["licenseUrl"])

    def test_dependency_graph_is_complete_and_acyclic(self):
        registry_root = Path(__file__).resolve().parents[2]
        packages = json.loads((registry_root / "packages.json").read_text(encoding="utf-8"))["packages"]
        graph = {package["id"]: package["dependencies"] for package in packages}

        for package_id, dependencies in graph.items():
            self.assertEqual(len(dependencies), len(set(dependencies)), package_id)
            self.assertNotIn(package_id, dependencies)
            self.assertTrue(set(dependencies) <= set(graph), package_id)

        visiting = set()
        visited = set()

        def visit(package_id):
            self.assertNotIn(package_id, visiting, f"dependency cycle at {package_id}")
            if package_id in visited:
                return
            visiting.add(package_id)
            for dependency in graph[package_id]:
                visit(dependency)
            visiting.remove(package_id)
            visited.add(package_id)

        for package_id in graph:
            visit(package_id)

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
