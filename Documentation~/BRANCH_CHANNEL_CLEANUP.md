# Branch Channel Cleanup

Audit date: 2026-07-01

Source: GitHub REST repository and branch metadata for `Deucarian` public repositories, queried from this workspace. The API response available here reported no admin or push permission, and the available GitHub connector did not expose a repository-settings write operation, so default branch changes remain a manual admin action.

## Policy

- `main` is the stable Git UPM channel.
- `develop` is the development and beta Git UPM channel.
- `codex/*` branches are temporary task branches and should not be repository defaults.
- Do not delete `codex/*` branches automatically; review them after the default branch is corrected.

## Required Admin Action

For each affected repository:

1. Open `https://github.com/Deucarian/<repo>/settings/branches`.
2. Change the default branch from the listed `codex/*` branch to `develop`.
3. Use `main` instead only when the maintainer confirms the repository is stable and should open on the stable channel.
4. Re-run the branch audit after changes and record the new default branch.

All affected repositories currently have both `main` and `develop`, so no branch creation is required before changing the default.

| Repository | Current default branch | Has main | Has develop | Recommended default | Required action |
| --- | --- | --- | --- | --- | --- |
| Attacks | `codex/game-template-phase-1-attacks` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Auto-Defense | `codex/game-template-phase-1t-auto-defense-save-progression-composition` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Auto-Defense-Suite | `codex/game-template-phase-1x-auto-defense-suite` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Combat | `codex/game-template-phase-1i-combat-resolver-closeout` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Defense-Games | `codex/game-template-phase-1v-package-manifest-alignment` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Encounters | `codex/game-template-phase-1-encounters` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Game-Content-Authoring | `codex/shared-game-content-authoring-package` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Gameplay-Foundation | `codex/game-template-phase-1-gameplay-foundation` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Idle-Progression | `codex/game-template-phase-1s-idle-progression` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Persistence | `codex/game-template-phase-1-persistence` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Progression | `codex/game-template-phase-1-progression` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Projectiles | `codex/game-template-phase-1l-generic-world-spawn-request` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Run-Upgrades | `codex/game-template-phase-1r-run-upgrades` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Template-Game-Idle-Auto-Defense | `codex/game-template-phase-2b-template-remote-registry` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Test-Automation | `codex/game-template-phase-1p-test-automation` | yes | yes | `develop` | Change default branch in GitHub settings. |
| Weapon-Systems | `codex/game-template-phase-1-weapon-systems` | yes | yes | `develop` | Change default branch in GitHub settings. |
| World-Navigation | `codex/game-template-phase-1m-world-navigation-spawn-compatibility` | yes | yes | `develop` | Change default branch in GitHub settings. |
| World-Spawning | `codex/game-template-phase-1v-package-manifest-alignment` | yes | yes | `develop` | Change default branch in GitHub settings. |

## Already Non-Task Defaults

The same audit saw `develop` defaults for `Monetization`, `Template-Game-Survivors`, `UI-FLow`, and `XR-UI`. The remaining public repositories reported `main` defaults.
