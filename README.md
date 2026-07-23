# Deucarian Package Registry

## Overview

This repository contains the package registry for the Deucarian Package Installer.

The installer reads `packages.json` from the public raw GitHub URL:

https://raw.githubusercontent.com/Deucarian/Package-Registry/main/packages.json

The registry is intentionally manual and explicit. Adding a new package means adding a new entry to `packages.json`.

Auto-discovery is intentionally avoided because it creates ambiguity around archived repositories, naming, package IDs, dependency resolution, and GitHub rate limits.

## Usage

Update `packages.json` when a package is added, removed, or gains an installer-visible dependency. Keep the Package Installer bundled fallback registry in sync when bootstrap behavior depends on the package list.

Project both consumer fallback catalogs from the canonical registry instead of editing them by hand:

```powershell
python Tools/project_package_catalogs.py --installer-root ../Package-Installer --bootstrap-root ../Bootstrap
python Tools/project_package_catalogs.py --installer-root ../Package-Installer --bootstrap-root ../Bootstrap --check
```

Write mode is the default. It writes the full canonical catalog to Package Installer and writes only the dependency-first closure needed to install `com.deucarian.package-installer` to Bootstrap. That Bootstrap catalog contains Editor, Logging, and Package Installer and deliberately omits mutable `stableVersion` and `developmentVersion` claims. `--check` compares parsed JSON semantically and exits non-zero when either consumer catalog has drifted.

Each consumer can pass only its own root. Consumer CI can use the reusable check without checking out or depending on the other consumer repository:

```yaml
jobs:
  check-catalog:
    uses: Deucarian/Package-Registry/.github/workflows/deucarian-catalog-projection-check.yml@develop
    with:
      catalog: installer # use bootstrap in the Bootstrap repository
```

## Distribution Policy

Current stable distribution uses Git URLs pinned to `#main`. Current development distribution uses Git URLs pinned to `#develop`.

npm/scoped-registry publishing, Git tags, and GitHub releases are deferred for now. Use Git URLs until a separate deliberate release wave enables another channel.

Package Registry is the source of truth for `stableUrl` and `developmentUrl`. Package Installer consumes the registry and its bundled fallback catalog.

## Architecture / Contributor Notes

- [ARCHITECTURE.md](ARCHITECTURE.md) is the single canonical architecture
  standard inherited by every cataloged Deucarian package through shared
  validation; the package-agent template links here instead of maintaining
  local copies.
- [CAPABILITY_OWNERSHIP.md](CAPABILITY_OWNERSHIP.md) lists owner packages for shared capabilities.
- [DISTRIBUTION_POLICY.md](DISTRIBUTION_POLICY.md) defines active Git-only package distribution.
- [RELEASE_POLICY.md](RELEASE_POLICY.md) defines deferred npm/tag/release policy and workflow requirements.
- [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md) explains allowed dependency layering.
- [Documentation~/START_HERE.md](Documentation~/START_HERE.md) gives the package ecosystem entry point for developers and designers.
- [Documentation~/ECOSYSTEM_POLISH_AUDIT.md](Documentation~/ECOSYSTEM_POLISH_AUDIT.md) tracks the current ecosystem polish pass.
- [Documentation~/BRANCH_CHANNEL_CLEANUP.md](Documentation~/BRANCH_CHANNEL_CLEANUP.md) lists default-branch cleanup actions requiring GitHub admin permissions.
- [CONTRIBUTING.md](CONTRIBUTING.md) describes validation and contribution workflow.
- [AGENTS.md](AGENTS.md) gives Codex and automation-specific repository guidance.

## Registry fields

- `schemaVersion`: Registry schema version used by the installer.
- `updatedAt`: Date this registry was last manually updated.
- `packages`: List of package entries available to the installer.
- `id`: Unique Unity package ID.
- `displayName`: Human-readable package name.
- `kind`: Canonical artifact kind: `Library`, `Tool`, `Integration`, `Suite`, or `Template`.
- `groupId`: Required functional-domain group used for navigation and ordering.
- `category`, `type`, `ecosystemGroup`: One-release compatibility projections for older Installer and Bootstrap versions. New consumers must not use them as canonical metadata.
- `description`: Short explanation of what the package provides.
- `stableUrl`: GitHub HTTPS Unity Package Manager URL for the stable install channel. Mature packages normally use `#main`; pre-stable bootstrap packages may temporarily point this at a verified development branch when `main` does not exist yet.
- `developmentUrl`: GitHub HTTPS Unity Package Manager URL for the development install channel.
- `dependencies`: Package IDs that must also exist in this registry and should be installed first by the Package Installer.
- `overviewOrder`: Optional positive integer used to order packages within their semantic overview sector.
- `integrationTargets`: Package IDs connected by an Integration package in the Package Installer ecosystem graph.
- `suiteMembers`: Package IDs composed by a Suite package in the Package Installer ecosystem graph.
- `recommendedWith`: Genuine non-structural recommendations. Reverse Integration and Suite relationships are derived and must not be stored.

The `id` value must exactly match the target package's `package.json` `name` value. The Package Installer uses that exact ID for installed-package detection.
Packages that declare another Deucarian package in their Unity `package.json` dependencies should also list that package here so dependency-first installation works from the installer.
Integration packages declare every owner package in `integrationTargets` and as a direct dependency. Suite dependencies exactly match `suiteMembers`.

## Capability ownership

- `com.deucarian.common` owns tiny approved low-level runtime primitives. In Wave 2C it owns only `UnityObjectUtility.DestroySafely(UnityEngine.Object target)` for safe transient Unity object cleanup across Play Mode and Edit Mode.
- `unity-object-lifetime` policy findings are generated by `Tools/Generate-DeucarianAudit.py`. Production direct `UnityEngine.Object.Destroy` / `DestroyImmediate` calls outside the owner are actionable unless a future semantic exception is documented; test fixture teardown remains local.
- `com.deucarian.testing` is intentionally not created.

## Current group hierarchy

```text
Infrastructure
State & Data
Runtime Services
Experience & Interaction
├── UI & Presentation
└── World & XR Interaction
Tools & Quality
Gameplay
├── Foundations
├── Progression & Meta
├── Combat & Weapons
├── Encounters & World
└── Genre Frameworks
Templates
└── Games
```

Promoted gameplay packages and starter templates use stable Git `#main` URLs and development Git `#develop` URLs. Use temporary same-branch stable and development URLs only for future pre-stable bootstrap packages whose repositories do not yet have `main` branches.

The three starter templates live directly in `Templates > Games`. Integration and Suite packages live beside their functional owners and remain distinguishable through `kind`.

## Artifact kinds and compatibility

- `Library`: reusable runtime or editor-facing capability packages, including existing Core, Framework, and OptionalIntegration packages.
- `Tool`: developer-facing tooling such as Installer, Diagnostics, authoring, build, and test automation.
- `Integration`: explicit adapters between declared package owners.
- `Suite`: implementation-free dependency composition packages with suite-owned samples.
- `Template`: installable starter projects validated in disposable Unity hosts.

Schema v2 retains legacy `category`, `type`, and `ecosystemGroup` values for one tagged release. They are removed after released Installer and Bootstrap versions have demonstrated v2 consumption.

## License

MIT. See [LICENSE.md](LICENSE.md).
