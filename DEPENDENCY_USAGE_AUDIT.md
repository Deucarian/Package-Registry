# Dependency Usage Audit

Schema version: 1

Summary: {"editor-only use": 5, "missing package dependency": 2, "required and used": 15, "sample-only use": 5}

Findings marked `apparently unused` are review prompts, not removal recommendations.

| Repository | Dependency/Reference | Classification | Evidence | Referenced assemblies | Source mentions |
| --- | --- | --- | --- | --- | --- |
| API | com.deucarian.logging | required and used | Editor production: Deucarian.API.Editor -> Deucarian.Logging; Runtime production: Deucarian.API -> Deucarian.Logging; Sample: Deucarian.API.Samples -> Deucarian.Logging | Deucarian.Logging | 0 |
| Diagnostics | com.deucarian.editor | editor-only use | Editor production: Deucarian.Diagnostics.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Diagnostics | com.deucarian.logging | required and used | Runtime production: Deucarian.Diagnostics -> Deucarian.Logging; Test: Deucarian.Diagnostics.Tests -> Deucarian.Logging | Deucarian.Logging | 0 |
| Logging | com.deucarian.editor | editor-only use | Editor production: Deucarian.Logging.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Object-Loading | Deucarian.Diagnostics | missing package dependency | Runtime production: Deucarian.ObjectLoading.Diagnostics -> Deucarian.Diagnostics |  |  |
| Object-Loading | Deucarian.Diagnostics | missing package dependency | Test: Deucarian.ObjectLoading.Diagnostics.Tests -> Deucarian.Diagnostics |  |  |
| Object-Loading | com.deucarian.logging | required and used | Runtime production: Deucarian.ObjectLoading -> Deucarian.Logging | Deucarian.Logging | 0 |
| Object-Selection | com.deucarian.logging | required and used | Runtime production: Deucarian.ObjectSelection -> Deucarian.Logging; Sample: Deucarian.ObjectSelection.Samples.PrimitiveSelection -> Deucarian.Logging | Deucarian.Logging | 0 |
| ObjectLoading-API-Integration | com.deucarian.api | required and used | Runtime production: Deucarian.ObjectLoading.APIIntegration -> Deucarian.API; Test: Deucarian.ObjectLoading.APIIntegration.Tests -> Deucarian.API | Deucarian.API | 0 |
| ObjectLoading-API-Integration | com.deucarian.object-loading | required and used | Runtime production: Deucarian.ObjectLoading.APIIntegration -> Deucarian.ObjectLoading; Test: Deucarian.ObjectLoading.APIIntegration.Tests -> Deucarian.ObjectLoading | Deucarian.ObjectLoading | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.core-state | required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.CoreState; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.CoreState; Test: Deucarian.ObjectSelection.CoreStateIntegration.Tests -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.logging | required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.Logging; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.Logging | Deucarian.Logging | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection | required and used | Runtime production: Deucarian.ObjectSelection.CoreStateIntegration -> Deucarian.ObjectSelection; Sample: Deucarian.ObjectSelection.CoreStateIntegration.Samples.CoreStateIntegrationSample -> Deucarian.ObjectSelection; Test: Deucarian.ObjectSelection.CoreStateIntegration.Tests -> Deucarian.ObjectSelection | Deucarian.ObjectSelection | 0 |
| Package-Installer | com.deucarian.editor | editor-only use | Editor production: Deucarian.PackageInstaller.Editor -> Deucarian.Editor; Test: Deucarian.PackageInstaller.Editor.Tests -> Deucarian.Editor | Deucarian.Editor | 0 |
| Package-Installer | com.deucarian.logging | editor-only use | Editor production: Deucarian.PackageInstaller.Editor -> Deucarian.Logging; Test: Deucarian.PackageInstaller.Editor.Tests -> Deucarian.Logging | Deucarian.Logging | 0 |
| Selection-Suite | com.deucarian.core-state | sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| Selection-Suite | com.deucarian.object-selection | sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.ObjectSelection | Deucarian.ObjectSelection | 0 |
| Selection-Suite | com.deucarian.object-selection.core-state-integration | sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.ObjectSelection.CoreStateIntegration | Deucarian.ObjectSelection.CoreStateIntegration | 0 |
| Selection-Suite | com.deucarian.ui-binding | sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.UIBinding | Deucarian.UIBinding | 0 |
| Selection-Suite | com.deucarian.ui-binding.core-state-integration | sample-only use | Sample: Deucarian.SelectionSuite.Samples.SelectionDemo -> Deucarian.UIBinding.CoreStateIntegration | Deucarian.UIBinding.CoreStateIntegration | 0 |
| Session | com.deucarian.logging | required and used | Runtime production: Deucarian.Session -> Deucarian.Logging; Sample: Deucarian.Session.Samples -> Deucarian.Logging | Deucarian.Logging | 0 |
| Session-API-Integration | com.deucarian.api | required and used | Runtime production: Deucarian.Session.APIIntegration -> Deucarian.API; Sample: Deucarian.Session.APIIntegration.Samples -> Deucarian.API; Test: Deucarian.Session.APIIntegration.Tests -> Deucarian.API | Deucarian.API | 0 |
| Session-API-Integration | com.deucarian.session | required and used | Runtime production: Deucarian.Session.APIIntegration -> Deucarian.Session; Sample: Deucarian.Session.APIIntegration.Samples -> Deucarian.Session; Test: Deucarian.Session.APIIntegration.Tests -> Deucarian.Session | Deucarian.Session | 0 |
| Theming | com.deucarian.editor | editor-only use | Editor production: Deucarian.Theming.Editor -> Deucarian.Editor | Deucarian.Editor | 0 |
| Theming | com.deucarian.logging | required and used | Editor production: Deucarian.Theming.Editor -> Deucarian.Logging; Runtime production: Deucarian.Theming -> Deucarian.Logging | Deucarian.Logging | 0 |
| UIBinding-CoreState-Integration | com.deucarian.core-state | required and used | Runtime production: Deucarian.UIBinding.CoreStateIntegration -> Deucarian.CoreState; Sample: Deucarian.UIBinding.CoreStateIntegration.Samples.BasicUsage -> Deucarian.CoreState; Test: Deucarian.UIBinding.CoreStateIntegration.Tests -> Deucarian.CoreState | Deucarian.CoreState | 0 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding | required and used | Runtime production: Deucarian.UIBinding.CoreStateIntegration -> Deucarian.UIBinding; Sample: Deucarian.UIBinding.CoreStateIntegration.Samples.BasicUsage -> Deucarian.UIBinding; Test: Deucarian.UIBinding.CoreStateIntegration.Tests -> Deucarian.UIBinding | Deucarian.UIBinding | 0 |
