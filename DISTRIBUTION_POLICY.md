# Deucarian Distribution Policy

## Public Catalog Scope

`packages.json` contains supported public open-foundation packages only. A package must not be added when its source, license, dependencies, or support status are not suitable for unauthenticated public Git distribution.

The following package IDs are reserved for separately distributed proprietary product development and are intentionally absent from the public catalog:

- `com.deucarian.theming`
- `com.deucarian.ui`
- `com.deucarian.camera-navigation`
- `com.deucarian.xr-ui`
- `com.deucarian.xr-ui.theming-integration`

Removing a package from this catalog does not rename its package ID, revoke an existing license, or change an existing Git branch. Re-adding a reserved package requires a separate, explicit distribution and licensing decision.

## Current Public Channels

Stable Deucarian Unity packages are distributed by Git URL pinned to the `main` branch:

```text
https://github.com/Deucarian/<Repo>.git#main
```

Development packages are distributed by Git URL pinned to the `develop` branch:

```text
https://github.com/Deucarian/<Repo>.git#develop
```

`packages.json` is the source of truth for public stable and development Git URLs. The Package Installer consumes the remote registry from `main` and keeps a bundled fallback catalog for offline or recovery flows. Proprietary products are not fetched by the public Package Installer.

`PUBLIC_CATALOG_UNITY_MATRIX.json` is the deterministic 38-package by two-channel clean-project test plan. Its 76 cases must remain current in CI. Executing all cases in clean Unity 2022.3 projects, with zero reserved packages and no package-originated errors or warnings, is a merge gate for catalog removal; generating the plan is not a substitute for that Unity execution.

## Deferred Channels

npm/scoped-registry publication is deferred. Do not publish Deucarian packages to npm as part of normal branch promotion.

Git tags and GitHub releases are also deferred. They are not required for the current stable Git workflow and must not be created automatically from branch promotion.

## Future Release Waves

Future npm/scoped-registry publication, Git tag creation, or GitHub release creation must happen through a separate deliberate release wave with explicit validation and manual approval.

Release-capable workflows must remain manual-only and guarded while Git-only distribution is active.
