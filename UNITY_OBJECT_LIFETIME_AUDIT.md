# Unity Object Lifetime Audit

Schema version: 1

Conclusion: **Implemented in com.deucarian.common**

Selected option: **Completed**

API proposal: UnityObjectUtility.DestroySafely(UnityEngine.Object target)

## Summary

| Metric | Count |
| --- | --- |
| direct Unity API call | 51 |
| helper call site | 13 |
| helper definition | 1 |

## Policy Summary

| Metric | Count |
| --- | --- |
| Allowed | 65 |

## Production Semantic Comparison

| Repository | Symbol | Assembly | Accepted type | Null behavior | Fake-null behavior | Play Mode | Edit Mode | Reference clearing | Collection behavior | Exception behavior | Call sites | Expected context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Testing Package Decision

| Metric | Value |
| --- | --- |
| Decision | KeepLocal |
| Reasoning | Repeated test findings are mostly explicit Object.DestroyImmediate(testObject) cleanup, not a higher-level fixture ownership abstraction. |
| Test repositories with direct cleanup | 9 |

## Findings

| Repository | File | Line | Scope | Kind | Symbol/Invocation | Policy disposition | Policy reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| API | Tests/Editor/ApiClientTests.cs | 384 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Bootstrap | Tests/Editor/DeucarianBootstrapTests.cs | 172 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Runtime/UnityObjectUtility.cs | 14 | Runtime production | helper definition | DestroySafely | Allowed | Canonical Common implementation owns the Play Mode/Edit Mode UnityEngine.Object destruction capability. |
| Common | Runtime/UnityObjectUtility.cs | 23 | Runtime production | direct Unity API call | Object.Destroy | Allowed | Canonical Common implementation owns the Play Mode/Edit Mode UnityEngine.Object destruction capability. |
| Common | Runtime/UnityObjectUtility.cs | 27 | Runtime production | direct Unity API call | Object.DestroyImmediate | Allowed | Canonical Common implementation owns the Play Mode/Edit Mode UnityEngine.Object destruction capability. |
| Common | Tests/EditMode/UnityObjectUtilityEditModeTests.cs | 13 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/EditMode/UnityObjectUtilityEditModeTests.cs | 22 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/EditMode/UnityObjectUtilityEditModeTests.cs | 24 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/EditMode/UnityObjectUtilityEditModeTests.cs | 34 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/EditMode/UnityObjectUtilityEditModeTests.cs | 46 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/PlayMode/UnityObjectUtilityPlayModeTests.cs | 15 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/PlayMode/UnityObjectUtilityPlayModeTests.cs | 25 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/PlayMode/UnityObjectUtilityPlayModeTests.cs | 36 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/PlayMode/UnityObjectUtilityPlayModeTests.cs | 43 | Test | direct Unity API call | Object.Destroy | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Common | Tests/PlayMode/UnityObjectUtilityPlayModeTests.cs | 53 | Test | helper call site | UnityObjectUtility.DestroySafely | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Loading | Runtime/Core/ObjectLoadHandle.cs | 71 | Runtime production | helper call site | UnityObjectUtility.DestroySafely | Allowed | Production code calls the canonical Deucarian.Common lifetime API. |
| Object-Selection | Tests/EditMode/HighlighterHookTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectHoverServiceTests.cs | 40 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectHoverServiceTests.cs | 66 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 25 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 45 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 65 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 85 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 105 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 116 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 143 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionServiceTests.cs | 161 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionServiceTests.cs | 162 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 135 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 171 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 177 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 44 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 45 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 46 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 67 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 161 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 257 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 258 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 262 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 356 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 357 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 358 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Editor/DeucarianThemingMenuToolsTests.cs | 142 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Editor/DeucarianUIToolkitThemeUtilityTests.cs | 24 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Runtime/DeucarianColorPaletteTests.cs | 18 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Runtime/DeucarianSelectableThemeColorsTests.cs | 19 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| Theming | Tests/Runtime/DeucarianUGUIAndTMPAdapterTests.cs | 20 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Runtime/GenericItemManager.cs | 176 | Runtime production | helper call site | UnityObjectUtility.DestroySafely | Allowed | Production code calls the canonical Deucarian.Common lifetime API. |
| UI-Binding | Runtime/GenericItemManager.cs | 184 | Runtime production | helper call site | UnityObjectUtility.DestroySafely | Allowed | Production code calls the canonical Deucarian.Common lifetime API. |
| UI-Binding | Runtime/GenericItemManager.cs | 219 | Runtime production | helper call site | UnityObjectUtility.DestroySafely | Allowed | Production code calls the canonical Deucarian.Common lifetime API. |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 26 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 31 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 223 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 29 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 34 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 39 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingSelectionVisualTests.cs | 25 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-Binding | Tests/Editor/UIBindingSelectionVisualTests.cs | 30 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-FLow | Runtime/Providers/UIFlowPrefabScreenProvider.cs | 79 | Runtime production | helper call site | UnityObjectUtility.DestroySafely | Allowed | Production code calls the canonical Deucarian.Common lifetime API. |
| UI-FLow | Tests/EditMode/UIFlowLogTests.cs | 32 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UI-FLow | Tests/PlayMode/UIFlowRuntimeNavigationTests.cs | 24 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate | Allowed | Test-only explicit Unity object teardown remains local; no shared testing package was approved. |
