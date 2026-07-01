# Deucarian Package Ecosystem Start Here

This guide is the short path for developers and designers deciding which Deucarian Unity packages to install.

## Channels

- Stable: install from Git URLs ending in `#main`.
- Development: install from Git URLs ending in `#develop`.
- Temporary `codex/*` branches are task branches and should not be used as install channels.
- npm/scoped registry publishing, GitHub Releases, and immutable release tags are deferred unless the release policy changes.

## Install Paths

Use either Unity Package Manager Git URLs directly or install `com.deucarian.package-installer` first:

```json
"com.deucarian.package-installer": "https://github.com/Deucarian/Package-Installer.git#main"
```

Development installer:

```json
"com.deucarian.package-installer": "https://github.com/Deucarian/Package-Installer.git#develop"
```

Open the installer from Unity:

```text
Tools > Deucarian > Package Installer
```

## Package Map By Use Case

| Use case | Start with | Add when needed |
| --- | --- | --- |
| First-time setup | Package Installer | Editor, Logging |
| API and networking | API | Session API Integration, Object Loading API Integration |
| Authenticated sessions | Session | API, Session API Integration |
| Object and scene loading | Object Loading | API, Object Loading API Integration |
| UI binding | UI Binding | Core State, UI Binding Core State Integration |
| UI navigation and presentation | UI Flow, UI, Theming | XR UI, XR UI Theming Integration |
| Object selection | Object Selection | Core State, Object Selection Core State Integration, Selection Suite |
| Diagnostics | Diagnostics | Logging |
| Gameplay foundations | Gameplay Foundation | Persistence, Progression, Run Upgrades |
| Auto-defense games | Auto Defense Suite | Idle Auto Defense template |
| Starter projects | Template Game packages | Game Content Authoring |

## Unity Compatibility Notes

Always confirm the current `package.json` before changing metadata. Known local checkout baselines from the 2026-07-01 scout pass:

- Mature infrastructure/runtime checkouts commonly target Unity `2021.3`.
- Theming, UI, XR UI, XR UI Theming Integration, and Camera Navigation target Unity `2022.3`.
- Gameplay and template packages should be validated from exact manifests before publishing compatibility metadata.

## Validation

Run Package Registry validation:

```powershell
python -m unittest discover Tools/tests
python Tools/deucarian_package_validator.py --registry-root . --repository-root . --config deucarian-package.json
```

Run registry/manifest alignment from a workspace with local package checkouts:

```powershell
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --json
```

For a strict full-audit workspace:

```powershell
python Tools/check_registry_manifest_alignment.py --registry-root . --audit-root C:/Repositories --require-checkouts --check
```

## Governance

- Capability ownership: `CAPABILITY_OWNERSHIP.md`
- Dependency rules: `DEPENDENCY_RULES.md`
- Distribution policy: `DISTRIBUTION_POLICY.md`
- Release policy: `RELEASE_POLICY.md`
- Branch cleanup checklist: `Documentation~/BRANCH_CHANNEL_CLEANUP.md`
- Ecosystem polish audit: `Documentation~/ECOSYSTEM_POLISH_AUDIT.md`
