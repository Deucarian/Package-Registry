# Deucarian Architecture Rules

This is the canonical architecture standard for every Deucarian package.
Package-specific documentation may add stricter rules, but it must not copy,
replace, or weaken this document.

Canonical URL:
`https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md`

Package Registry is the single source of truth for this standard, package
metadata, capability ownership, dependency rules, and validation tooling.
Every package consumes the standard through the shared package-validation
workflow. New or refreshed repository-level `AGENTS.md` files link here
instead of copying the rules; existing package notes are migrated during the
architecture-compliance pass.

## Engineering Principles

- Apply SOLID deliberately, with single responsibility judged by reasons to
  change rather than by class count alone.
- Prefer composition over inheritance. Inheritance is reserved for genuine
  substitutability or framework requirements, never merely for code reuse.
- Depend on abstractions across capability and package boundaries; concrete
  implementations are selected only in a composition root.
- Dependency injection is allowed, and constructor injection is required for
  ordinary C# services. Unity-created objects may use serialized dependencies
  or one explicit initialization method when Unity controls construction.
- Prefer pure functions and immutable values for policy, parsing, validation,
  mapping, and state calculations.
- Isolate mutations, Unity object ownership, I/O, networking, logging, and
  other side effects behind narrow adapters.
- Deucarian-owned player code must not use unbounded runtime reflection,
  dynamic construction, runtime assembly scanning, or reflection-based object
  mapping. Generate or explicitly compose runtime paths instead.
- Unavoidable external framework or compatibility reflection must be isolated,
  exact, documented, tested, and represented through the canonical AOT
  evidence protocol in `AOT_SAFETY.md`.
- Use Strategy for interchangeable policy and platform behavior.
- Use Observer-style events or streams for state propagation; consumers must
  not poll concrete services or maintain duplicate authoritative state.
- Keep modules independently constructible and test collaborators through
  their public contracts.
- Continuous integration validation is required for every package change.

## Source And Assembly Structure

- Namespaces must follow capability ownership and folder structure.
- Runtime, editor, integration, samples, and tests belong in separate assembly
  definitions whenever their dependency or platform boundaries differ.
- Package-to-package coupling must be visible in both `package.json` and
  assembly-definition references.
- Every Deucarian-owned editor window, settings provider, inspector, and tool
  surface must compose its visual shell, chrome, styles, icons, and shared
  workflow controls from `com.deucarian.editor`. Domain packages own their
  editor workflows, not a competing visual system. The only exceptions are
  `com.deucarian.editor` itself and an exception explicitly recorded in this
  standard, currently Bootstrap's self-contained setup UI.
- A production source file must not exceed 500 lines. Files approaching the
  limit should be reviewed for extraction of policy, presentation, storage,
  platform integration, or orchestration responsibilities.
- Generated sources may exceed the limit only when generation is documented
  and the validator can identify them deterministically.
- A coordinator may sequence several abstractions, but it must not also own
  their parsing, storage, rendering, or platform-specific implementations.

## State And Behavior

- Each domain state has one authoritative owner.
- Commands mutate through an explicit command port; observers consume a
  read-only state port.
- Animation presents a state transition and must not create an alternative
  state path.
- Resource ownership and disposal must be explicit, idempotent, and covered by
  tests.
- Compatibility adapters preserve old callers at boundaries while new domain
  code depends on the preferred abstraction.

## AOT And Stripping Safety

- `AOT_SAFETY.md` is the canonical player-reachability and evidence protocol.
- Runtime-dynamic behavior must be generated, explicitly composed, exactly
  declared, or owned by a narrowly audited external framework boundary.
- Domain packages own generation for their own runtime capability. Build
  Pipeline verifies evidence and final player assemblies; it does not absorb
  domain generators.
- Runtime packages do not depend on Build Pipeline merely to emit evidence.
  Evidence uses neutral assembly metadata.
- Application-owned `Assets/**/link.xml` files are forbidden in enforced
  builds. Generated linker descriptors under `Library` are build intermediates,
  not source-controlled architecture.
- Exact declarations identify individual assemblies and types. Wildcards,
  broad assembly preservation, and undocumented exceptions are forbidden.
