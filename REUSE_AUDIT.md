# Deucarian Reuse Audit

Schema version: 2

This is the hardened organization-wide audit snapshot for `Deucarian` at `develop`. It uses `tree-sitter-c-sharp` for C# parsing and records the current package sources and governance state.

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
| API | com.deucarian.api | 1.1.3 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.unitywebrequest, com.unity.nuget.newtonsoft-json, com.unity.modules.assetbundle, com.unity.modules.unitywebrequestassetbundle, com.unity.modules.unitywebrequesttexture, com.unity.modules.unitywebrequestwww | 4 | 169 |
| Attacks | com.deucarian.attacks | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.editor, com.deucarian.game-content-authoring | 4 | 389 |
| Auto-Defense | com.deucarian.auto-defense | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.defense-games, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems | 4 | 112 |
| Auto-Defense-Suite | com.deucarian.auto-defense-suite | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.combat, com.deucarian.encounters, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.defense-games, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems, com.deucarian.auto-defense, com.deucarian.run-upgrades, com.deucarian.idle-progression | 0 | 0 |
| Bootstrap | com.deucarian.bootstrap | 1.1.3 | 2021.3 | yes | clean | (none) | 2 | 1 |
| Build-Pipeline | com.deucarian.build-pipeline | 0.2.1 | 6000.0 | yes | clean | com.deucarian.editor, com.deucarian.logging | 2 | 53 |
| Camera-Navigation | com.deucarian.camera-navigation | 0.1.0 | 2022.3 | yes | clean | com.deucarian.common | 2 | 76 |
| Combat | com.deucarian.combat | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation | 2 | 218 |
| Common | com.deucarian.common | 0.2.0 | 2021.3 | yes | clean | (none) | 3 | 5 |
| Core-State | com.deucarian.core-state | 1.0.1 | 2021.3 | yes | clean | (none) | 3 | 38 |
| Defense-Games | com.deucarian.defense-games | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.world-spawning, com.deucarian.world-navigation | 3 | 122 |
| Diagnostics | com.deucarian.diagnostics | 0.1.3 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 63 |
| Editor | com.deucarian.editor | 1.0.2 | 2021.3 | yes | clean | (none) | 2 | 411 |
| Encounters | com.deucarian.encounters | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation | 2 | 238 |
| Game-Content-Authoring | com.deucarian.game-content-authoring | 0.1.0 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.editor, com.deucarian.gameplay-foundation | 2 | 1209 |
| Gameplay-Foundation | com.deucarian.gameplay-foundation | 0.1.0 | 2021.3 | yes | clean | (none) | 2 | 131 |
| Idle-Progression | com.deucarian.idle-progression | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.progression | 3 | 24 |
| Logging | com.deucarian.logging | 1.0.1 | 2021.3 | yes | clean | com.deucarian.editor | 4 | 69 |
| Monetization | com.deucarian.monetization | 0.1.0 | 6000.3 | yes | clean | (none) | 2 | 76 |
| Object-Loading | com.deucarian.object-loading | 1.2.1 | 2021.3 | yes | clean | com.deucarian.common, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 246 |
| Object-Selection | com.deucarian.object-selection | 1.0.3 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.physics | 3 | 104 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | 0.2.5 | 2021.3 | yes | clean | com.unity.nuget.newtonsoft-json, com.deucarian.api, com.deucarian.object-loading | 2 | 30 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | 1.0.3 | 2021.3 | yes | clean | com.deucarian.logging, com.deucarian.object-selection, com.deucarian.core-state | 3 | 10 |
| Package-Installer | com.deucarian.package-installer | 1.1.69 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging | 2 | 0 |
| Package-Registry | (none) | (none) | (none) | yes | clean | (none) | 0 | 0 |
| Persistence | com.deucarian.persistence | 0.1.0 | 2021.3 | yes | clean | com.unity.nuget.newtonsoft-json | 4 | 147 |
| Progression | com.deucarian.progression | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation | 2 | 159 |
| Projectiles | com.deucarian.projectiles | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.attacks, com.deucarian.world-navigation, com.deucarian.world-spawning | 2 | 120 |
| Run-Upgrades | com.deucarian.run-upgrades | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.weapon-systems, com.deucarian.editor, com.deucarian.game-content-authoring | 4 | 172 |
| Selection-Suite | com.deucarian.selection-suite | 1.0.3 | 2021.3 | yes | clean | com.deucarian.object-selection.core-state-integration, com.deucarian.core-state, com.deucarian.ui-binding.core-state-integration, com.deucarian.ui-binding, com.deucarian.object-selection | 1 | 0 |
| Session | com.deucarian.session | 1.0.4 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.jsonserialize | 3 | 65 |
| Session-API-Integration | com.deucarian.session.api-integration | 1.0.4 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.session | 3 | 3 |
| Template-Game-Idle-Auto-Defense | com.deucarian.template.game.idle-auto-defense | 0.1.1 | 6000.3 | yes | clean | com.deucarian.auto-defense-suite, com.deucarian.editor, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.monetization | 4 | 1068 |
| Template-Game-Movement-FPS | com.deucarian.template.game.movement-fps | 0.1.0 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.combat, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.run-upgrades, com.unity.inputsystem | 5 | 539 |
| Template-Game-Survivors | com.deucarian.template.game.survivors | 0.1.0 | 6000.3 | yes | clean | com.deucarian.attacks, com.deucarian.common, com.deucarian.combat, com.deucarian.encounters, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.projectiles, com.deucarian.run-upgrades, com.deucarian.weapon-systems, com.deucarian.world-spawning | 5 | 1153 |
| Test-Automation | com.deucarian.test-automation | 0.1.0 | 6000.3 | yes | clean | (none) | 1 | 0 |
| Theming | com.deucarian.theming | 1.0.2 | 2022.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.textmeshpro, com.unity.ugui, com.unity.modules.uielements | 4 | 608 |
| UI | com.deucarian.ui | 0.2.0 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.theming, com.unity.ugui, com.unity.modules.uielements | 2 | 184 |
| UI-Binding | com.deucarian.ui-binding | 1.1.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui | 3 | 75 |
| UI-FLow | com.deucarian.ui-flow | 0.4.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui, com.deucarian.logging | 6 | 341 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | 1.0.3 | 2021.3 | yes | clean | com.deucarian.core-state, com.deucarian.ui-binding | 3 | 15 |
| Weapon-Systems | com.deucarian.weapon-systems | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.editor, com.deucarian.projectiles, com.deucarian.game-content-authoring | 4 | 171 |
| World-Navigation | com.deucarian.world-navigation | 0.1.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.world-spawning | 3 | 96 |
| World-Spawning | com.deucarian.world-spawning | 0.2.0 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.gameplay-foundation | 3 | 133 |
| XR-UI | com.deucarian.xr-ui | 0.1.0 | 2022.3 | yes | clean | com.deucarian.common, com.unity.inputsystem, com.unity.textmeshpro, com.unity.ugui, com.unity.xr.core-utils, com.unity.xr.interaction.toolkit | 3 | 351 |
| XR-UI-Theming-Integration | com.deucarian.xr-ui.theming-integration | 0.1.0 | 2022.3 | yes | clean | com.deucarian.theming, com.deucarian.xr-ui | 2 | 1 |

## Corrected Counts

| Metric | Count |
| --- | --- |
| Repositories | 46 |
| Parsed methods/bodies analyzed | 12131 |
| Exact AST clone groups | 67 |
| Normalized structural clone groups | 109 |
| Same-symbol semantic candidates | 29 |
| Runtime public API symbols | 7108 |
| Editor public API symbols | 2087 |
| Test public symbols excluded from production API | 3039 |
| Sample public symbols excluded from production API | 225 |
| Internal/private production symbols | 9336 |
| Public API symbols missing XML documentation | 7764 |
| Debug invocation records | 25 |
| Unity object lifetime records | 487 |
| Documentation drift findings | 26 |
| Dependency usage findings | 147 |
| Dependency cycles | 0 |

## Extraction Position

`com.deucarian.common` owns the approved Unity object lifetime primitive. `EXTRACTION_CANDIDATES.md` contains generated evidence; reviewed outcomes are maintained separately in `EXTRACTION_DECISIONS.md`.
