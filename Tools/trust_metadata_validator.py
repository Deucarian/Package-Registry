#!/usr/bin/env python3
"""Validate support, security, package-link, and dependency-notice metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_TRUST_FILES = ("SUPPORT.md", "SECURITY.md", "THIRD_PARTY_NOTICES.md")
DEUCARIAN_EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@deucarian\.(?:com|nl)\b", re.IGNORECASE)
REPOSITORY_PATTERN = re.compile(
    r"^https://github\.com/Deucarian/(?P<name>[^/#]+?)(?:\.git)?$", re.IGNORECASE
)


def _load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _repository_name_from_manifest(manifest: dict[str, object]) -> str | None:
    repository = manifest.get("repository")
    if isinstance(repository, dict):
        repository = repository.get("url")
    if not isinstance(repository, str):
        return None
    normalized = repository.removeprefix("git+")
    match = REPOSITORY_PATTERN.match(normalized)
    return match.group("name") if match else None


def _require_text(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing required file: {path.name}")
        return ""
    text = path.read_text(encoding="utf-8-sig")
    if not text.strip():
        errors.append(f"required file is empty: {path.name}")
    return text


def _validate_package_manifest(
    root: Path,
    manifest: dict[str, object],
    repository_name: str,
    notices: str,
    errors: list[str],
) -> None:
    expected_urls = {
        "documentationUrl": f"https://github.com/Deucarian/{repository_name}/blob/main/README.md",
        "changelogUrl": f"https://github.com/Deucarian/{repository_name}/blob/main/CHANGELOG.md",
        "licensesUrl": f"https://github.com/Deucarian/{repository_name}/blob/main/LICENSE.md",
    }
    target_files = {
        "documentationUrl": "README.md",
        "changelogUrl": "CHANGELOG.md",
        "licensesUrl": "LICENSE.md",
    }
    for key, expected in expected_urls.items():
        if manifest.get(key) != expected:
            errors.append(f"{key} must be {expected}")
        if not (root / target_files[key]).is_file():
            errors.append(f"{key} target is missing: {target_files[key]}")

    dependencies = manifest.get("dependencies", {})
    if not isinstance(dependencies, dict):
        errors.append("package.json dependencies must be an object")
        return

    deucarian_dependencies = []
    external_dependencies = []
    for package_id, version in dependencies.items():
        if not isinstance(package_id, str) or not isinstance(version, str):
            errors.append("package.json dependency IDs and versions must be strings")
            continue
        if f"`{package_id}`" not in notices or f"`{version}`" not in notices:
            errors.append(f"THIRD_PARTY_NOTICES.md does not record {package_id} {version}")
        if package_id.startswith("com.deucarian."):
            deucarian_dependencies.append(package_id)
        else:
            external_dependencies.append(package_id)

    if deucarian_dependencies and "## Deucarian dependencies (not third-party)" not in notices:
        errors.append("Deucarian dependencies must be distinguished from third-party dependencies")
    if external_dependencies and "## External package dependencies" not in notices:
        errors.append("external package dependencies require an explicit notice section")
    if not dependencies and "declares no direct package dependencies" not in notices:
        errors.append("dependency-free manifests must be stated explicitly in THIRD_PARTY_NOTICES.md")


def _iter_requirement_pins(requirements_path: Path) -> Iterable[tuple[str, str]]:
    if not requirements_path.is_file():
        return
    for raw_line in requirements_path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s;]+)", line)
        if match:
            yield match.group(1), match.group(2)


def validate_repository(root: Path, repository_name: str | None = None) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    trust_text = {
        name: _require_text(root / name, errors) for name in REQUIRED_TRUST_FILES
    }
    package_path = root / "package.json"
    manifest: dict[str, object] | None = None
    if package_path.is_file():
        loaded = _load_json(package_path)
        if not isinstance(loaded, dict):
            errors.append("package.json root must be an object")
        else:
            manifest = loaded
            manifest_name = _repository_name_from_manifest(manifest)
            if repository_name and manifest_name and repository_name != manifest_name:
                errors.append(
                    f"repository name mismatch: argument={repository_name}, manifest={manifest_name}"
                )
            repository_name = repository_name or manifest_name

    if not repository_name:
        errors.append("repository name could not be derived; pass --repository-name")
        return errors

    support = trust_text["SUPPORT.md"]
    security = trust_text["SECURITY.md"]
    notices = trust_text["THIRD_PARTY_NOTICES.md"]
    expected_issues = f"https://github.com/Deucarian/{repository_name}/issues"
    expected_private_report = (
        f"https://github.com/Deucarian/{repository_name}/security/advisories/new"
    )
    if expected_issues not in support:
        errors.append(f"SUPPORT.md must use the repository issue tracker: {expected_issues}")
    if expected_private_report not in security:
        errors.append(
            "SECURITY.md must use the repository's GitHub private vulnerability reporting URL: "
            f"{expected_private_report}"
        )
    if "Do not open a public issue" not in security:
        errors.append("SECURITY.md must warn against public vulnerability disclosure")
    if "## Review basis" not in notices:
        errors.append("THIRD_PARTY_NOTICES.md must document its inventory review basis")

    for filename, text in trust_text.items():
        match = DEUCARIAN_EMAIL_PATTERN.search(text)
        if match:
            errors.append(f"{filename} contains an unverified Deucarian email address")

    if manifest is not None:
        _validate_package_manifest(root, manifest, repository_name, notices, errors)
    else:
        requirements = root / "Tools" / "audit-requirements.txt"
        pins = list(_iter_requirement_pins(requirements))
        if not pins:
            errors.append("non-package repository has no auditable tooling requirement pins")
        for distribution, version in pins:
            if f"`{distribution}`" not in notices or f"`{version}`" not in notices:
                errors.append(
                    f"THIRD_PARTY_NOTICES.md does not record tooling dependency "
                    f"{distribution} {version}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository-name")
    args = parser.parse_args()

    errors = validate_repository(args.repository_root, args.repository_name)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Trust metadata valid: {args.repository_root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
