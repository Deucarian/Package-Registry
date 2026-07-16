# Dependency Rules

`dependency-rules.json` is authoritative. These notes explain the practical package layering rules.

## Layering

1. `com.deucarian.common`
   - Lowest-level runtime primitive package.
   - No Logging, Editor, JSON, networking, diagnostics, state, UI, or domain dependencies.
2. Foundation packages
   - `com.deucarian.editor`
   - `com.deucarian.logging`
   - `com.deucarian.core-state`
3. Editor tooling packages
   - `com.deucarian.build-pipeline`
   - Depend on foundation packages and remain editor-only.
4. Runtime capability packages
   - API, Session, Object Loading, Object Selection, UI Binding, UI Flow, Theming, Diagnostics.
5. Integration packages
   - Adapters between declared target packages.
6. Suite packages
   - Dependency bundles and samples.
7. Package Installer
   - Installer/composition UI and registry channel handling.

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
- Optional companions are recommendations only. They must not imply install order or auto-install behavior.
- Optional diagnostics hooks should use version-defined asmdefs or guarded code.
- Integration package dependencies are hard requirements for that Integration package.

## Bootstrap Exception

Bootstrap is intentionally self-contained for first-time setup and repair. It may include minimal local fallback/setup code and must not depend on the normal Deucarian package graph.

## Cycles

Dependency cycles are forbidden. If a useful capability would create a cycle, stop and update the architecture decision in Package Registry before coding.
