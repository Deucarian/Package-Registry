# Deucarian Reuse Audit

Generated: 2026-06-22

This is the initial organization-wide audit snapshot required before any code extraction. It was generated from shallow `develop` clones under `C:\Repositories\_deucarian_org_audit` and writes governance artifacts in Package Registry on `develop`.

## Safety Summary

- Non-archived Deucarian repositories discovered: 19.
- Every discovered repository has a `develop` branch.
- The audit clones are clean and checked out on `develop`.
- No source extraction or dependency migration has been performed in this wave.
- Local working-copy blockers outside the audit clones were observed, including a dirty `Logging` checkout and several package folders on `main`; those were not edited.

## Inventory

| Repository | Package ID | Version | Unity | Develop | Main | Audit Clone | package.json dependencies | Asmdefs | Public API symbols | Workflows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| API | com.deucarian.api | 1.1.0 | 2021.3 | yes | yes | clean | com.deucarian.logging, com.unity.modules.unitywebrequest, com.unity.nuget.newtonsoft-json, com.unity.modules.assetbundle, com.unity.modules.unitywebrequestassetbundle, com.unity.modules.unitywebrequesttexture, com.unity.modules.unitywebrequestwww | 4 | 237 | 5 |
| Bootstrap | com.deucarian.bootstrap | 1.0.1 | 2021.3 | yes | yes | clean | (none) | 2 | 66 | 2 |
| Core-State | com.deucarian.core-state | 1.0.0 | 2021.3 | yes | yes | clean | (none) | 3 | 58 | 2 |
| Diagnostics | com.deucarian.diagnostics | 0.1.0 | 2021.3 | yes | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 95 | 0 |
| Editor | com.deucarian.editor | 1.0.0 | 2021.3 | yes | yes | clean | (none) | 2 | 115 | 2 |
| Logging | com.deucarian.logging | 1.0.0 | 2021.3 | yes | yes | clean | com.deucarian.editor | 4 | 116 | 2 |
| Object-Loading | com.deucarian.object-loading | 1.1.1 | 2021.3 | yes | yes | clean | com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 308 | 2 |
| Object-Selection | com.deucarian.object-selection | 1.0.2 | 2021.3 | yes | yes | clean | com.deucarian.logging, com.unity.modules.physics | 3 | 151 | 5 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | 0.2.0 | 2021.3 | yes | yes | clean | com.unity.nuget.newtonsoft-json, com.deucarian.api, com.deucarian.object-loading | 2 | 59 | 2 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | 1.0.2 | 2021.3 | yes | yes | clean | com.deucarian.logging, com.deucarian.object-selection, com.deucarian.core-state | 3 | 45 | 5 |
| Package-Installer | com.deucarian.package-installer | 1.1.55 | 2021.3 | yes | yes | clean | com.deucarian.editor, com.deucarian.logging | 2 | 738 | 2 |
| Package-Registry | (none) | (none) | (none) | yes | yes | clean | (none) | 0 | 0 | 1 |
| Selection-Suite | com.deucarian.selection-suite | 1.0.1 | 2021.3 | yes | yes | clean | com.deucarian.object-selection.core-state-integration, com.deucarian.core-state, com.deucarian.ui-binding.core-state-integration, com.deucarian.ui-binding, com.deucarian.object-selection | 1 | 13 | 3 |
| Session | com.deucarian.session | 1.0.2 | 2021.3 | yes | yes | clean | com.deucarian.logging, com.unity.modules.jsonserialize | 3 | 91 | 2 |
| Session-API-Integration | com.deucarian.session.api-integration | 1.0.1 | 2021.3 | yes | yes | clean | com.deucarian.api, com.deucarian.session | 3 | 13 | 2 |
| Theming | com.deucarian.theming | 1.0.0 | 2022.3 | yes | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.textmeshpro, com.unity.ugui, com.unity.modules.uielements | 4 | 287 | 2 |
| UI-Binding | com.deucarian.ui-binding | 1.0.1 | 2021.3 | yes | yes | clean | com.unity.ugui | 3 | 180 | 4 |
| UI-FLow | com.deucarian.ui-flow | 0.2.0 | 2021.3 | yes | yes | clean | com.unity.ugui | 6 | 416 | 0 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | 1.0.1 | 2021.3 | yes | yes | clean | com.deucarian.core-state, com.deucarian.ui-binding | 3 | 72 | 2 |

## High-Level Findings

- Normalized method clone groups across multiple repositories: 10.
- Same-symbol semantic clone candidates: 4.
- Direct Debug API hits: 49 total, 37 outside the initial allowlist.
- Unity object destruction/lifetime hits: 57.
- Deucarian package dependency version drift entries: 12.
- Package Registry dependency drift entries: 0.
- Dependency cycles detected: 0.

## Conservative Extraction Position

No extraction is recommended from this snapshot alone until each candidate is reviewed against the stated thresholds. The strongest follow-up candidates are:

1. Unity object destruction/lifetime helpers: run the dedicated DestroyUnityObject migration audit before deciding whether `com.deucarian.common`, `com.deucarian.editor`, or no extraction is appropriate.
2. Direct Debug API replacement: migrate non-allowed package code to `com.deucarian.logging` only when the package actually emits logs.
3. Package validation/workflow reuse: centralize repeated validation and workflow logic in a future Build Tools or `.github` governance repository.
4. README/version/dependency drift: fix documentation and registry drift before dependency waves.

## Detailed Data

See `DUPLICATION_REPORT.json` for full machine-readable occurrences, symbol samples, direct API usage, destruction usage, dependency drift, and cycle data.
