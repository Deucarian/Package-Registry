# Deucarian Package Capability Matrix

Generated: 2026-06-22

This matrix records capability ownership before migration. It is intentionally conservative: ownership does not imply every package should depend on the owner. Consumers should add dependencies only when they use the capability.

| Capability | Owner package | Owner repository | Current package.json consumers | Notes |
| --- | --- | --- | --- | --- |
| logging | com.deucarian.logging | Logging | com.deucarian.api, com.deucarian.diagnostics, com.deucarian.object-loading, com.deucarian.object-selection, com.deucarian.object-selection.core-state-integration, com.deucarian.package-installer, com.deucarian.session, com.deucarian.theming |  |
| editor-shell | com.deucarian.editor | Editor | com.deucarian.diagnostics, com.deucarian.logging, com.deucarian.package-installer, com.deucarian.theming |  |
| api-http-client | com.deucarian.api | API | com.deucarian.object-loading.api-integration, com.deucarian.session.api-integration |  |
| session | com.deucarian.session | Session | com.deucarian.session.api-integration |  |
| object-loading | com.deucarian.object-loading | Object-Loading | com.deucarian.object-loading.api-integration |  |
| repository-state | com.deucarian.core-state | Core-State | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |  |
| ui-binding | com.deucarian.ui-binding | UI-Binding | com.deucarian.selection-suite, com.deucarian.ui-binding.core-state-integration |  |
| ui-flow | com.deucarian.ui-flow | UI-FLow | (none) |  |
| world-selection | com.deucarian.object-selection | Object-Selection | com.deucarian.object-selection.core-state-integration, com.deucarian.selection-suite |  |
| runtime-theming | com.deucarian.theming | Theming | (none) |  |
| diagnostics | com.deucarian.diagnostics | Diagnostics | (none) |  |
| package-management | com.deucarian.package-installer | Package-Installer | (none) |  |
| registry-metadata | (pending) | Package-Registry | (none) |  |
| unity-object-lifetime | (pending) | (pending) | (none) |  |

## Governance Notes

- Bootstrap remains outside the normal dependency graph for first-time setup and repair.
- `unity-object-lifetime` is pending the dedicated DestroyUnityObject audit; no Common package is created by this report.
- Logging owns logging infrastructure and Unity console forwarding; package-specific category facades may remain local when they only declare domain categories.
- Editor owns editor-only chrome, icons, resources, package path/version helpers, and editor-only UI Toolkit helpers.

Machine-readable seed: `capabilities.json`.
