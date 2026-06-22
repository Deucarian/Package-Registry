from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "deucarian_package_validator.py"
SPEC = importlib.util.spec_from_file_location("deucarian_package_validator", SCRIPT_PATH)
validator_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validator_module
SPEC.loader.exec_module(validator_module)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class ValidatorFixture:
    def __init__(self, root: Path):
        self.root = root
        self.registry = root / "Package-Registry"
        self.package = root / "Alpha"
        self.registry.mkdir()
        self.package.mkdir()
        self._registry()
        self._package()

    def _registry(self) -> None:
        write_json(
            self.registry / "packages.json",
            {
                "groups": [{"id": "core", "displayName": "Core"}],
                "packages": [
                    {
                        "id": "com.deucarian.alpha",
                        "displayName": "Deucarian Alpha",
                        "groupId": "core",
                        "dependencies": ["com.deucarian.logging"],
                        "stableUrl": "https://github.com/Deucarian/Alpha.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Alpha.git#develop",
                    },
                    {
                        "id": "com.deucarian.logging",
                        "displayName": "Deucarian Logging",
                        "groupId": "core",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/Logging.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Logging.git#develop",
                    },
                    {
                        "id": "com.deucarian.diagnostics",
                        "displayName": "Deucarian Diagnostics",
                        "groupId": "core",
                        "dependencies": [],
                        "stableUrl": "https://github.com/Deucarian/Diagnostics.git#main",
                        "developmentUrl": "https://github.com/Deucarian/Diagnostics.git#develop",
                    },
                ],
            },
        )
        write_json(
            self.registry / "capabilities.json",
            {
                "schemaVersion": 2,
                "capabilities": [
                    {"id": "alpha", "description": "Alpha capability.", "ownerPackageId": "com.deucarian.alpha"},
                    {"id": "logging", "description": "Logging.", "ownerPackageId": "com.deucarian.logging"},
                    {
                        "id": "unity-object-lifetime",
                        "description": "Object lifetime.",
                        "ownerPackageId": "com.deucarian.common",
                        "canonicalSymbols": ["Deucarian.Common.UnityObjectUtility.DestroySafely"],
                    },
                ],
            },
        )
        write_json(
            self.registry / "dependency-rules.json",
            {"schemaVersion": 2, "layers": [{"id": "common", "packages": ["com.deucarian.common"]}]},
        )
        write_json(
            self.registry / "DUPLICATION_REPORT.json",
            {
                "repositories": [
                    {
                        "packageId": "com.deucarian.alpha",
                        "asmdefs": [{"name": "Deucarian.Alpha"}, {"name": "Deucarian.Alpha.Optional"}],
                    },
                    {"packageId": "com.deucarian.logging", "asmdefs": [{"name": "Deucarian.Logging"}]},
                    {"packageId": "com.deucarian.diagnostics", "asmdefs": [{"name": "Deucarian.Diagnostics"}]},
                ]
            },
        )
        write_json(self.registry / "DEPENDENCY_USAGE_AUDIT.json", {"findings": []})
        write_json(self.registry / "DEBUG_API_AUDIT.json", {"invocations": []})
        write_json(
            self.registry / "UNITY_OBJECT_LIFETIME_AUDIT.json",
            {"conclusion": {"actionableProductionCount": 0}, "occurrences": []},
        )

    def _package(self) -> None:
        write_json(
            self.package / "package.json",
            {
                "name": "com.deucarian.alpha",
                "displayName": "Deucarian Alpha",
                "version": "1.2.3",
                "unity": "2022.3",
                "repository": {"type": "git", "url": "https://github.com/Deucarian/Alpha.git"},
                "dependencies": {"com.deucarian.logging": "1.0.0"},
            },
        )
        write(self.package / "README.md", "# Alpha\n\nCurrent package version: 1.2.3")
        write(self.package / "CHANGELOG.md", "# Changelog\n\n## 1.2.3\n- Test.")
        write(self.package / "LICENSE.md", "MIT")
        write_json(
            self.package / "Runtime" / "Alpha.asmdef",
            {"name": "Deucarian.Alpha", "references": ["Deucarian.Logging"]},
        )
        write_json(
            self.package / "Editor" / "Alpha.Editor.asmdef",
            {"name": "Deucarian.Alpha.Editor", "includePlatforms": ["Editor"], "references": ["Deucarian.Alpha"]},
        )
        write_json(
            self.package / "Samples~" / "Demo" / "Alpha.Sample.asmdef",
            {"name": "Deucarian.Alpha.Sample", "references": ["Deucarian.Alpha"]},
        )
        write_json(
            self.package / "Tests" / "Editor" / "Alpha.Tests.asmdef",
            {"name": "Deucarian.Alpha.Tests", "references": ["Deucarian.Alpha"], "optionalUnityReferences": ["TestAssemblies"]},
        )
        write_json(
            self.package / "deucarian-package.json",
            {
                "packageId": "com.deucarian.alpha",
                "displayName": "Deucarian Alpha",
                "ownedCapabilities": ["alpha"],
                "runtimeAssemblies": ["Deucarian.Alpha"],
                "editorAssemblies": ["Deucarian.Alpha.Editor"],
                "sampleAssemblies": ["Deucarian.Alpha.Sample"],
                "testAssemblies": ["Deucarian.Alpha.Tests"],
                "requiredDependencies": ["com.deucarian.logging"],
                "optionalVersionDefinedDependencies": [],
                "allowedDirectDebugCalls": [],
                "allowedDirectUnityObjectLifetimeCalls": [],
                "expectedSamplesRoot": "Samples~",
            },
        )


