# Unity Object Lifetime Audit

Schema version: 1

Conclusion: **Create com.deucarian.common**

Selected option: **A**

API proposal: UnityObjectUtility.DestroySafely(UnityEngine.Object target)

## Summary

| Metric | Count |
| --- | --- |
| direct Unity API call | 52 |
| helper call site | 4 |
| helper definition | 2 |

## Production Semantic Comparison

| Repository | Symbol | Assembly | Accepted type | Null behavior | Fake-null behavior | Play Mode | Edit Mode | Reference clearing | Collection behavior | Exception behavior | Call sites | Expected context |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Object-Loading | Destroy | Deucarian.ObjectLoading | Object | returns without destroying | Unity fake-null covered by target == null | Object.Destroy | Object.DestroyImmediate | does not clear references | called from collection/list cleanup | does not catch exceptions | 1 | Runtime object load handle cleanup; safe in Play Mode and Edit Mode |
| UI-Binding | DestroyItem | Deucarian.UIBinding | GameObject | returns without destroying | Unity fake-null covered by target == null | Object.Destroy | Object.DestroyImmediate | does not clear references | called from collection/list cleanup | does not catch exceptions | 3 | Runtime item GameObject cleanup; safe in Play Mode and Edit Mode |
| UI-FLow | UIFlowPrefabScreenProvider::ReleaseAsync | Deucarian.UIFlow | GameObject | caller-owned or not explicit | not explicit | Object.Destroy | not supported by this implementation | does not clear references | single owned screen GameObject | does not catch exceptions | 1 | Runtime screen lease release; Play Mode lifecycle |

## Testing Package Decision

| Metric | Value |
| --- | --- |
| Decision | KeepLocal |
| Reasoning | Repeated test findings are mostly explicit Object.DestroyImmediate(testObject) cleanup, not a higher-level fixture ownership abstraction. |
| Test repositories with direct cleanup | 8 |

## Findings

| Repository | File | Line | Scope | Kind | Symbol/Invocation |
| --- | --- | --- | --- | --- | --- |
| API | Tests/Editor/ApiClientTests.cs | 384 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Bootstrap | Tests/Editor/DeucarianBootstrapTests.cs | 171 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Object-Loading | Runtime/Core/ObjectLoadHandle.cs | 70 | Runtime production | helper call site | UnityObjectUtility.Destroy |
| Object-Loading | Runtime/Utilities/UnityObjectUtility.cs | 7 | Runtime production | helper definition | Destroy |
| Object-Loading | Runtime/Utilities/UnityObjectUtility.cs | 16 | Runtime production | direct Unity API call | Object.Destroy |
| Object-Loading | Runtime/Utilities/UnityObjectUtility.cs | 20 | Runtime production | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/HighlighterHookTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectHoverServiceTests.cs | 40 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectHoverServiceTests.cs | 66 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 25 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 45 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 65 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 85 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 105 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 116 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionRegistryTests.cs | 143 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionServiceTests.cs | 161 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionServiceTests.cs | 162 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 135 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 171 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/ObjectSelectionVisualControllerTests.cs | 177 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 44 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 45 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 46 | Test | direct Unity API call | Object.DestroyImmediate |
| Object-Selection | Tests/EditMode/RaycastSelectionControllerTests.cs | 67 | Test | direct Unity API call | Object.DestroyImmediate |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 161 | Test | direct Unity API call | Object.DestroyImmediate |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 257 | Test | direct Unity API call | Object.DestroyImmediate |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 258 | Test | direct Unity API call | Object.DestroyImmediate |
| ObjectSelection-CoreState-Integration | Tests/EditMode/ObjectSelectionCoreStateIntegrationTests.cs | 262 | Test | direct Unity API call | Object.DestroyImmediate |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 356 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 357 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Editor/DeucarianDefaultThemeAssetFactoryTests.cs | 358 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Editor/DeucarianThemingMenuToolsTests.cs | 142 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Editor/DeucarianUIToolkitThemeUtilityTests.cs | 24 | Test | direct Unity API call | Object.DestroyImmediate |
| Theming | Tests/Runtime/DeucarianColorPaletteTests.cs | 18 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Runtime/DeucarianSelectableThemeColorsTests.cs | 19 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Theming | Tests/Runtime/DeucarianUGUIAndTMPAdapterTests.cs | 20 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Runtime/GenericItemManager.cs | 175 | Runtime production | helper call site | DestroyItem |
| UI-Binding | Runtime/GenericItemManager.cs | 183 | Runtime production | helper call site | DestroyItem |
| UI-Binding | Runtime/GenericItemManager.cs | 218 | Runtime production | helper call site | DestroyItem |
| UI-Binding | Runtime/GenericItemManager.cs | 248 | Runtime production | helper definition | DestroyItem |
| UI-Binding | Runtime/GenericItemManager.cs | 257 | Runtime production | direct Unity API call | Object.Destroy |
| UI-Binding | Runtime/GenericItemManager.cs | 261 | Runtime production | direct Unity API call | Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 26 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 31 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingContainerTests.cs | 223 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 29 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 34 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingNestedContainerTests.cs | 39 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingSelectionVisualTests.cs | 25 | Test | direct Unity API call | Object.DestroyImmediate |
| UI-Binding | Tests/Editor/UIBindingSelectionVisualTests.cs | 30 | Test | direct Unity API call | Object.DestroyImmediate |
| UI-FLow | Runtime/Providers/UIFlowPrefabScreenProvider.cs | 78 | Runtime production | direct Unity API call | Object.Destroy |
| UI-FLow | Tests/EditMode/UIFlowLogTests.cs | 32 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UI-FLow | Tests/PlayMode/UIFlowRuntimeNavigationTests.cs | 24 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate |
