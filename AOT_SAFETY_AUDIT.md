# Deucarian AOT Safety Audit

Authoritative runtime reflection and linker inventory for `Deucarian` at `develop`.

This report inventories current package-owned player-code findings. Editor-only reflection is excluded. Audit findings are migration work; an `Enforce` package with an unresolved finding fails validation.

## Summary

- Repositories scanned: **61**
- Repositories with findings: **20**
- Clean repositories: **41**
- Unresolved findings: **66**
- Suppressed findings: **0**
- Validation failures: **0**

## Finding Categories

| Rule | Count |
| --- | ---: |
| `reflection-based-newtonsoft` | 13 |
| `reflective-invocation` | 10 |
| `runtime-type-discovery` | 43 |

## Repository Status

| Package | Repository | Mode | Findings | Suppressed | Status |
| --- | --- | --- | ---: | ---: | --- |
| `com.deucarian.activity-visualization` | `Activity-Visualization` | `Audit` | 5 | 0 | Valid |
| `com.deucarian.api` | `API` | `Audit` | 3 | 0 | Valid |
| `com.deucarian.attacks` | `Attacks` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.auto-defense` | `Auto-Defense` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.auto-defense-suite` | `Auto-Defense-Suite` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.bootstrap` | `Bootstrap` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.build-pipeline` | `Build-Pipeline` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.camera-navigation` | `Camera-Navigation` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.camera-navigation.input-system-integration` | `CameraNavigation-InputSystem-Integration` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.combat` | `Combat` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.command-routing` | `Command-Routing` | `Audit` | 3 | 0 | Valid |
| `com.deucarian.command-routing.udp-integration` | `Command-Routing-UDP-Integration` | `Audit` | 2 | 0 | Valid |
| `com.deucarian.command-routing.webgl-integration` | `Command-Routing-WebGL-Integration` | `Audit` | 2 | 0 | Valid |
| `com.deucarian.common` | `Common` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.core-state` | `Core-State` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.defense-games` | `Defense-Games` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.diagnostics` | `Diagnostics` | `Audit` | 3 | 0 | Valid |
| `com.deucarian.editor` | `Editor` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.encounters` | `Encounters` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.game-content-authoring` | `Game-Content-Authoring` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.gameplay-foundation` | `Gameplay-Foundation` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.idle-progression` | `Idle-Progression` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.logging` | `Logging` | `Audit` | 2 | 0 | Valid |
| `com.deucarian.media` | `Media` | `Audit` | 3 | 0 | Valid |
| `com.deucarian.media.api-integration` | `Media-API-Integration` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.monetization` | `Monetization` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.object-loading` | `Object-Loading` | `Audit` | 3 | 0 | Valid |
| `com.deucarian.object-loading.api-integration` | `ObjectLoading-API-Integration` | `Audit` | 1 | 0 | Valid |
| `com.deucarian.object-selection` | `Object-Selection` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.object-selection.core-state-integration` | `ObjectSelection-CoreState-Integration` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.package-installer` | `Package-Installer` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.persistence` | `Persistence` | `Audit` | 2 | 0 | Valid |
| `com.deucarian.pointer-capture` | `Pointer-Capture` | `Audit` | 1 | 0 | Valid |
| `com.deucarian.progression` | `Progression` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.projectiles` | `Projectiles` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.run-upgrades` | `Run-Upgrades` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.selection-suite` | `Selection-Suite` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.session` | `Session` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.session.api-integration` | `Session-API-Integration` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.simultria-api` | `Simultria-API` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.simultria-viewer-connection` | `Simultria-Viewer-Connection` | `Audit` | 4 | 0 | Valid |
| `com.deucarian.template.game.idle-auto-defense` | `Template-Game-Idle-Auto-Defense` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.template.game.movement-fps` | `Template-Game-Movement-FPS` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.template.game.survivors` | `Template-Game-Survivors` | `Audit` | 4 | 0 | Valid |
| `com.deucarian.template.viewer.web` | `Template-Viewer-Web` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.test-automation` | `Test-Automation` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.theming` | `Theming` | `Audit` | 4 | 0 | Valid |
| `com.deucarian.ui` | `UI` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.ui-binding` | `UI-Binding` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.ui-binding.core-state-integration` | `UIBinding-CoreState-Integration` | `Audit` | 7 | 0 | Valid |
| `com.deucarian.ui-flow` | `UI-FLow` | `Audit` | 2 | 0 | Valid |
| `com.deucarian.viewer-authentication` | `Viewer-Authentication` | `Audit` | 1 | 0 | Valid |
| `com.deucarian.viewer-navigation` | `Viewer-Navigation` | `Audit` | 1 | 0 | Valid |
| `com.deucarian.viewer-rendering` | `Viewer-Rendering` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.viewer-shell` | `Viewer-Shell` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.weapon-systems` | `Weapon-Systems` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.web-viewer-suite` | `Web-Viewer-Suite` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.world-navigation` | `World-Navigation` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.world-spawning` | `World-Spawning` | `Audit` | 0 | 0 | Valid |
| `com.deucarian.xr-ui` | `XR-UI` | `Audit` | 13 | 0 | Valid |
| `com.deucarian.xr-ui.theming-integration` | `XR-UI-Theming-Integration` | `Audit` | 0 | 0 | Valid |

## Findings

### `com.deucarian.activity-visualization`

Repository: `Activity-Visualization`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/ActivityVisualizationStateOwner.Events.cs`:90 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/ActivityVisualizationStateOwner.Events.cs`:187 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/ActivityVisualizationStateOwner.cs`:185 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/ActivityVisualizationStateOwner.cs`:254 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/ActivityVisualizationStateOwner.cs`:290 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.api`

Repository: `API`  
Mode: `Audit`

- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/Core/NewtonsoftApiSerializer.cs`:23 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `reflection-based-newtonsoft` — `JsonConvert.DeserializeObject<T>` at `Runtime/Core/NewtonsoftApiSerializer.cs`:28 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `reflection-based-newtonsoft` — `JsonConvert.DeserializeObject` at `Runtime/Core/NewtonsoftApiSerializer.cs`:33 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.command-routing`

Repository: `Command-Routing`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/CommandDispatcher.cs`:138 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflection-based-newtonsoft` — `.ToObject<T>` at `Runtime/CommandEnvelope.cs`:50 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/CommandTransportBridge.cs`:191 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.command-routing.udp-integration`

Repository: `Command-Routing-UDP-Integration`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/UdpCommandTransport.cs`:249 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/UdpCommandTransport.cs`:252 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.command-routing.webgl-integration`

