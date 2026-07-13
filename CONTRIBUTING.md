# Contributing

Follow these rules for all Deucarian package changes.

## Branches

- Work on `develop` unless a maintainer explicitly requests another branch.
- Do not modify or merge `main` during feature/audit waves unless the task is promotion-only.
- Do not edit `Library/PackageCache` directly.

## Before Coding

1. Read the repository `AGENTS.md`.
2. Inspect existing files and local patterns.
3. Check `CAPABILITY_OWNERSHIP.md`.
4. Check `DEPENDENCY_RULES.md`.
5. Avoid broad refactors unless the audit or issue explicitly requires them.

## Before Adding A Helper

1. Search the current repository.
2. Search all Deucarian repositories.
3. Check `capabilities.json`.
4. Use the package that owns the capability.
5. Do not copy helpers between repositories.
6. Do not add unrelated APIs to Common.
7. Add a new shared capability only with audit evidence.

## Before Adding A Dependency

1. Confirm the dependency owns a capability this package directly uses.
2. Update asmdefs and `package.json` together.
3. Update `deucarian-package.json`.
4. Update `packages.json` and fallback catalogs if installer-visible metadata changes.
5. Do not guess versions.

## Validation

Run the shared validator from Package Registry:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File Tools/validate-deucarian-package.ps1 -RepositoryRoot <repo>
```

Or directly:

```powershell
python Tools/deucarian_package_validator.py --registry-root <Package-Registry> --repository-root <repo> --config <repo>/deucarian-package.json
```

For Package Registry, also run:

```powershell
python -m unittest discover Tools/tests
python Tools/project_package_catalogs.py --installer-root ../Package-Installer --bootstrap-root ../Bootstrap --check
python Tools/Generate-DeucarianAudit.py --audit-root <audit-root> --output-root . --organization Deucarian --ref develop --authoritative --format all --check
```

If coordinated Package Installer or Bootstrap changes have not landed locally yet, run the projection tool in write mode against temporary roots and then run `--check` against those same roots. Registry CI uses that order so it validates deterministic generation without depending on unmerged consumer branches.
Package Installer and Bootstrap CI should call `.github/workflows/deucarian-catalog-projection-check.yml` with `catalog: installer` or `catalog: bootstrap` respectively; each check is independent of the other consumer checkout.

## Commit Scope

- Commit focused changes per repository.
- Do not change package versions for documentation-only guidance.
- Do not publish npm packages unless the task explicitly asks for publication.
