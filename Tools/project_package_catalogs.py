#!/usr/bin/env python3
"""Project canonical Package Registry metadata into consumer fallback catalogs."""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import sys
from pathlib import Path
from typing import Any, Sequence


INSTALLER_PACKAGE_ID = "com.deucarian.package-installer"
INSTALLER_CATALOG_PATH = Path("PackageRegistry.json")
BOOTSTRAP_CATALOG_PATH = Path("Editor") / "PackageCatalogFallback.json"
BOOTSTRAP_PACKAGE_FIELDS = (
    "id",
    "displayName",
    "category",
    "description",
    "stableUrl",
    "developmentUrl",
    "dependencies",
)
PACKAGE_RELATIONSHIP_FIELDS = (
    "dependencies",
    "optionalCompanions",
    "optionalIntegrations",
    "integrationTargets",
    "recommendedWith",
    "suiteMembers",
)


class CatalogProjectionError(ValueError):
    """Raised when canonical registry data cannot produce a valid projection."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise CatalogProjectionError(f"{path} does not exist.") from exc
    except json.JSONDecodeError as exc:
        raise CatalogProjectionError(f"{path} is not valid JSON: {exc}") from exc


def serialize_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def package_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    packages = registry.get("packages")
    if not isinstance(packages, list):
        raise CatalogProjectionError("packages.json must contain a packages array.")

    index: dict[str, dict[str, Any]] = {}
    for position, package in enumerate(packages):
        if not isinstance(package, dict):
            raise CatalogProjectionError(f"packages[{position}] must be an object.")
        package_id = package.get("id")
        if not isinstance(package_id, str) or not package_id.strip():
            raise CatalogProjectionError(f"packages[{position}] must contain a non-empty id.")
        if package_id in index:
            raise CatalogProjectionError(f"packages.json contains duplicate package id {package_id}.")
        for field in PACKAGE_RELATIONSHIP_FIELDS:
            relationships = package.get(field, [])
            if not isinstance(relationships, list) or any(
                not isinstance(item, str) or not item.strip() for item in relationships
            ):
                raise CatalogProjectionError(
                    f"{package_id}: {field} must be an array of non-empty package ids."
                )
        index[package_id] = package

    for package_id, package in index.items():
        for field in PACKAGE_RELATIONSHIP_FIELDS:
            for related_package_id in package.get(field, []):
                if related_package_id not in index:
                    raise CatalogProjectionError(
                        f"{package_id}: {field} target {related_package_id} is not in packages.json."
                    )
    return index


def project_installer_catalog(registry: dict[str, Any]) -> dict[str, Any]:
    """Return the full canonical registry accepted by Package Installer."""

    if not isinstance(registry, dict):
        raise CatalogProjectionError("packages.json root must be an object.")
    package_index(registry)
    return copy.deepcopy(registry)


def dependency_first_closure(
    packages_by_id: dict[str, dict[str, Any]],
    target_package_id: str,
) -> list[dict[str, Any]]:
    if target_package_id not in packages_by_id:
        raise CatalogProjectionError(f"packages.json does not contain {target_package_id}.")

    ordered: list[dict[str, Any]] = []
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(package_id: str) -> None:
        if package_id in visited:
            return
        if package_id in visiting:
            cycle_start = visiting.index(package_id)
            cycle = visiting[cycle_start:] + [package_id]
            raise CatalogProjectionError("Dependency cycle detected: " + " -> ".join(cycle))

        visiting.append(package_id)
        package = packages_by_id[package_id]
        for dependency_id in sorted(package.get("dependencies", [])):
            visit(dependency_id)
        visiting.pop()
        visited.add(package_id)
        ordered.append(package)

    visit(target_package_id)
    return ordered


def project_bootstrap_catalog(
    registry: dict[str, Any],
    target_package_id: str = INSTALLER_PACKAGE_ID,
) -> dict[str, Any]:
    """Return Bootstrap's minimal dependency-first installer setup catalog."""

    if not isinstance(registry, dict):
        raise CatalogProjectionError("packages.json root must be an object.")
    if "schemaVersion" not in registry:
        raise CatalogProjectionError("packages.json must contain schemaVersion.")
    if "updatedAt" not in registry:
        raise CatalogProjectionError("packages.json must contain updatedAt.")

    packages_by_id = package_index(registry)
    closure = dependency_first_closure(packages_by_id, target_package_id)
    projected_packages: list[dict[str, Any]] = []
    for package in closure:
        package_id = package["id"]
        missing_fields = [field for field in BOOTSTRAP_PACKAGE_FIELDS if field not in package]
        if missing_fields:
            raise CatalogProjectionError(f"{package_id}: missing Bootstrap field(s): {', '.join(missing_fields)}.")
        projected_packages.append({field: copy.deepcopy(package[field]) for field in BOOTSTRAP_PACKAGE_FIELDS})

    return {
        "schemaVersion": copy.deepcopy(registry["schemaVersion"]),
        "updatedAt": copy.deepcopy(registry["updatedAt"]),
        "packages": projected_packages,
    }


def write_catalog(path: Path, expected: Any) -> None:
    content = serialize_json(expected)
    current = path.read_text(encoding="utf-8-sig") if path.exists() else None
    if current == content:
        print(f"unchanged: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote: {path}")


def check_catalog(path: Path, expected: Any) -> bool:
    if not path.exists():
        print(f"out of date: {path} is missing", file=sys.stderr)
        return False
    try:
        actual = read_json(path)
    except CatalogProjectionError as exc:
        print(f"out of date: {exc}", file=sys.stderr)
        return False
    if actual == expected:
        print(f"up to date: {path}")
        return True

    print(f"out of date: {path}", file=sys.stderr)
    expected_lines = serialize_json(expected).splitlines()
    actual_lines = serialize_json(actual).splitlines()
    for line in difflib.unified_diff(
        actual_lines,
        expected_lines,
        fromfile=str(path),
        tofile=f"{path} (projected)",
        lineterm="",
    ):
        print(line, file=sys.stderr)
    return False


def build_arg_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry-root",
        type=Path,
        default=repository_root,
        help="Package Registry checkout containing packages.json (default: this checkout).",
    )
    parser.add_argument(
        "--installer-root",
        type=Path,
        help="Optional Package Installer checkout that owns PackageRegistry.json.",
    )
    parser.add_argument(
        "--bootstrap-root",
        type=Path,
        help="Optional Bootstrap checkout that owns Editor/PackageCatalogFallback.json.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare parsed JSON semantically and exit non-zero on drift instead of writing files.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.installer_root is None and args.bootstrap_root is None:
        parser.error("at least one of --installer-root or --bootstrap-root is required")
    registry_path = args.registry_root.resolve() / "packages.json"

    try:
        registry = read_json(registry_path)
        catalogs: list[tuple[Path, dict[str, Any]]] = []
        if args.installer_root is not None:
            catalogs.append(
                (
                    args.installer_root.resolve() / INSTALLER_CATALOG_PATH,
                    project_installer_catalog(registry),
                )
            )
        if args.bootstrap_root is not None:
            catalogs.append(
                (
                    args.bootstrap_root.resolve() / BOOTSTRAP_CATALOG_PATH,
                    project_bootstrap_catalog(registry),
                )
            )
        if args.check:
            results = [check_catalog(path, catalog) for path, catalog in catalogs]
            return 0 if all(results) else 1
        for path, catalog in catalogs:
            write_catalog(path, catalog)
        return 0
    except (CatalogProjectionError, OSError) as exc:
        print(f"catalog projection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
