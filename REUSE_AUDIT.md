# Deucarian Reuse Audit

Schema version: 2

This is the hardened organization-wide audit snapshot for `Deucarian` at `main`. It uses `tree-sitter-c-sharp` for C# parsing and records the current package sources and governance state.

## Weaknesses Fixed From The Original Audit

- Replaced regex/braces C# discovery with syntax-aware Tree-sitter parsing.
- Public API counts now include only externally public Runtime and Editor production symbols.
- Debug usage counts now come from invocation expressions instead of prose/text matches.
- Unity object lifetime findings separate helper definitions, helper calls, and direct Unity API calls.
- Documentation version drift detection no longer treats every semantic version in README prose as the package version.
- Audit paths are repository-relative/canonical; no machine-specific audit-root paths are written.

## Inventory

| Repository | Package ID | Version | Unity | Develop | Audit Clone | package.json dependencies | Asmdefs | Production public API |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| API | com.deucarian.api | 1.1.4 | 2021.3 | no | clean | com.deucarian.logging, com.unity.modules.unitywebrequest, com.unity.nuget.newtonsoft-json, com.unity.modules.assetbundle, com.unity.modules.unitywebrequestassetbundle, com.unity.modules.unitywebrequesttexture, com.unity.modules.unitywebrequestwww | 4 | 169 |
| Attacks | com.deucarian.attacks | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.editor, com.deucarian.game-content-authoring | 5 | 389 |
| Auto-Defense | com.deucarian.auto-defense | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.defense-games, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems | 4 | 112 |
| Auto-Defense-Suite | com.deucarian.auto-defense-suite | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.combat, com.deucarian.encounters, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.defense-games, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems, com.deucarian.auto-defense, com.deucarian.run-upgrades, com.deucarian.idle-progression | 1 | 0 |
| Bootstrap | com.deucarian.bootstrap | 1.1.4 | 2021.3 | no | clean | (none) | 2 | 1 |
| Build-Pipeline | com.deucarian.build-pipeline | 0.2.2 | 6000.0 | no | clean | com.deucarian.editor, com.deucarian.logging | 2 | 53 |
| Camera-Navigation | com.deucarian.camera-navigation | 0.2.0 | 2022.3 | no | clean | com.deucarian.common | 3 | 105 |
| CameraNavigation-InputSystem-Integration | com.deucarian.camera-navigation.input-system-integration | 0.1.0 | 2022.3 | no | clean | com.deucarian.camera-navigation, com.unity.inputsystem | 3 | 58 |
| Combat | com.deucarian.combat | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation | 3 | 218 |
| Common | com.deucarian.common | 0.2.1 | 2021.3 | no | clean | (none) | 5 | 6 |
| Core-State | com.deucarian.core-state | 1.0.2 | 2021.3 | no | clean | (none) | 3 | 41 |
| Defense-Games | com.deucarian.defense-games | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.world-spawning, com.deucarian.world-navigation | 4 | 122 |
| Diagnostics | com.deucarian.diagnostics | 0.1.4 | 2021.3 | no | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 63 |
| Editor | com.deucarian.editor | 1.0.5 | 2021.3 | no | clean | (none) | 4 | 506 |
| Encounters | com.deucarian.encounters | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation | 3 | 238 |
| Game-Content-Authoring | com.deucarian.game-content-authoring | 0.1.1 | 6000.3 | no | clean | com.deucarian.common, com.deucarian.editor, com.deucarian.gameplay-foundation | 2 | 1252 |
| Gameplay-Foundation | com.deucarian.gameplay-foundation | 0.1.1 | 2021.3 | no | clean | (none) | 3 | 131 |
| Idle-Progression | com.deucarian.idle-progression | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.progression | 3 | 24 |
| Logging | com.deucarian.logging | 1.0.2 | 2021.3 | no | clean | com.deucarian.editor | 5 | 69 |
| Monetization | com.deucarian.monetization | 0.1.1 | 6000.3 | no | clean | (none) | 3 | 76 |
| Object-Loading | com.deucarian.object-loading | 1.2.2 | 2021.3 | no | clean | com.deucarian.common, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 5 | 246 |
| Object-Selection | com.deucarian.object-selection | 1.0.4 | 2021.3 | no | clean | com.deucarian.logging, com.unity.modules.physics | 3 | 118 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | 0.2.6 | 2021.3 | no | clean | com.unity.nuget.newtonsoft-json, com.deucarian.api, com.deucarian.object-loading | 3 | 30 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | 1.0.4 | 2021.3 | no | clean | com.deucarian.logging, com.deucarian.object-selection, com.deucarian.core-state | 3 | 25 |
| Package-Installer | com.deucarian.package-installer | 1.1.79 | 2021.3 | no | clean | com.deucarian.editor, com.deucarian.logging | 2 | 0 |
| Package-Registry | (none) | (none) | (none) | no | clean | (none) | 0 | 0 |
| Persistence | com.deucarian.persistence | 0.1.1 | 2021.3 | no | clean | com.unity.nuget.newtonsoft-json | 5 | 147 |
| Pointer-Capture | com.deucarian.pointer-capture | 0.1.2 | 2022.3 | no | clean | com.deucarian.editor | 5 | 57 |
| Progression | com.deucarian.progression | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation | 3 | 159 |
| Projectiles | com.deucarian.projectiles | 0.2.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.attacks, com.deucarian.world-navigation, com.deucarian.world-spawning | 3 | 120 |
| Run-Upgrades | com.deucarian.run-upgrades | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.weapon-systems, com.deucarian.editor, com.deucarian.game-content-authoring | 5 | 172 |
| Selection-Suite | com.deucarian.selection-suite | 1.0.4 | 2021.3 | no | clean | com.deucarian.object-selection.core-state-integration, com.deucarian.core-state, com.deucarian.ui-binding.core-state-integration, com.deucarian.ui-binding, com.deucarian.object-selection | 1 | 0 |
| Session | com.deucarian.session | 1.0.5 | 2021.3 | no | clean | com.deucarian.logging, com.unity.modules.jsonserialize | 3 | 65 |
| Session-API-Integration | com.deucarian.session.api-integration | 1.0.5 | 2021.3 | no | clean | com.deucarian.api, com.deucarian.session | 3 | 3 |
| Template-Game-Idle-Auto-Defense | com.deucarian.template.game.idle-auto-defense | 0.1.2 | 6000.3 | no | clean | com.deucarian.attacks, com.deucarian.auto-defense, com.deucarian.auto-defense-suite, com.deucarian.combat, com.deucarian.common, com.deucarian.defense-games, com.deucarian.editor, com.deucarian.encounters, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.idle-progression, com.deucarian.monetization, com.deucarian.persistence, com.deucarian.progression, com.deucarian.projectiles, com.deucarian.run-upgrades, com.deucarian.weapon-systems, com.deucarian.world-navigation, com.deucarian.world-spawning, com.unity.modules.particlesystem | 4 | 1068 |
| Template-Game-Movement-FPS | com.deucarian.template.game.movement-fps | 0.1.1 | 6000.3 | no | clean | com.deucarian.common, com.deucarian.combat, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.run-upgrades, com.unity.inputsystem, com.unity.modules.particlesystem | 5 | 539 |
| Template-Game-Survivors | com.deucarian.template.game.survivors | 0.1.1 | 6000.3 | no | clean | com.deucarian.attacks, com.deucarian.common, com.deucarian.combat, com.deucarian.encounters, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.projectiles, com.deucarian.run-upgrades, com.deucarian.weapon-systems, com.deucarian.world-spawning, com.unity.modules.particlesystem | 5 | 1153 |
| Test-Automation | com.deucarian.test-automation | 0.1.1 | 6000.3 | no | clean | (none) | 1 | 0 |
| Theming | com.deucarian.theming | 1.0.3 | 2022.3 | no | clean | com.deucarian.editor, com.deucarian.logging, com.unity.textmeshpro, com.unity.ugui, com.unity.modules.uielements | 6 | 608 |
| UI | com.deucarian.ui | 0.2.1 | 2022.3 | no | clean | com.deucarian.common, com.deucarian.theming, com.unity.ugui, com.unity.modules.uielements | 3 | 259 |
| UI-Binding | com.deucarian.ui-binding | 1.1.1 | 2021.3 | no | clean | com.deucarian.common, com.unity.ugui | 3 | 75 |
| UI-FLow | com.deucarian.ui-flow | 0.4.1 | 2021.3 | no | clean | com.deucarian.common, com.unity.ugui, com.deucarian.logging | 6 | 341 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | 1.0.4 | 2021.3 | no | clean | com.deucarian.core-state, com.deucarian.ui-binding | 3 | 15 |
| Weapon-Systems | com.deucarian.weapon-systems | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.editor, com.deucarian.projectiles, com.deucarian.game-content-authoring | 5 | 171 |
| World-Navigation | com.deucarian.world-navigation | 0.1.1 | 6000.3 | no | clean | com.deucarian.gameplay-foundation, com.deucarian.world-spawning | 4 | 96 |
| World-Spawning | com.deucarian.world-spawning | 0.2.1 | 6000.3 | no | clean | com.deucarian.common, com.deucarian.gameplay-foundation | 4 | 133 |
| XR-UI | com.deucarian.xr-ui | 0.1.1 | 2022.3 | no | clean | com.deucarian.common, com.unity.inputsystem, com.unity.textmeshpro, com.unity.ugui, com.unity.xr.core-utils, com.unity.xr.interaction.toolkit | 5 | 351 |
| XR-UI-Theming-Integration | com.deucarian.xr-ui.theming-integration | 0.1.1 | 2022.3 | no | clean | com.deucarian.theming, com.deucarian.xr-ui | 3 | 1 |

## Corrected Counts

| Metric | Count |
| --- | --- |
| Repositories | 48 |
| Parsed methods/bodies analyzed | 12669 |
| Exact AST clone groups | 68 |
| Normalized structural clone groups | 108 |
| Same-symbol semantic candidates | 29 |
| Runtime public API symbols | 7358 |
| Editor public API symbols | 2227 |
| Test public symbols excluded from production API | 3213 |
| Sample public symbols excluded from production API | 258 |
| Internal/private production symbols | 9697 |
| Public API symbols missing XML documentation | 8087 |
| Debug invocation records | 25 |
| Unity object lifetime records | 536 |
| Documentation drift findings | 28 |
| Dependency usage findings | 146 |
| Dependency cycles | 0 |

## Extraction Position

`com.deucarian.common` owns the approved Unity object lifetime primitive. `EXTRACTION_CANDIDATES.md` contains generated evidence; reviewed outcomes are maintained separately in `EXTRACTION_DECISIONS.md`.
