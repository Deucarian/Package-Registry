# Ecosystem Polish Audit

Audit date: 2026-07-01

This is the first scout pass for the Deucarian Unity package ecosystem polish goal. It records facts available from public GitHub metadata, the local `C:/Repositories` workspace, `packages.json`, and the new manifest alignment checker.

## Scope And Sources

- GitHub organization metadata: 43 public repositories returned for `Deucarian`.
- Package Registry catalog: 43 packages in `packages.json`.
- Local workspace: all 43 Package Registry package checkouts are present under `C:/Repositories` after this pass.
- Validation/tooling: `Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json`.

The GitHub API response available to this environment reported `admin=false` and `push=false`, so repository settings were not changed.

## Severity Summary

| Severity | Finding | Status |
| --- | --- | --- |
| Branch hygiene | 18 public repositories have a temporary `codex/*` default branch. | Documented in `Documentation~/BRANCH_CHANNEL_CLEANUP.md`; requires GitHub admin action. |
| Registry/fallback drift | Package Installer fallback was missing several registry packages, then later had gameplay/template dependency metadata that did not match direct manifest dependencies. | Fixed in the Package Installer branch by syncing installer-visible metadata, standardizing installer front-door docs and `main` workflow coverage, and aligning fallback gameplay/template dependencies with Package Registry. |
| Registry/manifest mismatch | No mismatch remains for all 43 locally matched package manifests after refreshing/cloning exact local checkouts, adding missing manifest repository URLs, and aligning registry dependencies. | Keep using the alignment checker before registry/fallback updates. |
| Missing local coverage | No registry package is currently missing an exact local checkout under `C:/Repositories`. | Re-run the checker after new packages are added or checkouts move. |
| Package skeleton gaps | Some local checkouts still lack `AGENTS.md`, `deucarian-package.json`, or validation workflows. | Infrastructure/integration docs and workflow gaps have draft PRs; Gameplay Foundation, Persistence, Progression, Idle Progression, Combat, Encounters, World Spawning, World Navigation, Game Content Authoring, Monetization, and Idle Auto Defense Template now have validation skeleton PRs; remaining gameplay/template skeleton work should proceed package-by-package after branch/default cleanup. |

## Local Checkout Coverage

The alignment checker matched all 43 package manifests from local checkouts and skipped no packages.

Matched package checkouts:

- `com.deucarian.camera-navigation`
- `com.deucarian.api`
- `com.deucarian.attacks`
- `com.deucarian.auto-defense`
- `com.deucarian.auto-defense-suite`
- `com.deucarian.combat`
- `com.deucarian.common`
- `com.deucarian.core-state`
- `com.deucarian.defense-games`
- `com.deucarian.diagnostics`
- `com.deucarian.editor`
- `com.deucarian.encounters`
- `com.deucarian.game-content-authoring`
- `com.deucarian.gameplay-foundation`
- `com.deucarian.idle-progression`
- `com.deucarian.logging`
- `com.deucarian.monetization`
- `com.deucarian.object-loading`
- `com.deucarian.object-loading.api-integration`
- `com.deucarian.object-selection`
- `com.deucarian.object-selection.core-state-integration`
- `com.deucarian.package-installer`
- `com.deucarian.persistence`
- `com.deucarian.progression`
- `com.deucarian.projectiles`
- `com.deucarian.run-upgrades`
- `com.deucarian.selection-suite`
- `com.deucarian.session`
- `com.deucarian.session.api-integration`
- `com.deucarian.template.game.idle-auto-defense`
- `com.deucarian.template.game.movement-fps`
- `com.deucarian.template.game.survivors`
- `com.deucarian.theming`
- `com.deucarian.test-automation`
- `com.deucarian.ui`
- `com.deucarian.ui-binding`
- `com.deucarian.ui-binding.core-state-integration`
- `com.deucarian.ui-flow`
- `com.deucarian.weapon-systems`
- `com.deucarian.world-navigation`
- `com.deucarian.world-spawning`
- `com.deucarian.xr-ui`
- `com.deucarian.xr-ui.theming-integration`

Package skeleton gaps with draft PRs from this polish pass:

