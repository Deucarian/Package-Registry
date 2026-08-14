# Deucarian AOT and Stripping Safety Standard

This document defines the ecosystem-wide contract for code that UnityLinker or an AOT backend cannot prove reachable through ordinary static calls.

## Goal

For Deucarian-owned player code:

```text
unbounded runtime reflection = 0
handwritten project link.xml files = 0
unknown runtime targets = 0
```

Editor-only reflection is allowed because Editor assemblies are not part of the player and are not subject to player stripping. Third-party or framework boundaries that cannot be rewritten must be isolated, exact, documented, tested, and machine-verifiable.

## Required strategy

Every runtime-dynamic feature must use one of these strategies:

1. **Generated** — a source generator or build step emits ordinary direct calls, factories, registries, serializers, or callback tables.
2. **Explicit composition** — application code constructs and registers the concrete runtime objects directly.
3. **Declared** — an unavoidable compatibility boundary identifies the exact call site and every hidden player type that must remain reachable.
4. **Framework** — a narrowly audited external framework owns its own AOT behavior and the adapter documents why no Deucarian declaration is required.

Anything outside those strategies is rejected by an enforced production build.

`Generated` and explicit composition are preferred. `Declared` is a migration or vendor-compatibility mechanism, not permission to add a new reflection framework.

## Ownership

- A domain package owns generation for its own domain. Command Routing owns command registries; a DI package would own service factories; a serialization package owns generated codecs.
- `com.deucarian.build-pipeline` owns final-player inspection, evidence verification, generated linker input, build-manifest reporting, and strict build enforcement.
- Package Registry owns this neutral evidence protocol and architecture policy.
- Consumer projects own project-specific composition and exact third-party exceptions.
- No runtime package depends on Build Pipeline merely to emit evidence.

## Assembly evidence protocol v1

Generators and integration packages emit standard `System.Reflection.AssemblyMetadataAttribute` values. Multiple attributes with the same key are allowed.

### Generated feature

```csharp
[assembly: AssemblyMetadata(
    "Deucarian.AOT.Feature",
    "serialization-json")]
```

The value is a stable, lower-case feature identifier.

### Exact dynamic-call exception

```csharp
[assembly: AssemblyMetadata(
    "Deucarian.AOT.Exception",
    "Vendor.Factory|Create|System.Activator::CreateInstance|Declared|Vendor compatibility boundary.")]
```

The value format is:

```text
declaringType|method|calledApi|strategy|reason
```

The assembly containing the attribute is the calling assembly. Fields are exact and pipe characters are not allowed inside field values.

### Exact preserve target

```csharp
[assembly: AssemblyMetadata(
    "Deucarian.AOT.PreserveType",
    "Vendor.Runtime|Vendor.CallbackReceiver|Constructed by the vendor boundary.")]
```

The value format is:

```text
assemblyName|fullTypeName|reason
```

Build Pipeline verifies the assembly and type against the managed player inputs before generating linker data. Wildcards and assembly-wide preservation are not part of protocol v1.

A package using a `Declared` exception must emit at least one exact preserve target. A stale declaration is a build finding and an enforced build failure.

## Project policy

Projects may version exact compatibility declarations at:

```text
ProjectSettings/DeucarianAotSafety.json
```

Project policy uses the same strategies and exact type declarations as package evidence. It must not contain secrets or machine-specific paths.

The default migration mode is `Audit`. Production CI must move to `Enforce` once existing findings are classified and migrated.

## Manual linker files

Application-owned `Assets/**/link.xml` files are forbidden in enforced builds.

Generated descriptors under `Library` are allowed because they are deterministic build intermediates derived from verified evidence. Opaque third-party package linker files may remain temporarily, but they must be surfaced by the ecosystem audit and replaced by package-owned evidence whenever the package is under Deucarian control.

## Serialization

Reflection-based object mapping is one use of runtime reflection, not the entire AOT problem.

The planned `com.deucarian.serialization` package will own reflection-free generated JSON codecs and their analyzer. API, Persistence, and Diagnostics are the first confirmed direct consumers. The package is not registered as installable until its repository, analyzer binary, tests, and stable/development channels exist.

Low-level token parsing with explicit field reads is allowed because it does not discover application object members at runtime.

## Package review requirements

A package review must determine whether runtime code uses:

- `System.Reflection`, `Type`, `Assembly`, or `Activator` for discovery or invocation.
- Reflection-based serializers.
- Runtime generic construction or expression compilation.
- String-based Unity dispatch.
- Native callbacks or plugin entry points not statically referenced.
- Package or project `link.xml` files.

Every occurrence is classified as generated, explicitly composed, declared, framework-owned, or forbidden. Editor-only and test-only occurrences are recorded separately and do not require player evidence.

## Build evidence

An enforced build manifest must record at least:

- Safety mode.
- Whether final linker inspection completed.
- Managed assemblies inspected.
- Generated feature IDs.
- Exact declared exceptions.
- Exact preserved types.
- Generated descriptor path.
- Manual project linker files.
- Unresolved findings.

A successful production build with `Enforce` means no unresolved finding remains. It does not guarantee that a live server will send schema-compatible data; external contract and smoke tests remain required.

## CI release gate

The production flow is:

```text
compile
static/package validation
EditMode tests
PlayMode tests
Enforce AOT inspection
player build
stripped-player smoke test
immutable artifact publication
deployment and post-deploy checks
```

Build and deployment are separate. Deployment consumes the tested artifact and does not rebuild it.
