#!/usr/bin/env python3
"""Syntax-aware responsibility review triggers with an explicit, non-growing debt baseline."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

LIMITS = {"lines": 500, "statements": 300, "methods": 40, "mutableGlobals": 0}
TYPE_NODES = {"class_declaration", "struct_declaration", "record_declaration", "record_struct_declaration"}
COLLECTIONS = {"Dictionary", "List", "HashSet", "Queue", "Stack", "ConcurrentDictionary"}
SIGNALS = {
    "presentation": {"GUILayout", "EditorGUILayout", "VisualElement", "GUI", "Canvas"},
    "storage": {"AssetDatabase", "EditorPrefs", "PlayerPrefs", "File", "FileStream"},
    "transport": {"UnityWebRequest", "HttpClient", "WebRequest"},
    "scene": {"GameObject", "Transform", "SceneManager"},
}


def load_auditor():
    name = "deucarian_shared_syntax_auditor"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("Generate-DeucarianAudit.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def collect_types(parsed):
    """Aggregate by assembly and qualified type, never by numbered partial file."""
    rows = {}
    if parsed.generated or parsed.tree is None or parsed.scope not in {"Runtime production", "Editor production"}:
        return rows
    source = parsed.text.encode("utf-8")

    def text(node):
        return source[node.start_byte:node.end_byte].decode("utf-8")

    def identifiers(node):
        if node.type == "identifier":
            yield text(node)
        for child in node.named_children:
            yield from identifiers(child)

    def visit(node, namespace=(), parents=()):
        if node.type in {"namespace_declaration", "file_scoped_namespace_declaration"}:
            name = node.child_by_field_name("name")
            namespace += (text(name),) if name else ()
        if node.type in TYPE_NODES:
            name = node.child_by_field_name("name")
            parameters = next((c for c in node.named_children if c.type == "type_parameter_list"), None)
            arity = len(parameters.named_children) if parameters else 0
            local = text(name) + (f"`{arity}" if arity else "")
            qualified = ".".join((*namespace, *parents, local))
            key = parsed.assembly + ":" + qualified
            row = rows.setdefault(key, {
                "type": qualified, "assembly": parsed.assembly, "scope": parsed.scope,
                "lines": 0, "statements": 0, "methods": 0, "mutableGlobals": 0,
                "parts": [], "signals": set(),
            })
            row["lines"] += node.end_point[0] - node.start_point[0] + 1
            row["parts"].append({"file": parsed.relative_path, "line": node.start_point[0] + 1})

            def members(member):
                if member.type in TYPE_NODES:
                    return
                if member.type.endswith("_statement"):
                    row["statements"] += 1
                if member.type in {"method_declaration", "constructor_declaration", "operator_declaration"}:
                    row["methods"] += 1
                if member.type in {"field_declaration", "event_field_declaration", "property_declaration"}:
                    modifiers = {text(c) for c in member.children if c.type == "modifier"}
                    declaration = next((c for c in member.named_children if c.type == "variable_declaration"), member)
                    declared_type = declaration.child_by_field_name("type")
                    tokens = set(identifiers(declared_type)) if declared_type else set()
                    if "static" in modifiers and "const" not in modifiers:
                        is_mutable = member.type != "property_declaration" and "readonly" not in modifiers
                        if member.type == "property_declaration":
                            accessors = member.child_by_field_name("accessors")
                            is_mutable = bool(accessors and re.search(r"\b(set|init)\s*;", text(accessors)))
                        if is_mutable or tokens.intersection(COLLECTIONS):
                            variables = [c for c in member.named_children if c.type == "variable_declaration"]
                            count = sum(c.type == "variable_declarator" for v in variables for c in v.named_children)
                            row["mutableGlobals"] += max(1, count)
                if member.type == "identifier":
                    for signal, names in SIGNALS.items():
                        if text(member) in names:
                            row["signals"].add(signal)
                for child in member.named_children:
                    members(child)

            body = node.child_by_field_name("body")
            if body:
                members(body)
            parents += (local,)
        for child in node.named_children:
            visit(child, namespace, parents)

    visit(parsed.tree.root_node)
    return rows


def merge_types(target, incoming):
    for key, row in incoming.items():
        if key not in target:
            target[key] = row
            continue
        existing = target[key]
        for metric in LIMITS:
            existing[metric] += row[metric]
        existing["parts"].extend(row["parts"])
        existing["signals"].update(row["signals"])


def scan_repository(root):
    audit = load_auditor()
    manifest = audit.read_json(root / "package.json") or {}
    governance = audit.read_json(root / "deucarian-package.json") or {}
    assemblies = audit.collect_asmdefs(root, governance)
    analyzer = audit.CSharpSyntaxAnalyzer(authoritative=True)
    types = {}
    for path in sorted(root.rglob("*.cs")):
        relative = path.relative_to(root).as_posix()
        if any(part in audit.SKIP_DIRS for part in Path(relative).parts):
            continue
        owner = audit.owning_asmdef(relative, assemblies)
        source = audit.read_text(path)
        parsed = audit.ParsedFile(
            repo=root.name, package_id=manifest.get("name"), repo_root=root, path=path,
            relative_path=relative, scope=audit.scope_for(relative, owner, governance),
            assembly=owner.get("name", "") if owner else "", text=source,
            governance=governance, generated=audit.is_generated_file(path, source))
        if parsed.generated or parsed.scope not in {"Runtime production", "Editor production"}:
            continue
        parsed.tree = analyzer.parser.parse(source.encode("utf-8"))
        if parsed.tree.root_node.has_error:
            recovered = audit.parser_source_with_contextual_identifier_recovery(source)
            parsed.tree = analyzer.parser.parse(recovered.encode("utf-8"))
        if parsed.tree.root_node.has_error:
            raise ValueError(f"C# parse error in {root.name}/{relative}")
        merge_types(types, collect_types(parsed))
    for row in types.values():
        row["signals"] = sorted(row["signals"])
        row["parts"].sort(key=lambda part: (part["file"], part["line"]))
    return {"packageId": manifest.get("name", root.name), "version": manifest.get("version", ""),
            "types": dict(sorted(types.items()))}


def compare(current, baseline, exceptions=None):
    """Existing debt is allowed, increases above the normal limit are not."""
    failures = []
    previous = baseline.get("types", {})
    reviewed = {}
    for entry in exceptions or []:
        if not entry.get("reason", "").strip() or not entry.get("version"):
            raise ValueError("Architecture exceptions require a version and an ownership rationale.")
        limits = entry.get("limits", {})
        if not limits or any(key not in LIMITS or not isinstance(value, int) or isinstance(value, bool) or value < 0
                             for key, value in limits.items()):
            raise ValueError("Architecture exception limits must be exact non-negative metric budgets.")
        if entry["version"] == current.get("version"):
            key = entry["assembly"] + ":" + entry["type"]
            if key in reviewed:
                raise ValueError(f"Duplicate architecture exception: {key}")
            reviewed[key] = limits
    for key, row in current["types"].items():
        old = previous.get(key, {})
        for metric, limit in LIMITS.items():
            allowed = max(limit, old.get(metric, 0), reviewed.get(key, {}).get(metric, 0))
            if row[metric] > allowed:
                failures.append({
                    "type": row["type"], "assembly": row["assembly"], "metric": metric,
                    "actual": row[metric], "allowed": allowed, "parts": row["parts"],
                })
    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--audit-root", type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--exceptions", type=Path)
    parser.add_argument("--write-baseline", action="store_true",
                        help="Explicitly capture reviewed debt; never used by CI.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if (args.repository_root is None) == (args.audit_root is None):
        parser.error("Provide exactly one of --repository-root or --audit-root.")
    roots = [args.repository_root] if args.repository_root else sorted(
        p for p in args.audit_root.iterdir() if p.is_dir() and (p / "package.json").exists())
    packages = {}
    for root in roots:
        result = scan_repository(root.resolve())
        package_id = result["packageId"]
        if package_id in packages:
            raise ValueError(f"Duplicate package source: {package_id}")
        packages[package_id] = result
    baseline = json.loads(args.baseline.read_text(encoding="utf-8")) if args.baseline.exists() else {}
    if args.write_baseline:
        reviewed = {
            package_id: {"types": {
                key: {metric: row[metric] for metric in LIMITS}
                for key, row in package["types"].items()
                if any(row[metric] > limit for metric, limit in LIMITS.items())
            }} for package_id, package in sorted(packages.items())
        }
        baseline = {"schemaVersion": 1, "policy": LIMITS, "packages": reviewed}
        args.baseline.parent.mkdir(parents=True, exist_ok=True)
        args.baseline.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Captured reviewed baseline for {len(packages)} packages.")
        return 0
    if baseline.get("schemaVersion") != 1 or baseline.get("policy") != LIMITS:
        raise ValueError("Missing or incompatible baseline; explicitly review and capture it first.")
    exception_path = args.exceptions or args.baseline.with_name("architecture-metrics-exceptions.json")
    exceptions = json.loads(exception_path.read_text(encoding="utf-8")) if exception_path.exists() else {"schemaVersion": 1, "packages": {}}
    if exceptions.get("schemaVersion") != 1:
        raise ValueError("Unsupported architecture exceptions schema.")
    failures = {key: compare(value, baseline["packages"].get(key, {}), exceptions.get("packages", {}).get(key, []))
                for key, value in packages.items()}
    failures = {key: value for key, value in failures.items() if value}
    report = {"schemaVersion": 1, "packages": packages, "regressions": failures,
              "note": "Syntax metrics are review triggers, not proof of SOLID compliance. Signals are advisory."}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for package_id, items in failures.items():
        for item in items:
            print(f"{package_id}: {item['type']} {item['metric']} {item['actual']} > reviewed limit {item['allowed']}")
    print(f"Architecture regression check: {len(packages)} packages, {sum(map(len, failures.values()))} regressions.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
