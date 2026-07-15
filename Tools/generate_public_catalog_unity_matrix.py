#!/usr/bin/env python3
"""Generate the deterministic clean-Unity validation matrix for the public catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from project_package_catalogs import CatalogProjectionError, dependency_first_closure, package_index


MATRIX_PATH = Path("PUBLIC_CATALOG_UNITY_MATRIX.json")
UNITY_VERSION = "2022.3"
CHANNELS = (
    ("stable", "stableUrl", "main"),
    ("development", "developmentUrl", "develop"),
)
RESERVED_PRODUCT_PACKAGE_IDS = frozenset(
    {
        "com.deucarian.camera-navigation",
        "com.deucarian.theming",
        "com.deucarian.ui",
        "com.deucarian.xr-ui",
        "com.deucarian.xr-ui.theming-integration",
    }
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise CatalogProjectionError(f"{path} does not exist.") from exc
    except json.JSONDecodeError as exc:
        raise CatalogProjectionError(f"{path} is not valid JSON: {exc}") from exc


def serialize_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_matrix(registry: dict[str, Any]) -> dict[str, Any]:
    packages_by_id = package_index(registry)
    reserved = sorted(RESERVED_PRODUCT_PACKAGE_IDS.intersection(packages_by_id))
    if reserved:
        raise CatalogProjectionError(
            "Public catalog contains reserved proprietary package ids: " + ", ".join(reserved)
        )

    cases: list[dict[str, Any]] = []
    for package_id in sorted(packages_by_id):
        closure = dependency_first_closure(packages_by_id, package_id)
        closure_ids = [package["id"] for package in closure]
        leaked = sorted(RESERVED_PRODUCT_PACKAGE_IDS.intersection(closure_ids))
        if leaked:
            raise CatalogProjectionError(
                f"{package_id}: dependency closure contains reserved package ids: {', '.join(leaked)}"
            )

        for channel, url_field, expected_branch in CHANNELS:
            closure_routes: list[dict[str, str]] = []
            for package in closure:
                route = package.get(url_field)
                expected_suffix = f".git#{expected_branch}"
                if not isinstance(route, str) or not route.endswith(expected_suffix):
                    raise CatalogProjectionError(
                        f"{package['id']}: {url_field} must end with {expected_suffix}."
                    )
                closure_routes.append({"id": package["id"], "url": route})

            cases.append(
                {
                    "caseId": f"{package_id}:{channel}",
                    "targetPackageId": package_id,
                    "channel": channel,
                    "unityVersion": UNITY_VERSION,
                    "dependencyFirstClosure": closure_routes,
                }
            )

    return {
        "schemaVersion": 1,
        "catalogUpdatedAt": registry.get("updatedAt"),
        "unityVersion": UNITY_VERSION,
        "packageCount": len(packages_by_id),
        "caseCount": len(cases),
        "cases": cases,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-root", type=Path, default=repository_root)
    parser.add_argument("--output", type=Path, default=repository_root / MATRIX_PATH)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the committed matrix differs from the deterministic catalog projection.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        registry = read_json(args.registry_root.resolve() / "packages.json")
        expected = serialize_json(build_matrix(registry))
        output = args.output.resolve()
        if args.check:
            if not output.exists():
                print(f"out of date: {output} is missing", file=sys.stderr)
                return 1
            if output.read_text(encoding="utf-8-sig") != expected:
                print(f"out of date: {output} differs from packages.json", file=sys.stderr)
                return 1
            print(f"verified: {output}")
            return 0

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(expected, encoding="utf-8")
        print(f"wrote: {output}")
        return 0
    except CatalogProjectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
