# Deucarian Package Capability Matrix

Schema version: 2

| Capability | Owner package | Owner repository | Current package.json consumers |
| --- | --- | --- | --- |
| logging | com.deucarian.logging | Logging | com.deucarian.api, com.deucarian.diagnostics, com.deucarian.object-loading, com.deucarian.object-selection, com.deucarian.object-selection.core-state-integration, com.deucarian.package-installer, com.deucarian.session, com.deucarian.theming, com.deucarian.ui-flow |
| editor-shell | com.deucarian.editor | Editor | com.deucarian.diagnostics, com.deucarian.logging, com.deucarian.package-installer, com.deucarian.theming |
| api-http-client | com.deucarian.api | API | com.deucarian.object-loading.api-integration, com.deucarian.session.api-integration |
| session | com.deucarian.session | Session | com.deucarian.session.api-integration |
| object-loading | com.deucarian.object-loading | Object-Loading | com.deucarian.object-loading.api-integration |
| repository-state | com.deucarian.core-state | Core-State | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| ui-binding | com.deucarian.ui-binding | UI-Binding | com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |
| ui-flow | com.deucarian.ui-flow | UI-FLow | (none) |
| world-selection | com.deucarian.object-selection | Object-Selection | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite |
| runtime-theming | com.deucarian.theming | Theming | (none) |
| diagnostics | com.deucarian.diagnostics | Diagnostics | (none) |
| package-management | com.deucarian.package-installer | Package-Installer | (none) |
| registry-metadata | (pending) | Package-Registry | (none) |
| unity-object-lifetime | com.deucarian.common | Common | com.deucarian.object-loading, com.deucarian.ui-binding, com.deucarian.ui-flow |

## Notes

- `unity-object-lifetime` is owned by `com.deucarian.common`: Implemented in com.deucarian.common.
- `Logging -> Editor` remains a review-required dependency exception.
- Capability ownership does not automatically justify adding dependencies; consumers must use the capability.
