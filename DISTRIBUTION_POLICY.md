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

## Review-only catalog entries

A registry feature branch may carry planned channel URLs so Package Installer and Bootstrap catalog projections can be reviewed before publication. Those entries are not distributable and the planned URLs are not evidence that either branch is reachable.

Do not promote a review-only entry to `develop` or `main` until all of the following are true:

- The package repository exists and contains the reviewed source.
- Its `develop` and `main` refs exist as required by the target channel.
- `deucarian_package_validator.py --check-remote-urls` passes for the registry.
- A clean consumer checkout resolves the package without workspace-relative sources.

Until that gate passes, generated fallback catalogs may be committed only on matching review branches and must not be described as installable or published.

## Deferred Channels

npm/scoped-registry publication is deferred. Do not publish Deucarian packages to npm as part of normal branch promotion.

Git tags and GitHub releases are also deferred. They are not required for the current stable Git workflow and must not be created automatically from branch promotion.

## Future Release Waves

Future npm/scoped-registry publication, Git tag creation, or GitHub release creation must happen through a separate deliberate release wave with explicit validation and manual approval.

Release-capable workflows must remain manual-only and guarded while Git-only distribution is active.
