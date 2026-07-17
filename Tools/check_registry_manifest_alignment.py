#!/usr/bin/env python3
"""Compare Package Registry entries with local Unity package manifests.

The checker is intentionally standard-library only so it can run in lightweight
metadata CI without a Unity installation. Missing local checkouts are warnings
by default because ecosystem work often runs from a partial workspace.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


DEUCARIAN_PACKAGE_PREFIX = "com.deucarian."
DEUCARIAN_REPO_RE = re.compile(r"github\.com[:/]Deucarian/([^/#?]+?)(?:\.git)?(?:[?#].*)?$", re.I)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def package_repo_name(package: dict[str, Any]) -> str:
    for field in ("stableUrl", "developmentUrl"):
        repo_name = repo_name_from_url(str(package.get(field) or ""))
        if repo_name:
            return repo_name
    return ""


def repo_name_from_url(url: str) -> str:
    match = DEUCARIAN_REPO_RE.search(strip_url_ref(url).split()[0])
    return match.group(1) if match else ""


def strip_url_ref(url: str) -> str:
    value = (url or "").strip()
    if "#" in value:
        value = value.split("#", 1)[0]
    return value


def normalize_repo_url(url: str) -> str:
    value = strip_url_ref(url)
    if value.startswith("git+"):
        value = value[4:]
    if value.startswith("git://github.com/"):
        value = "https://github.com/" + value[len("git://github.com/") :]
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value[len("git@github.com:") :]
    value = value.rstrip("/")
    if value and not value.endswith(".git"):
        value += ".git"
    return value


def manifest_repo_url(manifest: dict[str, Any]) -> str:
    repository = manifest.get("repository")
    if isinstance(repository, dict):
        return str(repository.get("url") or "")
    if isinstance(repository, str):
        return repository
    return ""


def deucarian_manifest_dependencies(manifest: dict[str, Any]) -> list[str]:
    dependencies = manifest.get("dependencies") or {}
    if not isinstance(dependencies, dict):
        return []
    return sorted(dep for dep in dependencies if dep.startswith(DEUCARIAN_PACKAGE_PREFIX))


def sorted_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return sorted(str(value).strip() for value in values if str(value).strip())


def unity_version_tuple(value: Any) -> tuple[int, ...]:
    parts = str(value or "").split(".")
    if not parts or any(not part.isdigit() for part in parts):
        return ()
    return tuple(int(part) for part in parts)


def display_path(path: Path) -> str:
    return str(path).replace("\\", "/")


class AlignmentChecker:
    def __init__(self, registry_root: Path, audit_root: Path, require_checkouts: bool = False):
        self.registry_root = registry_root.resolve()
        self.audit_root = audit_root.resolve()
        self.require_checkouts = require_checkouts
        self.checkout_index: dict[str, Path] = {}
        self.manifests_by_package_id: dict[str, dict[str, Any]] = {}
        self.findings: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    def build_report(self) -> dict[str, Any]:
        registry = read_json(self.registry_root / "packages.json")
        packages = registry.get("packages") if isinstance(registry, dict) else None
        if not isinstance(packages, list):
            raise ValueError("packages.json must contain a packages array.")

        self.checkout_index = self.build_checkout_index()
        self.manifests_by_package_id = self.load_manifests(packages)

        checked = 0
        missing_checkouts = []
        for package in packages:
            if not isinstance(package, dict):
                continue
            package_id = str(package.get("id") or "")
            repo_name = package_repo_name(package)
            checkout = self.find_checkout(repo_name)
            if checkout is None:
                message = {
                    "packageId": package_id,
                    "repository": repo_name,
                    "reason": "local checkout not found",
                }
                missing_checkouts.append(message)
                if self.require_checkouts:
                    self.findings.append(
                        {
                            "packageId": package_id,
                            "repository": repo_name,
                            "field": "checkout",
                            "registry": repo_name,
                            "manifest": "",
                            "message": "Local checkout is required but was not found.",
                        }
                    )
                continue
            checked += 1
            self.compare_package(package, checkout)

        if missing_checkouts and not self.require_checkouts:
            self.warnings.append(f"{len(missing_checkouts)} registry package(s) were skipped because local checkouts were not found.")

        return {
            "ok": not self.findings,
            "registryRoot": display_path(self.registry_root),
            "auditRoot": display_path(self.audit_root),
            "checkedPackages": checked,
            "missingCheckouts": missing_checkouts,
            "findings": sorted(self.findings, key=lambda item: (item.get("packageId", ""), item.get("field", ""))),
            "warnings": sorted(self.warnings),
        }

    def load_manifests(self, packages: list[Any]) -> dict[str, dict[str, Any]]:
        manifests: dict[str, dict[str, Any]] = {}
        for package in packages:
            if not isinstance(package, dict):
                continue
            package_id = str(package.get("id") or "")
            checkout = self.find_checkout(package_repo_name(package))
            manifest_path = checkout / "package.json" if checkout else None
            if manifest_path is None or not manifest_path.exists():
                continue
            try:
                manifest = read_json(manifest_path)
            except ValueError:
                continue
            if isinstance(manifest, dict):
                manifests[package_id] = manifest
        return manifests

    def build_checkout_index(self) -> dict[str, Path]:
        index: dict[str, Path] = {}
        if not self.audit_root.exists():
            return index
        for child in sorted((path for path in self.audit_root.iterdir() if path.is_dir()), key=lambda path: path.name.lower()):
            index.setdefault(child.name.lower(), child)
            repo_name = self.deucarian_remote_repo_name(child)
            if repo_name:
                index[repo_name.lower()] = child
        return index

    def deucarian_remote_repo_name(self, checkout: Path) -> str:
        if not (checkout / ".git").exists():
            return ""
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=checkout,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except Exception:
            return ""
        for line in result.stdout.splitlines():
            for token in line.split():
                repo_name = repo_name_from_url(token)
                if repo_name:
                    return repo_name
        return ""

    def find_checkout(self, repo_name: str) -> Path | None:
        if not repo_name:
            return None
        return self.checkout_index.get(repo_name.lower())

    def compare_package(self, package: dict[str, Any], checkout: Path) -> None:
        package_id = str(package.get("id") or "")
        manifest_path = checkout / "package.json"
        if not manifest_path.exists():
            self.add_finding(package_id, "package.json", "present", "missing", "Local checkout does not contain package.json.")
            return
        try:
            manifest = read_json(manifest_path)
        except ValueError as exc:
            self.add_finding(package_id, "package.json", "valid JSON", str(exc), "Manifest could not be parsed.")
            return
        if not isinstance(manifest, dict):
            self.add_finding(package_id, "package.json", "object", type(manifest).__name__, "Manifest root must be a JSON object.")
            return

        self.compare_field(package_id, "name", package_id, str(manifest.get("name") or ""))
        self.compare_field(package_id, "displayName", str(package.get("displayName") or ""), str(manifest.get("displayName") or ""))

        expected_repo_url = normalize_repo_url(strip_url_ref(str(package.get("stableUrl") or package.get("developmentUrl") or "")))
        actual_repo_url = normalize_repo_url(manifest_repo_url(manifest))
        if expected_repo_url and actual_repo_url:
            self.compare_field(package_id, "repository.url", expected_repo_url, actual_repo_url)
        elif expected_repo_url:
            self.add_finding(package_id, "repository.url", expected_repo_url, actual_repo_url, "Manifest repository URL is missing.")

        registry_deps = sorted_strings(package.get("dependencies") or [])
        manifest_deps = deucarian_manifest_dependencies(manifest)
        if registry_deps != manifest_deps:
            self.add_finding(
                package_id,
                "dependencies",
                registry_deps,
                manifest_deps,
                "Registry dependencies differ from Deucarian dependencies in package.json.",
            )
        dependency_versions = manifest.get("dependencies") or {}
        if not isinstance(dependency_versions, dict):
            dependency_versions = {}
        package_unity = unity_version_tuple(manifest.get("unity"))
        for dependency_id in registry_deps:
            dependency_manifest = self.manifests_by_package_id.get(dependency_id)
            if dependency_manifest is None:
                continue
            expected_version = str(dependency_manifest.get("version") or "")
            actual_version = str(dependency_versions.get(dependency_id) or "")
            if expected_version and actual_version != expected_version:
                self.add_finding(
                    package_id,
                    f"dependencyVersion:{dependency_id}",
                    expected_version,
                    actual_version,
                    "Direct Deucarian dependency version must equal the dependency package version.",
                )
            dependency_unity = unity_version_tuple(dependency_manifest.get("unity"))
            if package_unity and dependency_unity and package_unity < dependency_unity:
                self.add_finding(
                    package_id,
                    f"unityFloor:{dependency_id}",
                    str(manifest.get("unity") or ""),
                    str(dependency_manifest.get("unity") or ""),
                    "A package cannot declare a lower Unity floor than one of its dependencies.",
                )

    def compare_field(self, package_id: str, field: str, expected: Any, actual: Any) -> None:
        if expected != actual:
            self.add_finding(package_id, field, expected, actual, f"{field} differs between registry and package.json.")

    def add_finding(self, package_id: str, field: str, expected: Any, actual: Any, message: str) -> None:
        self.findings.append(
            {
                "packageId": package_id,
                "field": field,
                "registry": expected,
                "manifest": actual,
                "message": message,
            }
        )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--audit-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--require-checkouts", action="store_true", help="Treat missing local package checkouts as findings.")
    parser.add_argument("--json", action="store_true", help="Emit deterministic JSON output.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero when findings are present.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    checker = AlignmentChecker(args.registry_root, args.audit_root, args.require_checkouts)
    report = checker.build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        target = report["registryRoot"]
        if report["ok"]:
            print(f"Registry manifest alignment passed: {target}")
        else:
            print(f"Registry manifest alignment found {len(report['findings'])} issue(s): {target}")
            for finding in report["findings"]:
                print(f"- {finding['packageId']} {finding['field']}: {finding['message']}")
        for warning in report["warnings"]:
            print(f"warning: {warning}")
    return 1 if args.check and not report["ok"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
