# Dependency Rules

`dependency-rules.json` is authoritative. These notes explain the practical package layering rules.

## Dependency ranks

- Every catalog package appears in exactly one machine-readable rank in `dependency-rules.json`.
- Rank 0 contains dependency-free portfolio foundations, including Common.
- Every dependency must point to a strictly lower rank; this makes cycles and sideways coupling invalid by construction.
- Ranks describe dependency depth, not product taxonomy. Functional placement comes from `groupId`, while Integration, Suite, Template, Tool, and Library behavior comes from `kind`.
- Integration dependencies contain every `integrationTargets` entry plus only foundations the adapter actually uses.
- Suite dependencies exactly equal `suiteMembers`; Suite repositories remain implementation-free and own composition samples.
- Template assemblies and samples declare direct dependencies instead of relying on Suite transitivity.

## Dependency Checklist

Before adding a dependency:

1. Confirm the target package owns the capability being used.
2. Confirm the dependency is used by production, editor, sample, or test code.
3. Confirm asmdef references match `package.json`.
4. Update `deucarian-package.json`.
5. Update `packages.json` if the dependency is Installer-visible and required.
6. Update Package Installer and Bootstrap fallback catalogs when required.
7. Propagate exact versions without guessing.
8. Run shared validation and audit checks.

## Required Vs Optional

- Hard dependencies go in Unity `package.json`, registry `dependencies`, asmdef references, and package config.
- `recommendedWith` is a non-structural recommendation only. It does not imply install order or auto-install behavior.
- Reverse Integration and Suite relationships are derived from `integrationTargets` and `suiteMembers`.
- Optional diagnostics hooks should use version-defined asmdefs or guarded code.
- Integration package dependencies are hard requirements for that Integration package.

## Bootstrap Exception

Bootstrap is intentionally self-contained for first-time setup and repair. It may include minimal local fallback/setup code and must not depend on the normal Deucarian package graph.

## Cycles

Dependency cycles are forbidden. If a useful capability would create a cycle, stop and update the architecture decision in Package Registry before coding.
