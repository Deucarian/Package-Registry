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
- Avoid reflection unless a framework or compatibility boundary requires it
  and no explicit contract is practical. Isolate unavoidable reflection behind
  a narrow adapter, document the reason, and cover it with tests.
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

## Governance Sources

- `packages.json` defines installable packages, canonical functional groups, artifact kinds, dependencies, Integration targets, and Suite members.
- `capabilities.json` defines which package owns each reusable capability.
- `dependency-rules.json` defines the allowed package layering model.
- `DISTRIBUTION_POLICY.md` defines active stable/development Git channels.
- `RELEASE_POLICY.md` defines deferred npm/tag/release workflow policy.
- `Tools/deucarian_package_validator.py` enforces package manifests, asmdefs, documentation, audit policy, and registry/catalog consistency.
- Generated audit artifacts (`*_AUDIT.json`, `DUPLICATION_REPORT.json`) describe current organization state and must stay in sync.

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
- Package Registry owns metadata, capability ownership, dependency rules, and audit/validation tools. It must not contain runtime package code or editor UI implementation.
- Package Installer owns package installation, registry channel selection, dependency-first installation, and package-specific ecosystem visualization. It must not become a generic graph or UI framework.
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
6. Reflection is absent unless a documented, tested framework or compatibility
   boundary requires it behind a narrow adapter.
7. State has one owner and changes are observable.
8. Strategies replace branching where behavior is genuinely interchangeable.
9. Namespace, folder, and assembly-definition boundaries agree.
10. Production files stay within the 500-line responsibility limit.
11. Tests cover contracts, lifecycle/disposal, and important state transitions.
11. Every Deucarian-owned editor surface uses the shared Editor package rather
    than package-local chrome, styling, icons, or workflow controls.

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
