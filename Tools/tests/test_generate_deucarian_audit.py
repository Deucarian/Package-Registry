from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "Generate-DeucarianAudit.py"
SPEC = importlib.util.spec_from_file_location("generate_deucarian_audit", SCRIPT_PATH)
audit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


class AuditFixture:
    def __init__(self, root: Path):
        self.audit_root = root / "audit"
        self.output_root = root / "registry"
        self.audit_root.mkdir()
        self.output_root.mkdir()
        write_json(
            self.output_root / "packages.json",
            {
                "packages": [
                    {
                        "id": "com.deucarian.alpha",
                        "dependencies": ["com.deucarian.beta", "com.deucarian.logging"],
                        "stableUrl": "https://github.com/Deucarian/Alpha.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Alpha.git#develop",
                    },
                    {
                        "id": "com.deucarian.beta",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/Beta.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Beta.git#develop",
                    },
                    {
                        "id": "com.deucarian.logging",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/Logging.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Logging.git#develop",
                    },
                ]
            },
        )
        self._alpha()
        self._beta()
        self._logging()

    def build(self) -> dict:
        args = argparse.Namespace(
            audit_root=self.audit_root,
            output_root=self.output_root,
            organization="Deucarian",
            ref="fixture",
            authoritative=True,
            format="all",
            include_repository=[],
            exclude_repository=[],
            check=False,
        )
        return audit.build_report(args)

    def _package(self, name: str, package_id: str, version: str, deps: dict[str, str] | None = None) -> Path:
        repo = self.audit_root / name
        repo.mkdir()
        write_json(
            repo / "package.json",
            {
                "name": package_id,
                "version": version,
                "displayName": name,
                "unity": "2022.3",
                "dependencies": deps or {},
            },
        )
        write(repo / "CHANGELOG.md", f"# Changelog\n\n## {version}\n- Fixture release.")
        return repo

    def _alpha(self) -> None:
        repo = self._package(
            "Alpha",
            "com.deucarian.alpha",
            "1.2.3",
            {"com.deucarian.beta": "1.0.0", "com.deucarian.logging": "1.0.0"},
        )
        write(
            repo / "README.md",
            """
            # Alpha

            Current package version: 1.2.3

            Dependency examples:
            - com.deucarian.beta 9.9.9
            - com.deucarian.logging 1.0.0
            """,
        )
        write_json(
            repo / "Runtime" / "Alpha.asmdef",
            {"name": "Deucarian.Alpha", "references": ["Deucarian.Beta", "Deucarian.Logging"]},
        )
        write_json(repo / "Editor" / "Alpha.Editor.asmdef", {"name": "Deucarian.Alpha.Editor", "references": []})
        write_json(repo / "Tests" / "Alpha.Tests.asmdef", {"name": "Deucarian.Alpha.Tests", "references": ["Deucarian.Alpha"]})
        write(
            repo / "Runtime" / "Alpha.cs",
            """
            using UnityEngine;
            using D = UnityEngine.Debug;

            namespace Fixture
            {
                public class PublicAlpha
                {
                    /// <summary>Writes a direct runtime debug message.</summary>
                    public void DirectDebug()
                    {
                        // Debug.Log("comment only");
                        var text = "Debug.Log should stay a string";
                        Debug.Log(text);
                    }

                    public void AliasDebug()
                    {
                        D.LogWarning("alias");
                    }

                    public void Destroy(Object target)
                    {
                        if (target != null)
                        {
                            Object.Destroy(target);
                        }
                    }

                    public static void SafeDestroy(Object target)
                    {
                        if (target == null)
                        {
                            return;
                        }

                        if (Application.isPlaying)
                        {
                            Object.Destroy(target);
                        }
                        else
                        {
                            Object.DestroyImmediate(target);
                        }

                        target = null;
                    }

                    public int DuplicateOne(int value)
                    {
                        var total = value + 1;
                        for (var index = 0; index < 3; index++)
                        {
                            total += index;
                        }

                        return total;
                    }

                    public bool Validate(int value)
                    {
                        var threshold = 0;
                        var inspected = value + threshold;
                        if (inspected > 10)
                        {
                            inspected -= 10;
                        }

                        return inspected > threshold;
                    }

                    public string Braces()
                    {
                        return "{ still a string }";
                    }

                    public int Expression(int value) => value + 4;

                    public void WithLocal()
                    {
                        void NestedLocal()
                        {
                            Debug.LogError("nested");
                        }

                        NestedLocal();
                    }
                }

                internal class InternalAlpha
                {
                    public void HiddenPublic()
                    {
                    }
                }
            }
            """,
        )
        write(
            repo / "Editor" / "AlphaEditor.cs",
            """
            using UnityEngine;

            public class AlphaEditor
            {
                public void Kill(Object target)
                {
                    Object.DestroyImmediate(target);
                }
            }
            """,
        )
        write(
            repo / "Tests" / "AlphaTests.cs",
            """
            using UnityEngine;

            public class PublicTestFixture
            {
                public void TestOnlyDebug()
                {
                    Debug.Log("test");
                }
            }
            """,
        )

    def _beta(self) -> None:
        repo = self._package("Beta", "com.deucarian.beta", "1.0.0")
        write(repo / "README.md", "# Beta\n\nCurrent package version: 1.0.0")
        write_json(repo / "Runtime" / "Beta.asmdef", {"name": "Deucarian.Beta", "references": []})
        write(
            repo / "Runtime" / "Beta.cs",
            """
            namespace Fixture
            {
                public class PublicBeta
                {
                    public int DuplicateTwo(int input)
                    {
                        var result = input + 1;
                        for (var i = 0; i < 3; i++)
                        {
                            result += i;
                        }

                        return result;
                    }

                    public bool Validate(int value)
                    {
                        var threshold = 0;
                        var inspected = value - threshold;
                        if (inspected < -10)
                        {
                            inspected += 10;
                        }

                        return inspected < threshold;
                    }
                }
            }
            """,
        )

    def _logging(self) -> None:
        repo = self._package("Logging", "com.deucarian.logging", "1.0.0")
        write(repo / "README.md", "# Logging\n\nCurrent package version: 1.0.0")
        write_json(repo / "Runtime" / "Logging.asmdef", {"name": "Deucarian.Logging", "references": []})
        write(
            repo / "Runtime" / "Logging.cs",
            """
            namespace Fixture
            {
                public static class UnityConsoleLogSink
                {
                    public static void Log()
                    {
                        UnityEngine.Debug.Log("allowed sink");
                    }
                }
            }
            """,
        )


class GenerateDeucarianAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not audit.CSharpSyntaxAnalyzer(authoritative=False).available:
            raise unittest.SkipTest("tree-sitter C# parser is not installed")

    def build_fixture_report(self) -> dict:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return AuditFixture(Path(temp.name)).build()

    def test_debug_audit_uses_invocations_not_text_mentions(self) -> None:
        report = self.build_fixture_report()
        records = report["debugApi"]["invocations"]

        alpha_runtime = [
            item for item in records
            if item["repository"] == "Alpha" and item["scope"] == "Runtime production"
        ]
        invocations = {item["invocation"] for item in alpha_runtime}

        self.assertEqual({"Debug.Log", "D.LogWarning", "Debug.LogError"}, invocations)
        self.assertFalse(any("comment only" in item["invocation"] for item in records))
        self.assertTrue(any(item["repository"] == "Alpha" and item["scope"] == "Test" and item["initialDisposition"] == "allowed" for item in records))
        self.assertTrue(any(item["repository"] == "Logging" and item["classification"] == "Logging package sink implementation" and item["initialDisposition"] == "allowed" for item in records))

    def test_public_api_inventory_excludes_tests_and_internal_containing_types(self) -> None:
        report = self.build_fixture_report()
        symbols = report["publicApi"]["symbols"]
        symbol_names = {item["symbol"] for item in symbols}
        files = {item["file"] for item in symbols}

        self.assertIn("PublicAlpha", symbol_names)
        self.assertIn("DirectDebug", symbol_names)
        self.assertIn("Expression", symbol_names)
        self.assertNotIn("HiddenPublic", symbol_names)
        self.assertFalse(any(file.startswith("Tests/") for file in files))
        self.assertTrue(any(item["symbol"] == "PublicTestFixture" for item in report["publicApi"]["tests"]))
        self.assertTrue(any(item["symbol"] == "HiddenPublic" for item in report["publicApi"]["internalPrivate"]))

    def test_clone_analysis_uses_parsed_method_bodies(self) -> None:
        report = self.build_fixture_report()
        structural = report["duplication"]["normalizedStructuralCloneGroups"]
        semantic = report["duplication"]["sameSymbolSemanticCandidates"]

        self.assertTrue(any(set(group["repositories"]) == {"Alpha", "Beta"} for group in structural))
        self.assertTrue(any(group["groupKey"] == "validate" and set(group["repositories"]) == {"Alpha", "Beta"} for group in semantic))
        self.assertEqual([], report["parseFailures"])

    def test_lifetime_audit_separates_direct_calls_and_helper_definitions(self) -> None:
        report = self.build_fixture_report()
        records = report["unityObjectLifetime"]["occurrences"]

        self.assertTrue(any(item["repository"] == "Alpha" and item["occurrenceKind"] == "direct Unity API call" and item.get("invocation") == "Object.Destroy" for item in records))
        helper = next(item for item in records if item["repository"] == "Alpha" and item["occurrenceKind"] == "helper definition")
        self.assertTrue(helper["semantics"]["usesPlayModeCheck"])
        self.assertTrue(helper["semantics"]["usesDestroyImmediate"])

    def test_documentation_and_dependency_usage_are_classified_separately(self) -> None:
        report = self.build_fixture_report()
        doc_findings = report["documentationDrift"]["findings"]
        dep_findings = report["dependencyUsage"]["findings"]

        self.assertFalse(any(item["repository"] == "Alpha" and item["kind"] == "package version drift" for item in doc_findings))
        self.assertTrue(any(item["repository"] == "Alpha" and item["kind"] == "dependency version drift" and item["dependency"] == "com.deucarian.beta" for item in doc_findings))
        beta_usage = next(item for item in dep_findings if item["repository"] == "Alpha" and item.get("dependency") == "com.deucarian.beta")
        self.assertEqual("required and used", beta_usage["classification"])
        self.assertEqual([{"assembly": "Deucarian.Alpha", "asmdef": "Runtime/Alpha.asmdef", "reference": "Deucarian.Beta", "scope": "Runtime production"}], beta_usage["referencedBy"])
        self.assertFalse(any(item["repository"] == "Alpha" and item.get("assemblyReference") == "Deucarian.Alpha" for item in dep_findings))


if __name__ == "__main__":
    unittest.main()
