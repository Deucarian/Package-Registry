from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "generate_public_catalog_unity_matrix.py"
SPEC = importlib.util.spec_from_file_location("generate_public_catalog_unity_matrix", SCRIPT_PATH)
matrix = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = matrix
SPEC.loader.exec_module(matrix)


def package(package_id: str, dependencies: list[str]) -> dict:
    repository_name = package_id.rsplit(".", 1)[-1].title()
    return {
        "id": package_id,
        "stableUrl": f"https://github.com/Deucarian/{repository_name}.git#main",
        "developmentUrl": f"https://github.com/Deucarian/{repository_name}.git#develop",
        "dependencies": dependencies,
    }


class PublicCatalogUnityMatrixTests(unittest.TestCase):
    def test_matrix_is_dependency_first_and_has_both_channels(self) -> None:
        registry = {
            "updatedAt": "2026-07-15",
            "packages": [
                package("com.deucarian.consumer", ["com.deucarian.foundation"]),
                package("com.deucarian.foundation", []),
            ],
        }

        result = matrix.build_matrix(registry)

        self.assertEqual(2, result["packageCount"])
        self.assertEqual(4, result["caseCount"])
        consumer_cases = [case for case in result["cases"] if case["targetPackageId"].endswith("consumer")]
        self.assertEqual(["stable", "development"], [case["channel"] for case in consumer_cases])
        self.assertEqual(
            ["com.deucarian.foundation", "com.deucarian.consumer"],
            [item["id"] for item in consumer_cases[0]["dependencyFirstClosure"]],
        )

    def test_matrix_rejects_reserved_packages_and_wrong_channel_routes(self) -> None:
        reserved = {
            "updatedAt": "2026-07-15",
            "packages": [package("com.deucarian.theming", [])],
        }
        with self.assertRaisesRegex(matrix.CatalogProjectionError, "reserved proprietary"):
            matrix.build_matrix(reserved)

        wrong_route = package("com.deucarian.foundation", [])
        wrong_route["stableUrl"] = "https://github.com/Deucarian/Foundation.git#develop"
        with self.assertRaisesRegex(matrix.CatalogProjectionError, "stableUrl must end with .git#main"):
            matrix.build_matrix({"updatedAt": "2026-07-15", "packages": [wrong_route]})

    def test_repository_matrix_is_current_and_covers_76_cases(self) -> None:
        repository_root = Path(__file__).resolve().parents[2]
        result = matrix.build_matrix(matrix.read_json(repository_root / "packages.json"))

        self.assertEqual(38, result["packageCount"])
        self.assertEqual(76, result["caseCount"])
        self.assertEqual(
            0,
            len(
                matrix.RESERVED_PRODUCT_PACKAGE_IDS.intersection(
                    item["id"]
                    for case in result["cases"]
                    for item in case["dependencyFirstClosure"]
                )
            ),
        )

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "matrix.json"
            self.assertEqual(0, matrix.main(["--registry-root", str(repository_root), "--output", str(output)]))
            self.assertEqual(
                0,
                matrix.main(
                    ["--registry-root", str(repository_root), "--output", str(output), "--check"]
                ),
            )
            self.assertEqual(76, json.loads(output.read_text(encoding="utf-8"))["caseCount"])


if __name__ == "__main__":
    unittest.main()
