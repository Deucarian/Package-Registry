from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = TOOLS_ROOT / "Generate-DeucarianAotAudit.py"
SPEC = importlib.util.spec_from_file_location("generate_deucarian_aot_audit", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GenerateDeucarianAotAuditTests(unittest.TestCase):
    def test_generate_summarizes_clean_and_reflective_packages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_package(root / "Clean", "com.deucarian.clean", "public sealed class Clean { }")
            self.create_package(
                root / "Reflective",
                "com.deucarian.reflective",
                """
                using System;
                public static class Factory
                {
                    public static object Create(Type type)
                        => Activator.CreateInstance(type);
                }
                """,
            )

            audit = MODULE.generate(root, "Deucarian", "develop")

            self.assertEqual(audit["summary"]["repositoryCount"], 2)
            self.assertEqual(audit["summary"]["repositoriesWithFindings"], 1)
            self.assertEqual(audit["summary"]["cleanRepositoryCount"], 1)
            self.assertEqual(
                audit["summary"]["categoryCounts"],
                {"runtime-activator": 1},
            )
            reflective = next(
                item
                for item in audit["repositories"]
                if item["packageId"] == "com.deucarian.reflective"
            )
            self.assertEqual(reflective["findingCount"], 1)

    def test_write_and_check_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            audit_root = root / "audit"
            output_root = root / "output"
            self.create_package(audit_root / "Clean", "com.deucarian.clean", "public sealed class Clean { }")
            audit = MODULE.generate(audit_root, "Deucarian", "develop")

            self.assertTrue(MODULE.write_or_check(output_root, audit, check=False))
            self.assertTrue(MODULE.write_or_check(output_root, audit, check=True))
            json_path = output_root / MODULE.JSON_FILE
            data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(data["schemaVersion"], 1)
            (output_root / MODULE.MARKDOWN_FILE).write_text("stale\n", encoding="utf-8")
            self.assertFalse(MODULE.write_or_check(output_root, audit, check=True))

    @staticmethod
    def create_package(root: Path, package_id: str, source: str) -> None:
        runtime = root / "Runtime"
        runtime.mkdir(parents=True)
        (runtime / "Example.Runtime.asmdef").write_text(
            json.dumps({"name": "Example.Runtime"}),
            encoding="utf-8",
        )
        (runtime / "Example.cs").write_text(source, encoding="utf-8")
        (root / "deucarian-package.json").write_text(
            json.dumps(
                {
                    "packageId": package_id,
                    "runtimeAssemblies": ["Example.Runtime"],
                    "editorAssemblies": [],
                    "sampleAssemblies": [],
                    "testAssemblies": [],
                    "aotSafety": {"mode": "Audit", "exceptions": []},
                }
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
