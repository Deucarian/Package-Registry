# Debug API Audit

Schema version: 1

Counts actual C# invocation expressions plus fenced Markdown examples. Comments, strings, CHANGELOG mentions, and test method names are excluded from production-code counts.

## Policy Disposition Summary

| Metric | Count |
| --- | --- |
| Allowed | 7 |

## Log Level Summary

| Metric | Count |
| --- | --- |
| Error | 3 |
| Exception | 1 |
| Info | 1 |
| Warning | 2 |

## Policy Severity Summary

| Metric | Count |
| --- | --- |
| Info | 7 |

## Findings

| Repository | File | Line | Scope | Invocation | Log level | Policy disposition | Policy severity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Logging | Runtime/DeucarianLog.cs | 255 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 27 | Runtime production | UnityEngine.Debug.Log | Info | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 30 | Runtime production | UnityEngine.Debug.LogWarning | Warning | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 33 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 48 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 52 | Runtime production | UnityEngine.Debug.LogError | Error | Allowed | Info |
| Logging | Runtime/UnityConsoleLogSink.cs | 53 | Runtime production | UnityEngine.Debug.LogException | Exception | Allowed | Info |
