# Documentation Drift Audit

Schema version: 1

## Summary

| Metric | Count |
| --- | --- |
| Dependency version drift | 1 |
| Historical changelog reference | 12 |
| Legitimate generic bridge term | 1 |
| Migration documentation | 6 |

Historical changelog references preserve released history and are not rewrite recommendations.

## Findings

| Repository | Kind | File | Dependency | Expected/Value | Found |
| --- | --- | --- | --- | --- | --- |
| API | Historical changelog reference | CHANGELOG.md |  |  |  |
| Bootstrap | Historical changelog reference | CHANGELOG.md |  |  |  |
| Logging | Historical changelog reference | CHANGELOG.md |  |  |  |
| Logging | Legitimate generic bridge term | README.md |  |  |  |
| Object-Selection | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Migration documentation | README.md |  |  |  |
| ObjectSelection-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectSelection-CoreState-Integration | Migration documentation | README.md |  |  |  |
| Package-Installer | Historical changelog reference | CHANGELOG.md |  |  |  |
| Package-Installer | Migration documentation | README.md |  |  |  |
| Package-Registry | Migration documentation | DOCUMENTATION_DRIFT_DECISIONS.md |  |  |  |
| Selection-Suite | Dependency version drift |  | com.deucarian.ui-binding | 1.1.0 | 1.0.3 |
| Selection-Suite | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session-API-Integration | Migration documentation | README.md |  |  |  |
| UI-Binding | Historical changelog reference | CHANGELOG.md |  |  |  |
| UIBinding-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| UIBinding-CoreState-Integration | Migration documentation | README.md |  |  |  |
