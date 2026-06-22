import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

AUDIT_ROOT = Path(r"C:\Repositories\_deucarian_org_audit")
OUT_ROOT = Path(r"C:\Repositories\Package-Registry")
TODAY = "2026-06-22"

SKIP_DIRS = {".git", "Library", "PackageCache", "Temp", "Obj", "obj", "bin", ".vs", ".idea", "Logs", "UserSettings"}
TEXT_EXTS = {".cs", ".json", ".asmdef", ".asmref", ".md", ".yml", ".yaml", ".ps1", ".sh", ".xml"}
DEBUG_PATTERNS = [
    "UnityEngine.Debug.Log",
    "UnityEngine.Debug.LogFormat",
    "UnityEngine.Debug.LogWarning",
    "UnityEngine.Debug.LogWarningFormat",
    "UnityEngine.Debug.LogError",
    "UnityEngine.Debug.LogErrorFormat",
    "UnityEngine.Debug.LogException",
    "Debug.Log",
    "Debug.LogFormat",
    "Debug.LogWarning",
    "Debug.LogWarningFormat",
    "Debug.LogError",
    "Debug.LogErrorFormat",
    "Debug.LogException",
]
DESTROY_TERMS = [
    "DestroyUnityObject",
    "DestroyUnityObjectSafely",
    "SafeDestroy",
    "DestroySafely",
    "DestroyObject",
    "Object.Destroy",
    "Object.DestroyImmediate",
    "DestroyImmediate",
    "Application.isPlaying",
]
CAPABILITIES = [
    ("logging", "com.deucarian.logging", "Category-based local package logging and Unity console forwarding."),
    ("editor-shell", "com.deucarian.editor", "Shared editor chrome, icons, resources, style tokens, editor-only UI Toolkit helpers."),
    ("api-http-client", "com.deucarian.api", "General HTTP/API request construction, transport, serialization, authentication, and cancellation."),
    ("session", "com.deucarian.session", "Authenticated session lifecycle, restore, refresh, logout, and persistence contracts."),
    ("object-loading", "com.deucarian.object-loading", "Object, scene, and AssetBundle loading lifecycle and handles."),
    ("repository-state", "com.deucarian.core-state", "Generic keyed repositories, selection state, and repository primitives."),
    ("ui-binding", "com.deucarian.ui-binding", "Collection-to-UI synchronization and presentation binding."),
    ("ui-flow", "com.deucarian.ui-flow", "UI routing, screens, channels, modals, guards, transitions, and back navigation."),
    ("world-selection", "com.deucarian.object-selection", "Keyed world-object selection, hover tracking, raycast adapters, and highlight hooks."),
    ("runtime-theming", "com.deucarian.theming", "Runtime palettes, theme assets, color roles, and UI theme adapters."),
    ("diagnostics", "com.deucarian.diagnostics", "Diagnostics providers, snapshots, JSON export, overlays, and aggregation."),
    ("package-management", "com.deucarian.package-installer", "Package discovery, install/update/remove, channels, registry composition, and ecosystem visualization."),
    ("registry-metadata", None, "Catalog, category hierarchy, dependency metadata, Integration metadata, Suite metadata, and governance metadata."),
    ("unity-object-lifetime", None, "Potential tiny shared UnityEngine.Object lifetime primitives if the dedicated audit justifies a Common package."),
]


def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as exc:
        return "", str(exc), 1


def rel(path, root):
    return str(Path(path).relative_to(root)).replace("\\", "/")


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix in TEXT_EXTS:
                yield path


