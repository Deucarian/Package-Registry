# Debug API Audit

Schema version: 1

Counts actual C# invocation expressions plus fenced Markdown examples. Comments, strings, CHANGELOG mentions, and test method names are excluded from production-code counts.

## Policy Disposition Summary

| Metric | Count |
| --- | --- |
| Allowed | 25 |

## Log Level Summary

| Metric | Count |
| --- | --- |
| Error | 6 |
| Exception | 1 |
| Info | 5 |
| Warning | 13 |

## Policy Severity Summary

| Metric | Count |
| --- | --- |
| Info | 25 |

## Findings

| Repository | File | Line | Scope | Invocation | Log level | Policy disposition | Policy severity | Policy reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Auto-Defense | Tests/EditMode/AutoDefenseTests.cs | 278 | Test | Debug.Log | Info | Allowed | Info |  |
| Logging | Runtime/DeucarianLog.cs | 255 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 27 | Runtime production | UnityEngine.Debug.Log | Info | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 30 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 33 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 48 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 52 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Logging | Runtime/UnityConsoleLogSink.cs | 53 | Runtime production | UnityEngine.Debug.LogException | Exception | Allowed | Info | Reviewed exception declared in deucarian-package.json. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5258 | Runtime production | Debug.LogError | Error | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5311 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5323 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5349 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5359 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5511 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5525 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5539 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5553 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Idle-Auto-Defense | Runtime/IdleAutoDefenseTemplate.cs | 5567 | Runtime production | Debug.LogWarning | Warning | Allowed | Info | Template diagnostics are intentionally visible in the Unity console; replacing them with Logging should be handled with an explicit dependency/governance phase. |
| Template-Game-Movement-FPS | Editor/MovementFpsEditorContentValidation.cs | 26 | Editor production | Debug.LogError | Error | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Template-Game-Movement-FPS | Editor/MovementFpsEditorContentValidation.cs | 30 | Editor production | Debug.LogWarning | Warning | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Template-Game-Movement-FPS | Editor/MovementFpsEditorContentValidation.cs | 34 | Editor production | Debug.Log | Info | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Template-Game-Survivors | Editor/SurvivorsEditorContentValidation.cs | 26 | Editor production | Debug.LogError | Error | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Template-Game-Survivors | Editor/SurvivorsEditorContentValidation.cs | 30 | Editor production | Debug.LogWarning | Warning | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Template-Game-Survivors | Editor/SurvivorsEditorContentValidation.cs | 34 | Editor production | Debug.Log | Info | Allowed | Info | Template editor content validation intentionally prints validation summaries to the Unity console for developer visibility. |
| Weapon-Systems | Tests/EditMode/WeaponSystemsTests.cs | 345 | Test | Debug.Log | Info | Allowed | Info |  |
