# Deucarian Release Policy

## Active Policy

The current release policy is Git-only:

- `main` is the stable Git distribution channel.
- `develop` is the development Git distribution channel.
- npm/scoped-registry publishing is disabled and deferred.
- Git tags and GitHub releases are disabled and deferred.
- Branch promotion must not publish, tag, release, or commit release-prep changes automatically.

## Workflow Requirements

Validation workflows may run on push and pull request events.

Release-capable workflows must be manual-only through `workflow_dispatch` and must require the exact confirmation text:

```text
I understand this publishes a Deucarian package
```

While Git-only distribution is active, publish/tag/release paths should exit before touching npm, tags, releases, or release-prep commits.

## Source Of Truth

Package Registry owns distribution metadata through `packages.json`.

Package Installer consumes the registry and its bundled fallback catalog. Bootstrap consumes the registry and its bundled fallback catalog for Git setup and repair.
