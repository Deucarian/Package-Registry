# Capability Ownership

`capabilities.json` is authoritative. This file is the human-readable ownership map contributors and Codex should read before adding helpers or dependencies.

| Capability | Owner |
| --- | --- |
| Logging facade and Unity console sink | `com.deucarian.logging` |
| Common Unity object lifetime helper | `com.deucarian.common` |
| Editor chrome, icons, resources, editor UI helpers | `com.deucarian.editor` |
| Build workflows, final-player AOT inspection, generated linker evidence, artifact manifests, headless build APIs | `com.deucarian.build-pipeline` |
| Reflection-free generated JSON serialization | Proposed `com.deucarian.serialization`; not installable yet |
| HTTP/API transport, request building, response parsing, serializer integration | `com.deucarian.api` |
| Session lifecycle and persistence contracts | `com.deucarian.session` |
| Object/content/AssetBundle loading lifecycle | `com.deucarian.object-loading` |
| Generic repository and selection state primitives | `com.deucarian.core-state` |
| Collection-to-UI synchronization | `com.deucarian.ui-binding` |
| UI navigation, routing, screens, channels, and guards | `com.deucarian.ui-flow` |
| World-object selection, hover, raycast adapters | `com.deucarian.object-selection` |
| Flat Activity membership planning, revisions, baseline restoration, model visibility state | `com.deucarian.activity-visualization` |
| Viewer navigation toolbar/action state, reference/origin wiring, input gating, view cube UX | `com.deucarian.viewer-navigation` |
| Viewer camera, lighting, URP quality, post-processing, reflection, environment, and display settings | `com.deucarian.viewer-rendering` |
| Viewer status, diagnostics, display-settings chrome, responsive layout, menu coordination, theming, and input boundaries | `com.deucarian.viewer-shell` |
| Secure browser/WebGL command transport, iframe origin/source validation, host handshake | `com.deucarian.command-routing.webgl-integration` |
| Runtime themes, palettes, and adapters | `com.deucarian.theming` |
| Local diagnostics providers, snapshots, export, overlays | `com.deucarian.diagnostics` |
| Package install/update/remove and ecosystem visualization | `com.deucarian.package-installer` |
| Registry metadata, dependency rules, AOT evidence governance, audit, validation | Package Registry |

## Ownership Rules

- A package owns only the capability listed for it.
- Consumers depend on an owner package only when they directly use that capability.
- Integration packages may depend on their declared targets and small infrastructure packages they actually use.
- Suite packages should express composition through dependencies and samples, not copied code.
- Package Installer graph code is package-specific until an audit proves it belongs elsewhere.
- Domain packages own source generation for their own runtime capability. Build Pipeline verifies neutral evidence; it does not absorb domain generators.
- A proposed owner is not installable and must not be added as a dependency until its repository and release channels exist.

## AOT And Stripping Boundary

[AOT_SAFETY.md](AOT_SAFETY.md) defines the canonical runtime-dynamic-code contract.

Build Pipeline owns:

- Inspection of the actual managed player inputs.
- Verification of package and project AOT evidence.
- Exact generated linker descriptors.
- Strict production build failure and manifest evidence.

Build Pipeline does not own JSON codecs, command registries, dependency-injection factories, or other domain-generated runtime code. Those remain with their domain owner.

Application-owned handwritten `link.xml` files are not an accepted architecture. Unavoidable compatibility boundaries declare exact types through the neutral evidence protocol.

## Serialization Boundary

The proposed `com.deucarian.serialization` package will own generated JSON codecs, compile-time contract diagnostics, and serialization AOT evidence.

The first confirmed direct consumers are:

- `com.deucarian.api`
- `com.deucarian.persistence`
- `com.deucarian.diagnostics`

Command Routing remains independent while it uses explicit handler composition and low-level token parsing. Object Loading API Integration should move diagnostic export ownership to Diagnostics rather than take a Serialization dependency for one debug helper.

## Common Boundary

Common currently owns only:

- `Deucarian.Common.UnityObjectUtility.DestroySafely(UnityEngine.Object target)`

Common must not receive unrelated APIs just because more than one repository might use them. Reusable capability extraction needs audit evidence and an owner decision first.

## Logging Boundary

Logging owns direct Unity console forwarding. Direct `UnityEngine.Debug.*` calls outside the approved Logging sink/fallback locations are policy violations.

## Editor Boundary

Editor owns editor-only shell/UI resources. It does not own runtime theming and it does not own package installation, registry, or dependency resolution.