Repository: `Command-Routing-WebGL-Integration`  
Mode: `Audit`

- `reflection-based-newtonsoft` — `JsonConvert.DeserializeObject<WebGlInboundMessage>` at `Runtime/WebGlCommandTransport.cs`:165 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/WebGlCommandTransport.cs`:217 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.diagnostics`

Repository: `Diagnostics`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/DeucarianLoggingDiagnosticProvider.cs`:73 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/DiagnosticReportBuilder.cs`:70 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/DiagnosticsJsonExporter.cs`:17 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.logging`

Repository: `Logging`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/DeucarianLog.cs`:252 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/DeucarianLog.cs`:253 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.media`

Repository: `Media`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetProperty` at `Runtime/Unity/UnityVideoPlaybackSession.cs`:47 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.Invoke` at `Runtime/Unity/UnityVideoPlaybackSession.cs`:328 (`Reflection member invocation/access is not allowed in player code.`)
- `reflective-invocation` — `.SetValue` at `Runtime/Unity/UnityVideoPlaybackSession.cs`:372 (`Reflection member invocation/access is not allowed in player code.`)

### `com.deucarian.object-loading`

Repository: `Object-Loading`  
Mode: `Audit`

- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/Core/ObjectLoadRequest.cs`:169 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Pipeline/DefaultObjectDiagnostics.cs`:176 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Pipeline/ObjectLoadingPipeline.cs`:281 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.object-loading.api-integration`

Repository: `ObjectLoading-API-Integration`  
Mode: `Audit`

- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/Core/ApiObjectDownloadMapper.cs`:288 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.persistence`

Repository: `Persistence`  
Mode: `Audit`

- `reflection-based-newtonsoft` — `JsonConvert.SerializeObject` at `Runtime/Serialization/Serialization.cs`:41 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `reflection-based-newtonsoft` — `JsonConvert.DeserializeObject<T>` at `Runtime/Serialization/Serialization.cs`:44 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.pointer-capture`

Repository: `Pointer-Capture`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/DeucarianPointerCaptureController.cs`:484 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.simultria-viewer-connection`

