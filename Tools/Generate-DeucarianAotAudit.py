#!/usr/bin/env python3
"""Generate deterministic organization-wide Deucarian AOT safety audit artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from deucarian_aot_validator import AotValidator


JSON_FILE = "AOT_SAFETY_AUDIT.json"
MARKDOWN_FILE = "AOT_SAFETY_AUDIT.md"
SCHEMA_VERSION = 1
SKIP_REPOSITORIES = {"Package-Registry"}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--organization", default="Deucarian")
    parser.add_argument("--ref", default="develop")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    return parser


def generate(audit_root: Path, organization: str, ref: str) -> dict[str, Any]:
    root = audit_root.resolve()
    repositories: list[dict[str, Any]] = []
    category_counts: Counter[str] = Counter()
    mode_counts: Counter[str] = Counter()
    total_suppressed = 0

    if not root.is_dir():
        raise ValueError(f"Audit root does not exist: {root}")

    for repository_root in sorted(
        (path for path in root.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    ):
        if repository_root.name in SKIP_REPOSITORIES:
            continue
        config_path = repository_root / "deucarian-package.json"
        if not config_path.is_file():
            continue

        result = AotValidator(repository_root, config_path).validate()
        findings = sorted(
            result["findings"],
            key=lambda item: (
                item["file"],
                item["line"],
                item["rule"],
                item["symbol"],
            ),
        )
        suppressed = sorted(
            result["suppressedFindings"],
            key=lambda item: (
                item["file"],
                item["line"],
                item["rule"],
                item["symbol"],
            ),
        )
        repository_categories = Counter(item["rule"] for item in findings)
        category_counts.update(repository_categories)
        mode_counts[result["mode"]] += 1
        total_suppressed += len(suppressed)
        repositories.append(
            {
                "repository": repository_root.name,
                "packageId": result["packageId"],
                "mode": result["mode"],
                "ok": result["ok"],
                "findingCount": len(findings),
                "suppressedFindingCount": len(suppressed),
                "categories": dict(sorted(repository_categories.items())),
                "errors": sorted(result["errors"]),
                "findings": findings,
                "suppressedFindings": suppressed,
            }
        )

    repositories.sort(key=lambda item: (item["packageId"], item["repository"]))
    repositories_with_findings = sum(
        1 for repository in repositories if repository["findingCount"] > 0
    )
    validation_failures = sum(1 for repository in repositories if not repository["ok"])
    return {
        "schemaVersion": SCHEMA_VERSION,
        "organization": organization,
        "ref": ref,
        "summary": {
            "repositoryCount": len(repositories),
            "repositoriesWithFindings": repositories_with_findings,
            "cleanRepositoryCount": len(repositories) - repositories_with_findings,
            "totalFindingCount": sum(category_counts.values()),
            "totalSuppressedFindingCount": total_suppressed,
            "validationFailureCount": validation_failures,
            "modeCounts": dict(sorted(mode_counts.items())),
            "categoryCounts": dict(sorted(category_counts.items())),
        },
        "repositories": repositories,
    }


def render_markdown(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    lines = [
        "# Deucarian AOT Safety Audit",
        "",
        f"Authoritative runtime reflection and linker inventory for `{audit['organization']}` at `{audit['ref']}`.",
        "",
        "This report inventories current package-owned player-code findings. Editor-only reflection is excluded. Audit findings are migration work; an `Enforce` package with an unresolved finding fails validation.",
        "",
        "## Summary",
        "",
        f"- Repositories scanned: **{summary['repositoryCount']}**",
        f"- Repositories with findings: **{summary['repositoriesWithFindings']}**",
        f"- Clean repositories: **{summary['cleanRepositoryCount']}**",
        f"- Unresolved findings: **{summary['totalFindingCount']}**",
        f"- Suppressed findings: **{summary['totalSuppressedFindingCount']}**",
        f"- Validation failures: **{summary['validationFailureCount']}**",
        "",
        "## Finding Categories",
        "",
        "| Rule | Count |",
        "| --- | ---: |",
    ]
    category_counts = summary["categoryCounts"]
    if category_counts:
        for rule, count in category_counts.items():
            lines.append(f"| `{escape(rule)}` | {count} |")
    else:
        lines.append("| _None_ | 0 |")

    lines.extend(
        [
            "",
            "## Repository Status",
            "",
            "| Package | Repository | Mode | Findings | Suppressed | Status |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for repository in audit["repositories"]:
        status = "Valid" if repository["ok"] else "Failing"
        lines.append(
            "| `{}` | `{}` | `{}` | {} | {} | {} |".format(
                escape(repository["packageId"]),
                escape(repository["repository"]),
                escape(repository["mode"]),
                repository["findingCount"],
                repository["suppressedFindingCount"],
                status,
            )
        )

    repositories_with_findings = [
        repository
        for repository in audit["repositories"]
        if repository["findings"] or repository["errors"]
    ]
    lines.extend(["", "## Findings", ""])
    if not repositories_with_findings:
        lines.append("No unresolved runtime AOT findings.")
    for repository in repositories_with_findings:
        lines.extend(
            [
                f"### `{escape(repository['packageId'])}`",
                "",
                f"Repository: `{escape(repository['repository'])}`",
                f"Mode: `{escape(repository['mode'])}`",
                "",
            ]
        )
        for error in repository["errors"]:
            lines.append(f"- **Validation error:** {escape(error)}")
        for finding in repository["findings"]:
            lines.append(
                "- `{}` — `{}` at `{}`:{} (`{}`)".format(
                    escape(finding["rule"]),
                    escape(finding["symbol"]),
                    escape(finding["file"]),
                    finding["line"],
                    escape(finding["description"]),
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Migration Rule",
            "",
            "Each finding is generated away, explicitly composed, exactly declared with verified preserve targets, or isolated as an audited framework boundary. Application-owned handwritten `link.xml` is not a final disposition.",
            "",
        ]
    )
    return "\n".join(lines)


def write_or_check(output_root: Path, audit: dict[str, Any], check: bool) -> bool:
    output_root.mkdir(parents=True, exist_ok=True)
    expected = {
        JSON_FILE: json.dumps(audit, indent=2, sort_keys=True) + "\n",
        MARKDOWN_FILE: render_markdown(audit),
    }
    stale: list[str] = []
    for name, content in expected.items():
        path = output_root / name
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == content:
            continue
        if check:
            stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote: {path}")
    if stale:
        print("AOT safety audit artifacts are stale: " + ", ".join(stale), file=sys.stderr)
        return False
    return True


def escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    args = build_arg_parser().parse_args()
    try:
        audit = generate(args.audit_root, args.organization, args.ref)
    except Exception as exception:
        print(str(exception), file=sys.stderr)
        return 1
    if not write_or_check(args.output_root, audit, args.check):
        return 1
    return 0 if audit["summary"]["validationFailureCount"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
