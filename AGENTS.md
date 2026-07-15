# Deucarian Package Registry Agent Notes

Repository: `Deucarian/Package-Registry`
Package ID: none; this is the governance repository.

This repository owns the canonical Deucarian metadata, architecture rules, validation tooling, and generated audit artifacts.

## Ownership

This repository owns:

- `packages.json` package catalog and Installer-visible metadata.
- `capabilities.json` capability ownership registry.
- `dependency-rules.json` dependency layering rules.
- Shared validator and reusable GitHub workflows.
- Organization audit generation and committed audit artifacts.

This repository must not own:

- Runtime package code.
- Editor UI implementation.
- Package Installer graph/UI behavior.
- Domain package helpers that belong in a package owner.

## Dependencies

Required dependencies:

- None. This repository is metadata and Python tooling only.

Architecture exceptions:

- Package Registry owns governance metadata but does not install or run Unity package behavior.

## Policies

- Logging: no package runtime logging ownership here.
- Common: do not add runtime helper APIs here; Common owns only its approved runtime primitive.
- Editor UI: do not implement editor UI here; Editor and Package Installer own their package-specific surfaces.
- Diagnostics: audit artifacts may report diagnostics policy, but Diagnostics package owns diagnostics runtime/editor behavior.
- Testing: Python tests live under `Tools/tests`; generated audit artifacts must stay deterministic.

## Validation

```powershell
python -m unittest discover Tools/tests
python Tools/deucarian_package_validator.py --registry-root . --repository-root . --config deucarian-package.json
python Tools/project_package_catalogs.py --installer-root ../Package-Installer --bootstrap-root ../Bootstrap --check
python Tools/Generate-DeucarianAudit.py --audit-root <audit-root> --output-root . --organization Deucarian --ref develop --authoritative --format all --check
```

## Codex Guidance

- Inspect current files before changing governance data.
- Work on `develop`; do not modify or merge `main` unless the task is promotion-only.
- Do not edit `Library/PackageCache`.
- Do not guess package versions or dependency versions.
- Keep Package Installer and Bootstrap fallback catalogs aligned when package metadata changes.
- Generate consumer fallback catalogs with `Tools/project_package_catalogs.py`; do not maintain them by hand.
- Do not create new packages without explicit user request and audit evidence.
- Do not publish npm packages.
- Commit focused governance/tooling/doc changes and report validation results.

## Before Adding Code

- Confirm the change belongs in governance tooling rather than a package repo.
- Keep validator rules tied to `packages.json`, `capabilities.json`, `dependency-rules.json`, or audit artifacts.
- Preserve `Generate-DeucarianAudit.py` behavior unless the task explicitly changes audit scope.

## Before Adding A Dependency

- Is this a tooling dependency only?
- Can the validator remain standard-library Python?
- Does the dependency need CI installation and documentation?
- Does it affect package runtime/editor dependencies? If yes, stop.

## Before Adding A Helper

- Is the helper for governance tooling only?
- If the helper is a runtime/editor concept, it belongs in the capability owner package, not here.
- Check existing audit/validator helpers before adding another path.

## Debug And Unity Object Lifetime

- Runtime Debug and Unity object lifetime policies are documented and validated here, not implemented here.
- Production Unity object cleanup belongs to `com.deucarian.common`.
