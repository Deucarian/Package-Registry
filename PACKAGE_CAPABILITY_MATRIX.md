# Deucarian Package Capability Matrix

Schema version: 2

| Capability | Owner package | Owner repository | Current package.json consumers |
| --- | --- | --- | --- |
| activity-model-visualization | com.deucarian.activity-visualization | Activity-Visualization | (none) |
| aot-stripping-safety | com.deucarian.build-pipeline | Build-Pipeline | com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| api-http-client | com.deucarian.api | API | com.deucarian.media.api-integration, com.deucarian.object-loading.api-integration, com.deucarian.session.api-integration, com.deucarian.simultria-api, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.viewer-authentication, com.deucarian.web-viewer-suite |
| build-pipeline | com.deucarian.build-pipeline | Build-Pipeline | com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| camera-navigation | com.deucarian.camera-navigation | Camera-Navigation | com.deucarian.camera-navigation.input-system-integration, com.deucarian.template.viewer.web, com.deucarian.viewer-navigation, com.deucarian.web-viewer-suite |
| command-protocol | com.deucarian.command-routing | Command-Routing | com.deucarian.command-routing.udp-integration, com.deucarian.command-routing.webgl-integration, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.viewer-authentication, com.deucarian.web-viewer-suite |
| command-routing | com.deucarian.command-routing | Command-Routing | com.deucarian.command-routing.udp-integration, com.deucarian.command-routing.webgl-integration, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.viewer-authentication, com.deucarian.web-viewer-suite |
| command-routing-udp-transport | com.deucarian.command-routing.udp-integration | Command-Routing-UDP-Integration | (none) |
| command-routing-webgl-transport | com.deucarian.command-routing.webgl-integration | Command-Routing-WebGL-Integration | com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| diagnostics | com.deucarian.diagnostics | Diagnostics | com.deucarian.activity-visualization, com.deucarian.command-routing, com.deucarian.command-routing.udp-integration, com.deucarian.command-routing.webgl-integration, com.deucarian.template.viewer.web, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.web-viewer-suite |
| editor-shell | com.deucarian.editor | Editor | com.deucarian.api, com.deucarian.attacks, com.deucarian.build-pipeline, com.deucarian.camera-navigation, com.deucarian.command-routing, com.deucarian.command-routing.udp-integration, com.deucarian.command-routing.webgl-integration, com.deucarian.diagnostics, com.deucarian.game-content-authoring, com.deucarian.logging, com.deucarian.package-installer, com.deucarian.pointer-capture, com.deucarian.run-upgrades, com.deucarian.simultria-api, com.deucarian.simultria-viewer-connection, com.deucarian.template.game.idle-auto-defense, com.deucarian.theming, com.deucarian.viewer-authentication, com.deucarian.viewer-navigation, com.deucarian.weapon-systems |
| game-content-authoring | com.deucarian.game-content-authoring | Game-Content-Authoring | com.deucarian.attacks, com.deucarian.run-upgrades, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.weapon-systems |
| generated-json-serialization | (pending) | Package-Registry | (none) |
| logging | com.deucarian.logging | Logging | com.deucarian.activity-visualization, com.deucarian.api, com.deucarian.build-pipeline, com.deucarian.command-routing, com.deucarian.command-routing.udp-integration, com.deucarian.command-routing.webgl-integration, com.deucarian.diagnostics, com.deucarian.object-loading, com.deucarian.object-selection, com.deucarian.object-selection.core-state-integration, com.deucarian.package-installer, com.deucarian.session, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.theming, com.deucarian.ui-flow, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering |
| media-loading | com.deucarian.media | Media | com.deucarian.media.api-integration |
| media-playback | com.deucarian.media | Media | com.deucarian.media.api-integration |
| object-loading | com.deucarian.object-loading | Object-Loading | com.deucarian.object-loading.api-integration, com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| package-management | com.deucarian.package-installer | Package-Installer | (none) |
| pointer-capture | com.deucarian.pointer-capture | Pointer-Capture | com.deucarian.viewer-navigation, com.deucarian.web-viewer-suite |
| registry-metadata | (pending) | Package-Registry | (none) |
| repository-state | com.deucarian.core-state | Core-State | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| runtime-theming | com.deucarian.theming | Theming | com.deucarian.template.viewer.web, com.deucarian.ui, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.viewer-shell, com.deucarian.web-viewer-suite, com.deucarian.xr-ui.theming-integration |
| session | com.deucarian.session | Session | com.deucarian.session.api-integration, com.deucarian.simultria-api, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.viewer-authentication, com.deucarian.web-viewer-suite |
| shared-motion-easing | com.deucarian.common | Common | com.deucarian.camera-navigation, com.deucarian.game-content-authoring, com.deucarian.media, com.deucarian.object-loading, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.ui, com.deucarian.ui-binding, com.deucarian.ui-flow, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.viewer-shell, com.deucarian.world-spawning, com.deucarian.xr-ui |
| simultria-api-integration | com.deucarian.simultria-api | Simultria-API | com.deucarian.simultria-viewer-connection |
| simultria-viewer-development-connection | com.deucarian.simultria-viewer-connection | Simultria-Viewer-Connection | (none) |
| ui-binding | com.deucarian.ui-binding | UI-Binding | com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| ui-flow | com.deucarian.ui-flow | UI-FLow | (none) |
| ui-motion | com.deucarian.ui | UI | com.deucarian.template.viewer.web, com.deucarian.viewer-navigation, com.deucarian.viewer-shell, com.deucarian.web-viewer-suite |
| ui-presentation-primitives | com.deucarian.ui | UI | com.deucarian.template.viewer.web, com.deucarian.viewer-navigation, com.deucarian.viewer-shell, com.deucarian.web-viewer-suite |
| unity-object-lifetime | com.deucarian.common | Common | com.deucarian.camera-navigation, com.deucarian.game-content-authoring, com.deucarian.media, com.deucarian.object-loading, com.deucarian.template.game.idle-auto-defense, com.deucarian.template.game.movement-fps, com.deucarian.template.game.survivors, com.deucarian.ui, com.deucarian.ui-binding, com.deucarian.ui-flow, com.deucarian.viewer-navigation, com.deucarian.viewer-rendering, com.deucarian.viewer-shell, com.deucarian.world-spawning, com.deucarian.xr-ui |
| viewer-authentication | com.deucarian.viewer-authentication | Viewer-Authentication | com.deucarian.simultria-api, com.deucarian.simultria-viewer-connection, com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| viewer-navigation-experience | com.deucarian.viewer-navigation | Viewer-Navigation | com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| viewer-rendering-environment | com.deucarian.viewer-rendering | Viewer-Rendering | com.deucarian.template.viewer.web, com.deucarian.viewer-shell, com.deucarian.web-viewer-suite |
| viewer-shell-experience | com.deucarian.viewer-shell | Viewer-Shell | com.deucarian.template.viewer.web, com.deucarian.web-viewer-suite |
| world-selection | com.deucarian.object-selection | Object-Selection | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite |
| xr-world-ui-controls | com.deucarian.xr-ui | XR-UI | com.deucarian.xr-ui.theming-integration |

## Notes

- `unity-object-lifetime` is owned by `com.deucarian.common`: Implemented in com.deucarian.common.
- `Logging -> Editor` remains a review-required dependency exception.
- Capability ownership does not automatically justify adding dependencies; consumers must use the capability.
