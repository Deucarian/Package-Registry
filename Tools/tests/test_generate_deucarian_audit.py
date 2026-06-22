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
                    {
                        "id": "com.deucarian.gamma",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/Gamma.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Gamma.git#develop",
                    },
                    {
                        "id": "com.deucarian.sample-target",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/SampleTarget.git#main",
                        "developmentUrl": "https://github.com/Deucarian/SampleTarget.git#develop",
                    },
                ]
            },
        )
        self._alpha()
        self._beta()
        self._logging()
        self._gamma()
        self._sample_target()

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
                "repository": {"type": "git", "url": f"git+https://github.com/Deucarian/{name}.git"},
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
        write_json(repo / "Runtime.UGUI" / "Alpha.UGUI.asmdef", {"name": "Deucarian.Alpha.UGUI", "references": ["Deucarian.Alpha"]})
        write_json(repo / "Editor.Tools" / "Alpha.Editor.Tools.asmdef", {"name": "Deucarian.Alpha.Editor.Tools", "includePlatforms": ["Editor"], "references": []})
        write_json(repo / "Tests.EditMode" / "Alpha.Tests.EditMode.asmdef", {"name": "Deucarian.Alpha.Tests.EditMode", "references": ["Deucarian.Alpha"], "optionalUnityReferences": ["TestAssemblies"]})
        write_json(repo / "Samples~" / "Demo" / "Alpha.Sample.asmdef", {"name": "Deucarian.Alpha.Sample", "references": ["Deucarian.Alpha"]})
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
            repo / "Editor.Tools" / "AlphaEditor.cs",
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
            repo / "Tests.EditMode" / "AlphaTests.cs",
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
        write(
            repo / "Runtime.UGUI" / "AlphaButton.cs",
            """
            using UnityEngine;

            public class AlphaButton
            {
                public void Warn()
                {
                    Debug.LogWarning("runtime ugui warning");
                }
            }
            """,
        )
        write(
            repo / "Samples~" / "Demo" / "AlphaSample.cs",
            """
            public class AlphaSample
            {
                public void Use()
                {
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
        write(repo / "README.md", "# Logging\n\nCurrent package version: 1.0.0\n\nThis is an adapter bridge for console output.")
        write_json(repo / "Runtime" / "Logging.asmdef", {"name": "Deucarian.Logging", "references": []})
        write(
            repo / "Runtime" / "UnityConsoleLogSink.cs",
            """
            namespace Fixture
            {
                public static class UnityConsoleLogSink
                {
                    public static void Log()
                    {
                        UnityEngine.Debug.Log("allowed sink");
                        UnityEngine.Debug.LogWarning("allowed warning sink");
                    }
                }
            }
            """,
        )
        write(
            repo / "Editor" / "DeucarianLoggingMenu.cs",
            """
            namespace Fixture
            {
                public static class DeucarianLoggingMenu
                {
                    public static void ResetLoggingSettings()
                    {
                        UnityEngine.Debug.Log("non-sink logging menu");
                    }
                }
            }
            """,
        )

    def _gamma(self) -> None:
        repo = self._package("Gamma", "com.deucarian.gamma", "1.0.0")
        package_json = json.loads((repo / "package.json").read_text(encoding="utf-8"))
        package_json["repository"]["url"] = "git+https://github.com/Deucarian/Gamma-Bridge.git"
        write_json(repo / "package.json", package_json)
        write(
            repo / "README.md",
            """
            # Gamma

            Current package version: 1.0.0

            Install with:

            "com.deucarian.gamma": "https://github.com/Deucarian/Gamma-Bridge.git#main"
            """,
        )
        write(repo / "CHANGELOG.md", "# Changelog\n\n## 1.0.0\n- Renamed the Gamma Bridge package to Gamma Integration.")
        write_json(repo / "Runtime" / "Gamma.asmdef", {"name": "Deucarian.Gamma", "references": ["Deucarian.Beta"]})
        write_json(
            repo / "Runtime.Optional" / "Gamma.Optional.asmdef",
            {
                "name": "Deucarian.Gamma.Optional",
                "references": ["Deucarian.Logging"],
                "defineConstraints": ["DEUCARIAN_LOGGING_INSTALLED"],
                "versionDefines": [{"name": "com.deucarian.logging", "expression": "1.0.0", "define": "DEUCARIAN_LOGGING_INSTALLED"}],
            },
        )
        write_json(repo / "Tests.EditMode" / "Gamma.Tests.asmdef", {"name": "Deucarian.Gamma.Tests.EditMode", "references": ["Deucarian.Alpha"], "optionalUnityReferences": ["TestAssemblies"]})
        write_json(repo / "Samples~" / "Demo" / "Gamma.Sample.asmdef", {"name": "Deucarian.Gamma.Sample", "references": ["Deucarian.SampleTarget"]})
        write(repo / "Runtime" / "Gamma.cs", "public class GammaRuntime { }")
        write(repo / "Runtime.Optional" / "GammaOptional.cs", "public class GammaOptional { }")
        write(repo / "Tests.EditMode" / "GammaTests.cs", "public class GammaTests { }")
        write(repo / "Samples~" / "Demo" / "GammaSample.cs", "public class GammaSample { }")

    def _sample_target(self) -> None:
        repo = self._package("SampleTarget", "com.deucarian.sample-target", "1.0.0")
        write(repo / "README.md", "# Sample Target\n\nCurrent package version: 1.0.0")
        write_json(repo / "Runtime" / "SampleTarget.asmdef", {"name": "Deucarian.SampleTarget", "references": []})
        write(repo / "Runtime" / "SampleTarget.cs", "public class SampleTarget { }")


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

        self.assertEqual({"Debug.Log", "D.LogWarning", "Debug.LogError", "Debug.LogWarning"}, invocations)
        self.assertFalse(any("comment only" in item["invocation"] for item in records))
        warning = next(item for item in records if item["repository"] == "Alpha" and item["invocation"] == "Debug.LogWarning")
        self.assertEqual("Runtime production", warning["scope"])
        self.assertEqual("Warning", warning["logLevel"])
        self.assertEqual("Migrate", warning["policyDisposition"])
        self.assertEqual("Error", warning["policySeverity"])
        self.assertTrue(any(item["repository"] == "Alpha" and item["scope"] == "Test" and item["policyDisposition"] == "Allowed" for item in records))
        sink_warning = next(item for item in records if item["repository"] == "Logging" and item["invocation"] == "UnityEngine.Debug.LogWarning")
        self.assertEqual("Warning", sink_warning["logLevel"])
        self.assertEqual("Allowed", sink_warning["policyDisposition"])
        menu_log = next(item for item in records if item["repository"] == "Logging" and item["file"] == "Editor/DeucarianLoggingMenu.cs")
        self.assertEqual("Migrate", menu_log["policyDisposition"])

    def test_public_api_inventory_excludes_tests_and_internal_containing_types(self) -> None:
        report = self.build_fixture_report()
        symbols = report["publicApi"]["symbols"]
        symbol_names = {item["symbol"] for item in symbols}
        files = {item["file"] for item in symbols}

        self.assertIn("PublicAlpha", symbol_names)
        self.assertIn("DirectDebug", symbol_names)
        self.assertIn("Expression", symbol_names)
        self.assertNotIn("HiddenPublic", symbol_names)
        self.assertFalse(any(file.startswith("Tests") for file in files))
        self.assertTrue(any(item["symbol"] == "PublicTestFixture" for item in report["publicApi"]["tests"]))
        self.assertTrue(any(item["symbol"] == "HiddenPublic" for item in report["publicApi"]["internalPrivate"]))
        self.assertTrue(any(item["file"].startswith("Runtime.UGUI/") and item["scope"] == "Runtime production" for item in report["publicApi"]["runtimeProduction"]))
        self.assertTrue(any(item["file"].startswith("Editor.Tools/") and item["scope"] == "Editor production" for item in report["publicApi"]["editorProduction"]))
        self.assertTrue(any(item["file"].startswith("Samples~/") and item["scope"] == "Sample" for item in report["publicApi"]["samples"]))

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

        self.assertFalse(any(item["repository"] == "Alpha" and item["kind"] == "PackageVersionDrift" for item in doc_findings))
        self.assertTrue(any(item["repository"] == "Alpha" and item["kind"] == "DependencyVersionDrift" and item["dependency"] == "com.deucarian.beta" for item in doc_findings))
        beta_usage = next(item for item in dep_findings if item["repository"] == "Alpha" and item.get("dependency") == "com.deucarian.beta")
        self.assertEqual("RequiredAndUsed", beta_usage["classification"])
        self.assertEqual("Deucarian.Alpha", beta_usage["referencedBy"][0]["assembly"])
        self.assertEqual("Runtime/Alpha.asmdef", beta_usage["referencedBy"][0]["asmdef"])
        self.assertEqual("Deucarian.Beta", beta_usage["referencedBy"][0]["reference"])
        self.assertEqual("Runtime production", beta_usage["referencedBy"][0]["scope"])
        self.assertFalse(any(item["repository"] == "Alpha" and item.get("assemblyReference") == "Deucarian.Alpha" for item in dep_findings))

        gamma_beta = next(item for item in dep_findings if item["repository"] == "Gamma" and item.get("requiredPackage") == "com.deucarian.beta")
        self.assertEqual("MissingHardPackageDependency", gamma_beta["classification"])
        gamma_optional = next(item for item in dep_findings if item["repository"] == "Gamma" and item.get("requiredPackage") == "com.deucarian.logging")
        self.assertEqual("OptionalVersionDefinedUse", gamma_optional["classification"])
        self.assertEqual("VersionDefine", gamma_optional["referencedBy"][0]["guardKind"])
        gamma_test = next(item for item in dep_findings if item["repository"] == "Gamma" and item.get("requiredPackage") == "com.deucarian.alpha")
        self.assertEqual("TestOnlyUse", gamma_test["classification"])
        gamma_sample = next(item for item in dep_findings if item["repository"] == "Gamma" and item.get("requiredPackage") == "com.deucarian.sample-target")
        self.assertEqual("SampleOnlyUse", gamma_sample["classification"])

        self.assertTrue(any(item["repository"] == "Gamma" and item["kind"] == "ActiveRepositoryUrlDrift" and item.get("file") == "package.json" for item in doc_findings))
        self.assertTrue(any(item["repository"] == "Gamma" and item["kind"] == "ActiveDocumentationDrift" and item.get("file") == "README.md" for item in doc_findings))
        self.assertTrue(any(item["repository"] == "Gamma" and item["kind"] == "HistoricalChangelogReference" for item in doc_findings))
        self.assertTrue(any(item["repository"] == "Logging" and item["kind"] == "LegitimateGenericBridgeTerm" for item in doc_findings))

    def test_lifetime_conclusion_records_common_and_testing_decisions(self) -> None:
        conclusion = audit.classify_lifetime_conclusion(
            [
                {
                    "repository": "Object-Loading",
                    "file": "Runtime/Utilities/UnityObjectUtility.cs",
                    "symbol": "Destroy",
                    "assemblyPlatform": "Deucarian.ObjectLoading",
                    "scope": "Runtime production",
                    "occurrenceKind": "helper definition",
                    "semantics": {
                        "acceptedType": "Object",
                        "handlesNullOrFakeNull": True,
                        "usesPlayModeCheck": True,
                        "usesDestroy": True,
                        "usesDestroyImmediate": True,
                        "clearsReferences": False,
                        "handlesCollections": False,
                        "catchesExceptions": False,
                    },
                },
                {"repository": "Object-Loading", "scope": "Runtime production", "occurrenceKind": "helper call site", "invocation": "UnityObjectUtility.Destroy"},
                {
                    "repository": "UI-Binding",
                    "file": "Runtime/GenericItemManager.cs",
                    "symbol": "DestroyItem",
                    "assemblyPlatform": "Deucarian.UIBinding",
                    "scope": "Runtime production",
                    "occurrenceKind": "helper definition",
                    "semantics": {
                        "acceptedType": "GameObject",
                        "handlesNullOrFakeNull": True,
                        "usesPlayModeCheck": True,
                        "usesDestroy": True,
                        "usesDestroyImmediate": True,
                        "clearsReferences": False,
                        "handlesCollections": False,
                        "catchesExceptions": False,
                    },
                },
                {"repository": "UI-Binding", "scope": "Runtime production", "occurrenceKind": "helper call site", "invocation": "DestroyItem"},
                {"repository": "UI-FLow", "scope": "Runtime production", "occurrenceKind": "direct Unity API call", "containingSymbol": "UIFlowPrefabScreenProvider::Release", "file": "Runtime/Providers/UIFlowPrefabScreenProvider.cs", "invocation": "Object.Destroy"},
                {"repository": "UI-Binding", "scope": "Test", "occurrenceKind": "direct Unity API call", "invocation": "Object.DestroyImmediate"},
            ]
        )

        self.assertEqual("Create com.deucarian.common", conclusion["decision"])
        self.assertIn("UnityObjectUtility.DestroySafely(UnityEngine.Object target)", conclusion["apiProposal"])
        self.assertEqual("KeepLocal", conclusion["testingPackageDecision"]["decision"])

    def test_lifetime_policy_allows_common_and_canonical_consumers(self) -> None:
        records = [
            {
                "repository": "Common",
                "packageId": "com.deucarian.common",
                "file": "Runtime/UnityObjectUtility.cs",
                "symbol": "DestroySafely",
                "scope": "Runtime production",
                "occurrenceKind": "helper definition",
                "semantics": {
                    "acceptedType": "Object",
                    "handlesNullOrFakeNull": True,
                    "usesPlayModeCheck": True,
                    "usesDestroy": True,
                    "usesDestroyImmediate": True,
                    "clearsReferences": False,
                    "handlesCollections": False,
                    "catchesExceptions": False,
                },
            },
            {
                "repository": "Common",
                "packageId": "com.deucarian.common",
                "file": "Runtime/UnityObjectUtility.cs",
                "containingSymbol": "UnityObjectUtility::DestroySafely",
                "scope": "Runtime production",
                "occurrenceKind": "direct Unity API call",
                "invocation": "Object.Destroy",
            },
            {
                "repository": "Object-Loading",
                "packageId": "com.deucarian.object-loading",
                "file": "Runtime/Core/ObjectLoadHandle.cs",
                "scope": "Runtime production",
                "occurrenceKind": "helper call site",
                "invocation": "UnityObjectUtility.DestroySafely",
            },
            {
                "repository": "Legacy",
                "packageId": "com.deucarian.legacy",
                "file": "Runtime/Legacy.cs",
                "scope": "Runtime production",
                "occurrenceKind": "direct Unity API call",
                "invocation": "Object.DestroyImmediate",
            },
            {
                "repository": "UI-Binding",
                "packageId": "com.deucarian.ui-binding",
                "file": "Tests/EditMode/Fixture.cs",
                "scope": "Test",
                "occurrenceKind": "direct Unity API call",
                "invocation": "Object.DestroyImmediate",
            },
        ]

        audit.apply_lifetime_policy(records)
        conclusion = audit.classify_lifetime_conclusion(records)

        self.assertEqual("Allowed", records[0]["policyDisposition"])
        self.assertEqual("Allowed", records[1]["policyDisposition"])
        self.assertEqual("Allowed", records[2]["policyDisposition"])
        self.assertEqual("Migrate", records[3]["policyDisposition"])
        self.assertEqual("Allowed", records[4]["policyDisposition"])
        self.assertEqual("Implemented in com.deucarian.common", conclusion["decision"])
        self.assertEqual("com.deucarian.common", conclusion["canonicalOwner"])
        self.assertEqual(["Object-Loading"], conclusion["intendedConsumers"])


if __name__ == "__main__":
    unittest.main()
