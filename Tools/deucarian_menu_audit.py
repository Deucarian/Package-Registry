#!/usr/bin/env python3
"""Audit the compact, task-oriented Tools/Deucarian menu contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


MENU_RE = re.compile(r"\[\s*MenuItem\s*\(\s*(?P<expression>[^,\)]+)(?P<tail>[^\)]*)\)\s*\]")
EXECUTE_RE = re.compile(
    r"(?:Menu|EditorApplication)\.ExecuteMenuItem\s*\(\s*(?P<expression>[^\)]+)\)"
)
CONST_RE = re.compile(
    r"\bconst\s+string\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<expression>[^;]+);"
)
STRING_RE = re.compile(r'^"(?P<value>(?:[^"\\]|\\.)*)"$')
EXCLUDED_PARTS = {
    ".git",
    ".vs",
    "Library",
    "Temp",
    "Logs",
    "obj",
    "Build",
    "Builds",
    "node_modules",
    "PackageCache",
}
STALE_TEXT_SUFFIXES = {".cs", ".json", ".md", ".txt", ".uxml"}


@dataclass(frozen=True)
class MenuEntry:
    repository: str
    packageId: str
    file: str
    line: int
    path: str
    validator: bool


@dataclass(frozen=True)
class Finding:
    code: str
    repository: str
    packageId: str
    file: str
    line: int
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-root", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def repositories(root: Path) -> list[Path]:
    if (root / "package.json").is_file() or (root / "deucarian-package.json").is_file():
        return [root]
    return sorted(
        (item for item in root.iterdir() if item.is_dir() and not item.name.startswith(".")),
        key=lambda item: item.name.lower(),
    )


def package_id(repo: Path) -> str:
    manifest = repo / "package.json"
    if manifest.is_file():
        try:
            return str(json.loads(manifest.read_text(encoding="utf-8")).get("name") or "")
        except (OSError, json.JSONDecodeError):
            return ""
    return "com.deucarian.package-registry" if repo.name == "Package-Registry" else ""


def source_files(repo: Path) -> Iterable[Path]:
    for path in repo.rglob("*.cs"):
        if any(part in EXCLUDED_PARTS for part in path.relative_to(repo).parts):
            continue
        yield path


def stale_text_files(repo: Path) -> Iterable[Path]:
    for path in repo.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in STALE_TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.relative_to(repo).parts):
            continue
        yield path


def decode_string(value: str) -> str:
    return bytes(value, "utf-8").decode("unicode_escape")


def constants(text: str, seed: dict[str, str] | None = None) -> dict[str, str]:
    expressions = {match.group("name"): match.group("expression").strip() for match in CONST_RE.finditer(text)}
    resolved: dict[str, str] = dict(seed or {})
    for name in expressions:
        value = resolve_expression(expressions[name], expressions, resolved, {name})
        if value is not None:
            resolved[name] = value
    return resolved


def resolve_expression(
    expression: str,
    expressions: dict[str, str],
    resolved: dict[str, str],
    resolving: set[str],
) -> str | None:
    pieces: list[str] = []
    for raw in expression.strip().split("+"):
        token = raw.strip().strip("()")
        literal = STRING_RE.match(token)
        if literal:
            pieces.append(decode_string(literal.group("value")))
            continue
        short_name = token.split(".")[-1]
        name = token if token in resolved or token in expressions else short_name
        if name in resolved:
            pieces.append(resolved[name])
            continue
        if name not in expressions or name in resolving:
            return None
        resolving.add(name)
        value = resolve_expression(expressions[name], expressions, resolved, resolving)
        resolving.remove(name)
        if value is None:
            return None
        resolved[name] = value
        pieces.append(value)
    return "".join(pieces)


def expression_value(expression: str, known: dict[str, str]) -> str | None:
    return resolve_expression(expression, known, dict(known), set())


def repository_constants(repo: Path, seed: dict[str, str]) -> dict[str, str]:
    declarations: dict[str, set[str]] = {}
    for path in source_files(repo):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in CONST_RE.finditer(text):
            declarations.setdefault(match.group("name"), set()).add(
                match.group("expression").strip()
            )
    expressions = {
        name: next(iter(values))
        for name, values in declarations.items()
        if len(values) == 1
    }
    resolved = dict(seed)
    for name in expressions:
        if name in resolved:
            continue
        value = resolve_expression(expressions[name], expressions, resolved, {name})
        if value is not None:
            resolved[name] = value
    return resolved


def relative(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excluded_stale(path: str, exclusions: list[str]) -> bool:
    return any(path == item or path.startswith(item) for item in exclusions)


def audit(audit_root: Path, policy: dict) -> dict:
    approved: dict[str, str] = policy["approvedPaths"]
    root = str(policy["root"])
    prohibited = [str(item) for item in policy.get("prohibitedFragments", [])]
    bridge_pairs = {
        (item["callerPackageId"], item["path"])
        for item in policy.get("permittedCrossPackageMenuBridges", [])
    }
    stale_exclusions = list(policy.get("staleProjectSetupExclusions", []))
    external_constants = {
        str(name): str(value)
        for name, value in policy.get("knownConstants", {}).items()
    }
    entries: list[MenuEntry] = []
    findings: list[Finding] = []

    for repo in repositories(audit_root.resolve()):
        owner = package_id(repo)
        repo_constants = repository_constants(repo, external_constants)
        for path in source_files(repo):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = relative(path, repo)
            known = constants(text, repo_constants)
            for match in MENU_RE.finditer(text):
                value = expression_value(match.group("expression"), known)
                line = line_number(text, match.start())
                if value is None:
                    if "Deucarian" in match.group("expression"):
                        findings.append(Finding(
                            "UnresolvedMenuPath", repo.name, owner, rel, line,
                            "MenuItem path expression could not be resolved deterministically.",
                        ))
                    continue
                if not value.startswith(root):
                    continue
                validator = bool(re.search(r",\s*true(?:\s*,|\s*$)", match.group("tail")))
                entry = MenuEntry(repo.name, owner, rel, line, value, validator)
                entries.append(entry)
                if any(fragment in value for fragment in prohibited):
                    findings.append(Finding(
                        "TechnicalTaxonomy", repo.name, owner, rel, line,
                        f"Technical package taxonomy is prohibited in user navigation: {value}",
                    ))
                if value not in approved:
                    findings.append(Finding(
                        "UnauthorizedPath", repo.name, owner, rel, line,
                        f"Unauthorized Tools/Deucarian path: {value}",
                    ))
                elif approved[value] != owner:
                    findings.append(Finding(
                        "WrongOwner", repo.name, owner, rel, line,
                        f"{value} is owned by {approved[value]}, not {owner or repo.name}.",
                    ))

            for match in EXECUTE_RE.finditer(text):
                value = expression_value(match.group("expression"), known)
                if value is None or not value.startswith(root):
                    continue
                line = line_number(text, match.start())
                expected_owner = approved.get(value)
                if expected_owner and expected_owner != owner and (owner, value) not in bridge_pairs:
                    findings.append(Finding(
                        "CrossPackageMenuContract", repo.name, owner, rel, line,
                        f"Cross-package navigation to {value} must use a stable tool ID or public Open API.",
                    ))

    for repo in repositories(audit_root.resolve()):
        owner = package_id(repo)
        for path in stale_text_files(repo):
            rel = relative(path, repo)
            if excluded_stale(rel, stale_exclusions):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if "Tools/Deucarian/Project Setup" in text:
                findings.append(Finding(
                    "StaleProjectSetup", repo.name, owner, rel,
                    line_number(text, text.index("Tools/Deucarian/Project Setup")),
                    "Stale Project Setup menu text must be migrated to Control Center.",
                ))

    by_path: dict[str, list[MenuEntry]] = {}
    for entry in entries:
        if not entry.validator:
            by_path.setdefault(entry.path, []).append(entry)
    for path, declarations in by_path.items():
        if len(declarations) < 2:
            continue
        for entry in declarations:
            findings.append(Finding(
                "DuplicatePath", entry.repository, entry.packageId, entry.file, entry.line,
                f"Duplicate user-facing menu path has {len(declarations)} declarations: {path}",
            ))

    entries.sort(key=lambda item: (item.path, item.repository, item.file, item.line))
    findings.sort(key=lambda item: (item.code, item.repository, item.file, item.line))
    return {
        "schemaVersion": 1,
        "policySchemaVersion": policy.get("schemaVersion"),
        "auditRoot": ".",
        "summary": {
            "entryCount": len(entries),
            "userFacingPathCount": len(by_path),
            "findingCount": len(findings),
            "ok": not findings,
        },
        "entries": [asdict(item) for item in entries],
        "findings": [asdict(item) for item in findings],
    }


def markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# Deucarian Menu Governance Audit",
        "",
        f"- User-facing declarations: {summary['entryCount']}",
        f"- Unique paths: {summary['userFacingPathCount']}",
        f"- Findings: {summary['findingCount']}",
        f"- Result: {'PASS' if summary['ok'] else 'FAIL'}",
        "",
        "## Menu entries",
        "",
        "| Path | Owner | Repository | Source |",
        "|---|---|---|---|",
    ]
    for item in report["entries"]:
        validator = " (validator)" if item["validator"] else ""
        lines.append(
            f"| `{item['path']}` | `{item['packageId']}` | {item['repository']} | "
            f"`{item['file']}:{item['line']}`{validator} |"
        )
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("No menu governance violations.")
    else:
        for item in report["findings"]:
            lines.append(
                f"- **{item['code']}** `{item['repository']}/{item['file']}:{item['line']}`: "
                f"{item['message']}"
            )
    return "\n".join(lines) + "\n"


def write_or_check(output_root: Path, report: dict, check: bool) -> bool:
    outputs = {
        "MENU_AUDIT.json": json.dumps(report, indent=2, sort_keys=True) + "\n",
        "MENU_AUDIT.md": markdown(report),
    }
    stale: list[str] = []
    output_root.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        path = output_root / name
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        print("Menu audit artifacts are stale: " + ", ".join(stale), file=sys.stderr)
        return False
    return True


def main() -> int:
    args = parse_args()
    policy = json.loads(args.policy.resolve().read_text(encoding="utf-8"))
    report = audit(args.audit_root.resolve(), policy)
    artifacts_ok = write_or_check(args.output_root.resolve(), report, args.check)
    if not report["summary"]["ok"]:
        for finding in report["findings"][:20]:
            print(f"{finding['code']}: {finding['message']}", file=sys.stderr)
    return 0 if report["summary"]["ok"] and artifacts_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
