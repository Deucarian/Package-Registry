# AGENTS.md Template

Use this structure when adding or refreshing a repository-level `AGENTS.md`.

````markdown
# <Package Name> Agent Notes

Package ID: `<package-id>`

## Ownership

This package owns:

- <capability>

This package must not own:

- <out-of-scope capability>

## Dependencies

Required dependencies:

- `<package>`: <why>

Allowed dependency shape:

- <package-specific rule>

## Policies

- Logging: <package-specific rule>
- Common: <package-specific rule>
- Editor UI: <package-specific rule>
- Diagnostics: <package-specific rule>
- Testing: <package-specific rule>

## Validation

```powershell
python C:/Repositories/Package-Registry/Tools/deucarian_package_validator.py --registry-root C:/Repositories/Package-Registry --repository-root . --config deucarian-package.json
```

## Checklists

Before adding code:

- Inspect existing files.
- Keep the package inside its ownership boundary.
- Avoid broad refactors without audit support.

Before adding a dependency:

- Confirm the dependency owns the capability used.
- Confirm asmdef references and `package.json` agree.
- Update Package Registry/fallback catalogs if required.

Before adding a helper:

- Search current repo and all Deucarian repos.
- Check Package Registry capabilities.
- Reuse the owner package instead of copying helpers.
````
