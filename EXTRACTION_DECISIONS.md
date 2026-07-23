# Reviewed Extraction Decisions

Schema version: 1

This file is the human-reviewed decision ledger. `Tools/Generate-DeucarianAudit.py` never writes it; generated clone and reuse evidence is published in `EXTRACTION_CANDIDATES.md`.

| Decision ID | Status | Owner | Reviewed evidence | Decision and rationale |
| --- | --- | --- | --- | --- |
| package-boundaries-2026-07 | Accepted | Package Registry maintainers | Portfolio governance review, 2026-07-17 | Preserve all current package, Integration, Suite, Installer/Registry, Logging/Diagnostics, and navigation boundaries. The dependency graph is acyclic and no merger or repository split has sufficient evidence. |
| unity-object-lifetime | Completed | `com.deucarian.common` | Lifetime audit | Common owns `UnityObjectUtility.DestroySafely`; production consumers use it while explicit test teardown remains local. |
| game-content-authoring-provider-primitives | Completed | `com.deucarian.game-content-authoring` | Cross-repository structural clone audit and focused consumer scan | Shared editor-only provider/session state, validation, reference/list drawing, and preview/editing primitives replaced 49 substantive implementations across Attacks, Run Upgrades, Weapon Systems, and the Idle Auto Defense template, reducing production code by 347 lines. |
| object-loading-api-cache-helpers | Completed | `com.deucarian.object-loading` | Exact clone audit and 39-test Unity EditMode run | Object Loading now owns cache-hash and sensitive-header behavior; API Integration consumes the owner implementation without changing the repository boundary. |
| report-viewer-media-loading-playback | Completed | `com.deucarian.media` | 3D Report Viewer attachment loading, cancellation, Unity object lifetime, and VideoPlayer lifecycle review | Media owns typed resource loading, leases, latest-request coordination, and playback sessions; `com.deucarian.media.api-integration` adapts API transport while report metadata, pose resolution, overlays, and UI remain application responsibilities. |
| editor-select-and-ping | Completed | `com.deucarian.editor` | Editor-only structural clone audit and focused EditMode tests | Editor owns the selection-and-ping helper used by Theming, removing six duplicate implementations while retaining the compatibility delegate. |
| logging-editor-dependency | Follow-up | `com.deucarian.logging` | Dependency-boundary review | Retain Logging's current Editor dependency in this program; optional assembly or package-boundary changes require a separate compatibility analysis. |
| bootstrap-editor-style-copy | Rejected | Bootstrap | Dependency-boundary review | Keep Bootstrap drawing/style helpers local so first-time setup remains self-contained. |
| tiny-generic-helper-package | Rejected | Local package owners | Clone audit | Do not extract small copy, string, disposal, validation, sample-scaffolding, or test-fixture helpers based on occurrence count alone. |

Any new or changed decision must record its owner, reviewed evidence, status, and rationale here. Candidate hashes are intentionally not used as durable identities because generator improvements can change them without changing the underlying architecture question.

The clean 46-repository candidate audit reduced exact clone groups from 67 to 65 (178 to 162 occurrences) and normalized structural clone groups from 109 to 105 (335 to 309 occurrences), with no dependency cycle or actionable policy finding.