| Repository | Gap addressed | Draft PR |
| --- | --- | --- |
| Bootstrap | Added README polish and `main` workflow coverage after fast-forwarding `develop`; validator still warns that Bootstrap has no `packages.json` entry. | `https://github.com/Deucarian/Bootstrap/pull/2` |
| Camera-Navigation | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/Camera-Navigation/pull/1` |
| Combat | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, manifest repository metadata, and test asmdef validation metadata. | `https://github.com/Deucarian/Combat/pull/1` |
| Common | Added README polish, `main` workflow coverage, and synchronized AGENTS ownership notes with approved shared motion easing primitives. | `https://github.com/Deucarian/Common/pull/1` |
| Core-State | Added README polish, `main` workflow coverage, and Unity metadata for the guidance file from a clean Deucarian worktree because the existing local checkout points at a fork remote. | `https://github.com/Deucarian/Core-State/pull/1` |
| Diagnostics | Fast-forwarded the stale local checkout to upstream skeleton work, then added README polish, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Diagnostics/pull/1` |
| Editor | Added README polish and `main` workflow coverage while preserving shared editor shell API and UX standards guidance. | `https://github.com/Deucarian/Editor/pull/3` |
| Encounters | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, and manifest repository metadata. | `https://github.com/Deucarian/Encounters/pull/1` |
| Game-Content-Authoring | Added `AGENTS.md`, shared `package-validation.yml`, Unity metadata for the guidance file, and a validator-backed editor preview cleanup exception. | `https://github.com/Deucarian/Game-Content-Authoring/pull/1` |
| Gameplay-Foundation | Added `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, and manifest repository metadata. | `https://github.com/Deucarian/Gameplay-Foundation/pull/1` |
| Idle-Progression | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, and manifest repository metadata. | `https://github.com/Deucarian/Idle-Progression/pull/1` |
| Logging | Added README polish and `main` workflow coverage from a clean worktree off `origin/develop`, leaving the existing dirty local codex worktree untouched. | `https://github.com/Deucarian/Logging/pull/1` |
| Monetization | Added `AGENTS.md`, shared `package-validation.yml`, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Monetization/pull/1` |
| Object-Loading | Added README polish, stable/development Git install guidance, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Object-Loading/pull/1` |
| Object-Selection | Added README polish, corrected hyphenated Git/local paths, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Object-Selection/pull/1` |
| ObjectSelection-CoreState-Integration | Added README polish, corrected exact local checkout paths, updated validation guidance, and Unity metadata for the guidance file. | `https://github.com/Deucarian/ObjectSelection-CoreState-Integration/pull/1` |
| Persistence | Added `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, and manifest repository metadata. | `https://github.com/Deucarian/Persistence/pull/1` |
| Progression | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, manifest repository metadata, and test asmdef validation metadata. | `https://github.com/Deucarian/Progression/pull/1` |
| Selection-Suite | Added README polish, stable/development Git install guidance, troubleshooting notes, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Selection-Suite/pull/1` |
| Session | Added README polish, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Session/pull/1` |
| Session-API-Integration | Added README polish, `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/Session-API-Integration/pull/1` |
| Template-Game-Idle-Auto-Defense | Added `AGENTS.md`, shared `package-validation.yml`, Unity metadata for the guidance file, and synchronized config dependencies with `package.json`. | `https://github.com/Deucarian/Template-Game-Idle-Auto-Defense/pull/1` |
| Theming | Added README polish, stable/development Git install guidance, validation notes, and `main` workflow coverage while preserving detailed palette/theme workflows. | `https://github.com/Deucarian/Theming/pull/1` |
| UI | Added `AGENTS.md`, shared `package-validation.yml`, README polish, and Unity metadata for the new guidance file. | `https://github.com/Deucarian/UI/pull/1` |
| UI-Binding | Added README polish, stable/development Git install guidance, corrected local checkout path, and Unity metadata for the guidance file. | `https://github.com/Deucarian/UI-Binding/pull/1` |
| UIBinding-CoreState-Integration | Added README polish, corrected exact local checkout paths, added `main` workflow coverage, and Unity metadata for the guidance file. | `https://github.com/Deucarian/UIBinding-CoreState-Integration/pull/1` |
| UI-FLow | Added README polish, `main` workflow coverage, and Unity metadata for the guidance file while preserving the existing repository capitalization. | `https://github.com/Deucarian/UI-FLow/pull/1` |
| World-Navigation | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, and manifest repository metadata. | `https://github.com/Deucarian/World-Navigation/pull/1` |
| World-Spawning | Added `LICENSE.md`, `AGENTS.md`, `deucarian-package.json`, shared `package-validation.yml`, Unity metadata for the guidance file, manifest repository metadata, and Common-backed production Unity object cleanup. | `https://github.com/Deucarian/World-Spawning/pull/1` |
| XR-UI | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI/pull/1` |
| XR-UI-Theming-Integration | Added `AGENTS.md`, shared `package-validation.yml`, and README polish. | `https://github.com/Deucarian/XR-UI-Theming-Integration/pull/1` |

