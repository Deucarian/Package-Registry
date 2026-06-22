# Dependency Usage Audit

Schema version: 1

## Summary

| Metric | Count |
| --- | --- |
| Editor-only use | 5 |
| Optional version-defined use | 1 |
| Required and used | 19 |
| Sample-only use | 5 |

Findings marked `apparently unused` are review prompts, not removal recommendations.

| Repository | Dependency/Reference | Classification | Evidence | Referenced assemblies | Source mentions |
| --- | --- | --- | --- | --- | --- |
| API | com.deucarian.logging | Required and used | Editor production: Deucarian.API.Editor -> Deucarian.Logging; Runtime production: Deucarian.API -> Deucarian.Logging; Sample: Deucarian.API.Samples -> Deucarian.Logging | Deucarian.Logging | 0 |
| Diagnostics | com.deucarian.editor | Editor-only use | Editor production: Deucarian.Diagnostics.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Diagnostics | com.deucarian.logging | Required and used | Editor production: Deucarian.Diagnostics.Editor -> Deucarian.Logging; Runtime production: Deucarian.Diagnostics -> Deucarian.Logging; Test: Deucarian.Diagnostics.Tests -> Deucarian.Logging | Deucarian.Logging | 0 |
| Logging | com.deucarian.editor | Editor-only use | Editor production: Deucarian.Logging.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Object-Loading | com.deucarian.diagnostics | Optional version-defined use | Runtime production: Deucarian.ObjectLoading.Diagnostics -> Deucarian.Diagnostics [versionDefine com.deucarian.diagnostics => DEUCARIAN_DIAGNOSTICS_INSTALLED]; Test: Deucarian.ObjectLoading.Diagnostics.Tests -> Deucarian.Diagnostics [versionDefine com.deucarian.diagnostics => DEUCARIAN_DIAGNOSTICS_INSTALLED] | Deucarian.Diagnostics |  |
| Object-Loading | com.deucarian.common | Required and used | Runtime production: Deucarian.ObjectLoading -> Deucarian.Common | Deucarian.Common | 0 |
| Object-Loading | com.deucarian.logging | Required and used | Runtime production: Deucarian.ObjectLoading -> Deucarian.Logging | Deucarian.Logging | 0 |
| Object-Selection | com.deucarian.logging | Required and used | Runtime production: Deucarian.ObjectSelection -> Deucarian.Logging; Sample: Deucarian.ObjectSelection.Samples.PrimitiveSelection -> Deucarian.Logging | Deucarian.Logging | 0 |
| ObjectLoading-API-Integration | com.deucarian.api | Required and used | Runtime production: Deucarian.ObjectLoading.APIIntegration -> Deucarian.API; Test: Deucarian.ObjectLoading.APIIntegration.Tests -> Deucarian.API | Deucarian.API | 0 |
| ObjectLoading-API-Integration | com.deucarian.object-loading | Required and used | Runtime production: Deucarian.ObjectLoading.APIIntegration -> Deucarian.ObjectLoading; Test: Deucarian.ObjectLoading.APIIntegration.Tests -> Deucarian.ObjectLoading | Deucarian.ObjectLoading | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.core-state | Required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.CoreState; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.CoreState; Test: Deucarian.ObjectSelection.CoreStateIntegration.Tests -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.logging | Required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.Logging; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.Logging | Deucarian.Logging | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection | Required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.ObjectSelection; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.ObjectSelection; Test: Deucarian.ObjectSelection.CoreStateIntegration.Tests -> Deucarian.ObjectSelection | Deucarian.ObjectSelection | 0 |
| Package-Installer | com.deucarian.editor | Editor-only use | Editor production: Deucarian.PackageInstaller.Editor -> Deucarian.Editor; Test: Deucarian.PackageInstaller.Editor.Tests -> Deucarian.Editor | Deucarian.Editor | 0 |
| Package-Installer | com.deucarian.logging | Editor-only use | Editor production: Deucarian.PackageInstaller.Editor -> Deucarian.Logging; Test: Deucarian.PackageInstaller.Editor.Tests -> Deucarian.Logging | Deucarian.Logging | 0 |
| Selection-Suite | com.deucarian.core-state | Sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| Selection-Suite | com.deucarian.object-selection | Sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.ObjectSelection | Deucarian.ObjectSelection | 0 |
| Selection-Suite | com.deucarian.object-selection.core-state-integration | Sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.ObjectSelection.CoreStateIntegration | Deucarian.ObjectSelection.CoreStateIntegration | 0 |
| Selection-Suite | com.deucarian.ui-binding | Sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.UIBinding | Deucarian.UIBinding | 0 |
| Selection-Suite | com.deucarian.ui-binding.core-state-integration | Sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.UIBinding.CoreStateIntegration | Deucarian.UIBinding.CoreStateIntegration | 0 |
| Session | com.deucarian.logging | Required and used | Runtime production: Deucarian.Session -> Deucarian.Logging; Sample: Deucarian.Session.Samples -> Deucarian.Logging | Deucarian.Logging | 0 |
| Session-API-Integration | com.deucarian.api | Required and used | Runtime production: Deucarian.Session.APIIntegration -> Deucarian.API; Sample: Deucarian.Session.APIIntegration.Samples -> Deucarian.API; Test: Deucarian.Session.APIIntegration.Tests -> Deucarian.API | Deucarian.API | 0 |
| Session-API-Integration | com.deucarian.session | Required and used | Runtime production: Deucarian.Session.APIIntegration -> Deucarian.Session; Sample: Deucarian.Session.APIIntegration.Samples -> Deucarian.Session; Test: Deucarian.Session.APIIntegration.Tests -> Deucarian.Session | Deucarian.Session | 0 |
| Theming | com.deucarian.editor | Editor-only use | Editor production: Deucarian.Theming.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Theming | com.deucarian.logging | Required and used | Editor production: Deucarian.Theming.Editor -> Deucarian.Logging; Runtime production: Deucarian.Theming -> Deucarian.Logging | Deucarian.Logging | 0 |
| UI-Binding | com.deucarian.common | Required and used | Runtime production: Deucarian.UIBinding -> Deucarian.Common | Deucarian.Common | 0 |
| UI-FLow | com.deucarian.common | Required and used | Runtime production: Deucarian.UIFlow -> Deucarian.Common | Deucarian.Common | 0 |
| UI-FLow | com.deucarian.logging | Required and used | Editor production: Deucarian.UIFlow.Editor -> Deucarian.Logging; Runtime production: Deucarian.UIFlow -> Deucarian.Logging; Runtime production: Deucarian.UIFlow.UGUI -> Deucarian.Logging; Sample: Deucarian.UIFlow.Samples.BasicFlow -> Deucarian.Logging; Test: Deucarian.UIFlow.Tests.EditMode -> Deucarian.Logging | Deucarian.Logging | 0 |
| UIBinding-CoreState-Integration | com.deucarian.core-state | Required and used | Runtime production: Deucarian.UIBinding.CoreStateIntegration -> Deucarian.CoreState; Sample: Deucarian.UIBinding.CoreStateIntegration.Samples.BasicUsage -> Deucarian.CoreState; Test: Deucarian.UIBinding.CoreStateIntegration.Tests -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding | Required and used | Runtime production: Deucarian.UIBinding.CoreStateIntegration -> Deucarian.UIBinding; Sample: Deucarian.UIBinding.CoreStateIntegration.Samples.BasicUsage -> Deucarian.UIBinding; Test: Deucarian.UIBinding.CoreStateIntegration.Tests -> Deucarian.UIBinding | Deucarian.UIBinding | 0 |
