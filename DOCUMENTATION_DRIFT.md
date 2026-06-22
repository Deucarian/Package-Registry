# Documentation Drift Audit

Schema version: 1

## Summary

| Metric | Count |
| --- | --- |
| Active documentation drift | 4 |
| Active repository URL drift | 10 |
| Dependency version drift | 2 |
| Historical changelog reference | 12 |
| Legitimate generic bridge term | 1 |
| Migration documentation | 2 |
| Package version drift | 8 |
| Review required | 3 |

Historical changelog references preserve released history and are not rewrite recommendations.

## Findings

| Repository | Kind | File | Dependency | Expected/Value | Found |
| --- | --- | --- | --- | --- | --- |
| API | Historical changelog reference | CHANGELOG.md |  |  |  |
| API | Package version drift |  |  | 1.1.0 | 1.0.2 |
| Bootstrap | Historical changelog reference | CHANGELOG.md |  |  |  |
| Bootstrap | Package version drift |  |  | 1.0.1 | 0.1.8 |
| Editor | Package version drift |  |  | 1.0.0 | 0.1.2 |
| Logging | Historical changelog reference | CHANGELOG.md |  |  |  |
| Logging | Legitimate generic bridge term | README.md |  |  |  |
| Logging | Package version drift |  |  | 1.0.0 | 0.2.6 |
| Logging | Package version drift |  |  | 1.0.0 | 0.2.6 |
| Object-Loading | Dependency version drift |  | com.deucarian.logging | 0.2.5 | 0.2.2 |
| Object-Loading | Package version drift |  |  | 1.1.1 | 1.1.0 |
| Object-Selection | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Object-Loading-API-Bridge.git#main |  |
| ObjectLoading-API-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Object-Loading-API-Bridge.git#develop |  |
| ObjectLoading-API-Integration | Active repository URL drift | package.json |  | git+https://github.com/Deucarian/Object-Loading-API-Bridge.git |  |
| ObjectLoading-API-Integration | Dependency version drift |  | com.deucarian.api | 1.1.0 | 1.0.2 |
| ObjectLoading-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| ObjectLoading-API-Integration | Migration documentation | README.md |  |  |  |
| ObjectSelection-CoreState-Integration | Active documentation drift | README.md |  |  |  |
| ObjectSelection-CoreState-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Object-Selection-Bridge.git#main |  |
| ObjectSelection-CoreState-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Object-Selection-Bridge.git#develop |  |
| ObjectSelection-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| Package-Installer | Historical changelog reference | CHANGELOG.md |  |  |  |
| Package-Installer | Migration documentation | README.md |  |  |  |
| Package-Installer | Package version drift |  |  | 1.1.55 | 1.1.44 |
| Package-Registry | Review required | README.md |  |  |  |
| Selection-Suite | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session | Historical changelog reference | CHANGELOG.md |  |  |  |
| Session-API-Integration | Active documentation drift | README.md |  |  |  |
| Session-API-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Session-API-Bridge.git#main |  |
| Session-API-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/Session-API-Bridge.git#develop |  |
| Session-API-Integration | Active repository URL drift | package.json |  | git+https://github.com/Deucarian/Session-API-Bridge.git |  |
| Session-API-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
| Theming | Package version drift |  |  | 1.0.0 | 0.4.2 |
| UI-Binding | Historical changelog reference | CHANGELOG.md |  |  |  |
| UI-FLow | Review required | Documentation~/Integrations.md |  |  |  |
| UI-FLow | Review required | README.md |  |  |  |
| UIBinding-CoreState-Integration | Active documentation drift | CONTRIBUTING.md |  |  |  |
| UIBinding-CoreState-Integration | Active documentation drift | README.md |  |  |  |
| UIBinding-CoreState-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/UI-Binding-CoreState-Bridge.git#main |  |
| UIBinding-CoreState-Integration | Active repository URL drift |  |  | https://github.com/Deucarian/UI-Binding-CoreState-Bridge.git#develop |  |
| UIBinding-CoreState-Integration | Historical changelog reference | CHANGELOG.md |  |  |  |