- Editor-only reflection is allowed when it remains in an Editor assembly and
  never enters player code.
- Production CI must use enforced AOT inspection after migration findings are
  classified and resolved.

## Governance Sources

- `packages.json` defines installable packages, canonical functional groups, artifact kinds, dependencies, Integration targets, and Suite members.
- `capabilities.json` defines which package owns each reusable capability.
- `dependency-rules.json` defines the allowed package layering model.
- `AOT_SAFETY.md` defines runtime-dynamic-code policy, evidence metadata, and stripping gates.
- `DISTRIBUTION_POLICY.md` defines active stable/development Git channels.
- `RELEASE_POLICY.md` defines deferred npm/tag/release workflow policy.
- `Tools/deucarian_package_validator.py` enforces package manifests, asmdefs, documentation, audit policy, and registry/catalog consistency.
- Generated audit artifacts (`*_AUDIT.json`, `DUPLICATION_REPORT.json`) describe current organization state and must stay in sync.
- The authoritative organization source audit provisions public catalog repositories. Packages marked `sourceVisibility: private` remain governed by registry metadata and their own package-validation workflow but are excluded from credential-free cross-repository source provisioning.

## Distribution And Release

- `main` is the stable Git distribution channel through registry `stableUrl` values.
- `develop` is the development Git distribution channel through registry `developmentUrl` values.
- npm/scoped-registry publication is deferred and must not run during branch promotion.
- Git tags and GitHub releases are deferred and must not be created automatically.
- Future npm, tag, or GitHub release publication requires a separate deliberate release wave.

## Package Roles

- Bootstrap owns first-time setup and repair only. It is self-contained by design and must not depend on Editor, Logging, Common, or Package Installer.
- Common owns tiny dependency-free runtime primitives only. It currently exposes only `Deucarian.Common.UnityObjectUtility.DestroySafely(UnityEngine.Object target)`.
- Logging owns the package logging facade and Unity console sink. Direct `UnityEngine.Debug` calls are allowed only in the approved Logging sink/fallback locations.
- Editor owns shared editor chrome, icons, editor resources, and editor-only UI Toolkit helpers. It must not own runtime theming or package installation logic.
- Build Pipeline owns Build Profile policy, final-player AOT inspection, evidence verification, generated linker input, artifact manifests, and headless build entry points. It must not own domain serialization, command routing, DI, or other runtime generators.
- Package Registry owns metadata, capability ownership, dependency rules, AOT evidence governance, and audit/validation tools. It must not contain runtime package code or editor UI implementation.
- Package Installer owns package installation, registry channel selection, dependency-first installation, and package-specific ecosystem visualization. It must not become a generic graph or UI framework.
- Authentication owns reusable target-based session composition, secure local persistence, token lifecycle, and sanitized authentication status. Backend sign-in and refresh endpoints remain application-specific adapters, and viewer command integration remains an optional assembly.
- Integration packages own adapter code between declared target packages only. They must not duplicate target-package logic or introduce independent frameworks.
- Suite packages own dependency composition, samples, and installable bundles only. They must not duplicate implementation logic.
- Functional groups answer where a package belongs; `kind` answers what is shipped. Integration and Suite are artifact kinds, not top-level domains.
- Legacy `category`, `type`, and `ecosystemGroup` fields are compatibility projections for one schema-v2 release and are not governance inputs.

## Reuse Before Extraction

Before adding a helper or local utility:

1. Search the current repository.
2. Search all Deucarian repositories.
3. Check `capabilities.json`.
4. Use the package that owns the capability.
5. Add a package dependency only when production/editor/sample code directly uses that capability.
6. Do not copy helpers between repositories.
7. Do not create a new shared package without audit evidence.
8. Do not add unrelated APIs to Common.
9. Treat generated duplication output as candidates; only the reviewed decision ledger authorizes an extraction.

## Review Standard

Architecture reviews must check:

