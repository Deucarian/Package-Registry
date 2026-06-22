# Deucarian Reuse Audit

Schema version: 2

This is the hardened organization-wide audit snapshot for `Deucarian` at `develop`. It uses `tree-sitter-c-sharp` for C# parsing and records the current package sources and governance state.

## Weaknesses Fixed From The Original Audit

- Replaced regex/braces C# discovery with syntax-aware Tree-sitter parsing.
- Public API counts now include only externally public Runtime and Editor production symbols.
- Debug usage counts now come from invocation expressions instead of prose/text matches.
- Unity object lifetime findings separate helper definitions, helper calls, and direct Unity API calls.
- Documentation version drift detection no longer treats every semantic version in README prose as the package version.
- Audit paths are repository-relative/canonical; no machine-specific audit-root paths are written.

## Inventory

| Repository | Package ID | Version | Unity | Develop | Audit Clone | package.json dependencies | Asmdefs | Production public API |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| API | com.deucarian.api | 1.1.0 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.unitywebrequest, com.unity.nuget.newtonsoft-json, com.unity.modules.assetbundle, com.unity.modules.unitywebrequestassetbundle, com.unity.modules.unitywebrequesttexture, com.unity.modules.unitywebrequestwww | 4 | 169 |
| Bootstrap | com.deucarian.bootstrap | 1.0.2 | 2021.3 | yes | clean | (none) | 2 | 1 |
| Common | com.deucarian.common | 0.1.0 | 2021.3 | yes | clean | (none) | 3 | 2 |
| Core-State | com.deucarian.core-state | 1.0.0 | 2021.3 | yes | clean | (none) | 3 | 38 |
| Diagnostics | com.deucarian.diagnostics | 0.1.1 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 62 |
| Editor | com.deucarian.editor | 1.0.0 | 2021.3 | yes | clean | (none) | 2 | 91 |
| Logging | com.deucarian.logging | 1.0.1 | 2021.3 | yes | clean | com.deucarian.editor | 4 | 69 |
| Object-Loading | com.deucarian.object-loading | 1.2.0 | 2021.3 | yes | clean | com.deucarian.common, com.deucarian.logging, com.unity.nuget.newtonsoft-json | 4 | 246 |
| Object-Selection | com.deucarian.object-selection | 1.0.2 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.physics | 3 | 104 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | 0.2.3 | 2021.3 | yes | clean | com.unity.nuget.newtonsoft-json, com.deucarian.api, com.deucarian.object-loading | 2 | 30 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | 1.0.2 | 2021.3 | yes | clean | com.deucarian.logging, com.deucarian.object-selection, com.deucarian.core-state | 3 | 10 |
| Package-Installer | com.deucarian.package-installer | 1.1.57 | 2021.3 | yes | clean | com.deucarian.editor, com.deucarian.logging | 2 | 0 |
| Package-Registry | (none) | (none) | (none) | yes | clean | (none) | 0 | 0 |
| Selection-Suite | com.deucarian.selection-suite | 1.0.2 | 2021.3 | yes | clean | com.deucarian.object-selection.core-state-integration, com.deucarian.core-state, com.deucarian.ui-binding.core-state-integration, com.deucarian.ui-binding, com.deucarian.object-selection | 1 | 0 |
| Session | com.deucarian.session | 1.0.2 | 2021.3 | yes | clean | com.deucarian.logging, com.unity.modules.jsonserialize | 3 | 65 |
| Session-API-Integration | com.deucarian.session.api-integration | 1.0.2 | 2021.3 | yes | clean | com.deucarian.api, com.deucarian.session | 3 | 3 |
| Theming | com.deucarian.theming | 1.0.0 | 2022.3 | yes | clean | com.deucarian.editor, com.deucarian.logging, com.unity.textmeshpro, com.unity.ugui, com.unity.modules.uielements | 4 | 221 |
| UI-Binding | com.deucarian.ui-binding | 1.1.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui | 3 | 75 |
| UI-FLow | com.deucarian.ui-flow | 0.4.0 | 2021.3 | yes | clean | com.deucarian.common, com.unity.ugui, com.deucarian.logging | 6 | 341 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | 1.0.2 | 2021.3 | yes | clean | com.deucarian.core-state, com.deucarian.ui-binding | 3 | 15 |

## Corrected Counts

| Metric | Count |
| --- | --- |
| Repositories | 20 |
| Parsed methods/bodies analyzed | 3110 |
| Exact AST clone groups | 15 |
| Normalized structural clone groups | 22 |
| Same-symbol semantic candidates | 5 |
| Runtime public API symbols | 1323 |
| Editor public API symbols | 219 |
| Test public symbols excluded from production API | 779 |
| Sample public symbols excluded from production API | 142 |
| Internal/private production symbols | 2915 |
| Public API symbols missing XML documentation | 877 |
| Debug invocation records | 7 |
| Unity object lifetime records | 65 |
| Documentation drift findings | 20 |
| Dependency usage findings | 30 |
| Dependency cycles | 0 |

## Extraction Position

`com.deucarian.common` owns the approved Unity object lifetime primitive. `EXTRACTION_DECISIONS.md` records completed and remaining reviewed dispositions for candidates produced by the hardened analyzer.
