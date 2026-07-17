from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "project_package_catalogs.py"
SPEC = importlib.util.spec_from_file_location("project_package_catalogs", SCRIPT_PATH)
projection = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = projection
SPEC.loader.exec_module(projection)


def package(
    package_id: str,
    dependencies: list[str],
    *,
    stable_version: str | None = None,
) -> dict:
    repository_name = package_id.rsplit(".", 1)[-1].replace("-", "_").title().replace("_", "-")
    result = {
        "id": package_id,
        "displayName": "Deucarian " + repository_name,
        "kind": "Tool" if package_id == projection.INSTALLER_PACKAGE_ID else "Library",
        "groupId": "infrastructure",
        "category": "Tools" if package_id == projection.INSTALLER_PACKAGE_ID else "Core",
        "type": "Tool" if package_id == projection.INSTALLER_PACKAGE_ID else "Core",
        "ecosystemGroup": "Infrastructure",
        "description": f"{package_id} description.",
        "stableUrl": f"https://github.com/Deucarian/{repository_name}.git#main",
        "developmentUrl": f"https://github.com/Deucarian/{repository_name}.git#develop",
        "dependencies": dependencies,
    }
    if stable_version is not None:
        result["stableVersion"] = stable_version
        result["developmentVersion"] = stable_version + "-dev"
    return result


def registry_fixture() -> dict:
    return {
        "schemaVersion": 1,
        "updatedAt": "2026-07-13",
        "groups": [{"id": "infrastructure", "displayName": "Infrastructure"}],
        "packages": [
            package(
                projection.INSTALLER_PACKAGE_ID,
                ["com.deucarian.logging", "com.deucarian.editor"],
                stable_version="1.1.60",
            ),
            package("com.deucarian.unrelated", []),
            package("com.deucarian.logging", ["com.deucarian.editor"]),
            package("com.deucarian.editor", []),
        ],
    }


def write_json(path: Path, data: object, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(data, separators=(",", ":")) + "\n"
    else:
        text = json.dumps(data, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


class PackageCatalogProjectionTests(unittest.TestCase):
    def test_installer_projection_is_the_full_canonical_catalog(self) -> None:
        registry = registry_fixture()

        projected = projection.project_installer_catalog(registry)

        self.assertEqual(registry, projected)
        self.assertIsNot(registry, projected)
        self.assertEqual(4, len(projected["packages"]))
        self.assertIn("groups", projected)

    def test_bootstrap_projection_is_exact_dependency_first_installer_closure(self) -> None:
        projected = projection.project_bootstrap_catalog(registry_fixture())

        self.assertEqual(
            [
                "com.deucarian.editor",
                "com.deucarian.logging",
                projection.INSTALLER_PACKAGE_ID,
            ],
            [item["id"] for item in projected["packages"]],
        )
        self.assertEqual(set(projection.BOOTSTRAP_PACKAGE_FIELDS), set(projected["packages"][0]))
        self.assertEqual(registry_fixture()["groups"], projected["groups"])
        for item in projected["packages"]:
            self.assertNotIn("stableVersion", item)
            self.assertNotIn("developmentVersion", item)
            self.assertIn("groupId", item)
            self.assertIn("kind", item)
            self.assertNotIn("iconKey", item)

    def test_projection_rejects_missing_dependencies_and_cycles(self) -> None:
        missing = registry_fixture()
        missing["packages"][2]["dependencies"] = ["com.deucarian.missing"]
        with self.assertRaisesRegex(projection.CatalogProjectionError, "is not in packages.json"):
            projection.project_bootstrap_catalog(missing)

        cyclic = registry_fixture()
        cyclic["packages"][3]["dependencies"] = [projection.INSTALLER_PACKAGE_ID]
        with self.assertRaisesRegex(projection.CatalogProjectionError, "Dependency cycle detected"):
            projection.project_bootstrap_catalog(cyclic)

    def test_write_and_semantic_check_modes_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry_root = root / "Package-Registry"
            installer_root = root / "Package-Installer"
            bootstrap_root = root / "Bootstrap"
            write_json(registry_root / "packages.json", registry_fixture())

            arguments = [
                "--registry-root",
                str(registry_root),
                "--installer-root",
                str(installer_root),
                "--bootstrap-root",
                str(bootstrap_root),
            ]
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(0, projection.main(arguments))

            installer_path = installer_root / projection.INSTALLER_CATALOG_PATH
            bootstrap_path = bootstrap_root / projection.BOOTSTRAP_CATALOG_PATH
            installer_data = json.loads(installer_path.read_text(encoding="utf-8"))
            write_json(installer_path, installer_data, compact=True)

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(0, projection.main([*arguments, "--check"]))

            bootstrap_data = json.loads(bootstrap_path.read_text(encoding="utf-8"))
            bootstrap_data["packages"].pop()
            write_json(bootstrap_path, bootstrap_data)
            before_check = bootstrap_path.read_text(encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(1, projection.main([*arguments, "--check"]))
            self.assertEqual(before_check, bootstrap_path.read_text(encoding="utf-8"))

    def test_each_consumer_can_run_independent_write_and_check_modes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry_root = root / "Package-Registry"
            installer_root = root / "Package-Installer"
            bootstrap_root = root / "Bootstrap"
            write_json(registry_root / "packages.json", registry_fixture())

            common_arguments = ["--registry-root", str(registry_root)]
            consumer_arguments = (
                ["--installer-root", str(installer_root)],
                ["--bootstrap-root", str(bootstrap_root)],
            )
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                for arguments in consumer_arguments:
                    self.assertEqual(0, projection.main([*common_arguments, *arguments]))
                    self.assertEqual(0, projection.main([*common_arguments, *arguments, "--check"]))

            self.assertTrue((installer_root / projection.INSTALLER_CATALOG_PATH).exists())
            self.assertTrue((bootstrap_root / projection.BOOTSTRAP_CATALOG_PATH).exists())

    def test_repository_catalog_projects_expected_bootstrap_packages(self) -> None:
        registry_root = Path(__file__).resolve().parents[2]
        registry = projection.read_json(registry_root / "packages.json")

        projected = projection.project_bootstrap_catalog(registry)

        self.assertEqual(
            [
                "com.deucarian.editor",
                "com.deucarian.logging",
                projection.INSTALLER_PACKAGE_ID,
            ],
            [item["id"] for item in projected["packages"]],
        )


if __name__ == "__main__":
    unittest.main()
