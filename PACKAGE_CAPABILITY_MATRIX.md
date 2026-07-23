# Deucarian Package Capability Matrix

Schema version: 2

| Capability | Owner package | Owner repository | Current package.json consumers |
| --- | --- | --- | --- |
| api-http-client | com.deucarian.api | API | com.deucarian.object-loading.api-integration, com.deucarian.session.api-integration |
| build-pipeline | com.deucarian.build-pipeline | Build-Pipeline | (none) |
| camera-navigation | com.deucarian.camera-navigation | Camera-Navigation | com.deucarian.camera-navigation.input-system-integration |
| diagnostics | com.deucarian.diagnostics | Diagnostics | (none) |
| editor-shell | com.deucarian.editor | Editor | com.deucarian.attacks, com.deucarian.build-pipeline, com.deucarian.diagnostics, com.deucarian.game-content-authoring, com.deucarian.logging, com.deucarian.package-installer, com.deucarian.pointer-capture, com.deucarian.run-upgrades, com.deucarian.template.game.idle-auto-defense, com.deucarian.theming, com.deucarian.weapon-systems |
| game-content-authoring | com.deucarian.game-content-authoring | Game-Content-Authoring | com.deucarian.attacks, com.deucarian.run-upgrades, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.weapon-systems |
| logging | com.deucarian.logging | Logging | com.deucarian.api, com.deucarian.build-pipeline, com.deucarian.diagnostics, com.deucarian.object-loading, com.deucarian.object-selection, com.deucarian.object-selection.core-state-integration, com.deucarian.package-installer, com.deucarian.session, com.deucarian.theming, com.deucarian.ui-flow |
| object-loading | com.deucarian.object-loading | Object-Loading | com.deucarian.object-loading.api-integration |
| package-management | com.deucarian.package-installer | Package-Installer | (none) |
| pointer-capture | com.deucarian.pointer-capture | Pointer-Capture | (none) |
| registry-metadata | (pending) | Package-Registry | (none) |
| repository-state | com.deucarian.core-state | Core-State | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| runtime-theming | com.deucarian.theming | Theming | com.deucarian.ui, com.deucarian.xr-ui.theming-integration |
| session | com.deucarian.session | Session | com.deucarian.session.api-integration |
| shared-motion-easing | com.deucarian.common | Common | com.deucarian.camera-navigation, com.deucarian.game-content-authoring, com.deucarian.object-loading, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.ui, com.deucarian.ui-binding, com.deucarian.ui-flow, com.deucarian.world-spawning, com.deucarian.xr-ui |
| ui-binding | com.deucarian.ui-binding | UI-Binding | com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| ui-flow | com.deucarian.ui-flow | UI-FLow | (none) |
| ui-motion | com.deucarian.ui | UI | (none) |
| ui-presentation-primitives | com.deucarian.ui | UI | (none) |
| unity-object-lifetime | com.deucarian.common | Common | com.deucarian.camera-navigation, com.deucarian.game-content-authoring, com.deucarian.object-loading, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.ui, com.deucarian.ui-binding, com.deucarian.ui-flow, com.deucarian.world-spawning, com.deucarian.xr-ui |
| world-selection | com.deucarian.object-selection | Object-Selection | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite |
| xr-world-ui-controls | com.deucarian.xr-ui | XR-UI | com.deucarian.xr-ui.theming-integration |

## Notes

- `unity-object-lifetime` is owned by `com.deucarian.common`: Implemented in com.deucarian.common.
- `Logging -> Editor` remains a review-required dependency exception.
- Capability ownership does not automatically justify adding dependencies; consumers must use the capability.
