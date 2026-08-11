from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from deucarian_aot_validator import AotValidator  # noqa: E402


class DeucarianAotValidatorTests(unittest.TestCase):
    def test_audit_reports_runtime_newtonsoft_without_failing(self) -> None:
        with self.package() as root:
            self.write_runtime(
                root,
                "Parser.cs",
                """
                using Newtonsoft.Json;
                public static class Parser
                {
                    public static Dto Parse(string json)
                        => JsonConvert.DeserializeObject<Dto>(json);
                }
                public sealed class Dto { }
                """,
            )

            result = AotValidator(root).validate()

            self.assertTrue(result["ok"])
            self.assertEqual(result["mode"], "Audit")
            self.assertEqual(
                [finding["rule"] for finding in result["findings"]],
                ["reflection-based-newtonsoft"],
            )
            self.assertTrue(result["warnings"])

    def test_enforce_rejects_runtime_reflection(self) -> None:
        with self.package(mode="Enforce") as root:
            self.write_runtime(
                root,
                "Factory.cs",
                """
                using System;
                public static class Factory
                {
                    public static object Create(Type type)
                        => Activator.CreateInstance(type);
                }
                """,
            )

            result = AotValidator(root).validate()

            self.assertFalse(result["ok"])
            self.assertEqual(result["findings"][0]["rule"], "runtime-activator")
            self.assertTrue(any("runtime-activator" in error for error in result["errors"]))

    def test_editor_reflection_is_not_player_finding(self) -> None:
        with self.package(mode="Enforce") as root:
            editor = root / "Editor"
            editor.mkdir()
            (editor / "Editor.asmdef").write_text(
                json.dumps({"name": "Example.Editor", "includePlatforms": ["Editor"]}),
                encoding="utf-8",
            )
            (editor / "Discovery.cs").write_text(
                "using System; class Discovery { object X(Type t) => Activator.CreateInstance(t); }",
                encoding="utf-8",
            )

            result = AotValidator(root).validate()

            self.assertTrue(result["ok"])
            self.assertEqual(result["findings"], [])

    def test_delegate_invoke_is_not_mistaken_for_unity_string_dispatch(self) -> None:
        with self.package(mode="Enforce") as root:
            self.write_runtime(
                root,
                "Signals.cs",
                """
                using System;
                using UnityEngine;
                public sealed class Signals : MonoBehaviour
                {
                    public event Action Changed;
                    public void Raise() => Changed?.Invoke();
                }
                """,
            )

            result = AotValidator(root).validate()

            self.assertTrue(result["ok"])
            self.assertEqual(result["findings"], [])

    def test_literal_unity_dispatch_is_detected(self) -> None:
        with self.package(mode="Enforce") as root:
            self.write_runtime(
                root,
                "Legacy.cs",
                """
                using UnityEngine;
                public sealed class Legacy : MonoBehaviour
                {
                    public void Run() => Invoke("Refresh", 1f);
                }
                """,
            )

            result = AotValidator(root).validate()

            self.assertFalse(result["ok"])
            self.assertEqual(result["findings"][0]["rule"], "unity-string-dispatch")

    def test_exact_exception_suppresses_only_the_reported_symbol(self) -> None:
        with self.package(
            mode="Enforce",
            exceptions=[
                {
                    "file": "Runtime/Factory.cs",
                    "rule": "runtime-activator",
                    "symbol": "Activator.CreateInstance",
                    "strategy": "Declared",
                    "reason": "Vendor compatibility boundary.",
                    "preserveTypes": [
                        {
                            "assemblyName": "Vendor.Runtime",
                            "typeName": "Vendor.CallbackReceiver",
                            "reason": "Created by the vendor boundary.",
                        }
                    ],
                }
            ],
        ) as root:
            self.write_runtime(
                root,
                "Factory.cs",
                """
                using System;
                public static class Factory
                {
                    public static object Create(Type type)
                        => Activator.CreateInstance(type);
                }
                """,
            )

            result = AotValidator(root).validate()

            self.assertTrue(result["ok"])
            self.assertEqual(result["findings"], [])
            self.assertEqual(len(result["suppressedFindings"]), 1)

    def test_declared_exception_requires_exact_preserve_targets(self) -> None:
        with self.package(
            mode="Audit",
            exceptions=[
                {
                    "file": "Runtime/Factory.cs",
                    "rule": "runtime-activator",
                    "symbol": "Activator.CreateInstance",
                    "strategy": "Declared",
                    "reason": "Incomplete exception.",
                }
            ],
        ) as root:
            result = AotValidator(root).validate()

            self.assertFalse(result["ok"])
            self.assertTrue(any("preserveTypes" in error for error in result["errors"]))

    def test_manual_link_xml_is_audited(self) -> None:
        with self.package() as root:
            (root / "Runtime" / "link.xml").write_text("<linker />", encoding="utf-8")

            result = AotValidator(root).validate()

            self.assertTrue(result["ok"])
            self.assertEqual(result["findings"][0]["rule"], "manual-link-xml")

    def package(self, mode: str = "Audit", exceptions: list[dict] | None = None):
        case = self

        class PackageContext:
            def __enter__(self) -> Path:
                self.temp = tempfile.TemporaryDirectory()
                root = Path(self.temp.name)
                runtime = root / "Runtime"
                runtime.mkdir()
                (runtime / "Example.Runtime.asmdef").write_text(
                    json.dumps({"name": "Example.Runtime"}),
                    encoding="utf-8",
                )
                config = {
                    "packageId": "com.deucarian.example",
                    "runtimeAssemblies": ["Example.Runtime"],
                    "editorAssemblies": [],
                    "sampleAssemblies": [],
                    "testAssemblies": [],
                    "aotSafety": {
                        "mode": mode,
                        "exceptions": exceptions or [],
                    },
                }
                (root / "deucarian-package.json").write_text(
                    json.dumps(config),
                    encoding="utf-8",
                )
                return root

            def __exit__(self, exc_type, exc, traceback) -> None:
                self.temp.cleanup()

        return PackageContext()

    @staticmethod
    def write_runtime(root: Path, name: str, content: str) -> None:
        (root / "Runtime" / name).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
