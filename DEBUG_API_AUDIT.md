# Debug API Audit

Schema version: 1

Counts actual C# invocation expressions plus fenced Markdown examples. Comments, strings, CHANGELOG mentions, and test method names are excluded from production-code counts.

Summary: {"allowed": 8, "migrate": 20, "review required": 17}

| Repository | File | Line | Scope | Invocation | Disposition |
| --- | --- | --- | --- | --- | --- |
| Diagnostics | Editor/DiagnosticsWindow.cs | 254 | Editor production | Debug.LogWarning | migrate |
| Logging | Editor/DeucarianLoggingMenu.cs | 29 | Editor production | UnityEngine.Debug.Log | allowed |
| Logging | Runtime/DeucarianLog.cs | 255 | Runtime production | UnityEngine.Debug.LogWarning | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 27 | Runtime production | UnityEngine.Debug.Log | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 30 | Runtime production | UnityEngine.Debug.LogWarning | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 33 | Runtime production | UnityEngine.Debug.LogError | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 48 | Runtime production | UnityEngine.Debug.LogError | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 52 | Runtime production | UnityEngine.Debug.LogError | allowed |
| Logging | Runtime/UnityConsoleLogSink.cs | 53 | Runtime production | UnityEngine.Debug.LogException | allowed |
| Object-Loading | README.md | 193 | Documentation example | yield return pipeline.LoadAsync(request, result => Debug.Log(result.Message)); | review required |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 43 | Sample | Debug.Log | migrate |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 53 | Sample | Debug.Log | migrate |
| ObjectLoading-API-Integration | Samples~/ApiDownloaderSample/ApiIntegrationDownloaderSample.cs | 57 | Sample | Debug.LogError | migrate |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 16 | Editor production | Debug.Log | migrate |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 25 | Editor production | Debug.LogError | migrate |
| UI-FLow | Editor/UIFlowProjectValidator.cs | 29 | Editor production | Debug.LogWarning | migrate |
| UI-FLow | Runtime.UGUI/UIFlowAction.cs | 22 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowAction.cs | 34 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowBackButton.cs | 60 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowBackButton.cs | 72 | Other | Debug.LogException | review required |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 43 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 87 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowButtonAction.cs | 104 | Other | Debug.LogException | review required |
| UI-FLow | Runtime.UGUI/UIFlowDismissButton.cs | 56 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowDismissButton.cs | 68 | Other | Debug.LogException | review required |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 63 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 69 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowNavigateButton.cs | 93 | Other | Debug.LogException | review required |
| UI-FLow | Runtime.UGUI/UIFlowPresentRouteAction.cs | 27 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowPushRouteAction.cs | 32 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowReplaceRouteAction.cs | 27 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime.UGUI/UIFlowResetRouteAction.cs | 29 | Other | Debug.LogWarning | review required |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 454 | Runtime production | Debug.LogWarning | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 461 | Runtime production | Debug.LogWarning | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 742 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 782 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 792 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 798 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 834 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 855 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Navigation/UIFlowHost.cs | 875 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Runtime/Screens/UIFlowScreen.cs | 256 | Runtime production | Debug.LogException | migrate |
| UI-FLow | Samples~/BasicFlow/BasicFlowConfirmQuitAction.cs | 25 | Sample | Debug.LogWarning | migrate |
| UI-FLow | Samples~/BasicFlow/BasicFlowConfirmQuitAction.cs | 32 | Sample | Debug.Log | migrate |
| UI-FLow | Samples~/BasicFlow/BasicFlowPushMessageAction.cs | 26 | Sample | Debug.LogWarning | migrate |
