# Deucarian Distribution Policy

## Current Channels

Stable Deucarian Unity packages are distributed by Git URL pinned to the `main` branch:

```text
https://github.com/Deucarian/<Repo>.git#main
```

Development packages are distributed by Git URL pinned to the `develop` branch:

```text
https://github.com/Deucarian/<Repo>.git#develop
```

`packages.json` is the source of truth for stable and development Git URLs. The Package Installer consumes the remote registry from `main` and keeps a bundled fallback catalog for offline or recovery flows.

## Deferred Channels

npm/scoped-registry publication is deferred. Do not publish Deucarian packages to npm as part of normal branch promotion.

Git tags and GitHub releases are also deferred. They are not required for the current stable Git workflow and must not be created automatically from branch promotion.

## Future Release Waves

Future npm/scoped-registry publication, Git tag creation, or GitHub release creation must happen through a separate deliberate release wave with explicit validation and manual approval.

Release-capable workflows must remain manual-only and guarded while Git-only distribution is active.
