# Capability Ownership

`capabilities.json` is authoritative. This file is the human-readable ownership map contributors and Codex should read before adding helpers or dependencies.

| Capability | Owner |
| --- | --- |
| Logging facade and Unity console sink | `com.deucarian.logging` |
| Common Unity object lifetime helper | `com.deucarian.common` |
| Editor chrome, icons, resources, editor UI helpers | `com.deucarian.editor` |
| HTTP/API transport, request building, response parsing | `com.deucarian.api` |
| Session lifecycle and persistence contracts | `com.deucarian.session` |
| Object/content/AssetBundle loading lifecycle | `com.deucarian.object-loading` |
| Generic repository and selection state primitives | `com.deucarian.core-state` |
| Collection-to-UI synchronization | `com.deucarian.ui-binding` |
| UI navigation, routing, screens, channels, and guards | `com.deucarian.ui-flow` |
| World-object selection, hover, raycast adapters | `com.deucarian.object-selection` |
| Runtime themes, palettes, and adapters | `com.deucarian.theming` |
| Local diagnostics providers, snapshots, export, overlays | `com.deucarian.diagnostics` |
| Package install/update/remove and ecosystem visualization | `com.deucarian.package-installer` |
| Registry metadata, dependency rules, audit, validation | Package Registry |

## Ownership Rules

- A package owns only the capability listed for it.
- Consumers depend on an owner package only when they directly use that capability.
- Integration packages may depend on their declared targets and small infrastructure packages they actually use.
- Suite packages should express composition through dependencies and samples, not copied code.
- Package Installer graph code is package-specific until an audit proves it belongs elsewhere.

## Common Boundary

Common currently owns only:

- `Deucarian.Common.UnityObjectUtility.DestroySafely(UnityEngine.Object target)`

Common must not receive unrelated APIs just because more than one repository might use them. Reusable capability extraction needs audit evidence and an owner decision first.

## Logging Boundary

Logging owns direct Unity console forwarding. Direct `UnityEngine.Debug.*` calls outside the approved Logging sink/fallback locations are policy violations.

## Editor Boundary

Editor owns editor-only shell/UI resources. It does not own runtime theming and it does not own package installation, registry, or dependency resolution.
