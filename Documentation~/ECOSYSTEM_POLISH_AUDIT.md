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
| Registry/fallback drift | Package Installer fallback was missing `UI`, `XR UI`, `Camera Navigation`, and `XR UI Theming Integration`. | Fixed in the Package Installer branch by syncing installer-visible metadata; the same branch now also standardizes installer front-door docs and `main` workflow coverage. |
| Registry/manifest mismatch | No mismatch remains for the 12 locally matched package manifests after refreshing stale local checkouts. | Keep using the alignment checker before registry/fallback updates. |
| Missing local coverage | 31 registry packages were not available as exact local checkouts for manifest comparison. | Use exact repo checkouts or a generated audit root before strict alignment. |
| Package skeleton gaps | Some local checkouts lack `AGENTS.md`, `deucarian-package.json`, or validation workflows. | Bootstrap, Camera Navigation, Common, Core State, Editor, Logging, Object Loading, Theming, UI, XR UI, XR UI Theming Integration, and Diagnostics have draft PRs; no remaining exact local checkout skeleton gap is known. |

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
| Bootstrap | Added README polish and `main` workflow coverage after fast-forwarding `develop`; validator still warns that Bootstrap has no `packages.json` entry. | `https://github.com/Deucarian/Bootstrap/pull/2` |
| Camera-Navigation | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/Camera-Navigation/pull/1` |
| Common | Added README polish, `main` workflow coverage, and synchronized AGENTS ownership notes with approved shared motion easing primitives. | `https://github.com/Deucarian/Common/pull/1` |
| Core-State | Added README polish, `main` workflow coverage, and Unity metadata for the guidance file from a clean Deucarian worktree because the existing local checkout points at a fork remote. | `https://github.com/Deucarian/Core-State/pull/1` |
| Diagnostics | Fast-forwarded the stale local checkout to upstream skeleton work, then added README polish, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Diagnostics/pull/1` |
| Editor | Added README polish and `main` workflow coverage while preserving shared editor shell API and UX standards guidance. | `https://github.com/Deucarian/Editor/pull/3` |
| Logging | Added README polish and `main` workflow coverage from a clean worktree off `origin/develop`, leaving the existing dirty local codex worktree untouched. | `https://github.com/Deucarian/Logging/pull/1` |
| Object-Loading | Added README polish, stable/development Git install guidance, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Object-Loading/pull/1` |
| Theming | Added README polish, stable/development Git install guidance, validation notes, and `main` workflow coverage while preserving detailed palette/theme workflows. | `https://github.com/Deucarian/Theming/pull/1` |
| UI | Added `AGENTS.md`, shared `package-validation.yml`, README polish, and Unity metadata for the new guidance file. | `https://github.com/Deucarian/UI/pull/1` |
| XR-UI | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI/pull/1` |
| XR-UI-Theming-Integration | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI-Theming-Integration/pull/1` |

Remaining notable local checkout gaps from the scout pass:

- No remaining exact local checkout skeleton gap is known after the current draft PR set.
- Non-exact local fork/legacy checkouts such as `ObjectSelection` and bridge-era repositories still require exact Deucarian checkouts before strict package-level patching.

Catalog follow-up:

- Bootstrap validates locally, but the shared validator reports `com.deucarian.bootstrap: no packages.json entry found.` Decide whether Bootstrap should remain a setup-only package outside the installable catalog or be modeled explicitly in Package Registry without making Package Installer own Bootstrap setup behavior.

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
