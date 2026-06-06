# JorisHoef Package Registry

This repository contains the package registry for the JorisHoef Package Installer.

The installer reads `packages.json` from the public raw GitHub URL:

https://raw.githubusercontent.com/JorisHoef/Package-Registry/main/packages.json

The registry is intentionally manual and explicit. Adding a new package means adding a new entry to `packages.json`.

Auto-discovery is intentionally avoided because it creates ambiguity around archived repositories, naming, package IDs, dependency resolution, and GitHub rate limits.

## Registry fields

- `schemaVersion`: Registry schema version used by the installer.
- `updatedAt`: Date this registry was last manually updated.
- `packages`: List of package entries available to the installer.
- `id`: Unique Unity package ID.
- `displayName`: Human-readable package name.
- `category`: Package grouping shown by the installer.
- `description`: Short explanation of what the package provides.
- `stableUrl`: GitHub HTTPS Unity Package Manager URL for the stable branch.
- `developmentUrl`: GitHub HTTPS Unity Package Manager URL for the development branch.
- `dependencies`: Package IDs that must also exist in this registry.

The `id` value must exactly match the target package's `package.json` `name` value. The Package Installer uses that exact ID for installed-package detection.

## Current categories

- `Core`: foundational standalone packages.
- `UI`: UI presentation packages.
- `World`: world-object and scene-interaction packages.
- `Bridge`: explicit integration packages between two package owners.
- `Suites`: curated bundles that install a complete stack through declared dependencies.