Repository: `Simultria-Viewer-Connection`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/Authentication/SimultriaViewerConnectionAuthentication.cs`:334 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Authentication/SimultriaViewerRuntimeConnectionProvider.cs`:137 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflection-based-newtonsoft` — `.FromObject` at `Runtime/Initialization/SimultriaViewerInitializationCommand.cs`:32 (`Newtonsoft object mapping discovers constructors and members through reflection.`)
- `reflection-based-newtonsoft` — `.FromObject` at `Runtime/Initialization/SimultriaViewerInitializationCommand.cs`:57 (`Newtonsoft object mapping discovers constructors and members through reflection.`)

### `com.deucarian.template.game.survivors`

Repository: `Template-Game-Survivors`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetFields` at `Runtime/SurvivorsAuthoredContent.cs`:2453 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetFields` at `Runtime/SurvivorsContentValidation.cs`:2421 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.GetValue` at `Runtime/SurvivorsContentValidation.cs`:2427 (`Reflection member invocation/access is not allowed in player code.`)
- `reflective-invocation` — `.GetValue` at `Runtime/SurvivorsContentValidation.cs`:2432 (`Reflection member invocation/access is not allowed in player code.`)

### `com.deucarian.theming`

Repository: `Theming`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/UIToolkit/DeucarianUIToolkitThemeUtility.cs`:218 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/UIToolkit/DeucarianUIToolkitThemeUtility.cs`:219 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/UIToolkit/DeucarianUIToolkitThemeUtility.cs`:239 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/UIToolkit/DeucarianUIToolkitThemeUtility.cs`:240 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.ui-binding.core-state-integration`

Repository: `UIBinding-CoreState-Integration`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/SelectionUIBinding.cs`:100 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetProperty` at `Runtime/SelectionUIBinding.cs`:101 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.GetValue` at `Runtime/SelectionUIBinding.cs`:105 (`Reflection member invocation/access is not allowed in player code.`)
- `runtime-type-discovery` — `.GetMethod` at `Runtime/SelectionUIBinding.cs`:112 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.Invoke` at `Runtime/SelectionUIBinding.cs`:121 (`Reflection member invocation/access is not allowed in player code.`)
- `runtime-type-discovery` — `.GetMethod` at `Runtime/SelectionUIBinding.cs`:125 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.Invoke` at `Runtime/SelectionUIBinding.cs`:134 (`Reflection member invocation/access is not allowed in player code.`)

### `com.deucarian.ui-flow`

Repository: `UI-FLow`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/Navigation/UIFlowContext.cs`:63 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Navigation/UIFlowPresentationState.cs`:104 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.viewer-authentication`

Repository: `Viewer-Authentication`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/ViewerRuntimeConnectionProviderRegistry.cs`:155 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.viewer-navigation`

Repository: `Viewer-Navigation`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetType` at `Runtime/ViewerNavigationUiInputBlocker.cs`:102 (`Runtime type/member discovery must be generated or explicitly composed.`)

### `com.deucarian.xr-ui`

Repository: `XR-UI`  
Mode: `Audit`

- `runtime-type-discovery` — `.GetProperty` at `Runtime/Controls/CustomInputFieldPressTarget.cs`:216 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.GetValue` at `Runtime/Controls/CustomInputFieldPressTarget.cs`:230 (`Reflection member invocation/access is not allowed in player code.`)
- `reflective-invocation` — `.SetValue` at `Runtime/Controls/CustomInputFieldPressTarget.cs`:243 (`Reflection member invocation/access is not allowed in player code.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:71 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:205 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetMethod` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:230 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:230 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `reflective-invocation` — `.Invoke` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:239 (`Reflection member invocation/access is not allowed in player code.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/Controls/CustomSelectableFeedbackInstaller.cs`:246 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/XR/XrUiPokeAffordanceInstaller.cs`:121 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/XR/XrUiPokeAffordanceInstaller.cs`:142 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/XR/XrUiPokeAffordanceInstaller.cs`:158 (`Runtime type/member discovery must be generated or explicitly composed.`)
- `runtime-type-discovery` — `.GetType` at `Runtime/XrUiControlExclusionRegistry.cs`:94 (`Runtime type/member discovery must be generated or explicitly composed.`)

## Migration Rule

Each finding is generated away, explicitly composed, exactly declared with verified preserve targets, or isolated as an audited framework boundary. Application-owned handwritten `link.xml` is not a final disposition.