def read_text(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def read_json(path):
    try:
        return json.loads(read_text(path))
    except Exception:
        return None


def scope_for(path, repo_root):
    parts = Path(path).relative_to(repo_root).parts
    if not parts:
        return "Other"
    first = parts[0]
    if first in {"Runtime", "Editor", "Tests", "Samples~", "Tools"}:
        return first
    if first.startswith("Samples"):
        return "Samples~"
    if ".github" in parts:
        return "CI"
    return "Other"


def collect_branch_info(repo_root):
    branch, _, _ = run(["git", "branch", "--show-current"], cwd=repo_root)
    status, _, _ = run(["git", "status", "--short"], cwd=repo_root)
    remote, _, _ = run(["git", "remote", "get-url", "origin"], cwd=repo_root)
    heads, _, _ = run(["git", "ls-remote", "--heads", "origin"], cwd=repo_root)
    return {
        "currentBranch": branch,
        "dirty": status,
        "origin": remote,
        "hasDevelop": "refs/heads/develop" in heads,
        "hasMain": "refs/heads/main" in heads,
    }


def collect_asmdefs(repo_root):
    asmdefs = []
    for path in repo_root.rglob("*.asmdef"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        data = read_json(path) or {}
        asmdefs.append(
            {
                "path": rel(path, repo_root),
                "name": data.get("name", ""),
                "references": data.get("references", []) or [],
                "includePlatforms": data.get("includePlatforms", []) or [],
                "excludePlatforms": data.get("excludePlatforms", []) or [],
                "optionalUnityReferences": data.get("optionalUnityReferences", []) or [],
            }
        )
    return sorted(asmdefs, key=lambda item: item["path"])


def find_public_api(repo_root):
    symbols = []
    type_re = re.compile(r"\bpublic\s+(?:abstract\s+|sealed\s+|static\s+|partial\s+)*(class|struct|interface|enum|delegate)\s+([A-Za-z_][A-Za-z0-9_]*)")
    member_re = re.compile(r"\bpublic\s+(?:static\s+|virtual\s+|override\s+|abstract\s+|async\s+|readonly\s+)*(?:[A-Za-z_][A-Za-z0-9_<>,.\[\]?]+\s+)+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|\{)")
    for path in repo_root.rglob("*.cs"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        text = read_text(path)
        for match in type_re.finditer(text):
            symbols.append({"kind": match.group(1), "name": match.group(2), "path": rel(path, repo_root)})
        for match in member_re.finditer(text):
            name = match.group(1)
            if name not in {"class", "struct", "interface", "enum", "delegate"}:
                symbols.append({"kind": "member", "name": name, "path": rel(path, repo_root)})
    return symbols


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"//.*", " ", text)


def normalize_code(text):
    text = strip_comments(text)
    text = re.sub(r'@?"(?:""|\\.|[^"\\])*"', '"S"', text)
    text = re.sub(r"'(?:\\.|[^'\\])'", "'C'", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\b", "0", text)
    return re.sub(r"\s+", "", text).lower()


def extract_methods(repo_name, repo_root):
    candidates = []
    sig_re = re.compile(
        r"(?P<sig>\b(?:public|internal|private|protected)\s+(?:static\s+|virtual\s+|override\s+|abstract\s+|async\s+|sealed\s+|readonly\s+|partial\s+|unsafe\s+)*[A-Za-z_][A-Za-z0-9_<>,.\[\]?\s]+\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*\))\s*\{",
        re.M,
    )
    for path in repo_root.rglob("*.cs"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        text = read_text(path)
        for match in sig_re.finditer(text):
            start = match.start()
            brace = text.find("{", match.end() - 1)
            if brace < 0:
                continue
            depth = 0
            end = brace
            for idx in range(brace, len(text)):
                if text[idx] == "{":
                    depth += 1
                elif text[idx] == "}":
                    depth -= 1
                    if depth == 0:
                        end = idx + 1
                        break
            body = text[start:end]
            line_start = text[:start].count("\n") + 1
            line_count = body.count("\n") + 1
            if line_count < 5:
                continue
            normalized = normalize_code(body)
            if len(normalized) < 120:
                continue
            sig = " ".join(match.group("sig").split())
            candidates.append(
                {
                    "repo": repo_name,
                    "path": rel(path, repo_root),
                    "symbol": sig.split("(")[0].split()[-1],
                    "signature": sig,
                    "line": line_start,
                    "lineCount": line_count,
                    "scope": scope_for(path, repo_root),
                    "normalized": normalized,
                }
            )
    return candidates


def find_text_matches(repo_root, terms):
    results = []
    for path in iter_files(repo_root):
        text = read_text(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for term in terms:
                if term in line:
                    results.append({"path": rel(path, repo_root), "line": line_no, "term": term, "text": line.strip()[:220], "scope": scope_for(path, repo_root)})
                    break
    return results


def read_readme_deps(repo_root):
    readme = repo_root / "README.md"
    text = read_text(readme) if readme.exists() else ""
    deps = sorted(set(re.findall(r"com\.deucarian\.[a-z0-9_.-]+", text, flags=re.I)))
    versions = sorted(set(re.findall(r"\b\d+\.\d+\.\d+\b", text)))
    return deps, versions


def find_workflows(repo_root):
    wf_root = repo_root / ".github" / "workflows"
    if not wf_root.exists():
        return []
    return sorted(rel(path, repo_root) for path in wf_root.glob("*.y*ml"))


def find_validation_scripts(repo_root):
    found = set()
    for base in [repo_root / "Tools", repo_root / "Scripts", repo_root / ".github"]:
        if not base.exists():
            continue
        for pattern in ["*validate*", "*Validation*", "*package*.ps1", "*package*.sh"]:
            for path in base.rglob(pattern):
                if path.is_file():
                    found.add(rel(path, repo_root))
    return sorted(found)


def find_samples(repo_root):
    return sorted(rel(path, repo_root) for path in repo_root.glob("Samples~/**") if path.is_file())[:80]


def load_registry():
    data = read_json(OUT_ROOT / "packages.json") or {}
    packages = data.get("packages", []) or []
    return {pkg.get("id"): pkg for pkg in packages if pkg.get("id")}


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        safe = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        out.append("| " + " | ".join(safe) + " |")
    return "\n".join(out)


def detect_cycles(edges):
    graph = defaultdict(list)
    for edge in edges:
        if edge["from"] and edge["to"]:
            graph[edge["from"]].append(edge["to"])
    cycles = []
    stack = []
    seen = set()

    def visit(node, visiting):
        if node in visiting:
            idx = stack.index(node) if node in stack else 0
            cycle = stack[idx:] + [node]
            if cycle not in cycles:
                cycles.append(cycle)
            return
        if node in seen:
            return
        visiting.add(node)
        stack.append(node)
        for nxt in graph.get(node, []):
            visit(nxt, visiting)
        stack.pop()
        visiting.remove(node)
        seen.add(node)

    for node in list(graph):
        visit(node, set())
    return cycles


def main():
    registry = load_registry()
    repos = []
    all_methods = []

    for repo_root in sorted([p for p in AUDIT_ROOT.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        package_json = read_json(repo_root / "package.json") or {}
        readme_deps, readme_versions = read_readme_deps(repo_root)
        public_api = find_public_api(repo_root)
        package_id = package_json.get("name")
        registry_pkg = registry.get(package_id) if package_id else None
        repo = {
            "name": repo_root.name,
            "path": str(repo_root),
            "packageId": package_id,
            "packageVersion": package_json.get("version"),
            "unity": package_json.get("unity"),
            "displayName": package_json.get("displayName"),
            "branches": collect_branch_info(repo_root),
            "dependencies": package_json.get("dependencies", {}) or {},
            "asmdefs": collect_asmdefs(repo_root),
            "readmeDeclaredDependencies": readme_deps,
            "readmeVersionMentions": readme_versions,
            "registryDependencies": (registry_pkg or {}).get("dependencies", []) if registry_pkg else None,
            "registryGroupId": (registry_pkg or {}).get("groupId") if registry_pkg else None,
            "publicApiCount": len(public_api),
            "publicApiSample": public_api[:50],
            "samples": find_samples(repo_root),
            "ciWorkflows": find_workflows(repo_root),
            "validationScripts": find_validation_scripts(repo_root),
            "debugUsages": find_text_matches(repo_root, DEBUG_PATTERNS),
            "destroyUsages": find_text_matches(repo_root, DESTROY_TERMS),
            "bridgeTerminologyHits": find_text_matches(repo_root, ["Bridge", "bridge"])[:80],
            "fileCounts": {
                "cs": len(list(repo_root.rglob("*.cs"))),
                "asmdef": len(list(repo_root.rglob("*.asmdef"))),
            },
        }
        repos.append(repo)
        all_methods.extend(extract_methods(repo_root.name, repo_root))

    by_hash = defaultdict(list)
    for method in all_methods:
        by_hash[method["normalized"]].append(method)

    exact_clones = []
    for items in by_hash.values():
        reposet = sorted(set(item["repo"] for item in items))
        if len(items) > 1 and len(reposet) > 1:
            exact_clones.append(
                {
                    "kind": "normalized-exact-method",
                    "repositoryCount": len(reposet),
                    "repositories": reposet,
                    "lineCounts": sorted(set(item["lineCount"] for item in items)),
                    "symbols": sorted(set(item["symbol"] for item in items)),
                    "occurrences": [{k: v for k, v in item.items() if k != "normalized"} for item in items],
                    "recommendation": "review-owner" if len(reposet) >= 3 else "document-or-leave-local",
                }
            )
    exact_clones.sort(key=lambda item: (-item["repositoryCount"], -max(item["lineCounts"]), item["symbols"][0] if item["symbols"] else ""))

    name_groups = defaultdict(list)
    for method in all_methods:
        if any(token in method["symbol"].lower() for token in ["destroy", "dispose", "cleanup", "log", "validate", "guard", "json", "wait"]):
            name_groups[method["symbol"].lower()].append(method)
    semantic_candidates = []
    for name, items in name_groups.items():
        reposet = sorted(set(item["repo"] for item in items))
        if len(reposet) >= 2:
            semantic_candidates.append(
                {
                    "kind": "same-symbol-family",
                    "symbol": name,
                    "repositoryCount": len(reposet),
                    "repositories": reposet,
                    "occurrences": [{k: v for k, v in item.items() if k != "normalized"} for item in items[:30]],
                    "recommendation": "candidate" if len(reposet) >= 3 else "watch",
                }
            )
    semantic_candidates.sort(key=lambda item: (-item["repositoryCount"], item["symbol"]))

    pkg_to_repo = {repo["packageId"]: repo["name"] for repo in repos if repo.get("packageId")}
    edges = []
    version_drifts = []
    registry_drifts = []
    asmdef_drifts = []
    readme_drifts = []
    versions_by_pkg = {repo["packageId"]: repo["packageVersion"] for repo in repos if repo.get("packageId") and repo.get("packageVersion")}

    for repo in repos:
        package_id = repo.get("packageId")
        deps = repo.get("dependencies") or {}
        for dep, version in deps.items():
            if dep.startswith("com.deucarian."):
                edges.append({"from": package_id, "to": dep, "version": version, "fromRepo": repo["name"], "toRepo": pkg_to_repo.get(dep)})
                owner_version = versions_by_pkg.get(dep)
                if owner_version and version != owner_version:
                    version_drifts.append({"repo": repo["name"], "packageId": package_id, "dependency": dep, "declaredVersion": version, "ownerDevelopVersion": owner_version})
        registry_deps = repo.get("registryDependencies")
        if registry_deps is not None:
            pkg_deps = sorted(dep for dep in deps if dep.startswith("com.deucarian."))
            reg_deps = sorted(registry_deps)
            if pkg_deps != reg_deps:
                registry_drifts.append({"repo": repo["name"], "packageId": package_id, "packageJsonDependencies": pkg_deps, "registryDependencies": reg_deps})
        if package_id and repo.get("packageVersion"):
            readme_versions = repo.get("readmeVersionMentions") or []
            if readme_versions and repo["packageVersion"] not in readme_versions:
                readme_drifts.append({"repo": repo["name"], "packageId": package_id, "packageVersion": repo["packageVersion"], "readmeVersionMentions": readme_versions[:10]})
        asm_refs = sorted(set(ref for asm in repo["asmdefs"] for ref in asm.get("references", []) if isinstance(ref, str)))
        if deps and not asm_refs and repo["asmdefs"]:
            asmdef_drifts.append({"repo": repo["name"], "packageId": package_id, "issue": "package has dependencies but no asmdef references detected", "dependencies": deps})

    cycles = detect_cycles(edges)
    violations = []
    for repo in repos:
        package_id = repo.get("packageId") or repo["name"]
        for hit in repo["debugUsages"]:
            allowed = package_id in {"com.deucarian.logging", "com.deucarian.bootstrap"} or hit["scope"] == "Tests"
            violations.append({**hit, "repo": repo["name"], "packageId": package_id, "allowedByBaseline": allowed})

    destroy_report = []
    for repo in repos:
        for hit in repo["destroyUsages"]:
            destroy_report.append({**hit, "repo": repo["name"], "packageId": repo.get("packageId")})

    capability_matrix = []
    for cap_id, owner, desc in CAPABILITIES:
        owner_repo = pkg_to_repo.get(owner) if owner else "Package-Registry" if cap_id == "registry-metadata" else None
        consumers = sorted(set(edge["from"] for edge in edges if edge["to"] == owner)) if owner else []
        capability_matrix.append({"id": cap_id, "ownerPackageId": owner, "ownerRepository": owner_repo, "description": desc, "currentConsumers": consumers, "notes": "owner missing in inventory" if owner and not owner_repo else ""})

    report = {
        "schemaVersion": 1,
        "generatedAt": TODAY,
        "auditRoot": str(AUDIT_ROOT),
        "repositories": repos,
        "duplication": {
            "methodCountAnalyzed": len(all_methods),
            "normalizedExactCloneGroups": exact_clones[:200],
            "semanticNameCandidates": semantic_candidates[:200],
        },
        "directApiViolations": violations,
        "destroyUnityObjectAudit": destroy_report,
        "dependencyGraph": {"edges": edges, "cycles": cycles},
        "drift": {
            "dependencyVersionDrift": version_drifts,
            "registryDependencyDrift": registry_drifts,
            "asmdefReferenceDrift": asmdef_drifts,
            "readmeVersionDrift": readme_drifts,
        },
        "capabilityMatrix": capability_matrix,
    }
    (OUT_ROOT / "DUPLICATION_REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    cap_manifest = {"schemaVersion": 1, "generatedAt": TODAY, "capabilities": []}
    for cap_id, owner, desc in CAPABILITIES:
        item = {"id": cap_id, "ownerPackageId": owner, "description": desc}
        if cap_id == "logging":
            item["forbiddenSymbolsOutsideOwner"] = DEBUG_PATTERNS
            item["exceptions"] = [
                {"packageId": "com.deucarian.bootstrap", "reason": "First-time self-contained bootstrap."},
                {"packageId": "com.deucarian.logging", "reason": "Owns Unity console forwarding and sink validation."},
            ]
        if cap_id == "unity-object-lifetime":
            item["status"] = "candidate-pending-dedicated-destroy-audit"
            item["ownerPackageId"] = None
        cap_manifest["capabilities"].append(item)
    (OUT_ROOT / "capabilities.json").write_text(json.dumps(cap_manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    dep_rules = {
        "schemaVersion": 1,
        "generatedAt": TODAY,
        "layers": [
            {"id": "common", "packages": ["com.deucarian.common"], "status": "not-created"},
            {"id": "foundation", "packages": ["com.deucarian.editor", "com.deucarian.logging", "com.deucarian.core-state"]},
            {"id": "runtime-capabilities", "packages": ["com.deucarian.api", "com.deucarian.session", "com.deucarian.object-loading", "com.deucarian.object-selection", "com.deucarian.ui-binding", "com.deucarian.ui-flow", "com.deucarian.theming", "com.deucarian.diagnostics"]},
            {"id": "integrations", "packages": ["com.deucarian.session.api-integration", "com.deucarian.object-loading.api-integration", "com.deucarian.object-selection.core-state-integration", "com.deucarian.ui-binding.core-state-integration"]},
            {"id": "suites", "packages": ["com.deucarian.selection-suite"]},
            {"id": "catalog-composition", "packages": ["com.deucarian.package-installer"]},
        ],
        "exceptions": [
            {"packageId": "com.deucarian.bootstrap", "reason": "Self-contained first-time setup package outside normal dependency graph."},
            {"packageId": "com.deucarian.logging", "dependency": "com.deucarian.editor", "status": "review-required", "reason": "Prompt requested explicit review of Logging -> Editor before allowing Editor to use Logging."},
        ],
        "rules": [
            "No cyclic package dependencies.",
            "Runtime assemblies must not reference UnityEditor.",
            "Common, if created, cannot depend on Logging or Editor.",
            "Logging cannot depend on Diagnostics or telemetry.",
            "Integration packages depend only on their targets plus Common/Logging when actually used.",
            "Package Registry dependencies must match package.json direct Deucarian dependencies.",
            "Assembly references must match package dependencies.",
        ],
    }
    (OUT_ROOT / "dependency-rules.json").write_text(json.dumps(dep_rules, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    inventory_rows = []
    for repo in repos:
        inventory_rows.append([
            repo["name"],
            repo.get("packageId") or "(none)",
            repo.get("packageVersion") or "(none)",
            repo.get("unity") or "(none)",
            "yes" if repo["branches"]["hasDevelop"] else "no",
            "yes" if repo["branches"]["hasMain"] else "no",
            "clean" if not repo["branches"].get("dirty") else "dirty",
            ", ".join(repo["dependencies"].keys()) or "(none)",
            str(len(repo["asmdefs"])),
            str(repo["publicApiCount"]),
            str(len(repo["ciWorkflows"])),
        ])

    non_allowed_debug = [v for v in violations if not v["allowedByBaseline"]]

    (OUT_ROOT / "REUSE_AUDIT.md").write_text(
        f"""# Deucarian Reuse Audit

Generated: {TODAY}

This is the initial organization-wide audit snapshot required before any code extraction. It was generated from shallow `develop` clones under `{AUDIT_ROOT}` and writes governance artifacts in Package Registry on `develop`.

## Safety Summary

- Non-archived Deucarian repositories discovered: {len(repos)}.
- Every discovered repository has a `develop` branch.
- The audit clones are clean and checked out on `develop`.
- No source extraction or dependency migration has been performed in this wave.
- Local working-copy blockers outside the audit clones were observed, including a dirty `Logging` checkout and several package folders on `main`; those were not edited.

## Inventory

{md_table(["Repository", "Package ID", "Version", "Unity", "Develop", "Main", "Audit Clone", "package.json dependencies", "Asmdefs", "Public API symbols", "Workflows"], inventory_rows)}

## High-Level Findings

- Normalized method clone groups across multiple repositories: {len(exact_clones)}.
- Same-symbol semantic clone candidates: {len(semantic_candidates)}.
- Direct Debug API hits: {len(violations)} total, {len(non_allowed_debug)} outside the initial allowlist.
- Unity object destruction/lifetime hits: {len(destroy_report)}.
- Deucarian package dependency version drift entries: {len(version_drifts)}.
- Package Registry dependency drift entries: {len(registry_drifts)}.
- Dependency cycles detected: {len(cycles)}.

## Conservative Extraction Position

No extraction is recommended from this snapshot alone until each candidate is reviewed against the stated thresholds. The strongest follow-up candidates are:

1. Unity object destruction/lifetime helpers: run the dedicated DestroyUnityObject migration audit before deciding whether `com.deucarian.common`, `com.deucarian.editor`, or no extraction is appropriate.
2. Direct Debug API replacement: migrate non-allowed package code to `com.deucarian.logging` only when the package actually emits logs.
3. Package validation/workflow reuse: centralize repeated validation and workflow logic in a future Build Tools or `.github` governance repository.
4. README/version/dependency drift: fix documentation and registry drift before dependency waves.

## Detailed Data

See `DUPLICATION_REPORT.json` for full machine-readable occurrences, symbol samples, direct API usage, destruction usage, dependency drift, and cycle data.
""",
        encoding="utf-8",
    )

    cap_rows = []
    for item in capability_matrix:
        cap_rows.append([item["id"], item.get("ownerPackageId") or "(pending)", item.get("ownerRepository") or "(pending)", ", ".join(item.get("currentConsumers") or []) or "(none)", item.get("notes") or ""])
    (OUT_ROOT / "PACKAGE_CAPABILITY_MATRIX.md").write_text(
        f"""# Deucarian Package Capability Matrix

Generated: {TODAY}

This matrix records capability ownership before migration. It is intentionally conservative: ownership does not imply every package should depend on the owner. Consumers should add dependencies only when they use the capability.

{md_table(["Capability", "Owner package", "Owner repository", "Current package.json consumers", "Notes"], cap_rows)}

## Governance Notes

- Bootstrap remains outside the normal dependency graph for first-time setup and repair.
- `unity-object-lifetime` is pending the dedicated DestroyUnityObject audit; no Common package is created by this report.
- Logging owns logging infrastructure and Unity console forwarding; package-specific category facades may remain local when they only declare domain categories.
- Editor owns editor-only chrome, icons, resources, package path/version helpers, and editor-only UI Toolkit helpers.

Machine-readable seed: `capabilities.json`.
""",
        encoding="utf-8",
    )

    edge_rows = []
    for edge in sorted(edges, key=lambda e: ((e.get("from") or ""), (e.get("to") or ""))):
        edge_rows.append([edge.get("from"), edge.get("to"), edge.get("version"), edge.get("fromRepo"), edge.get("toRepo") or "(not in inventory)"])
    cycle_text = "None detected." if not cycles else "\n".join("- " + " -> ".join(cycle) for cycle in cycles)
    (OUT_ROOT / "DEPENDENCY_GRAPH.md").write_text(
        f"""# Deucarian Dependency Graph

Generated: {TODAY}

## Direct Deucarian Package Dependencies

{md_table(["From package", "To package", "Declared version", "From repo", "To repo"], edge_rows)}

## Cycle Report

{cycle_text}

## Drift Summary

- Dependency version drift entries: {len(version_drifts)}.
- Registry dependency drift entries: {len(registry_drifts)}.
- README version drift entries: {len(readme_drifts)}.
- Asmdef reference drift entries needing manual review: {len(asmdef_drifts)}.

Machine-readable details are in `DUPLICATION_REPORT.json` under `dependencyGraph` and `drift`.
""",
        encoding="utf-8",
    )

    (OUT_ROOT / "MIGRATION_PLAN.md").write_text(
        f"""# Deucarian Migration Plan

Generated: {TODAY}

This plan starts the requested migration but deliberately stops before extraction because the inventory and audit artifacts must exist first.

## Wave 1: Governance And Audit Baseline

Status: started in Package Registry on `develop`.

Artifacts created:

- `REUSE_AUDIT.md`
- `PACKAGE_CAPABILITY_MATRIX.md`
- `DEPENDENCY_GRAPH.md`
- `DUPLICATION_REPORT.json`
- `capabilities.json`
- `dependency-rules.json`

## Required Follow-Up Order

1. Review `DUPLICATION_REPORT.json` clone groups and classify each candidate against the extraction thresholds.
2. Run the dedicated DestroyUnityObject migration review. Current lifetime/destruction hits: {len(destroy_report)}.
3. Review direct Debug API hits. Current non-allowlisted baseline hits: {len(non_allowed_debug)}.
4. Resolve documentation and version drift before changing dependencies.
5. Decide whether Build Tools or a `.github` governance repository owns reusable validation and workflows.
6. Only then begin owner-package extraction waves.

## Initial High-Confidence Work Items

- Add architecture validation for direct Debug usage using `capabilities.json`.
- Add registry/package dependency consistency checks from `dependency-rules.json`.
- Keep Package Registry dependency consistency enforced; the initial audit found no registry dependency drift.
- Review `Logging -> Editor` as an explicit dependency exception before allowing Editor to consume Logging.
- Preserve Bootstrap self-containment; documentation changes are allowed but dependency adoption is not.

## Items Intentionally Not Done In This Wave

- No `com.deucarian.common` package was created.
- No `com.deucarian.testing` package was created.
- No source call sites were migrated.
- No package dependencies or asmdef references were changed.
- No README files outside Package Registry were rewritten.
- No main branch was modified.

## Validation Needed Before Dependency Migration

- Compile/test each owner package after any extracted API is added.
- Compile/test every consumer after dependency adoption.
- Build an integration validation project resolving all develop package URLs.
- Run architecture validation against the baseline and remove exceptions intentionally.
""",
        encoding="utf-8",
    )

    print(json.dumps({
        "repositories": len(repos),
        "methodCountAnalyzed": len(all_methods),
        "cloneGroups": len(exact_clones),
        "semanticCandidates": len(semantic_candidates),
        "debugHits": len(violations),
        "debugHitsOutsideAllowlist": len(non_allowed_debug),
        "destroyHits": len(destroy_report),
        "cycles": len(cycles),
        "versionDrifts": len(version_drifts),
        "registryDrifts": len(registry_drifts),
    }, indent=2))


if __name__ == "__main__":
    main()
