# Debug API Audit

Schema version: 1

Counts actual C# invocation expressions plus fenced Markdown examples. Comments, strings, CHANGELOG mentions, and test method names are excluded from production-code counts.

## Policy Disposition Summary

| Metric | Count |
| --- | --- |
| Allowed | 8 |
| Migrate | 36 |
| Review required | 1 |

## Log Level Summary

| Metric | Count |
| --- | --- |
| Error | 5 |
| Exception | 13 |
| Info | 7 |
| Warning | 20 |

## Policy Severity Summary

| Metric | Count |
| --- | --- |
| Error | 36 |
| Info | 8 |
| Warning | 1 |

## Findings

| Repository | File | Line | Scope | Invocation | Log level | Policy disposition | Policy severity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Diagnostics | Editor/DiagnosticsWindow.cs | 254 | Editor production | Debug.LogWarning | Warning | Migrate | Error |
| Logging | Editor/DeucarianLoggingMenu.cs | 29 | Editor production | UnityEngine.Debug.Log | Info | Allowed | Info |
| Logging | Runtime/DeucarianLog.cs | 255 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 27 | Runtime production | UnityEngine.Debug.Log | Info | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 30 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 33 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 48 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 52 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 53 | Runtime production | UnityEngine.Debug.LogException | Exception | Allowed | Info |
| Object-Loading | README.md | 195 | Documentation example | yield return pipeline.LoadAsync(request, result => Debug.Log(result.Message)); | Info | ReviewRequired | Warning |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 43 | Sample | Debug.Log | Info | Migrate | Error |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 53 | Sample | Debug.Log | Info | Migrate | Error |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 57 | Sample | Debug.LogError | Error | Migrate | Error |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 16 | Editor production | Debug.Log | Info | Migrate | Error |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 25 | Editor production | Debug.LogError | Error | Migrate | Error |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 29 | Editor production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowAction.cs | 22 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowAction.cs | 34 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowBackButton.cs | 60 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowBackButton.cs | 72 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 43 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 87 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 104 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowDismissButton.cs | 56 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowDismissButton.cs | 68 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 63 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 69 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 93 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowPresentRouteAction.cs | 27 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowPushRouteAction.cs | 32 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowReplaceRouteAction.cs | 27 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime.UGUI/UIFlowResetRouteAction.cs | 29 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 454 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 461 | Runtime production | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 742 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 782 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 792 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 798 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 834 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 855 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 875 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Runtime/Screens/UIFlowScreen.cs | 256 | Runtime production | Debug.LogException | Exception | Migrate | Error |
| UI-FLow | Samples~/BasicFlow/BasicFlowConfirmQuitAction.cs | 25 | Sample | Debug.LogWarning | Warning | Migrate | Error |
| UI-FLow | Samples~/BasicFlow/BasicFlowConfirmQuitAction.cs | 32 | Sample | Debug.Log | Info | Migrate | Error |
| UI-FLow | Samples~/BasicFlow/BasicFlowPushMessageAction.cs | 26 | Sample | Debug.LogWarning | Warning | Migrate | Error |
