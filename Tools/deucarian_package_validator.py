#!/usr/bin/env python3
"""Shared Deucarian package and registry validator."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from project_package_catalogs import (  # noqa: E402
    CatalogProjectionError,
    project_bootstrap_catalog,
    project_installer_catalog,
)


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
PACKAGE_ID_RE = re.compile(r"^com\.deucarian(\.[a-z0-9]+(?:-[a-z0-9]+)*)+$")
ICON_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UNITY_VERSION_RE = re.compile(r"^\d{4}\.\d+$")
GIT_URL_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git#(?P<branch>[A-Za-z0-9._/-]+)$")
README_VERSION_PATTERNS = (
    re.compile(r"Current package version\s*[:|]\s*`?(\d+\.\d+\.\d+)`?", re.I),
    re.compile(r"\|\s*Package version\s*\|\s*`?(\d+\.\d+\.\d+)`?\s*\|", re.I),
    re.compile(r"\|\s*Version\s*\|\s*`?(\d+\.\d+\.\d+)`?\s*\|", re.I),
)
CHANGELOG_VERSION_RE = re.compile(r"^##\s+\[?(\d+\.\d+\.\d+)\]?", re.M)
SKIP_DIRS = {".git", "Library", "PackageCache", "Temp", "Obj", "obj", "bin", ".vs", ".idea", "Logs"}
GENERATED_ARCHIVE_EXTENSIONS = {".unitypackage", ".zip", ".tar", ".tgz"}
DESTROY_HELPER_NAMES = {
    "DestroyUnityObject",
    "DestroyUnityObjectSafely",
    "SafeDestroy",
    "DestroySafely",
    "DestroyObject",
    "DestroyItem",
}
DEBUG_CALL_RE = re.compile(r"\b(?:UnityEngine\.)?Debug\.(Log(?:Format|WarningFormat|Warning|ErrorFormat|Error|Exception)?)\s*\(")
LIFETIME_CALL_RE = re.compile(r"\b(?:UnityEngine\.)?Object\.(DestroyImmediate|Destroy)\s*\(")
HELPER_DEFINITION_RE = re.compile(
    r"^\s*(?:public|internal|private|protected)\s+"
    r"(?:static\s+)?(?:void|Task|ValueTask|IEnumerator|[A-Za-z_][A-Za-z0-9_<>,.\[\]?]*)\s+"
    r"(?P<name>DestroyUnityObjectSafely|DestroyUnityObject|SafeDestroy|DestroySafely|DestroyObject|DestroyItem)\s*\(",
    re.M,
)
RELEASE_CONFIRMATION_TEXT = "I understand this publishes a Deucarian package"
WORKFLOW_FILE_RE = re.compile(r"\.ya?ml$", re.I)
NPM_PUBLISH_RE = re.compile(r"\bnpm\s+publish\b", re.I)
NPM_TOKEN_RE = re.compile(r"\b(?:NPM_TOKEN|NODE_AUTH_TOKEN)\b")
TRUSTED_PUBLISHING_RE = re.compile(r"\bid-token\s*:\s*write\b", re.I)
GIT_TAG_RE = re.compile(r"\bgit\s+tag\b", re.I)
GITHUB_RELEASE_RE = re.compile(r"\bgh\s+release\b|actions/create-release|softprops/action-gh-release", re.I)
GIT_RELEASE_PREP_RE = re.compile(r"\bgit\s+(?:commit|push)\b", re.I)
WORKFLOW_PUSH_RE = re.compile(r"^\s*push\s*:|\bon\s*:\s*\[[^\]]*\bpush\b|^\s*on\s*:\s*push\s*$", re.I | re.M)
WORKFLOW_DISPATCH_RE = re.compile(r"^\s*workflow_dispatch\s*:|\bon\s*:\s*\[[^\]]*\bworkflow_dispatch\b|^\s*on\s*:\s*workflow_dispatch\s*$", re.I | re.M)
WORKFLOW_TAG_TRIGGER_RE = re.compile(r"^\s*tags\s*:", re.I | re.M)
RELEASE_ARTIFACT_RE = re.compile(r"\brelease\b|upload-artifact|git\s+archive|Compress-Archive", re.I)
RELEASE_WORKFLOW_NAME_RE = re.compile(r"^\s*name\s*:\s*.*\brelease\b", re.I | re.M)
PACKAGE_KINDS = {"Library", "Tool", "Integration", "Suite", "Template"}
PUBLIC_PACKAGE_STATUSES = {"active", "preview", "deprecated"}
PUBLIC_INSTALL_METHODS = {"upm-git"}
SAMPLE_POLICIES = {"compiled-example", "playable-scene", "tool", "composition", "template"}


class ValidationError(Exception):
    pass


class Validator:
    def __init__(self, registry_root: Path, repository_root: Path | None = None, config_path: Path | None = None, check_remote_urls: bool = False):
        self.registry_root = registry_root.resolve()
        self.repository_root = repository_root.resolve() if repository_root else None
        self.config_path = config_path.resolve() if config_path else None
        self.check_remote_urls = check_remote_urls
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.details: dict[str, Any] = {}
        self.packages = self.read_json(self.registry_root / "packages.json", required=False) or {"packages": []}
        self.capabilities = self.read_json(self.registry_root / "capabilities.json", required=False) or {"capabilities": []}
        self.dependency_rules = self.read_json(self.registry_root / "dependency-rules.json", required=False) or {}
        self.duplication_report = self.read_json(self.registry_root / "DUPLICATION_REPORT.json", required=False) or {}
        self.debug_audit = self.read_json(self.registry_root / "DEBUG_API_AUDIT.json", required=False) or {}
        self.lifetime_audit = self.read_json(self.registry_root / "UNITY_OBJECT_LIFETIME_AUDIT.json", required=False) or {}
        self.dependency_usage_audit = self.read_json(self.registry_root / "DEPENDENCY_USAGE_AUDIT.json", required=False) or {}
        self.registry_packages_by_id = {pkg.get("id"): pkg for pkg in self.packages.get("packages", []) if isinstance(pkg, dict) and pkg.get("id")}
        self.registry_groups_by_id = {group.get("id"): group for group in self.packages.get("groups", []) if isinstance(group, dict) and group.get("id")}
        self.capabilities_by_owner = defaultdict(list)
        for capability in self.capabilities.get("capabilities", []):
            if isinstance(capability, dict) and capability.get("ownerPackageId"):
                self.capabilities_by_owner[capability["ownerPackageId"]].append(capability.get("id"))
        self.assembly_to_package = self.build_assembly_index()

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def read_json(self, path: Path, required: bool = True) -> Any:
        if not path.exists():
            if required:
                self.fail(f"{self.display_path(path)} is missing.")
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            self.fail(f"{self.display_path(path)} is not valid JSON: {exc}")
            return None

    def display_path(self, path: Path) -> str:
        try:
            if self.repository_root and path.resolve().is_relative_to(self.repository_root):
                return path.resolve().relative_to(self.repository_root).as_posix()
            if path.resolve().is_relative_to(self.registry_root):
                return path.resolve().relative_to(self.registry_root).as_posix()
        except Exception:
            pass
        return str(path)

    def text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return path.read_text(encoding="utf-8", errors="replace")

    def iter_files(self, root: Path) -> list[Path]:
        files: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for filename in sorted(filenames):
                files.append(Path(dirpath) / filename)
        return files

    def build_assembly_index(self) -> dict[str, str]:
        index: dict[str, str] = {}
        for repo in self.duplication_report.get("repositories", []):
            package_id = repo.get("packageId")
            if not package_id:
                continue
            for asmdef in repo.get("asmdefs", []):
                name = asmdef.get("name")
                if name:
                    index[name] = package_id
        return index

    def validate_package(self) -> dict[str, Any]:
        if not self.repository_root:
            raise ValidationError("--repository-root is required for package validation.")
        config_path = self.config_path or self.repository_root / "deucarian-package.json"
        config = self.read_json(config_path)
        if not isinstance(config, dict):
            config = {}
        repo_type = config.get("repositoryType", "unity-package")
        if repo_type == "package-registry":
            self.validate_registry_repository_config(config)
        else:
            self.validate_unity_package(config)
        return self.result("package", config.get("packageId") or config.get("repositoryName") or self.repository_root.name)

    def validate_all(self, audit_root: Path) -> dict[str, Any]:
        package_results = []
        for repo in sorted([p for p in audit_root.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
            config = repo / "deucarian-package.json"
            if not config.exists():
                self.fail(f"{repo.name}: deucarian-package.json is missing.")
                continue
            child = Validator(self.registry_root, repo, config, self.check_remote_urls)
            package_results.append(child.validate_package())
            self.errors.extend(f"{repo.name}: {error}" for error in child.errors)
            self.warnings.extend(f"{repo.name}: {warning}" for warning in child.warnings)
        self.validate_registry()
        self.details["packageResults"] = package_results
        return self.result("organization", str(audit_root))

    def validate_unity_package(self, config: dict[str, Any]) -> None:
        root = self.repository_root
        assert root is not None
        required_config = [
            "packageId",
            "displayName",
            "runtimeAssemblies",
            "editorAssemblies",
            "sampleAssemblies",
            "testAssemblies",
            "requiredDependencies",
            "samplePolicy",
        ]
        for field in required_config:
            if field not in config:
                self.fail(f"deucarian-package.json: {field} is required.")

        package_json = self.read_json(root / "package.json")
        if not isinstance(package_json, dict):
            package_json = {}
        package_id = config.get("packageId")
        if package_id and not PACKAGE_ID_RE.match(package_id):
            self.fail(f"{package_id}: packageId must use the com.deucarian.* namespace.")
        if package_json.get("name") != package_id:
            self.fail(f"package.json name {package_json.get('name')!r} does not match config packageId {package_id!r}.")
        if package_json.get("displayName") != config.get("displayName"):
            self.fail(f"package.json displayName {package_json.get('displayName')!r} does not match config displayName {config.get('displayName')!r}.")
        if not SEMVER_RE.match(str(package_json.get("version", ""))):
            self.fail(f"{package_id}: package.json version must be SemVer, got {package_json.get('version')!r}.")
        if not package_json.get("unity"):
            self.fail(f"{package_id}: package.json unity version is required.")
        repository_url = ((package_json.get("repository") or {}) if isinstance(package_json.get("repository"), dict) else {}).get("url", "")
        if not repository_url:
            self.fail(f"{package_id}: package.json repository.url is required.")
        elif "Bridge.git" in repository_url:
            self.fail(f"{package_id}: package.json repository.url still uses Bridge terminology.")

        dependencies = package_json.get("dependencies") or {}
        if not isinstance(dependencies, dict):
            self.fail(f"{package_id}: package.json dependencies must be an object.")
            dependencies = {}
        for dep, version in sorted(dependencies.items()):
            if not isinstance(version, str) or not version.strip():
                self.fail(f"{package_id}: dependency {dep} has an empty version.")
            elif not (SEMVER_RE.match(version) or version.startswith("file:") or version.startswith("http")):
                self.fail(f"{package_id}: dependency {dep} version {version!r} is not valid.")
        expected_deps = sorted(config.get("requiredDependencies") or [])
        actual_deps = sorted(dependencies.keys())
        if actual_deps != expected_deps:
            self.fail(f"{package_id}: package.json dependencies {actual_deps} do not match config requiredDependencies {expected_deps}.")

        for required_file in ("README.md", "CHANGELOG.md", "LICENSE.md"):
            if not (root / required_file).exists():
                self.fail(f"{package_id}: {required_file} is required.")
        self.validate_documentation_versions(package_json, config)

        asmdefs = self.collect_asmdefs(root)
        asmdefs_by_name = {asm["name"]: asm for asm in asmdefs if asm.get("name")}
        self.validate_configured_assemblies(package_id, config, asmdefs_by_name)
        self.validate_asmdef_dependencies(package_id, dependencies, config, asmdefs)
        self.validate_samples(root, config, asmdefs)
        self.validate_generated_files(root)
        self.validate_release_workflow_policy(root)
        self.validate_architecture_calls(package_id, config, root)
        self.validate_capability_ownership(package_id, config)
        self.validate_registry_entry(package_id, dependencies)
        if package_id == "com.deucarian.common":
            self.validate_common_api(root)

    def validate_capability_ownership(self, package_id: str, config: dict[str, Any]) -> None:
        configured = sorted(config.get("ownedCapabilities") or [])
        registered = sorted(cap for cap in self.capabilities_by_owner.get(package_id, []) if cap)
        if configured != registered:
            self.fail(f"{package_id}: ownedCapabilities {configured} do not match capabilities.json owner entries {registered}.")

    def validate_registry_repository_config(self, config: dict[str, Any]) -> None:
        if config.get("repositoryName") != "Package-Registry":
            self.fail("Package Registry config must use repositoryName Package-Registry.")
        self.validate_registry()
        for required in ("packages.json", "capabilities.json", "dependency-rules.json"):
            if not (self.registry_root / required).exists():
                self.fail(f"Package Registry requires {required}.")

    def validate_documentation_versions(self, package_json: dict[str, Any], config: dict[str, Any]) -> None:
        assert self.repository_root is not None
        version = str(package_json.get("version", ""))
        readme = self.repository_root / "README.md"
        if readme.exists():
            text = self.text(readme)
            for pattern in README_VERSION_PATTERNS:
                match = pattern.search(text)
                if match:
                    if match.group(1) != version:
                        self.fail(f"README.md declares version {match.group(1)}, expected {version}.")
                    break
            active_url_match = re.search(r"https://github\.com/Deucarian/[^)\s`]*Bridge(?:\.git)?", text, re.I)
            if active_url_match and not config.get("allowsHistoricalBridgeDocumentation", False):
                self.fail("README.md contains active Bridge repository terminology.")
        changelog = self.repository_root / "CHANGELOG.md"
        if changelog.exists() and not config.get("changelogVersionExempt", False):
            match = CHANGELOG_VERSION_RE.search(self.text(changelog))
            if match and match.group(1) != version:
                self.fail(f"CHANGELOG.md latest version {match.group(1)}, expected {version}.")

    def collect_asmdefs(self, root: Path) -> list[dict[str, Any]]:
        asmdefs = []
        for path in sorted(root.rglob("*.asmdef")):
            if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                continue
            data = self.read_json(path)
            if not isinstance(data, dict):
                continue
            relative = path.relative_to(root).as_posix()
            data = dict(data)
            data["path"] = relative
            data["scope"] = self.asmdef_scope(relative, data)
            asmdefs.append(data)
        return asmdefs

    def asmdef_scope(self, relative: str, asmdef: dict[str, Any]) -> str:
        if "TestAssemblies" in (asmdef.get("optionalUnityReferences") or []) or "/Tests/" in f"/{relative}" or relative.startswith("Tests"):
            return "test"
        if relative.startswith("Samples~"):
            return "sample"
        if "Editor" in (asmdef.get("includePlatforms") or []) or relative.startswith("Editor"):
            return "editor"
        return "runtime"

    def validate_configured_assemblies(self, package_id: str, config: dict[str, Any], asmdefs_by_name: dict[str, dict[str, Any]]) -> None:
        expected_by_scope = {
            "runtime": config.get("runtimeAssemblies") or [],
            "editor": config.get("editorAssemblies") or [],
            "sample": config.get("sampleAssemblies") or [],
            "test": config.get("testAssemblies") or [],
        }
        configured = {name for names in expected_by_scope.values() for name in names}
        actual = set(asmdefs_by_name.keys())
        if configured != actual:
            self.fail(f"{package_id}: configured assemblies {sorted(configured)} do not match asmdefs {sorted(actual)}.")
        for scope, names in expected_by_scope.items():
            for name in names:
                asmdef = asmdefs_by_name.get(name)
                if not asmdef:
                    self.fail(f"{package_id}: configured {scope} assembly {name} is missing.")
                    continue
                if asmdef["scope"] != scope:
                    self.fail(f"{package_id}: assembly {name} is configured as {scope} but detected as {asmdef['scope']}.")
                refs = asmdef.get("references") or []
                if scope == "runtime" and any(ref == "UnityEditor" or ref.startswith("UnityEditor.") for ref in refs):
                    self.fail(f"{package_id}: runtime assembly {name} must not reference UnityEditor.")
                if scope in {"runtime", "editor"} and "TestAssemblies" in (asmdef.get("optionalUnityReferences") or []):
                    self.fail(f"{package_id}: production assembly {name} must not reference TestAssemblies.")
                if scope == "test" and "TestAssemblies" not in (asmdef.get("optionalUnityReferences") or []):
                    self.fail(f"{package_id}: test assembly {name} must include optionalUnityReferences TestAssemblies.")

    def validate_asmdef_dependencies(self, package_id: str, dependencies: dict[str, str], config: dict[str, Any], asmdefs: list[dict[str, Any]]) -> None:
        declared_deps = set(dependencies.keys())
        optional_deps = set(config.get("optionalVersionDefinedDependencies") or [])
        for asmdef in asmdefs:
            for reference in asmdef.get("references") or []:
                clean = reference.replace("GUID:", "")
                owner = self.assembly_to_package.get(clean)
                if not owner or owner == package_id:
                    continue
                if owner in declared_deps:
                    continue
                if owner in optional_deps and self.asmdef_has_optional_guard(asmdef, owner):
                    continue
                if asmdef["scope"] == "test":
                    continue
                self.fail(f"{package_id}: {asmdef['path']} references {clean} from {owner} without a package.json dependency.")
        registry_package = self.registry_packages_by_id.get(package_id)
        if registry_package is not None:
            registry_deps = sorted(dep for dep in registry_package.get("dependencies", []) if str(dep).startswith("com.deucarian."))
            package_deps = sorted(dep for dep in declared_deps if dep.startswith("com.deucarian."))
            if registry_deps != package_deps:
                self.fail(f"{package_id}: registry dependencies {registry_deps} do not match package.json Deucarian dependencies {package_deps}.")

    def asmdef_has_optional_guard(self, asmdef: dict[str, Any], package_id: str) -> bool:
        return any(item.get("name") == package_id for item in asmdef.get("versionDefines") or []) or bool(asmdef.get("defineConstraints"))

    def validate_samples(self, root: Path, config: dict[str, Any], asmdefs: list[dict[str, Any]]) -> None:
        if (root / "Samples").exists() or (root / "Assets").exists():
            self.fail("Samples must live under Samples~, and package repos must not contain Assets/Samples.")
        package_id = str(config.get("packageId") or "<unknown>")
        policy = config.get("samplePolicy")
        if policy not in SAMPLE_POLICIES:
            self.fail(f"{package_id}: samplePolicy must be one of {sorted(SAMPLE_POLICIES)}, got {policy!r}.")
            return
        expected_root = config.get("expectedSamplesRoot")
        has_sample_asmdef = any(asm["scope"] == "sample" for asm in asmdefs)
        if has_sample_asmdef and expected_root and not (root / expected_root).exists():
            self.fail(f"Expected samples root {expected_root} is missing.")
        package_assemblies = set((config.get("runtimeAssemblies") or []) + (config.get("editorAssemblies") or []))
        for asmdef in asmdefs:
            if asmdef["scope"] != "sample" or not package_assemblies:
                continue
            refs = set(asmdef.get("references") or [])
            if refs.isdisjoint(package_assemblies):
                self.fail(f"{asmdef['path']}: sample asmdef must reference at least one package production assembly directly.")

        package_json = self.read_json(root / "package.json", required=False) or {}
        declared_samples = package_json.get("samples") or []
        if not isinstance(declared_samples, list):
            self.fail(f"{package_id}: package.json samples must be an array.")
            declared_samples = []
        declared_paths = {
            str(sample.get("path") or "").replace("\\", "/").rstrip("/")
            for sample in declared_samples
            if isinstance(sample, dict)
        }
        samples_root = root / "Samples~"
        sample_dirs = sorted(path for path in samples_root.iterdir() if path.is_dir()) if samples_root.exists() else []
        actual_paths = {path.relative_to(root).as_posix() for path in sample_dirs}
        if declared_paths != actual_paths:
            self.fail(
                f"{package_id}: package.json sample paths {sorted(declared_paths)} "
                f"do not match Samples~ directories {sorted(actual_paths)}."
            )

        if policy in {"compiled-example", "playable-scene", "composition"} and not sample_dirs:
            self.fail(f"{package_id}: samplePolicy {policy} requires at least one Samples~ entry.")
        for sample_dir in sample_dirs:
            relative = sample_dir.relative_to(root).as_posix()
            if not any(path.name.lower().startswith("readme") for path in sample_dir.iterdir() if path.is_file()):
                self.fail(f"{package_id}: {relative} requires a README.")
            if not any(sample_dir.rglob("*.asmdef")):
                self.fail(f"{package_id}: {relative} requires an isolated sample asmdef.")
            if policy in {"playable-scene", "composition"} and not any(sample_dir.rglob("*.unity")):
                self.fail(f"{package_id}: {relative} requires a playable Unity scene.")

        if policy == "tool" and not (config.get("testAssemblies") or []):
            self.fail(f"{package_id}: tool packages require at least one automated test assembly.")
        if policy == "composition" and self.registry_packages_by_id.get(package_id, {}).get("kind") != "Suite":
            self.fail(f"{package_id}: composition samplePolicy is reserved for Suite packages.")
        if policy == "template":
            template_root = root / "TemplateSource~"
            template_scenes = list(template_root.rglob("*.unity")) if template_root.exists() else []
            sample_scenes = [scene for sample_dir in sample_dirs for scene in sample_dir.rglob("*.unity")]
            if not template_scenes and not sample_scenes:
                self.fail(f"{package_id}: template samplePolicy requires a playable scene in TemplateSource~ or Samples~.")
            for path in self.iter_files(root):
                relative = path.relative_to(root).as_posix()
                simulated_length = 101 + len(relative)
                if simulated_length >= 240:
                    self.fail(
                        f"{package_id}: {relative} reaches {simulated_length} characters "
                        "under the 100-character Windows host-root simulation (limit 239)."
                    )

    def validate_generated_files(self, root: Path) -> None:
        for forbidden in ("Library", "Temp", "Obj", "Build", "Builds", "ProjectSettings", "Packages"):
            if (root / forbidden).exists():
                self.fail(f"Generated/project directory must not be committed: {forbidden}.")
        meta_guids: dict[str, str] = {}
        for path in self.iter_files(root):
            relative = path.relative_to(root).as_posix()
            if path.suffix.lower() in GENERATED_ARCHIVE_EXTENSIONS:
                self.fail(f"Generated archive must not be committed: {relative}.")
            if path.suffix == ".meta":
                match = re.search(r"^guid:\s*([a-fA-F0-9]+)", self.text(path), re.M)
                if match:
                    guid = match.group(1).lower()
                    if guid in meta_guids:
                        self.fail(f"Duplicate Unity .meta GUID {guid}: {meta_guids[guid]} and {relative}.")
                    meta_guids[guid] = relative

    def validate_architecture_calls(self, package_id: str, config: dict[str, Any], root: Path) -> None:
        allowed_debug_files = {item.get("file", "").replace("\\", "/") for item in config.get("allowedDirectDebugCalls") or []}
        allowed_lifetime_files = {item.get("file", "").replace("\\", "/") for item in config.get("allowedDirectUnityObjectLifetimeCalls") or []}
        for path in self.iter_files(root):
            if path.suffix != ".cs":
                continue
            relative = path.relative_to(root).as_posix()
            scope = self.path_scope(relative)
            text = self.strip_comments_and_strings(self.text(path))
            if scope == "test":
                continue
            if DEBUG_CALL_RE.search(text) and relative not in allowed_debug_files:
                self.fail(f"{package_id}: prohibited direct UnityEngine.Debug call in {relative}.")
            lifetime_matches = list(LIFETIME_CALL_RE.finditer(text))
            if lifetime_matches and relative not in allowed_lifetime_files:
                self.fail(f"{package_id}: prohibited direct UnityEngine.Object destruction call in {relative}.")
            helper_matches = [m.group("name") for m in HELPER_DEFINITION_RE.finditer(text)]
            if helper_matches and package_id != "com.deucarian.common":
                self.fail(f"{package_id}: copied lifetime helper {helper_matches[0]} in {relative}.")

    def path_scope(self, relative: str) -> str:
        if relative.startswith("Tests") or "/Tests/" in f"/{relative}":
            return "test"
        if relative.startswith("Samples~"):
            return "sample"
        if relative.startswith("Editor"):
            return "editor"
        return "runtime"

    def strip_comments_and_strings(self, text: str) -> str:
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        text = re.sub(r"//.*", " ", text)
        text = re.sub(r'@?"(?:""|\\.|[^"\\])*"', '"S"', text)
        text = re.sub(r"'(?:\\.|[^'\\])'", "'C'", text)
        return text

    def validate_common_api(self, root: Path) -> None:
        runtime = root / "Runtime"
        public_methods = []
        for path in sorted(runtime.rglob("*.cs")):
            text = self.strip_comments_and_strings(self.text(path))
            for match in re.finditer(r"\bpublic\s+(?:static\s+)?[A-Za-z0-9_<>,.\[\] ]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text):
                public_methods.append((path.relative_to(root).as_posix(), match.group(1)))
        approved_public_methods = Counter(
            {
                ("Runtime/UnityObjectUtility.cs", "DestroySafely"): 2,
                ("Runtime/DeucarianEasing.cs", "Evaluate"): 1,
            }
        )
        if Counter(public_methods) != approved_public_methods:
            self.fail(f"com.deucarian.common exposes unexpected public methods: {public_methods}.")

    def validate_registry_entry(self, package_id: str, dependencies: dict[str, str]) -> None:
        entry = self.registry_packages_by_id.get(package_id)
        if not entry:
            self.warn(f"{package_id}: no packages.json entry found.")
            return
        for field in ("stableUrl", "developmentUrl"):
            value = entry.get(field, "")
            match = GIT_URL_RE.match(value)
            if not match:
                self.fail(f"{package_id}: registry {field} must be a GitHub URL with branch fragment.")
            elif field == "stableUrl" and match.group("branch") != "main":
                self.fail(f"{package_id}: stableUrl must target #main.")
            elif field == "developmentUrl" and match.group("branch") != "develop":
                self.fail(f"{package_id}: developmentUrl must target #develop.")

    def validate_registry(self) -> None:
        self.validate_registry_schema()
        self.validate_capabilities_schema()
        self.validate_dependency_rules_schema()
        self.validate_authoritative_audit_artifacts()
        self.validate_catalog_projection()
        self.validate_catalog_sync()
        self.validate_release_workflow_policy(self.registry_root)

    def validate_catalog_projection(self) -> None:
        try:
            installer = project_installer_catalog(self.packages)
            bootstrap = project_bootstrap_catalog(self.packages)
        except CatalogProjectionError as exc:
            self.fail(f"packages.json cannot produce fallback catalogs: {exc}")
            return
        self.details["catalogProjection"] = {
            "installerPackageCount": len(installer.get("packages", [])),
            "bootstrapPackageIds": [package["id"] for package in bootstrap.get("packages", [])],
        }

    def validate_release_workflow_policy(self, root: Path) -> None:
        workflows_root = root / ".github" / "workflows"
        summary: dict[str, Any] = {
            "releaseWorkflowCount": 0,
            "publishWorkflowCount": 0,
            "autoPublishViolations": [],
            "manualPublishWorkflows": [],
            "guardedManualPublishWorkflows": [],
        }
        if not workflows_root.exists():
            self.details["releasePolicy"] = summary
            return

        publish_scripts = self.package_publish_scripts(root)
        for path in sorted(workflows_root.iterdir(), key=lambda item: item.name.lower()):
            if not path.is_file() or not WORKFLOW_FILE_RE.search(path.name):
                continue
            text = self.text(path)
            relative = self.display_path(path)
            uses_publish_script = self.workflow_invokes_publish_script(text, publish_scripts)
            can_publish = bool(
                NPM_PUBLISH_RE.search(text)
                or NPM_TOKEN_RE.search(text)
                or TRUSTED_PUBLISHING_RE.search(text)
                or uses_publish_script
            )
            creates_release_artifact = bool(
                GIT_TAG_RE.search(text)
                or GITHUB_RELEASE_RE.search(text)
                or (WORKFLOW_TAG_TRIGGER_RE.search(text) and RELEASE_ARTIFACT_RE.search(text))
                or (RELEASE_WORKFLOW_NAME_RE.search(text) and RELEASE_ARTIFACT_RE.search(text))
            )
            commits_release_prep = bool(GIT_RELEASE_PREP_RE.search(text))
            is_release_workflow = can_publish or creates_release_artifact or commits_release_prep
            if not is_release_workflow:
                continue

            summary["releaseWorkflowCount"] += 1
            has_push_trigger = bool(WORKFLOW_PUSH_RE.search(text))
            has_manual_trigger = bool(WORKFLOW_DISPATCH_RE.search(text))
            has_confirmation = "confirm_release" in text and RELEASE_CONFIRMATION_TEXT in text

            if can_publish:
                summary["publishWorkflowCount"] += 1
                summary["manualPublishWorkflows"].append(relative)

            if has_push_trigger:
                summary["autoPublishViolations"].append(relative)
                self.fail(f"{relative}: release/publish workflow must not run on push.")
            if can_publish and not has_manual_trigger:
                self.fail(f"{relative}: publish-capable workflow must be workflow_dispatch only.")
            if is_release_workflow and has_manual_trigger and not has_confirmation:
                self.fail(f"{relative}: release/publish workflow must require confirm_release with exact text {RELEASE_CONFIRMATION_TEXT!r}.")
            if can_publish and has_manual_trigger and has_confirmation and not has_push_trigger:
                summary["guardedManualPublishWorkflows"].append(relative)

        for key in ("autoPublishViolations", "manualPublishWorkflows", "guardedManualPublishWorkflows"):
            summary[key] = sorted(summary[key])
        self.details["releasePolicy"] = summary

    def package_publish_scripts(self, root: Path) -> set[str]:
        package_json = self.read_json(root / "package.json", required=False)
        if not isinstance(package_json, dict):
            return set()
        scripts = package_json.get("scripts") or {}
        if not isinstance(scripts, dict):
            return set()
        return {str(name) for name, command in scripts.items() if isinstance(command, str) and NPM_PUBLISH_RE.search(command)}

    def workflow_invokes_publish_script(self, text: str, publish_scripts: set[str]) -> bool:
        for script in publish_scripts:
            script_pattern = re.escape(script)
            if re.search(rf"\bnpm\s+(?:run|run-script)\s+{script_pattern}(?:\s|$)", text, re.I):
                return True
        return False

    def validate_authoritative_audit_artifacts(self) -> None:
        accepted_dependency_classifications = {
            "RequiredAndUsed",
            "EditorOnlyUse",
            "SampleOnlyUse",
            "TestOnlyUse",
            "OptionalVersionDefinedUse",
            "SuiteComposition",
        }
        for finding in self.dependency_usage_audit.get("findings", []):
            classification = finding.get("classification")
            if classification not in accepted_dependency_classifications:
                package_id = finding.get("packageId", "<unknown>")
                dependency = finding.get("dependency", "<unknown>")
                self.fail(f"DEPENDENCY_USAGE_AUDIT.json: {package_id} -> {dependency} is {classification}.")

        for invocation in self.debug_audit.get("invocations", []):
            if invocation.get("policyDisposition") != "Allowed":
                package_id = invocation.get("packageId", "<unknown>")
                file_path = invocation.get("file", "<unknown>")
                line = invocation.get("line", "?")
                self.fail(f"DEBUG_API_AUDIT.json: {package_id} {file_path}:{line} is not Allowed.")

        conclusion = self.lifetime_audit.get("conclusion") or {}
        actionable = int(conclusion.get("actionableProductionCount") or 0)
        if actionable:
            self.fail(f"UNITY_OBJECT_LIFETIME_AUDIT.json: {actionable} actionable production lifetime call(s) remain.")
        for occurrence in self.lifetime_audit.get("occurrences", []):
            if occurrence.get("policyDisposition") != "Allowed":
                package_id = occurrence.get("packageId", "<unknown>")
                file_path = occurrence.get("file", "<unknown>")
                line = occurrence.get("line", "?")
                self.fail(f"UNITY_OBJECT_LIFETIME_AUDIT.json: {package_id} {file_path}:{line} is not Allowed.")

    def validate_registry_schema(self) -> None:
        data = self.packages
        if data.get("schemaVersion") != 2:
            self.fail(f"packages.json: schemaVersion must be 2, got {data.get('schemaVersion')!r}.")
        groups = data.get("groups")
        if not isinstance(groups, list):
            self.fail("packages.json: groups must be an array.")
            groups = []
        group_ids: set[str] = set()
        group_parents: dict[str, str] = {}
        sort_orders: set[int] = set()
        for group in groups:
            if not isinstance(group, dict):
                self.fail("packages.json: every group entry must be an object.")
                continue
            group_id = group.get("id")
            if not isinstance(group_id, str) or not group_id:
                self.fail(f"packages.json: invalid group id {group_id!r}.")
                continue
            if group_id in group_ids:
                self.fail(f"packages.json: duplicate group id {group_id}.")
            group_ids.add(group_id)
            if not group.get("displayName"):
                self.fail(f"packages.json: group {group_id} requires displayName.")
            self.validate_icon_key(f"packages.json group {group_id}", group.get("iconKey"))
            parent = group.get("parentGroupId") or ""
            if not isinstance(parent, str):
                self.fail(f"packages.json: group {group_id} parentGroupId must be a string.")
                parent = ""
            group_parents[group_id] = parent
            order = group.get("sortOrder")
            if not isinstance(order, int):
                self.fail(f"packages.json: group {group_id} requires integer sortOrder.")
            elif order in sort_orders:
                self.fail(f"packages.json: duplicate group sortOrder {order}.")
            else:
                sort_orders.add(order)
        for group_id, parent in group_parents.items():
            if parent and parent not in group_ids:
                self.fail(f"packages.json: group {group_id} has unknown parentGroupId {parent}.")
        for group_id in sorted(group_ids):
            seen: set[str] = set()
            current = group_id
            depth = 0
            while group_parents.get(current):
                if current in seen:
                    self.fail(f"packages.json: group hierarchy contains a cycle at {group_id}.")
                    break
                seen.add(current)
                current = group_parents[current]
                depth += 1
                if depth > 1:
                    self.fail(f"packages.json: group {group_id} exceeds the maximum depth of two levels.")
                    break
        if not isinstance(data.get("packages"), list):
            self.fail("packages.json: packages must be an array.")
            return
        ids: set[str] = set()
        for pkg in data["packages"]:
            if not isinstance(pkg, dict):
                self.fail("packages.json: every package entry must be an object.")
                continue
            package_id = pkg.get("id")
            if not package_id or not PACKAGE_ID_RE.match(str(package_id)):
                self.fail(f"packages.json: invalid package id {package_id!r}.")
                continue
            if package_id in ids:
                self.fail(f"packages.json: duplicate package id {package_id}.")
            ids.add(package_id)
            kind = pkg.get("kind")
            if kind not in PACKAGE_KINDS:
                self.fail(f"{package_id}: kind must be one of {sorted(PACKAGE_KINDS)}, got {kind!r}.")
            if not isinstance(pkg.get("displayName"), str) or not pkg["displayName"].strip():
                self.fail(f"{package_id}: displayName is required.")
            if not isinstance(pkg.get("description"), str) or not pkg["description"].strip():
                self.fail(f"{package_id}: description is required as the public purpose summary.")
            for legacy_field in ("category", "type", "ecosystemGroup"):
                if not pkg.get(legacy_field):
                    self.fail(f"{package_id}: legacy bridge field {legacy_field} is required for schema v2 rollout.")
            self.validate_icon_key(str(package_id), pkg.get("iconKey"))
            group_id = pkg.get("groupId")
            if not group_id:
                self.fail(f"{package_id}: groupId is required.")
            elif group_id not in self.registry_groups_by_id:
                self.fail(f"{package_id}: unknown groupId {group_id}.")
            for reverse_field in ("optionalCompanions", "optionalIntegrations"):
                if reverse_field in pkg:
                    self.fail(f"{package_id}: {reverse_field} is a derived reverse relation and must not be stored in schema v2.")
            for field, branch in (("stableUrl", "main"), ("developmentUrl", "develop")):
                url = pkg.get(field, "")
                match = GIT_URL_RE.match(str(url))
                if not match:
                    self.fail(f"{package_id}: {field} must be a GitHub URL with branch fragment.")
                elif match.group("branch") != branch:
                    self.fail(f"{package_id}: {field} must target #{branch}.")
                elif self.check_remote_urls and not self.git_ref_exists(url):
                    self.fail(f"{package_id}: {field} does not resolve: {url}.")
            self.validate_public_package_metadata(str(package_id), pkg)
            dependencies = pkg.get("dependencies") or []
            if not isinstance(dependencies, list) or any(not isinstance(dep, str) or not dep for dep in dependencies):
                self.fail(f"{package_id}: dependencies must be an array of non-empty package ids.")
                dependencies = []
            if len(dependencies) != len(set(dependencies)) or package_id in dependencies:
                self.fail(f"{package_id}: dependencies must not contain duplicates or self references.")
            for dep in dependencies:
                if dep not in ids and dep not in self.registry_packages_by_id:
                    self.fail(f"{package_id}: dependency {dep} is not in packages.json.")
            relations: dict[str, list[str]] = {}
            for field in ("integrationTargets", "suiteMembers", "recommendedWith"):
                value = pkg.get(field) or []
                if not isinstance(value, list) or any(not isinstance(target, str) or not target for target in value):
                    self.fail(f"{package_id}: {field} must be an array of non-empty package ids.")
                    value = []
                if len(value) != len(set(value)) or package_id in value:
                    self.fail(f"{package_id}: {field} must not contain duplicates or self references.")
                for target in value:
                    if target not in self.registry_packages_by_id:
                        self.fail(f"{package_id}: {field} target {target} is not in packages.json.")
                relations[field] = value
            integration_targets = relations["integrationTargets"]
            suite_members = relations["suiteMembers"]
            recommended = relations["recommendedWith"]
            if kind == "Integration":
                if not integration_targets:
                    self.fail(f"{package_id}: Integration packages require integrationTargets.")
                missing_targets = sorted(set(integration_targets) - set(dependencies))
                if missing_targets:
                    self.fail(f"{package_id}: integrationTargets missing from dependencies: {missing_targets}.")
            elif integration_targets:
                self.fail(f"{package_id}: only Integration packages may declare integrationTargets.")
            if kind == "Suite":
                if not suite_members:
                    self.fail(f"{package_id}: Suite packages require suiteMembers.")
                if set(suite_members) != set(dependencies):
                    self.fail(f"{package_id}: suiteMembers must exactly match dependencies.")
            elif suite_members:
                self.fail(f"{package_id}: only Suite packages may declare suiteMembers.")
            structural = set(integration_targets) | set(suite_members)
            overlap = sorted(structural & set(recommended))
            if overlap:
                self.fail(f"{package_id}: recommendedWith duplicates structural relations: {overlap}.")
        cycles = self.detect_cycles({pkg["id"]: pkg.get("dependencies") or [] for pkg in data["packages"] if isinstance(pkg, dict) and pkg.get("id")})
        for cycle in cycles:
            self.fail("Dependency cycle detected: " + " -> ".join(cycle))

    def validate_public_package_metadata(self, package_id: str, package: dict[str, Any]) -> None:
        public = package.get("public")
        if not isinstance(public, dict):
            self.fail(f"{package_id}: public metadata is required.")
            return

        status = public.get("status")
        if status not in PUBLIC_PACKAGE_STATUSES:
            self.fail(f"{package_id}: public.status must be one of {sorted(PUBLIC_PACKAGE_STATUSES)}, got {status!r}.")

        install_method = public.get("installMethod")
        if install_method not in PUBLIC_INSTALL_METHODS:
            self.fail(
                f"{package_id}: public.installMethod must be one of {sorted(PUBLIC_INSTALL_METHODS)}, "
                f"got {install_method!r}."
            )

        unity = public.get("unity")
        if not isinstance(unity, str) or not UNITY_VERSION_RE.fullmatch(unity):
            self.fail(f"{package_id}: public.unity must match {UNITY_VERSION_RE.pattern}.")

        stable_url = str(package.get("stableUrl") or "")
        repository_url = stable_url.removesuffix(".git#main")
        expected_urls = {
            "documentationUrl": f"{repository_url}/blob/main/README.md",
            "licenseUrl": f"{repository_url}/blob/main/LICENSE.md",
        }
        for field, expected in expected_urls.items():
            value = public.get(field)
            if value != expected:
                self.fail(f"{package_id}: public.{field} must be {expected!r}, got {value!r}.")

    def validate_icon_key(self, owner: str, icon_key: Any) -> None:
        if not isinstance(icon_key, str) or not ICON_KEY_RE.fullmatch(icon_key):
            self.fail(f"{owner}: iconKey must match {ICON_KEY_RE.pattern}.")

    def git_ref_exists(self, url: str) -> bool:
        match = GIT_URL_RE.match(url)
        if not match:
            return False
        base = url.split("#", 1)[0]
        branch = match.group("branch")
        result = subprocess.run(["git", "ls-remote", "--heads", base, branch], capture_output=True, text=True, timeout=30)
        return result.returncode == 0 and bool(result.stdout.strip())

    def detect_cycles(self, graph: dict[str, list[str]]) -> list[list[str]]:
        cycles: list[list[str]] = []
        stack: list[str] = []
        seen: set[str] = set()

        def visit(node: str, visiting: set[str]) -> None:
            if node in visiting:
                cycles.append(stack[stack.index(node):] + [node])
                return
            if node in seen:
                return
            visiting.add(node)
            stack.append(node)
            for dep in sorted(graph.get(node, [])):
                if dep in graph:
                    visit(dep, visiting)
            stack.pop()
            visiting.remove(node)
            seen.add(node)

        for node in sorted(graph):
            visit(node, set())
        return cycles

    def validate_capabilities_schema(self) -> None:
        if self.capabilities.get("schemaVersion") != 2:
            self.fail(f"capabilities.json: schemaVersion must be 2, got {self.capabilities.get('schemaVersion')!r}.")
        caps = self.capabilities.get("capabilities")
        if not isinstance(caps, list):
            self.fail("capabilities.json: capabilities must be an array.")
            return
        capability_ids: set[str] = set()
        for cap in caps:
            if not isinstance(cap, dict) or not cap.get("id") or "description" not in cap:
                self.fail("capabilities.json: every capability needs id and description.")
                continue
            capability_id = str(cap["id"])
            if capability_id in capability_ids:
                self.fail(f"capabilities.json: duplicate capability id {capability_id}.")
            capability_ids.add(capability_id)
            owner = cap.get("ownerPackageId")
            if owner is not None and owner not in self.registry_packages_by_id:
                self.fail(f"capabilities.json: {capability_id} has unknown ownerPackageId {owner}.")
        lifetime = next((cap for cap in caps if cap.get("id") == "unity-object-lifetime"), None)
        if lifetime:
            if lifetime.get("ownerPackageId") != "com.deucarian.common":
                self.fail("unity-object-lifetime capability must be owned by com.deucarian.common.")
            if "Deucarian.Common.UnityObjectUtility.DestroySafely" not in (lifetime.get("canonicalSymbols") or []):
                self.fail("unity-object-lifetime capability must declare the DestroySafely canonical symbol.")

    def validate_dependency_rules_schema(self) -> None:
        if self.dependency_rules.get("schemaVersion") != 3:
            self.fail(f"dependency-rules.json: schemaVersion must be 3, got {self.dependency_rules.get('schemaVersion')!r}.")
        layers = self.dependency_rules.get("layers")
        if not isinstance(layers, list):
            self.fail("dependency-rules.json: layers must be an array.")
            return
        layer_ids: set[str] = set()
        ranks: set[int] = set()
        assignments: dict[str, int] = {}
        for layer in layers:
            if not isinstance(layer, dict):
                self.fail("dependency-rules.json: every layer must be an object.")
                continue
            layer_id = layer.get("id")
            rank = layer.get("rank")
            packages = layer.get("packages")
            if not isinstance(layer_id, str) or not layer_id:
                self.fail("dependency-rules.json: every layer requires id.")
                continue
            if layer_id in layer_ids:
                self.fail(f"dependency-rules.json: duplicate layer id {layer_id}.")
            layer_ids.add(layer_id)
            if not isinstance(rank, int) or rank < 0:
                self.fail(f"dependency-rules.json: layer {layer_id} requires a non-negative integer rank.")
                continue
            if rank in ranks:
                self.fail(f"dependency-rules.json: duplicate layer rank {rank}.")
            ranks.add(rank)
            if not isinstance(packages, list):
                self.fail(f"dependency-rules.json: layer {layer_id} packages must be an array.")
                continue
            for package_id in packages:
                if package_id in assignments:
                    self.fail(f"dependency-rules.json: {package_id} is assigned to more than one layer.")
                assignments[package_id] = rank
        registry_ids = set(self.registry_packages_by_id)
        missing = sorted(registry_ids - set(assignments))
        unknown = sorted(set(assignments) - registry_ids)
        if missing:
            self.fail(f"dependency-rules.json: packages missing layer assignments: {missing}.")
        if unknown:
            self.fail(f"dependency-rules.json: unknown package assignments: {unknown}.")
        if assignments.get("com.deucarian.common") != 0:
            self.fail("dependency-rules.json: com.deucarian.common must be assigned to rank 0.")
        for package_id, package in self.registry_packages_by_id.items():
            package_rank = assignments.get(package_id)
            if package_rank is None:
                continue
            for dependency in package.get("dependencies") or []:
                dependency_rank = assignments.get(dependency)
                if dependency_rank is not None and dependency_rank >= package_rank:
                    self.fail(
                        f"dependency-rules.json: {package_id} (rank {package_rank}) depends on "
                        f"{dependency} (rank {dependency_rank}); dependencies must point to a lower rank."
                    )
        exceptions = self.dependency_rules.get("exceptions") or []
        if not isinstance(exceptions, list):
            self.fail("dependency-rules.json: exceptions must be an array.")
        else:
            known_exception_ids = registry_ids | {"com.deucarian.bootstrap"}
            for exception in exceptions:
                if not isinstance(exception, dict) or not exception.get("reason"):
                    self.fail("dependency-rules.json: every exception requires a reason.")
                    continue
                if exception.get("packageId") not in known_exception_ids:
                    self.fail(f"dependency-rules.json: exception has unknown packageId {exception.get('packageId')}.")
                dependency = exception.get("dependency")
                if dependency is not None and dependency not in registry_ids:
                    self.fail(f"dependency-rules.json: exception has unknown dependency {dependency}.")

    def validate_catalog_sync(self) -> None:
        installer = self.registry_root.parent / "_deucarian_org_audit" / "Package-Installer" / "PackageRegistry.json"
        bootstrap = self.registry_root.parent / "_deucarian_org_audit" / "Bootstrap" / "Editor" / "PackageCatalogFallback.json"
        # Fall back to sibling checkouts when Package Registry itself is inside the audit root.
        if not installer.exists():
            installer = self.registry_root.parent / "Package-Installer" / "PackageRegistry.json"
        if not bootstrap.exists():
            bootstrap = self.registry_root.parent / "Bootstrap" / "Editor" / "PackageCatalogFallback.json"
        for label, path in (("Package Installer bundled catalog", installer), ("Bootstrap fallback catalog", bootstrap)):
            if path.exists():
                self.compare_catalog(label, path)

    def compare_catalog(self, label: str, path: Path) -> None:
        data = self.read_json(path, required=False)
        if not isinstance(data, dict) or not isinstance(data.get("packages"), list):
            self.fail(f"{label}: package list is missing.")
            return
        bundled = {pkg.get("id"): pkg for pkg in data["packages"] if isinstance(pkg, dict) and pkg.get("id")}
        for package_id, registry_pkg in self.registry_packages_by_id.items():
            if package_id not in bundled:
                continue
            bundled_pkg = bundled[package_id]
            for field in ("stableUrl", "developmentUrl"):
                if bundled_pkg.get(field) != registry_pkg.get(field):
                    self.fail(f"{label}: {package_id} {field} differs from packages.json.")
            if sorted(bundled_pkg.get("dependencies") or []) != sorted(registry_pkg.get("dependencies") or []):
                self.fail(f"{label}: {package_id} dependencies differ from packages.json.")

    def result(self, mode: str, target: str) -> dict[str, Any]:
        return {
            "ok": not self.errors,
            "mode": mode,
            "target": target,
            "errors": sorted(self.errors),
            "warnings": sorted(self.warnings),
            "details": self.details,
        }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--audit-root", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--ci", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit deterministic JSON output.")
    parser.add_argument("--check-remote-urls", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    validator = Validator(args.registry_root, args.repository_root, args.config, args.check_remote_urls)
    if args.all:
        if not args.audit_root:
            print("--audit-root is required with --all", file=sys.stderr)
            return 2
        result = validator.validate_all(args.audit_root.resolve())
    else:
        result = validator.validate_package()

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        target = result["target"]
        if result["ok"]:
            print(f"Deucarian validation passed: {target}")
        else:
            print(f"Deucarian validation failed: {target}", file=sys.stderr)
            for error in result["errors"]:
                print(f"- {error}", file=sys.stderr)
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
