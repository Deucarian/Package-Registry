# Deucarian Architecture Rules

This repository is the governance source for Deucarian Unity package metadata, capability ownership, dependency rules, and validation tooling.

## Governance Sources

- `packages.json` defines installable packages, Installer-visible dependencies, Integration metadata, Suite metadata, and category/group placement.
- `capabilities.json` defines which package owns each reusable capability.
- `dependency-rules.json` defines the allowed package layering model.
- `DISTRIBUTION_POLICY.md` defines active stable/development Git channels.
- `RELEASE_POLICY.md` defines deferred npm/tag/release workflow policy.
- `Tools/deucarian_package_validator.py` enforces package manifests, asmdefs, documentation, audit policy, and registry/catalog consistency.
- Generated audit artifacts (`*_AUDIT.json`, `DUPLICATION_REPORT.json`) describe current organization state and must stay in sync.

## Distribution And Release

- `main` is the stable Git distribution channel through registry `stableUrl` values.
- `develop` is the development Git distribution channel through registry `developmentUrl` values.
- npm/scoped-registry publication is deferred and must not run during branch promotion.
- Git tags and GitHub releases are deferred and must not be created automatically.
- Future npm, tag, or GitHub release publication requires a separate deliberate release wave.

## Package Roles

- Bootstrap owns first-time setup and repair only. It is self-contained by design and must not depend on Editor, Logging, Common, or Package Installer.
- Common owns tiny dependency-free runtime primitives only. It currently exposes only `Deucarian.Common.UnityObjectUtility.DestroySafely(UnityEngine.Object target)`.
- Logging owns the package logging facade and Unity console sink. Direct `UnityEngine.Debug` calls are allowed only in the approved Logging sink/fallback locations.
- Editor owns shared editor chrome, icons, editor resources, and editor-only UI Toolkit helpers. It must not own runtime theming or package installation logic.
- Package Registry owns metadata, capability ownership, dependency rules, and audit/validation tools. It must not contain runtime package code or editor UI implementation.
- Package Installer owns package installation, registry channel selection, dependency-first installation, and package-specific ecosystem visualization. It must not become a generic graph or UI framework.
- Integration packages own adapter code between declared target packages only. They must not duplicate target-package logic or introduce independent frameworks.
- Suite packages own dependency composition, samples, and installable bundles only. They must not duplicate implementation logic.

## Reuse Before Extraction

Before adding a helper or local utility:

1. Search the current repository.
2. Search all Deucarian repositories.
3. Check `capabilities.json`.
4. Use the package that owns the capability.
5. Add a package dependency only when production/editor/sample code directly uses that capability.
6. Do not copy helpers between repositories.
7. Do not create a new shared package without audit evidence.
8. Do not add unrelated APIs to Common.

## Logging

- Production code outside Logging should use the package-owned logging facade.
- Direct Unity Debug calls are forbidden outside approved Logging implementation points.
- Bootstrap may remain self-contained and local for first-time setup.
- Diagnostics may observe/report diagnostics locally, but it does not own Logging.

## Common

- Common must stay small, runtime-only, dependency-free, and evidence-driven.
- Common must not grow into a generic utility bucket.
- Do not add logging, editor, JSON, networking, diagnostics, state, UI, or domain helpers to Common.
- Production Unity object cleanup outside Common should call `UnityObjectUtility.DestroySafely`.
- Test fixture teardown may use `DestroyImmediate` directly.

## Diagnostics

- Diagnostics owns local snapshots, providers, export, overlays, and diagnostics views.
- Diagnostics does not own telemetry/uploading.
- Optional diagnostics integration from other packages must remain optional/version-defined unless a hard dependency is explicitly approved.

## Adding A Capability

1. Prove repeated production use or clear package ownership pressure with audit data.
2. Decide whether an existing package owns the capability.
3. Update `capabilities.json`.
4. Update `dependency-rules.json` only if layering changes.
5. Update affected `deucarian-package.json` files.
6. Update `packages.json` and fallback catalogs only when package dependencies or Installer-visible metadata change.
7. Run shared validation and the authoritative audit.
