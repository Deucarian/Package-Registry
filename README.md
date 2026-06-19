# Deucarian Package Registry

## Overview

This repository contains the package registry for the Deucarian Package Installer.

The installer reads `packages.json` from the public raw GitHub URL:

https://raw.githubusercontent.com/Deucarian/Package-Registry/main/packages.json

The registry is intentionally manual and explicit. Adding a new package means adding a new entry to `packages.json`.

Auto-discovery is intentionally avoided because it creates ambiguity around archived repositories, naming, package IDs, dependency resolution, and GitHub rate limits.

## Usage

Update `packages.json` when a package is added, removed, or gains an installer-visible dependency. Keep the Package Installer bundled fallback registry in sync when bootstrap behavior depends on the package list.

## Registry fields

- `schemaVersion`: Registry schema version used by the installer.
- `updatedAt`: Date this registry was last manually updated.
- `packages`: List of package entries available to the installer.
- `id`: Unique Unity package ID.
- `displayName`: Human-readable package name.
- `category`: Package grouping shown by the installer.
- `description`: Short explanation of what the package provides.
- `stableUrl`: GitHub HTTPS Unity Package Manager URL for the stable `#main` branch.
- `developmentUrl`: GitHub HTTPS Unity Package Manager URL for the development `#develop` branch.
- `dependencies`: Package IDs that must also exist in this registry and should be installed first by the Package Installer.
- `groupId`: Optional Package Installer Ecosystem Graph structural group ID. Supported top-level IDs are `infrastructure`, `state-data`, `runtime-services`, `experience-interaction`, `tools-quality`, `integrations`, and `suites`.
- `ecosystemGroup`: Legacy Package Installer overview-wheel sector override retained for older installers. Prefer `groupId` for new entries.
- `overviewOrder`: Optional positive integer used to order packages within their semantic overview sector.
- `optionalCompanions`: Package IDs that are useful optional add-ons but must not be installed automatically as dependencies.
- `optionalIntegrations`: Integration package IDs that are useful for this package but must not be installed automatically as dependencies.
- `integrationTargets`: Package IDs connected by an Integration package in the Package Installer ecosystem graph.
- `suiteMembers`: Package IDs composed by a Suite package in the Package Installer ecosystem graph.

The `id` value must exactly match the target package's `package.json` `name` value. The Package Installer uses that exact ID for installed-package detection.
Packages that declare another Deucarian package in their Unity `package.json` dependencies should also list that package here so dependency-first installation works from the installer.
Packages that merely light up optional integration behavior should list that package in `optionalCompanions` instead of `dependencies`.
Integration packages use `category` value `Integration`; the old bridge package IDs are replaced by `api-integration` and `core-state-integration` package IDs.

## Current categories

- `Editor`: editor-only package tooling, chrome, and infrastructure.
- `Core`: standalone runtime, state, and service packages.
- `UI`: UI presentation packages.
- `World`: world-object and scene-interaction packages.
- `Tools`: developer-facing installer, diagnostics, and package tooling.
- `Integration`: explicit integration packages between two package owners.
- `Suites`: curated bundles that install a complete stack through declared dependencies.

## License

See [LICENSE.md](LICENSE.md).