1. The capability belongs to this package according to `capabilities.json`.
2. Dependencies point toward the declared owner and do not create a cycle.
3. Public consumers can depend on abstractions rather than concrete services.
4. Construction is explicit and testable.
5. Policies are pure where practical and side effects stay at boundaries.
6. Runtime reflection is absent, generated away, explicitly composed, or represented by exact canonical AOT evidence.
7. State has one owner and changes are observable.
8. Strategies replace branching where behavior is genuinely interchangeable.
9. Namespace, folder, and assembly-definition boundaries agree.
10. Production files stay within the 500-line responsibility limit.
11. Tests cover contracts, lifecycle/disposal, and important state transitions.
12. Every Deucarian-owned editor surface uses the shared Editor package rather than package-local chrome, styling, icons, or workflow controls.
13. Player builds do not depend on handwritten application `link.xml` files.

## Logging

- Any package that emits package-owned production logs must declare
  `com.deucarian.logging` as a required dependency and route those logs through
  its facade. Logging is not an optional consumer choice once a package owns
  log-producing behavior.
- Packages that do not emit production logs should not add Logging merely for
  symmetry.
- Direct Unity Debug calls are forbidden outside approved Logging implementation points.
- Bootstrap may remain self-contained and local for first-time setup.
- Diagnostics may observe/report diagnostics locally, but it does not own Logging.

## Common

- Common must stay small, runtime-only, dependency-free, and evidence-driven.
- Common must not grow into a generic utility bucket.
- Do not add logging, editor, JSON, networking, diagnostics, state, UI, or domain helpers to Common.
- Production Unity object cleanup outside Common should call `UnityObjectUtility.DestroySafely`.
- Test fixture teardown may use `DestroyImmediate` directly.

## Diagnostics

- Diagnostics owns local snapshots, providers, export, overlays, and diagnostics views.
- Diagnostics does not own telemetry/uploading.
- Operational packages must declare `com.deucarian.diagnostics` as a required
  dependency and automatically register sanitized providers for their live
  operational instances. Operational packages own runtime state, I/O,
  networking, async work, connections, queues, caches, resource lifecycles, or
  other behavior whose health cannot be understood from pure return values
  alone.
- Pure policy/value packages, passive data contracts, editor-only authoring
  packages, integration-free adapters with no owned operational state, and
  implementation-free Suite packages may omit Diagnostics.
- Diagnostics must expose health and lifecycle metadata without retaining
  secrets or application payloads. Registration and disposal are explicit,
  idempotent, and tested.
- A package must not offer diagnostics as a consumer-facing toggle when the
  package itself meets the operational definition above.

## Editor Surfaces

- Any package that owns a custom editor window, settings provider, inspector,
  wizard, simulator, or diagnostics surface must declare
  `com.deucarian.editor` as a required dependency.
- Editor surfaces consume the Editor package's public chrome, workbench,
  styles, icons, status rows, and workflow controls. They never copy theme
  values or maintain a second package-local visual language.

## Adding A Capability

1. Prove repeated production use or clear package ownership pressure with audit data.
2. Decide whether an existing package owns the capability.
3. Update `capabilities.json`.
4. Update `dependency-rules.json` only if layering changes.
5. Update affected `deucarian-package.json` files.
6. Update `packages.json` and fallback catalogs only when package dependencies or Installer-visible metadata change.
7. Run shared validation and the authoritative audit.

## Editor navigation and Control Center policy

`com.deucarian.editor` owns the Deucarian Control Center shell, stable tool
navigation contracts, contribution registries, area IDs, and ordinary menu
policy. Domain packages continue to own their state, validation, actions, and
standalone specialist windows. Contributions expose only bounded, sanitized
local snapshots and register explicitly from editor assemblies; runtime
assembly scanning is not a discovery mechanism.

The approved global menu paths and their owners are defined in
`menu-policy.json`. Installing a runtime package does not create a menu branch.
Low-frequency debugging, documentation, reset, test, audit, and generation
actions belong in the Control Center Developer, Diagnostics, or Authoring
areas. Cross-package navigation uses stable tool IDs or a public `Open` API.
Bootstrap's single audited Package Installer bridge is the only dependency-free
literal-menu exception.

`Tools/deucarian_menu_audit.py` scans organization source and user-facing text assets for declarations,
duplicates, unauthorized owners and paths, technical taxonomy, stale Project
Setup strings, and hard-coded cross-package menu calls. It emits deterministic
`MENU_AUDIT.json` and `MENU_AUDIT.md` artifacts and runs in both registry and
shared package-validation CI.
