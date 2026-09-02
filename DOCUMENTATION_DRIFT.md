# Documentation Drift Audit

Schema version: 1

## Summary

| Metric | Count |
| --- | --- |
| Dependency version drift | 2 |
| Historical changelog reference | 16 |
| Legitimate generic bridge term | 1 |
| Migration documentation | 10 |
| Review required | 14 |

Historical changelog references preserve released history and are not rewrite recommendations.

## Findings

| Repository | Kind | File | Dependency | Expected/Value | Found |
| --- | --- | --- | --- | --- | --- |
| API | Historical changelog reference | CHANGELOG.md |  |  |  |
| Bootstrap | Historical changelog reference | CHANGELOG.md |  |  |  |
| Bootstrap | Migration documentation | README.md |  |  |  |
| Build-Pipeline | Dependency version drift |  | com.deucarian.editor | 1.2.0 | 1.0.5 |
| Build-Pipeline | Dependency version drift |  | com.deucarian.logging | 1.0.4 | 1.0.2 |
| Build-Pipeline | Review required | README.md |  |  |  |
| Command-Routing | Historical changelog reference | CHANGELOG.md |  |  |  |
| Command-Routing-WebGL-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| Defense-Games | Review required | Documentation~/CrossGenre.md |  |  |  |
| Diagnostics | Review required | README.md |  |  |  |
| Logging | Historical changelog reference | CHANGELOG.md |  |  |  |
| Logging | Legitimate generic bridge term | README.md |  |  |  |
| Object-Selection | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Migration documentation | README.md |  |  |  |
| ObjectSelection-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectSelection-CoreState-Integration | Migration documentation | README.md |  |  |  |
| Package-Installer | Historical changelog reference | CHANGELOG.md |  |  |  |
| Package-Installer | Migration documentation | README.md |  |  |  |
| Package-Registry | Migration documentation | ARCHITECTURE.md |  |  |  |
| Package-Registry | Migration documentation | DOCUMENTATION_DRIFT_DECISIONS.md |  |  |  |
| Package-Registry | Migration documentation | MIGRATION_PLAN.md |  |  |  |
| Package-Registry | Review required | EXTRACTION_DECISIONS.md |  |  |  |
| Pointer-Capture | Review required | AGENTS.md |  |  |  |
| Pointer-Capture | Review required | README.md |  |  |  |
| Selection-Suite | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| Simultria-API | Review required | Documentation~/index.md |  |  |  |
| Simultria-Viewer-Connection | Migration documentation | README.md |  |  |  |
| Template-Game-Survivors | Migration documentation | Documentation~/validation.md |  |  |  |
| Template-Game-Survivors | Review required | Documentation~/game-content-authoring.md |  |  |  |
| Template-Viewer-Web | Historical changelog reference | CHANGELOG.md |  |  |  |
| Template-Viewer-Web | Review required | Documentation~/architecture.md |  |  |  |
| Test-Automation | Review required | Documentation~/lifecycle.md |  |  |  |
| UI-Binding | Historical changelog reference | CHANGELOG.md |  |  |  |
| UIBinding-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| UIBinding-CoreState-Integration | Migration documentation | README.md |  |  |  |
| Web-Viewer-Suite | Review required | Documentation~/index.md |  |  |  |
| WebGL-Template | Historical changelog reference | CHANGELOG.md |  |  |  |
| WebGL-Template | Review required | AGENTS.md |  |  |  |
| WebGL-Template | Review required | README.md |  |  |  |
| XR-UI-Theming-Integration | Review required | AGENTS.md |  |  |  |
