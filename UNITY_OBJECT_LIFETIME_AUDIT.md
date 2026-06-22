# Unity Object Lifetime Audit

Schema version: 1

Conclusion: **runtime Common package justified**

Summary: {"direct Unity API call": 51}

| Repository | File | Line | Scope | Kind | Symbol/Invocation |
| --- | --- | --- | --- | --- | --- |
| API | Tests/Editor/ApiClientTests.cs | 384 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| Bootstrap | Tests/Editor/DeucarianBootstrapTests.cs | 171 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
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
| UI-FLow | Tests/PlayMode/UIFlowRuntimeNavigationTests.cs | 24 | Test | direct Unity API call | UnityEngine.Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/RepositoryUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 26 | Test | direct Unity API call | Object.DestroyImmediate |
| UIBinding-CoreState-Integration | Tests/Editor/SelectionUIBindingTests.cs | 31 | Test | direct Unity API call | Object.DestroyImmediate |