class DeucarianPackageValidatorTests(unittest.TestCase):
    def test_valid_package_uses_configured_manifest_assemblies_capability_and_registry_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            validator = validator_module.Validator(fixture.registry, fixture.package)

            result = validator.validate_package()

            self.assertTrue(result["ok"], result["errors"])

    def test_registry_audit_artifact_rejects_non_allowed_debug_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write_json(
                fixture.registry / "DEBUG_API_AUDIT.json",
                {
                    "invocations": [
                        {
                            "packageId": "com.deucarian.alpha",
                            "file": "Runtime/Alpha.cs",
                            "line": 4,
                            "policyDisposition": "Actionable",
                        }
                    ]
                },
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_registry()

            self.assertIn("DEBUG_API_AUDIT.json: com.deucarian.alpha Runtime/Alpha.cs:4 is not Allowed.", validator.errors)

    def test_common_api_boundary_rejects_extra_public_runtime_method(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            common = Path(temp) / "Common"
            common.mkdir()
            write(
                common / "Runtime" / "UnityObjectUtility.cs",
                """
                namespace Deucarian.Common
                {
                    public static class UnityObjectUtility
                    {
                        public static void DestroySafely(UnityEngine.Object target) {}
                        public static void ExtraApi() {}
                    }
                }
                """,
            )
            validator = validator_module.Validator(fixture.registry, common)

            validator.validate_common_api(common)

            self.assertTrue(any("unexpected public methods" in error for error in validator.errors))

    def test_optional_version_defined_dependency_reference_does_not_require_hard_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write_json(
                fixture.package / "Runtime" / "Alpha.Optional.asmdef",
                {
                    "name": "Deucarian.Alpha.Optional",
                    "references": ["Deucarian.Diagnostics"],
                    "versionDefines": [{"name": "com.deucarian.diagnostics", "expression": "0.1.0", "define": "HAS_DIAGNOSTICS"}],
                },
            )
            config_path = fixture.package / "deucarian-package.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["runtimeAssemblies"].append("Deucarian.Alpha.Optional")
            config["optionalVersionDefinedDependencies"] = ["com.deucarian.diagnostics"]
            write_json(config_path, config)
            validator = validator_module.Validator(fixture.registry, fixture.package)

            result = validator.validate_package()

            self.assertTrue(result["ok"], result["errors"])

    def test_release_policy_allows_validation_workflow_on_push(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "validate.yml",
                """
                name: Validate
                on:
                  push:
                    branches: [main, develop]
                  pull_request:
                jobs:
                  validate:
                    runs-on: ubuntu-latest
                    steps:
                      - uses: actions/checkout@v4
                      - run: python Tools/validate.py
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertEqual([], validator.errors)
            self.assertEqual(0, validator.details["releasePolicy"]["releaseWorkflowCount"])

    def test_release_policy_rejects_npm_publish_on_push(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "npm-stable.yml",
                """
                name: Publish
                on:
                  push:
                    branches: [main]
                jobs:
                  publish:
                    runs-on: ubuntu-latest
                    steps:
                      - run: npm publish
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertTrue(any("must not run on push" in error for error in validator.errors))
            self.assertEqual(1, validator.details["releasePolicy"]["publishWorkflowCount"])
            self.assertEqual([".github/workflows/npm-stable.yml"], validator.details["releasePolicy"]["autoPublishViolations"])

    def test_release_policy_rejects_tag_creation_on_push(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "release.yml",
                """
                name: Release
                on:
                  push:
                    branches: [main]
                jobs:
                  release:
                    runs-on: ubuntu-latest
                    steps:
                      - run: git tag v1.2.3
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertTrue(any("must not run on push" in error for error in validator.errors))
            self.assertEqual(1, validator.details["releasePolicy"]["releaseWorkflowCount"])

    def test_release_policy_accepts_guarded_manual_publish_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "npm-development.yml",
                f"""
                name: Publish Preview
                on:
                  workflow_dispatch:
                    inputs:
                      confirm_release:
                        description: "Type exactly: {validator_module.RELEASE_CONFIRMATION_TEXT}"
                        required: true
                        type: string
                jobs:
                  publish:
                    runs-on: ubuntu-latest
                    steps:
                      - run: npm publish --tag develop
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertEqual([], validator.errors)
            self.assertEqual([".github/workflows/npm-development.yml"], validator.details["releasePolicy"]["guardedManualPublishWorkflows"])

    def test_release_policy_counts_guarded_manual_release_artifact_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "release-package.yml",
                f"""
                name: Release Package Artifact
                on:
                  workflow_dispatch:
                    inputs:
                      confirm_release:
                        description: "Type exactly: {validator_module.RELEASE_CONFIRMATION_TEXT}"
                        required: true
                        type: string
                jobs:
                  package:
                    runs-on: ubuntu-latest
                    steps:
                      - uses: actions/upload-artifact@v4
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertEqual([], validator.errors)
            self.assertEqual(1, validator.details["releasePolicy"]["releaseWorkflowCount"])
            self.assertEqual(0, validator.details["releasePolicy"]["publishWorkflowCount"])

    def test_release_policy_rejects_unguarded_manual_publish_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            write(
                fixture.package / ".github" / "workflows" / "npm-development.yml",
                """
                name: Publish Preview
                on:
                  workflow_dispatch:
                    inputs:
                      mode:
                        type: choice
                        options: [dry-run, publish]
                jobs:
                  publish:
                    runs-on: ubuntu-latest
                    steps:
                      - run: npm publish --tag develop
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertTrue(any("must require confirm_release" in error for error in validator.errors))

    def test_release_policy_detects_publish_through_package_script(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = ValidatorFixture(Path(temp))
            package_json = json.loads((fixture.package / "package.json").read_text(encoding="utf-8"))
            package_json["scripts"] = {"release:stable": "npm publish --access public"}
            write_json(fixture.package / "package.json", package_json)
            write(
                fixture.package / ".github" / "workflows" / "npm-stable.yml",
                """
                name: Publish Stable
                on:
                  push:
                    branches: [main]
                jobs:
                  publish:
                    runs-on: ubuntu-latest
                    steps:
                      - run: npm run release:stable
                """,
            )
            validator = validator_module.Validator(fixture.registry, fixture.package)

            validator.validate_release_workflow_policy(fixture.package)

            self.assertEqual(1, validator.details["releasePolicy"]["publishWorkflowCount"])
            self.assertTrue(any("must not run on push" in error for error in validator.errors))


if __name__ == "__main__":
    unittest.main()