Manifest repository URL gaps with draft PRs from this polish pass:

| Repository | Gap addressed | Draft PR |
| --- | --- | --- |
| Attacks | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Attacks/pull/1` |
| Auto-Defense | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Auto-Defense/pull/1` |
| Auto-Defense-Suite | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Auto-Defense-Suite/pull/1` |
| Defense-Games | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Defense-Games/pull/1` |
| Projectiles | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Projectiles/pull/1` |
| Run-Upgrades | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Run-Upgrades/pull/1` |
| Template-Game-Movement-FPS | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Template-Game-Movement-FPS/pull/1` |
| Template-Game-Survivors | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Template-Game-Survivors/pull/1` |
| Test-Automation | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Test-Automation/pull/1` |
| Weapon-Systems | Added `package.json` repository metadata so manifest URL alignment can verify the package. | `https://github.com/Deucarian/Weapon-Systems/pull/1` |

Deferred exact-checkout polish:

| Repository | Current state | Follow-up |
| --- | --- | --- |
| ObjectLoading-API-Integration | Exact checkout is present and registry alignment passes; `AGENTS.md`, `deucarian-package.json`, and Unity metadata are present, but README/workflow polish remains. | Resolve branch/default-branch hygiene first because `origin/main` contains Unity metadata commit `78341b9` that is not on `origin/develop`. |

Remaining notable local checkout gaps from the scout pass:

- None. The current workspace has exact checkouts for all 43 Package Registry entries.
- Non-exact local fork/legacy checkouts such as `ObjectSelection` can be ignored for registry alignment now that exact Deucarian checkouts exist.

Catalog follow-up completed in this pass:

- Package Registry and Package Installer fallback dependencies now match direct Deucarian dependencies in local `package.json` manifests for `Attacks`, `Run-Upgrades`, `Weapon-Systems`, `Template-Game-Idle-Auto-Defense`, and `Template-Game-Movement-FPS`.
- `World-Spawning` now declares `com.deucarian.common` across `package.json`, Package Registry, and Package Installer fallback metadata because production cleanup uses Common's approved `UnityObjectUtility.DestroySafely`.
- `Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json` now reports 43 checked packages, no missing checkouts, no findings, and no warnings.

Remaining catalog follow-up:

- Bootstrap validates locally, but the shared validator reports `com.deucarian.bootstrap: no packages.json entry found.` Decide whether Bootstrap should remain a setup-only package outside the installable catalog or be modeled explicitly in Package Registry without making Package Installer own Bootstrap setup behavior.

## Registry Alignment Checker

Added `Tools/check_registry_manifest_alignment.py` to compare registry package entries with local Unity `package.json` manifests when checkouts are available.

Checks included:

- registry package ID equals `package.json` `name`
- registry display name equals `package.json` `displayName`
- registry GitHub repository URL aligns with `package.json` `repository.url`
- registry `dependencies` align with Deucarian package dependencies in `package.json`

Default behavior keeps missing local checkouts as warnings. Use `--require-checkouts` for a strict full-audit workspace.

Latest full-workspace result: 43 checked packages, no missing checkouts, no findings, and no warnings.

Useful commands:

```powershell
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --require-checkouts --check
```

## Next Phase Recommendations

1. Fix GitHub default branches listed in `Documentation~/BRANCH_CHANNEL_CLEANUP.md`.
2. Add missing `deucarian-package.json`, `AGENTS.md`, and shared `package-validation.yml` files to gameplay/template packages package-by-package.
3. Continue README normalization after each package skeleton validates.
4. Resolve `ObjectLoading-API-Integration` branch/default-branch hygiene before README/workflow polish there.
5. Re-check Package Installer and Bootstrap fallback catalogs whenever `packages.json` changes.
