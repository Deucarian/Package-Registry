# Ecosystem Polish Audit

Audit date: 2026-07-01

This is the first scout pass for the Deucarian Unity package ecosystem polish goal. It records facts available from public GitHub metadata, the local `C:/Repositories` workspace, `packages.json`, and the new manifest alignment checker.

## Scope And Sources

- GitHub organization metadata: 43 public repositories returned for `Deucarian`.
- Package Registry catalog: 43 packages in `packages.json`.
- Local workspace: partial checkout set under `C:/Repositories`; not every Deucarian repository is present locally.
- Validation/tooling: `Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json`.

The GitHub API response available to this environment reported `admin=false` and `push=false`, so repository settings were not changed.

## Severity Summary

| Severity | Finding | Status |
| --- | --- | --- |
| Branch hygiene | 18 public repositories have a temporary `codex/*` default branch. | Documented in `Documentation~/BRANCH_CHANNEL_CLEANUP.md`; requires GitHub admin action. |
| Registry/fallback drift | Package Installer fallback was missing `UI`, `XR UI`, `Camera Navigation`, and `XR UI Theming Integration`. | Fixed in the Package Installer branch by syncing installer-visible metadata. |
| Registry/manifest mismatch | No mismatch remains for the 12 locally matched package manifests after refreshing stale local checkouts. | Keep using the alignment checker before registry/fallback updates. |
| Missing local coverage | 31 registry packages were not available as exact local checkouts for manifest comparison. | Use exact repo checkouts or a generated audit root before strict alignment. |
| Package skeleton gaps | Some local checkouts lack `AGENTS.md`, `deucarian-package.json`, or validation workflows. | Camera Navigation and XR UI have draft PRs; remaining gaps are recorded below. |

## Local Checkout Coverage

The alignment checker matched 12 package manifests from local checkouts and skipped 31 packages whose exact Deucarian checkout was not present locally.

Matched package checkouts:

- `com.deucarian.camera-navigation`
- `com.deucarian.common`
- `com.deucarian.core-state`
- `com.deucarian.diagnostics`
- `com.deucarian.editor`
- `com.deucarian.logging`
- `com.deucarian.object-loading`
- `com.deucarian.package-installer`
- `com.deucarian.theming`
- `com.deucarian.ui`
- `com.deucarian.xr-ui`
- `com.deucarian.xr-ui.theming-integration`
- one legacy local bridge checkout was present but does not satisfy the exact current `ObjectLoading-API-Integration` repo name.

Package skeleton gaps with draft PRs from this polish pass:

| Repository | Gap addressed | Draft PR |
| --- | --- | --- |
| Camera-Navigation | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/Camera-Navigation/pull/1` |
| XR-UI | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI/pull/1` |
| XR-UI-Theming-Integration | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI-Theming-Integration/pull/1` |

Remaining notable local checkout gaps from the scout pass:

| Repository | Gap |
| --- | --- |
| Core-State | Local checkout is a fork remote; missing `AGENTS.md`; missing `CHANGELOG.md`; missing `LICENSE.md`; missing `deucarian-package.json`. |
| Diagnostics | Missing `AGENTS.md`; missing `deucarian-package.json`; no `.github/workflows` directory. |
| Logging | Local checkout is dirty and on a `codex/*` branch; missing `AGENTS.md`; missing `deucarian-package.json`. |
| UI | Missing `AGENTS.md`; no `.github/workflows` directory. |

## Registry Alignment Checker

Added `Tools/check_registry_manifest_alignment.py` to compare registry package entries with local Unity `package.json` manifests when checkouts are available.

Checks included:

- registry package ID equals `package.json` `name`
- registry display name equals `package.json` `displayName`
- registry GitHub repository URL aligns with `package.json` `repository.url`
- registry `dependencies` align with Deucarian package dependencies in `package.json`

Default behavior keeps missing local checkouts as warnings. Use `--require-checkouts` for a strict full-audit workspace.

Useful commands:

```powershell
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --require-checkouts --check
```

## Next Phase Recommendations

1. Fix GitHub default branches listed in `Documentation~/BRANCH_CHANNEL_CLEANUP.md`.
2. Re-run the alignment checker from a full exact checkout/audit root.
3. Add missing `deucarian-package.json` files and shared `package-validation.yml` workflows package-by-package.
4. Continue README normalization after each package skeleton validates.
5. Re-check Package Installer and Bootstrap fallback catalogs whenever `packages.json` changes.
