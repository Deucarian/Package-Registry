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
| Activity-Visualization | com.deucarian.activity-visualization | 0.1.0 | 2021.3 | yes | clean | com.deucarian.diagnostics, com.deucarian.logging | 3 | 111 |
| API | com.deucarian.api | 2.1.0 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.modules.unitywebrequest, com.unity.nuget.newtonsoft-json, com.unity.modules.assetbundle, com.unity.modules.unitywebrequestassetbundle, com.unity.modules.unitywebrequesttexture, com.unity.modules.unitywebrequestwww, com.deucarian.diagnostics | 6 | 397 |
| Attacks | com.deucarian.attacks | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.editor, com.deucarian.game-content-authoring, com.deucarian.diagnostics | 8 | 445 |
| Auto-Defense | com.deucarian.auto-defense | 0.1.1 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.defense-games, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems | 4 | 112 |
| Auto-Defense-Suite | com.deucarian.auto-defense-suite | 0.1.1 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.combat, com.deucarian.encounters, com.deucarian.world-spawning, com.deucarian.world-navigation, com.deucarian.defense-games, com.deucarian.attacks, com.deucarian.projectiles, com.deucarian.weapon-systems, com.deucarian.auto-defense, com.deucarian.run-upgrades, com.deucarian.idle-progression | 1 | 0 |
| Bootstrap | com.deucarian.bootstrap | 1.2.15 | 2021.3 | yes | clean | (none) | 2 | 3 |
| Build-Pipeline | com.deucarian.build-pipeline | 0.6.5 | 6000.0 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.mono-cecil | 2 | 89 |
| Camera-Navigation | com.deucarian.camera-navigation | 0.4.0 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.editor, com.deucarian.diagnostics, com.unity.modules.imgui, com.unity.render-pipelines.universal | 7 | 225 |
| CameraNavigation-InputSystem-Integration | com.deucarian.camera-navigation.input-system-integration | 0.1.7 | 2022.3 | yes | clean | com.deucarian.camera-navigation, com.unity.inputsystem | 4 | 84 |
| Combat | com.deucarian.combat | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.editor, com.deucarian.diagnostics | 8 | 305 |
| Command-Routing | com.deucarian.command-routing | 0.3.0 | 2021.3 | yes | clean | com.deucarian.diagnostics, com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 6 | 181 |
| Command-Routing-UDP-Integration | com.deucarian.command-routing.udp-integration | 0.1.6 | 2021.3 | yes | clean | com.deucarian.command-routing, com.deucarian.diagnostics, com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 41 |
| Command-Routing-WebGL-Integration | com.deucarian.command-routing.webgl-integration | 0.1.7 | 2021.3 | yes | clean | com.deucarian.command-routing, com.deucarian.diagnostics, com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 46 |
| Common | com.deucarian.common | 0.3.0 | 2021.3 | yes | clean | (none) | 5 | 6 |
| Core-State | com.deucarian.core-state | 1.1.0 | 2021.3 | yes | clean | (none) | 4 | 41 |
| Defense-Games | com.deucarian.defense-games | 0.1.1 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.encounters, com.deucarian.combat, com.deucarian.world-spawning, com.deucarian.world-navigation | 4 | 122 |
| Diagnostics | com.deucarian.diagnostics | 0.2.4 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 65 |
| Editor | com.deucarian.editor | 1.13.0 | 2021.3 | yes | clean | (none) | 4 | 1152 |
| Encounters | com.deucarian.encounters | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.editor, com.deucarian.diagnostics, com.deucarian.world-spawning | 8 | 296 |
| Game-Content-Authoring | com.deucarian.game-content-authoring | 0.3.0 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.editor, com.deucarian.gameplay-foundation | 2 | 1275 |
| Gameplay-Foundation | com.deucarian.gameplay-foundation | 0.2.0 | 2021.3 | yes | clean | com.deucarian.editor | 7 | 203 |
| Idle-Progression | com.deucarian.idle-progression | 0.1.1 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.progression | 3 | 24 |
| Logging | com.deucarian.logging | 1.0.8 | 2021.3 | yes | clean | com.deucarian.editor | 5 | 70 |
| Media | com.deucarian.media | 0.2.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.modules.audio, com.unity.modules.unitywebrequest, com.unity.modules.unitywebrequestaudio, com.unity.modules.video, com.deucarian.editor | 8 | 149 |
| Media-API-Integration | com.deucarian.media.api-integration | 0.1.0 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.media | 3 | 13 |
| Monetization | com.deucarian.monetization | 0.2.0 | 6000.3 | yes | clean | com.deucarian.editor, com.deucarian.diagnostics | 8 | 146 |
| Notifications | com.deucarian.notifications | 0.5.0 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.diagnostics, com.deucarian.editor, com.deucarian.theming, com.deucarian.ui, com.unity.textmeshpro, com.unity.ugui | 10 | 255 |
| Object-Loading | com.deucarian.object-loading | 1.3.0 | 2021.3 | yes | clean | com.deucarian.common, com.deucarian.logging, com.unity.nuget.newtonsoft-json, com.deucarian.editor | 9 | 292 |
| Object-Selection | com.deucarian.object-selection | 1.1.0 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.physics | 4 | 135 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | 0.2.9 | 2021.3 | yes | clean | com.unity.nuget.newtonsoft-json, com.deucarian.api, com.deucarian.object-loading | 3 | 48 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | 1.0.4 | 2021.3 | yes | clean | com.deucarian.logging, com.deucarian.object-selection, com.deucarian.core-state | 3 | 25 |
| Package-Installer | com.deucarian.package-installer | 1.7.0 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging | 2 | 18 |
| Package-Registry | (none) | (none) | (none) | yes | clean | (none) | 0 | 0 |
| Persistence | com.deucarian.persistence | 0.2.0 | 2021.3 | yes | clean | com.unity.nuget.newtonsoft-json, com.deucarian.editor | 7 | 177 |
| Pointer-Capture | com.deucarian.pointer-capture | 0.2.0 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.diagnostics, com.deucarian.editor | 5 | 70 |
| Progression | com.deucarian.progression | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.editor | 8 | 262 |
| Projectiles | com.deucarian.projectiles | 0.3.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.combat, com.deucarian.attacks, com.deucarian.world-navigation, com.deucarian.world-spawning, com.deucarian.editor | 6 | 162 |
| Run-Upgrades | com.deucarian.run-upgrades | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.weapon-systems, com.deucarian.editor, com.deucarian.game-content-authoring, com.deucarian.diagnostics, com.deucarian.combat | 8 | 222 |
| Selection-Suite | com.deucarian.selection-suite | 1.0.4 | 2021.3 | yes | clean | com.deucarian.object-selection.core-state-integration, com.deucarian.core-state, com.deucarian.ui-binding.core-state-integration, com.deucarian.ui-binding, com.deucarian.object-selection | 1 | 0 |
| Session | com.deucarian.session | 1.1.0 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.jsonserialize | 4 | 78 |
| Session-API-Integration | com.deucarian.session.api-integration | 1.3.0 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.session, com.unity.nuget.newtonsoft-json | 3 | 62 |
| Simultria-API | com.deucarian.simultria-api | 1.2.2 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.editor, com.deucarian.session, com.deucarian.session.api-integration, com.deucarian.authentication, com.unity.nuget.newtonsoft-json | 5 | 197 |
| Simultria-Viewer-Connection | com.deucarian.simultria-viewer-integration | 1.3.1 | 6000.0 | yes | clean | com.deucarian.api, com.deucarian.build-pipeline, com.deucarian.command-routing, com.deucarian.editor, com.deucarian.logging, com.deucarian.session, com.deucarian.simultria-api, com.deucarian.authentication, com.unity.nuget.newtonsoft-json | 3 | 221 |
| Template-Game-Idle-Auto-Defense | com.deucarian.template.game.idle-auto-defense | 0.1.5 | 6000.3 | yes | clean | com.deucarian.attacks, com.deucarian.auto-defense, com.deucarian.auto-defense-suite, com.deucarian.combat, com.deucarian.common, com.deucarian.defense-games, com.deucarian.editor, com.deucarian.encounters, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.idle-progression, com.deucarian.monetization, com.deucarian.persistence, com.deucarian.progression, com.deucarian.projectiles, com.deucarian.run-upgrades, com.deucarian.weapon-systems, com.deucarian.world-navigation, com.deucarian.world-spawning, com.unity.modules.particlesystem | 4 | 1079 |
| Template-Game-Movement-FPS | com.deucarian.template.game.movement-fps | 0.1.3 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.combat, com.deucarian.editor, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.run-upgrades, com.unity.inputsystem, com.unity.modules.particlesystem | 5 | 548 |
| Template-Game-Survivors | com.deucarian.template.game.survivors | 0.1.4 | 6000.3 | yes | clean | com.deucarian.attacks, com.deucarian.common, com.deucarian.combat, com.deucarian.encounters, com.deucarian.editor, com.deucarian.game-content-authoring, com.deucarian.gameplay-foundation, com.deucarian.persistence, com.deucarian.progression, com.deucarian.projectiles, com.deucarian.run-upgrades, com.deucarian.weapon-systems, com.deucarian.world-spawning, com.unity.modules.particlesystem | 5 | 1172 |
| Template-Viewer | com.deucarian.template.viewer | 0.3.2 | 6000.0 | yes | clean | com.deucarian.api, com.deucarian.camera-navigation, com.deucarian.command-routing, com.deucarian.common, com.deucarian.diagnostics, com.deucarian.logging, com.deucarian.object-loading, com.deucarian.object-loading.api-integration, com.deucarian.session, com.deucarian.session.api-integration, com.deucarian.theming, com.deucarian.ui, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.viewer-shell, com.deucarian.authentication, com.unity.nuget.newtonsoft-json, com.unity.modules.uielements | 4 | 214 |
| Template-Viewer-Web | com.deucarian.template.viewer.web | 0.6.1 | 6000.0 | yes | clean | com.deucarian.build-pipeline, com.deucarian.command-routing, com.deucarian.command-routing.webgl-integration, com.deucarian.diagnostics, com.deucarian.template.viewer, com.deucarian.theming, com.deucarian.authentication, com.deucarian.webgl-template, com.unity.textmeshpro, com.unity.nuget.newtonsoft-json | 8 | 50 |
| Test-Automation | com.deucarian.test-automation | 0.1.3 | 6000.3 | yes | clean | com.deucarian.editor | 2 | 0 |
| Theming | com.deucarian.theming | 1.10.0 | 2022.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.deucarian.media, com.unity.textmeshpro, com.unity.ugui, com.unity.modules.uielements | 9 | 981 |
| UI | com.deucarian.ui | 0.3.0 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.theming, com.unity.ugui, com.unity.modules.uielements | 4 | 536 |
| UI-Binding | com.deucarian.ui-binding | 1.2.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui | 4 | 83 |
| UI-FLow | com.deucarian.ui-flow | 0.5.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui, com.deucarian.logging, com.deucarian.editor | 8 | 375 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | 1.0.4 | 2021.3 | yes | clean | com.deucarian.core-state, com.deucarian.ui-binding | 3 | 15 |
| Viewer-Authentication | com.deucarian.authentication | 1.1.0 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.editor, com.deucarian.session, com.deucarian.session.api-integration, com.unity.nuget.newtonsoft-json | 6 | 163 |
| Viewer-Navigation | com.deucarian.viewer-navigation | 0.4.0 | 2022.3 | yes | clean | com.deucarian.camera-navigation, com.deucarian.camera-navigation.input-system-integration, com.deucarian.common, com.deucarian.diagnostics, com.deucarian.editor, com.deucarian.logging, com.deucarian.pointer-capture, com.deucarian.theming, com.deucarian.ui, com.unity.ugui, com.unity.modules.uielements, com.unity.render-pipelines.universal | 6 | 190 |
| Viewer-Rendering | com.deucarian.viewer-rendering | 0.1.0 | 6000.0 | yes | clean | com.deucarian.common, com.deucarian.diagnostics, com.deucarian.logging, com.deucarian.theming, com.unity.render-pipelines.universal | 4 | 179 |
| Viewer-Shell | com.deucarian.viewer-shell | 0.1.0 | 6000.0 | yes | clean | com.deucarian.common, com.deucarian.theming, com.deucarian.ui, com.deucarian.viewer-rendering, com.unity.modules.uielements | 2 | 90 |
| Weapon-Systems | com.deucarian.weapon-systems | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.attacks, com.deucarian.editor, com.deucarian.projectiles, com.deucarian.game-content-authoring, com.deucarian.diagnostics, com.deucarian.combat | 8 | 224 |
| Web-Viewer-Suite | com.deucarian.web-viewer-suite | 0.2.0 | 6000.0 | yes | clean | com.deucarian.api, com.deucarian.build-pipeline, com.deucarian.camera-navigation, com.deucarian.camera-navigation.input-system-integration, com.deucarian.command-routing, com.deucarian.command-routing.webgl-integration, com.deucarian.diagnostics, com.deucarian.object-loading, com.deucarian.object-loading.api-integration, com.deucarian.pointer-capture, com.deucarian.session, com.deucarian.session.api-integration, com.deucarian.theming, com.deucarian.ui, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.viewer-shell, com.deucarian.authentication, com.deucarian.webgl-template, com.unity.nuget.newtonsoft-json | 1 | 0 |
| WebGL-Template | com.deucarian.webgl-template | 0.1.1 | 6000.0 | yes | clean | com.deucarian.build-pipeline, com.unity.modules.jsonserialize | 3 | 10 |
| World-Navigation | com.deucarian.world-navigation | 0.2.0 | 6000.3 | yes | clean | com.deucarian.gameplay-foundation, com.deucarian.world-spawning, com.deucarian.diagnostics, com.deucarian.editor | 7 | 142 |
| World-Spawning | com.deucarian.world-spawning | 0.3.0 | 6000.3 | yes | clean | com.deucarian.common, com.deucarian.gameplay-foundation, com.deucarian.editor | 7 | 208 |
| XR-UI | com.deucarian.xr-ui | 0.4.0 | 2022.3 | yes | clean | com.deucarian.theming, com.deucarian.common, com.deucarian.editor, com.unity.inputsystem, com.unity.textmeshpro, com.unity.ugui, com.unity.xr.core-utils, com.unity.xr.interaction.toolkit | 6 | 368 |
| XR-UI-Theming-Integration | com.deucarian.xr-ui.theming-integration | 0.3.1 | 2022.3 | yes | clean | com.deucarian.common, com.deucarian.theming, com.deucarian.xr-ui | 4 | 2 |

## Corrected Counts

| Metric | Count |
| --- | --- |
| Repositories | 65 |
| Parsed methods/bodies analyzed | 21413 |
| Exact AST clone groups | 97 |
| Normalized structural clone groups | 168 |
| Same-symbol semantic candidates | 41 |
| Runtime public API symbols | 10848 |
| Editor public API symbols | 3606 |
| Test public symbols excluded from production API | 7663 |
| Sample public symbols excluded from production API | 638 |
| Internal/private production symbols | 19095 |
| Public API symbols missing XML documentation | 11858 |
| Debug invocation records | 17 |
| Unity object lifetime records | 1203 |
| Documentation drift findings | 52 |
| Dependency usage findings | 283 |
| Dependency cycles | 0 |

## Extraction Position

`com.deucarian.common` owns the approved Unity object lifetime primitive. `EXTRACTION_CANDIDATES.md` contains generated evidence; reviewed outcomes are maintained separately in `EXTRACTION_DECISIONS.md`.
