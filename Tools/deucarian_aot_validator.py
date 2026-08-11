#!/usr/bin/env python3
"""Audit Deucarian Unity packages for runtime reflection and manual linker rules."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


SKIP_DIRS = {
    ".git",
    ".idea",
    ".vs",
    "Library",
    "Logs",
    "Obj",
    "Packages",
    "ProjectSettings",
    "Temp",
    "bin",
    "obj",
}
AOT_MODES = {"Audit", "Enforce"}
AOT_STRATEGIES = {"Generated", "Declared", "Framework"}


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    pattern: re.Pattern[str]
    prerequisite: str = ""
    source_mode: str = "stripped"


@dataclass(frozen=True)
class Finding:
    rule: str
    description: str
    file: str
    line: int
    symbol: str


RULES = (
    Rule(
        "runtime-activator",
        "Runtime construction through Activator cannot prove a closed target set.",
        re.compile(r"\b(?:System\.)?Activator\s*\.\s*CreateInstance\s*\("),
    ),
    Rule(
        "runtime-type-discovery",
        "Runtime type/member discovery must be generated or explicitly composed.",
        re.compile(
            r"(?:\b(?:System\.)?Type\s*\.\s*GetType\s*\(|"
            r"\.\s*(?:GetType|GetMethod|GetMethods|GetMember|GetMembers|"
            r"GetProperty|GetProperties|GetField|GetFields|GetConstructor|"
            r"GetConstructors|GetEvent|GetEvents|GetNestedType|GetNestedTypes|"
            r"GetInterface|GetInterfaces|MakeGenericType|MakeGenericMethod)\s*\()"
        ),
    ),
    Rule(
        "runtime-assembly-discovery",
        "Runtime assembly discovery/loading must be replaced by a closed registry.",
        re.compile(
            r"(?:\b(?:System\.Reflection\.)?Assembly\s*\.\s*"
            r"(?:Load|LoadFrom|LoadFile|GetExecutingAssembly|GetAssembly)\s*\(|"
            r"\.\s*GetAssemblies\s*\(|\.\s*GetTypes\s*\()"
        ),
    ),
    Rule(
        "reflective-invocation",
        "Reflection member invocation/access is not allowed in player code.",
        re.compile(
            r"\.\s*(?:Invoke|InvokeMember|GetValue|SetValue|CreateDelegate|"
            r"AddEventHandler|RemoveEventHandler)\s*\("
        ),
        "reflection",
    ),
    Rule(
        "reflection-based-newtonsoft",
        "Newtonsoft object mapping discovers constructors and members through reflection.",
        re.compile(
            r"(?:\bJsonConvert\s*\.\s*(?:SerializeObject|DeserializeObject|PopulateObject)"
            r"\s*(?:<[^>]+>)?\s*\(|"
            r"\bJsonSerializer\s*\.\s*(?:Create|Serialize|Deserialize|Populate)"
            r"\s*(?:<[^>]+>)?\s*\(|"
            r"\.\s*(?:ToObject|FromObject)\s*(?:<[^>]+>)?\s*\()"
        ),
        "newtonsoft",
    ),
    Rule(
        "reflection-based-system-text-json",
        "System.Text.Json calls require generated metadata in Unity player code.",
        re.compile(
            r"\bJsonSerializer\s*\.\s*(?:Serialize|SerializeToUtf8Bytes|Deserialize)\s*(?:<[^>]+>)?\s*\("
        ),
        "system-text-json",
    ),
    Rule(
        "reflection-based-xml",
        "XML/DataContract object mapping requires an explicit generated or declared AOT strategy.",
        re.compile(
            r"\b(?:XmlSerializer|DataContractSerializer)\s*(?:\(|\.\s*(?:Serialize|Deserialize|ReadObject|WriteObject)\s*\()"
        ),
    ),
    Rule(
        "runtime-expression-compilation",
        "Expression tree compilation is runtime code generation and is not portable to all AOT targets.",
        re.compile(r"\.\s*Compile\s*\("),
        "expressions",
    ),
    Rule(
        "unity-string-dispatch",
        "Unity string-based dispatch hides the target method or component from static reachability.",
        re.compile(
            r"(?:(?:\.\s*|\b)(?:SendMessage|BroadcastMessage|SendMessageUpwards)\s*\(|"
            r"(?:\.\s*|\b)(?:Invoke|InvokeRepeating|StartCoroutine|StopCoroutine|GetComponent|AddComponent)\s*"
            r"\(\s*(?:\$@|@\$|\$|@)?\")"
        ),
        "unity",
        "comments-only",
    ),
)
RULES_BY_ID = {rule.id: rule for rule in RULES}


class AotValidator:
    def __init__(self, repository_root: Path, config_path: Path | None = None):
        self.root = repository_root.resolve()
        self.config_path = (config_path or self.root / "deucarian-package.json").resolve()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.findings: list[Finding] = []
        self.suppressed: list[Finding] = []
        self.used_exception_indexes: set[int] = set()
        self.config = self.read_json(self.config_path)
        self.package_id = str(self.config.get("packageId") or self.root.name)
        self.policy = self.read_policy()

    def validate(self) -> dict[str, Any]:
        if not self.root.is_dir():
            self.errors.append(f"Repository root does not exist: {self.root}")
            return self.result()

        for path in self.runtime_source_files():
            self.scan_source(path)
        self.scan_linker_files()
        self.apply_exceptions()

        mode = self.policy["mode"]
        unresolved = [finding for finding in self.findings if finding not in self.suppressed]
        for finding in unresolved:
            message = self.format_finding(finding)
            if mode == "Enforce":
                self.errors.append(message)
            else:
                self.warnings.append(message)

        for index, exception in enumerate(self.policy["exceptions"]):
            if index not in self.used_exception_indexes:
                self.warnings.append(
                    f"{self.package_id}: stale AOT exception does not match a finding: "
                    f"{exception['file']} [{exception['rule']}] {exception['symbol']!r}."
                )

        return self.result()

    def read_policy(self) -> dict[str, Any]:
        raw = self.config.get("aotSafety") or {}
        if not isinstance(raw, dict):
            self.errors.append(f"{self.package_id}: aotSafety must be an object.")
            raw = {}

        mode = raw.get("mode", "Audit")
        if mode not in AOT_MODES:
            self.errors.append(
                f"{self.package_id}: aotSafety.mode must be one of {sorted(AOT_MODES)}, got {mode!r}."
            )
            mode = "Audit"

        exceptions = raw.get("exceptions") or []
        if not isinstance(exceptions, list):
            self.errors.append(f"{self.package_id}: aotSafety.exceptions must be an array.")
            exceptions = []

        validated: list[dict[str, Any]] = []
        for index, item in enumerate(exceptions):
            label = f"{self.package_id}: aotSafety.exceptions[{index}]"
            if not isinstance(item, dict):
                self.errors.append(f"{label} must be an object.")
                continue
            file_path = normalize_path(str(item.get("file") or ""))
            rule = str(item.get("rule") or "")
            symbol = normalize_symbol(str(item.get("symbol") or ""))
            strategy = str(item.get("strategy") or "")
            reason = str(item.get("reason") or "").strip()
            if not file_path or any(character in file_path for character in "*?["):
                self.errors.append(f"{label}.file must be one exact repository-relative path.")
            if rule not in RULES_BY_ID and rule != "manual-link-xml":
                self.errors.append(f"{label}.rule is unknown: {rule!r}.")
            if not symbol:
                self.errors.append(f"{label}.symbol is required and must match the reported symbol exactly.")
            if strategy not in AOT_STRATEGIES:
                self.errors.append(
                    f"{label}.strategy must be one of {sorted(AOT_STRATEGIES)}."
                )
            if not reason:
                self.errors.append(f"{label}.reason is required.")

            preserve_types = item.get("preserveTypes") or []
            if not isinstance(preserve_types, list):
                self.errors.append(f"{label}.preserveTypes must be an array.")
                preserve_types = []
            if strategy == "Declared" and not preserve_types:
                self.errors.append(
                    f"{label}: Declared exceptions require at least one exact preserveTypes entry."
                )
            for preserve_index, preserve in enumerate(preserve_types):
                preserve_label = f"{label}.preserveTypes[{preserve_index}]"
                if not isinstance(preserve, dict):
                    self.errors.append(f"{preserve_label} must be an object.")
                    continue
                if not str(preserve.get("assemblyName") or "").strip():
                    self.errors.append(f"{preserve_label}.assemblyName is required.")
                type_name = str(preserve.get("typeName") or "").strip()
                if not type_name or "*" in type_name:
                    self.errors.append(f"{preserve_label}.typeName must be exact and non-wildcard.")
                if not str(preserve.get("reason") or "").strip():
                    self.errors.append(f"{preserve_label}.reason is required.")

            validated.append(
                {
                    "file": file_path,
                    "rule": rule,
                    "symbol": symbol,
                    "strategy": strategy,
                    "reason": reason,
                    "preserveTypes": preserve_types,
                }
            )

        return {"mode": mode, "exceptions": validated}

    def runtime_source_files(self) -> Iterable[Path]:
        runtime_assemblies = set(self.config.get("runtimeAssemblies") or [])
        asmdefs: list[tuple[Path, str]] = []
        for path in self.root.rglob("*.asmdef"):
            if is_skipped(path, self.root):
                continue
            data = self.read_json(path, required=False)
            name = data.get("name") if isinstance(data, dict) else None
            if name:
                asmdefs.append((path.parent.resolve(), str(name)))
        asmdefs.sort(key=lambda item: len(item[0].parts), reverse=True)

        for path in iter_files(self.root, ".cs"):
            relative = normalize_path(path.relative_to(self.root).as_posix())
            if relative.startswith("Editor/") or relative.startswith("Tests/") or relative.startswith("Samples~/"):
                continue
            owner = next(
                (name for directory, name in asmdefs if path.resolve().is_relative_to(directory)),
                None,
            )
            if owner is not None:
                if owner in runtime_assemblies:
                    yield path
                continue
            if relative.startswith("Runtime/"):
                yield path

    def scan_source(self, path: Path) -> None:
        relative = normalize_path(path.relative_to(self.root).as_posix())
        source = self.text(path)
        stripped = strip_comments_and_literals(source)
        comments_only = strip_comments(source)
        prerequisites = {
            "reflection": bool(
                re.search(
                    r"\busing\s+System\.Reflection\s*;|\b(?:MethodInfo|PropertyInfo|FieldInfo|ConstructorInfo|MemberInfo)\b",
                    stripped,
                )
            ),
            "newtonsoft": bool(
                re.search(r"\busing\s+Newtonsoft\.Json(?:\.Linq)?\s*;|\bNewtonsoft\.Json\.", stripped)
            ),
            "system-text-json": bool(
                re.search(r"\busing\s+System\.Text\.Json\s*;|\bSystem\.Text\.Json\.", stripped)
            ),
            "expressions": bool(
                re.search(r"\busing\s+System\.Linq\.Expressions\s*;|\bSystem\.Linq\.Expressions\.", stripped)
            ),
            "unity": bool(
                re.search(r"\busing\s+UnityEngine\s*;|\bUnityEngine\.", stripped)
            ),
        }

        seen: set[tuple[str, int, str]] = set()
        for rule in RULES:
            if rule.prerequisite and not prerequisites.get(rule.prerequisite, False):
                continue
            scan_text = comments_only if rule.source_mode == "comments-only" else stripped
            for match in rule.pattern.finditer(scan_text):
                line = scan_text.count("\n", 0, match.start()) + 1
                symbol = normalize_symbol(match.group(0))
                key = (rule.id, line, symbol)
                if key in seen:
                    continue
                seen.add(key)
                self.findings.append(
                    Finding(
                        rule=rule.id,
                        description=rule.description,
                        file=relative,
                        line=line,
                        symbol=symbol,
                    )
                )

    def scan_linker_files(self) -> None:
        for path in iter_files(self.root, "link.xml", exact_name=True):
            relative = normalize_path(path.relative_to(self.root).as_posix())
            self.findings.append(
                Finding(
                    rule="manual-link-xml",
                    description=(
                        "Handwritten linker descriptors are not an accepted Deucarian runtime architecture; "
                        "emit exact generated AOT evidence instead."
                    ),
                    file=relative,
                    line=1,
                    symbol="link.xml",
                )
            )

    def apply_exceptions(self) -> None:
        for finding in self.findings:
            for index, exception in enumerate(self.policy["exceptions"]):
                if (
                    exception["file"] == finding.file
                    and exception["rule"] == finding.rule
                    and exception["symbol"] == finding.symbol
                ):
                    self.suppressed.append(finding)
                    self.used_exception_indexes.add(index)
                    break

    def result(self) -> dict[str, Any]:
        unresolved = [finding for finding in self.findings if finding not in self.suppressed]
        return {
            "ok": not self.errors,
            "packageId": self.package_id,
            "mode": self.policy["mode"],
            "errors": sorted(set(self.errors)),
            "warnings": sorted(set(self.warnings)),
            "findings": [asdict(item) for item in sorted(unresolved, key=finding_key)],
            "suppressedFindings": [
                asdict(item) for item in sorted(self.suppressed, key=finding_key)
            ],
        }

    def format_finding(self, finding: Finding) -> str:
        return (
            f"{self.package_id}: {finding.file}:{finding.line} "
            f"[{finding.rule}] {finding.description} Found {finding.symbol!r}."
        )

    def read_json(self, path: Path, required: bool = True) -> Any:
        if not path.exists():
            if required:
                self.errors.append(f"Missing JSON file: {path}")
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            self.errors.append(f"Invalid JSON {path}: {exc}")
            return {}

    @staticmethod
    def text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return path.read_text(encoding="utf-8", errors="replace")


def iter_files(root: Path, suffix_or_name: str, exact_name: bool = False) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(directory for directory in dirnames if directory not in SKIP_DIRS)
        for filename in sorted(filenames):
            if (exact_name and filename == suffix_or_name) or (
                not exact_name and filename.endswith(suffix_or_name)
            ):
                yield Path(dirpath) / filename


def is_skipped(path: Path, root: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(root).parts)


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", lambda match: preserve_newlines(match.group(0)), text, flags=re.S)
    return re.sub(r"//[^\n]*", " ", text)


def strip_comments_and_literals(text: str) -> str:
    text = strip_comments(text)
    text = re.sub(
        r'(?:\$@|@\$|\$|@)?"(?:""|\\.|[^"\\])*"',
        lambda match: preserve_newlines(match.group(0)),
        text,
        flags=re.S,
    )
    text = re.sub(r"'(?:\\.|[^'\\])'", "'C'", text)
    return text


def preserve_newlines(value: str) -> str:
    return "\n" * value.count("\n") + " "


def normalize_path(value: str) -> str:
    return value.strip().replace("\\", "/").lstrip("./")


def normalize_symbol(value: str) -> str:
    return re.sub(r"\s+", "", value).rstrip("(")


def finding_key(finding: Finding) -> tuple[str, int, str, str]:
    return (finding.file, finding.line, finding.rule, finding.symbol)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--ci", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    validator = AotValidator(args.repository_root, args.config)
    result = validator.validate()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        if result["ok"]:
            print(
                f"Deucarian AOT validation passed: {result['packageId']} "
                f"({result['mode']}, {len(result['findings'])} unresolved finding(s))"
            )
        else:
            print(f"Deucarian AOT validation failed: {result['packageId']}", file=sys.stderr)
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
