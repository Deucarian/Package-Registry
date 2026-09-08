#!/usr/bin/env python3
"""Compare immutable Git revisions, with per-package patches and production clone metrics.

This is a measurement/reporting tool, not an extraction gate. Similar bodies do
not establish shared ownership, and changes in these metrics do not prove SOLID.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

from deucarian_architecture_metrics import collect_types, load_auditor, merge_types

MIN_BODY_TOKENS = 30
PRODUCTION = {"Runtime production", "Editor production"}
METHODS = {"method_declaration", "constructor_declaration"}


def git(root, *arguments, input_bytes=None):
    result = subprocess.run(
        ["git", "-c", "core.longpaths=true", "-C", str(root), *arguments],
        input=input_bytes, capture_output=True, timeout=300)
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def revision_files(root, revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Comparison revisions must be full immutable commit IDs.")
    resolved = git(root, "rev-parse", "--verify", revision + "^{commit}").decode().strip()
    if resolved != revision:
        raise ValueError("Revision is not a commit.")
    paths = git(root, "ls-tree", "-r", "--name-only", "-z", revision).decode("utf-8").split("\0")
    paths = sorted(path for path in paths if path.endswith((".cs", ".asmdef"))
                   or path in {"package.json", "deucarian-package.json"})
    if any("\n" in path or "\r" in path for path in paths):
        raise ValueError("Newlines in source paths are unsupported.")
    requests = "".join(f"{revision}:{path}\n" for path in paths).encode("utf-8")
    stream = io.BytesIO(git(root, "cat-file", "--batch", input_bytes=requests))
    files = {}
    for path in paths:
        header = stream.readline().decode("ascii").split()
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"Source is not a Git blob: {path}")
        content = stream.read(int(header[2]))
        if stream.read(1) != b"\n":
            raise ValueError("Malformed Git batch response.")
        files[path] = content.decode("utf-8-sig").replace("\r\n", "\n")
    return files


def tokens(node, source):
    """Keep punctuation and literals, discard only whitespace and syntax comments."""
    if node.type == "comment":
        return []
    if not node.children:
        return [source[node.start_byte:node.end_byte].decode("utf-8")]
    return [token for child in node.children for token in tokens(child, source)]


def digest(values):
    return hashlib.sha256(json.dumps(values, ensure_ascii=True).encode("utf-8")).hexdigest()


def analyze_sources(repository, files):
    audit = load_auditor()
    analyzer = audit.CSharpSyntaxAnalyzer(authoritative=True)
    governance = json.loads(files.get("deucarian-package.json", "{}"))
    assemblies = [{**json.loads(content), "path": path} for path, content in files.items()
                  if path.endswith(".asmdef")]
    methods = []
    types = {}
    production_files = 0
    production_lines = 0
    for path, content in sorted(files.items()):
        if not path.endswith(".cs") or any(part in audit.SKIP_DIRS for part in Path(path).parts):
            continue
        assembly = audit.owning_asmdef(path, assemblies)
        scope = audit.scope_for(path, assembly, governance)
        if scope not in PRODUCTION or audit.is_generated_file(Path(path), content):
            continue
        source = content.encode("utf-8")
        tree = analyzer.parser.parse(source)
        if tree.root_node.has_error:
            tree = analyzer.parser.parse(audit.parser_source_with_contextual_identifier_recovery(content).encode("utf-8"))
        if tree.root_node.has_error:
            raise ValueError(f"Unparsed production source: {repository}/{path}")
        production_files += 1
        production_lines += len(content.splitlines())
        parsed = audit.ParsedFile(
            repo=repository, package_id=None, repo_root=Path(repository), path=Path(path),
            relative_path=path, scope=scope, assembly=assembly.get("name", "") if assembly else "",
            text=content, governance=governance, generated=False)
        parsed.tree = tree
        merge_types(types, collect_types(parsed))
        for node in audit.walk(tree.root_node):
            if node.type not in METHODS:
                continue
            body = node.child_by_field_name("body")
            if body is None:
                body = next((child for child in node.named_children if child.type == "arrow_expression_clause"), None)
            if body is None:
                continue
            body_tokens = tokens(body, source)
            if len(body_tokens) < MIN_BODY_TOKENS:
                continue
            locals_ = analyzer._local_identifiers(node, source)
            # Structural candidates normalize local/parameter spellings only.
            # Literals, members and called API names remain significant.
            normalized = ["<local>" if token in locals_ else token for token in body_tokens]
            methods.append({
                "repository": repository, "file": path, "line": node.start_point[0] + 1,
                "symbol": audit.child_text(node, "name", source), "tokens": len(body_tokens),
                "exactHash": digest(body_tokens), "localNameNormalizedHash": digest(normalized),
            })
    for row in types.values():
        row["signals"] = sorted(row["signals"])
    return {"productionFiles": production_files, "productionLines": production_lines,
            "types": dict(sorted(types.items())), "methods": methods}


def clone_metrics(methods, key):
    groups = defaultdict(list)
    for method in methods:
        groups[method[key]].append(method)
    clones = []
    redundant_tokens = 0
    for fingerprint, occurrences in sorted(groups.items()):
        if len(occurrences) < 2:
            continue
        counts = [item["tokens"] for item in occurrences]
        redundant = sum(counts) - max(counts)
        redundant_tokens += redundant
        clones.append({"hash": fingerprint, "redundantTokens": redundant,
                       "crossPackage": len({item["repository"] for item in occurrences}) > 1,
                       "occurrences": occurrences})
    eligible_tokens = sum(item["tokens"] for item in methods)
    return {"eligibleMethods": len(methods), "eligibleBodyTokens": eligible_tokens,
            "cloneGroups": len(clones), "crossPackageCloneGroups": sum(row["crossPackage"] for row in clones),
            "redundantBodyTokens": redundant_tokens,
            "redundantBodyTokenPercent": round(100 * redundant_tokens / eligible_tokens, 4) if eligible_tokens else 0,
            "groups": clones}


def summarize(analysis):
    methods = analysis["methods"]
    return {key: value for key, value in analysis.items() if key != "methods"} | {
        "exact": clone_metrics(methods, "exactHash"),
        "localNameNormalized": clone_metrics(methods, "localNameNormalizedHash")}


def write_report(manifest, output):
    entries = manifest["repositories"]
    names = [entry["repository"] for entry in entries]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate repository entries.")
    output.mkdir(parents=True, exist_ok=True)
    (output / "diffs").mkdir(exist_ok=True)
    packages = []
    all_methods = {"before": [], "after": []}
    for entry in sorted(entries, key=lambda row: row["repository"]):
        name = entry["repository"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            raise ValueError("Unsafe repository name.")
        if entry.get("excludedReason"):
            packages.append(dict(entry))
            continue
        root = Path(entry["repositoryRoot"])
        before, after = entry["before"], entry["after"]
        row = {key: entry[key] for key in ("repository", "before", "after")}
        row["note"] = entry.get("note", "")
        row["diffStat"] = git(root, "diff", "--stat", before, after, "--").decode("utf-8")
        row["changedPaths"] = git(root, "diff", "--name-only", "-z", before, after, "--").decode("utf-8").strip("\0").split("\0") if before != after else []
        row["changedPaths"] = [path for path in row["changedPaths"] if path]
        row["patch"] = "diffs/" + name + ".diff"
        (output / row["patch"]).write_bytes(git(root, "diff", "--binary", "--full-index", "--no-ext-diff", before, after, "--"))
        for phase, revision in (("before", before), ("after", after)):
            analysis = analyze_sources(name, revision_files(root, revision))
            all_methods[phase].extend(analysis["methods"])
            row[phase + "Metrics"] = summarize(analysis)
        packages.append(row)
        print(f"Compared {name}: {len(row['changedPaths'])} changed paths", flush=True)
    totals = {phase: {"exact": clone_metrics(methods, "exactHash"),
                      "localNameNormalized": clone_metrics(methods, "localNameNormalizedHash")}
              for phase, methods in all_methods.items()}
    report = {"schemaVersion": 1, "methodology": {
        "minimumBodyTokens": MIN_BODY_TOKENS, "scope": "Production C# methods and constructors only; no generated, sample or test code.",
        "exact": "Identical syntax-leaf tokens, excluding comments and whitespace. Includes intra-package and cross-package clones.",
        "localNameNormalized": "Heuristic candidates with local/parameter spellings normalized; literals and API names retained. Not a semantic-equivalence claim.",
        "percentage": "Redundant body tokens divided by eligible body tokens. Each clone group retains one copy; overlapping report categories are never summed.",
        "limitations": "Not statement-fragment, cross-language or semantic duplication coverage. Clones can be intentional. File moves do not alone remove clones. No metric is a behavior or SOLID score."
    }, "repositories": packages, "portfolio": totals}
    (output / "comparison.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Package refactor comparison", "", manifest.get("description", ""), "",
             "Exact revisions and complete Git patches are provided for every included repository. Games and unavailable baselines are explicitly excluded, not reported as zero changes.", "",
             "## Duplication measurement", "", report["methodology"]["scope"], "", report["methodology"]["percentage"], "",
             "| Measurement | Before | After |", "| --- | ---: | ---: |"]
    for key, title in (("exact", "Exact copied bodies"), ("localNameNormalized", "Local-name-normalized candidates")):
        old, new = totals["before"][key], totals["after"][key]
        lines.append(f"| {title}: redundant eligible tokens | {old['redundantBodyTokens']} ({old['redundantBodyTokenPercent']}%) | {new['redundantBodyTokens']} ({new['redundantBodyTokenPercent']}%) |")
    lines += ["", report["methodology"]["limitations"], "", "## Per-package Git diff", "",
              "| Repository | Before | After | Changed paths | Full patch |", "| --- | --- | --- | ---: | --- |"]
    for row in packages:
        if row.get("excludedReason"):
            lines.append(f"| {row['repository']} | — | — | — | Excluded: {row['excludedReason']} |")
        else:
            lines.append(f"| {row['repository']} | `{row['before']}` | `{row['after']}` | {len(row['changedPaths'])} | [Diff]({(output / row['patch']).as_posix()}) |")
    lines += ["", "Detailed type metrics, clone locations and diff statistics: [comparison.json](" + (output / "comparison.json").as_posix() + ").", ""]
    (output / "COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_report(json.loads(args.manifest.read_text(encoding="utf-8")), args.output.resolve())


if __name__ == "__main__":
    main()
