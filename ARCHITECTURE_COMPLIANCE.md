# Architecture Compliance

Schema version: 1

Canonical standard: https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md

This report separates required repository setup from the existing refactor
backlog. Setup findings should be corrected immediately. Existing production
files above 500 lines are
tracked as refactor work rather than making every current package fail CI at
once.

## Summary

- Repositories: 63
- Fully compliant repositories: 11

| Metric | Count |
| --- | --- |
| RefactorBacklog | 97 |
| SetupRequired | 48 |

| Metric | Count |
| --- | --- |
| MissingCanonicalArchitectureReference | 44 |
| MissingSharedArchitectureValidation | 4 |
| ProductionFileExceedsLineLimit | 97 |

## Repository Status

| Repository | Package | Status | Architecture reference | Shared validation | Production files | Test assemblies | Oversized files | Unowned files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Activity-Visualization | com.deucarian.activity-visualization | SetupRequired | No | Yes | 24 | 1 | 0 | 0 |
| API | com.deucarian.api | RefactorBacklog | Yes | Yes | 69 | 1 | 1 | 0 |
| Attacks | com.deucarian.attacks | SetupRequired | No | Yes | 30 | 1 | 5 | 0 |
| Auto-Defense | com.deucarian.auto-defense | SetupRequired | No | Yes | 1 | 2 | 0 | 0 |
| Auto-Defense-Suite | com.deucarian.auto-defense-suite | SetupRequired | No | Yes | 0 | 0 | 0 | 0 |
| Bootstrap | com.deucarian.bootstrap | Compliant | Yes | Yes | 35 | 1 | 0 | 0 |
| Build-Pipeline | com.deucarian.build-pipeline | RefactorBacklog | Yes | Yes | 23 | 1 | 2 | 0 |
| Camera-Navigation | com.deucarian.camera-navigation | RefactorBacklog | Yes | Yes | 26 | 1 | 1 | 0 |
| CameraNavigation-InputSystem-Integration | com.deucarian.camera-navigation.input-system-integration | Compliant | Yes | Yes | 9 | 1 | 0 | 0 |
| Combat | com.deucarian.combat | SetupRequired | No | Yes | 2 | 1 | 0 | 0 |
| Command-Routing | com.deucarian.command-routing | RefactorBacklog | Yes | Yes | 30 | 1 | 1 | 0 |
| Command-Routing-UDP-Integration | com.deucarian.command-routing.udp-integration | Compliant | Yes | Yes | 9 | 1 | 0 | 0 |
| Command-Routing-WebGL-Integration | com.deucarian.command-routing.webgl-integration | SetupRequired | No | Yes | 11 | 1 | 0 | 0 |
| Common | com.deucarian.common | SetupRequired | No | Yes | 2 | 2 | 0 | 0 |
| Core-State | com.deucarian.core-state | SetupRequired | No | Yes | 10 | 1 | 0 | 0 |
| Defense-Games | com.deucarian.defense-games | SetupRequired | No | Yes | 1 | 2 | 0 | 0 |
| Diagnostics | com.deucarian.diagnostics | RefactorBacklog | Yes | Yes | 16 | 1 | 1 | 0 |
| Editor | com.deucarian.editor | RefactorBacklog | Yes | Yes | 40 | 2 | 2 | 0 |
| Encounters | com.deucarian.encounters | SetupRequired | No | Yes | 1 | 1 | 0 | 0 |
| Game-Content-Authoring | com.deucarian.game-content-authoring | SetupRequired | No | Yes | 33 | 1 | 13 | 0 |
| Gameplay-Foundation | com.deucarian.gameplay-foundation | SetupRequired | No | Yes | 5 | 1 | 0 | 0 |
| Idle-Progression | com.deucarian.idle-progression | SetupRequired | No | Yes | 1 | 1 | 0 | 0 |
| Logging | com.deucarian.logging | Compliant | Yes | Yes | 15 | 2 | 0 | 0 |
| Media | com.deucarian.media | Compliant | Yes | Yes | 11 | 1 | 0 | 0 |
| Media-API-Integration | com.deucarian.media.api-integration | Compliant | Yes | Yes | 4 | 1 | 0 | 0 |
| Monetization | com.deucarian.monetization | SetupRequired | No | Yes | 1 | 1 | 0 | 0 |
| Object-Loading | com.deucarian.object-loading | SetupRequired | No | Yes | 19 | 2 | 1 | 0 |
| Object-Selection | com.deucarian.object-selection | SetupRequired | No | Yes | 25 | 1 | 0 | 0 |
| ObjectLoading-API-Integration | com.deucarian.object-loading.api-integration | SetupRequired | No | Yes | 4 | 1 | 0 | 0 |
| ObjectSelection-CoreState-Integration | com.deucarian.object-selection.core-state-integration | SetupRequired | No | Yes | 5 | 1 | 0 | 0 |
| Package-Installer | com.deucarian.package-installer | RefactorBacklog | Yes | Yes | 59 | 1 | 13 | 0 |
| Package-Registry |  | Compliant | Yes | Yes | 0 | 0 | 0 | 0 |
| Persistence | com.deucarian.persistence | SetupRequired | No | Yes | 8 | 1 | 0 | 0 |
| Pointer-Capture | com.deucarian.pointer-capture | Compliant | Yes | Yes | 9 | 1 | 0 | 0 |
| Progression | com.deucarian.progression | SetupRequired | No | Yes | 4 | 1 | 0 | 0 |
| Projectiles | com.deucarian.projectiles | SetupRequired | No | Yes | 1 | 1 | 0 | 0 |
| Run-Upgrades | com.deucarian.run-upgrades | SetupRequired | No | Yes | 9 | 1 | 3 | 0 |
| Selection-Suite | com.deucarian.selection-suite | SetupRequired | No | Yes | 0 | 0 | 0 | 0 |
| Session | com.deucarian.session | Compliant | Yes | Yes | 15 | 1 | 0 | 0 |
| Session-API-Integration | com.deucarian.session.api-integration | Compliant | Yes | Yes | 13 | 1 | 0 | 0 |
| Simultria-API | com.deucarian.simultria-api | SetupRequired | No | Yes | 35 | 1 | 0 | 0 |
| Simultria-Viewer-Connection | com.deucarian.simultria-viewer-integration | SetupRequired | No | No | 29 | 1 | 3 | 0 |
| Template-Game-Idle-Auto-Defense | com.deucarian.template.game.idle-auto-defense | SetupRequired | No | Yes | 49 | 2 | 15 | 0 |
| Template-Game-Movement-FPS | com.deucarian.template.game.movement-fps | SetupRequired | No | Yes | 19 | 2 | 3 | 0 |
| Template-Game-Survivors | com.deucarian.template.game.survivors | SetupRequired | No | Yes | 23 | 2 | 13 | 0 |
| Template-Viewer-Web | com.deucarian.template.viewer.web | SetupRequired | No | Yes | 23 | 2 | 2 | 0 |
| Test-Automation | com.deucarian.test-automation | Compliant | Yes | Yes | 0 | 1 | 0 | 0 |
| Theming | com.deucarian.theming | RefactorBacklog | Yes | Yes | 71 | 2 | 7 | 0 |
| UI | com.deucarian.ui | SetupRequired | No | Yes | 14 | 1 | 1 | 0 |
| UI-Binding | com.deucarian.ui-binding | SetupRequired | No | Yes | 12 | 1 | 0 | 0 |
| UI-FLow | com.deucarian.ui-flow | SetupRequired | No | Yes | 45 | 2 | 2 | 0 |
| UIBinding-CoreState-Integration | com.deucarian.ui-binding.core-state-integration | SetupRequired | No | Yes | 3 | 1 | 0 | 0 |
| Viewer-Authentication | com.deucarian.authentication | SetupRequired | No | Yes | 46 | 1 | 1 | 0 |
| Viewer-Navigation | com.deucarian.viewer-navigation | SetupRequired | No | Yes | 29 | 2 | 0 | 0 |
| Viewer-Rendering | com.deucarian.viewer-rendering | SetupRequired | No | No | 16 | 2 | 0 | 0 |
| Viewer-Shell | com.deucarian.viewer-shell | SetupRequired | No | No | 17 | 1 | 0 | 0 |
| Weapon-Systems | com.deucarian.weapon-systems | SetupRequired | No | Yes | 9 | 1 | 1 | 0 |
| Web-Viewer-Suite | com.deucarian.web-viewer-suite | SetupRequired | No | Yes | 0 | 0 | 0 | 0 |
| WebGL-Template | com.deucarian.webgl-template | SetupRequired | No | No | 2 | 1 | 0 | 0 |
| World-Navigation | com.deucarian.world-navigation | SetupRequired | No | Yes | 1 | 2 | 0 | 0 |
| World-Spawning | com.deucarian.world-spawning | SetupRequired | No | Yes | 1 | 2 | 1 | 0 |
| XR-UI | com.deucarian.xr-ui | SetupRequired | No | Yes | 38 | 1 | 5 | 0 |
| XR-UI-Theming-Integration | com.deucarian.xr-ui.theming-integration | SetupRequired | No | Yes | 1 | 1 | 0 | 0 |

## Findings

| Repository | Kind | Disposition | File | Lines | Limit | Action |
| --- | --- | --- | --- | --- | --- | --- |
| API | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Core/ApiComposition.cs | 512 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Activity-Visualization | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Attacks | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Attacks | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/AttackProviderV2.cs | 1523 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Attacks | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/AttackGameContentAuthoringProviders.cs | 1342 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Attacks | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/EnemyProviderV2.cs | 1277 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Attacks | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/WaveProviderV2.cs | 1201 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Attacks | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/AttackGameContentPreview.cs | 1101 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Auto-Defense | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Auto-Defense-Suite | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Build-Pipeline | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/DeucarianBuildManagerWindow.cs | 952 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Build-Pipeline | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/NewtonsoftLinking/NewtonsoftJsonContractDiscovery.cs | 594 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Camera-Navigation | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/DeucarianOrbitCameraController.cs | 562 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Combat | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Command-Routing | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/CommandRoutingEditorWindow.cs | 922 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Command-Routing-WebGL-Integration | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Common | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Core-State | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Defense-Games | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Diagnostics | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/DiagnosticsWindow.cs | 646 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Editor | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/DeucarianEditorWorkbench.cs | 1180 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Editor | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/DeucarianEditorWorkbenchGUI.cs | 581 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Encounters | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Game-Content-Authoring | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentEditSessionCoordinator.cs | 1835 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentEditWorkbench.cs | 1752 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentStructuredCollectionEditing.cs | 1280 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentLibraryProviderV2.cs | 1264 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentAuthoringObjectPreview.cs | 997 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentEditingModels.cs | 954 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentAuthoringWindow.cs | 824 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentPackAwareViews.cs | 714 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentCollectionEditing.cs | 713 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentLibraryService.cs | 592 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentPackBrowser.cs | 585 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentPackModels.cs | 553 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Game-Content-Authoring | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentPackContext.cs | 537 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Gameplay-Foundation | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Idle-Progression | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Monetization | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Object-Loading | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Object-Loading | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Core/ObjectLoadTypes.cs | 513 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Object-Selection | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| ObjectLoading-API-Integration | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| ObjectSelection-CoreState-Integration | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/UI/PackageInstaller/PackageEcosystemGraphView.cs | 11367 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/PackageInstallerWindow.cs | 8638 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageUpdateCheckService.cs | 2888 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageEcosystemGraphLayout.cs | 2513 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageInstallService.cs | 1950 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageDependencyInstaller.cs | 1479 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageSampleImportService.cs | 977 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Models/PackageEcosystemGraph.cs | 838 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageOperationStateRepository.cs | 724 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageDetectionService.cs | 640 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageEcosystemGraphBuilder.cs | 599 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageRegistryProvider.cs | 551 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Package-Installer | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Services/PackageGraphHierarchyBuilder.cs | 508 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Persistence | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Progression | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Projectiles | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Run-Upgrades | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Run-Upgrades | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/RunUpgradeProviderV2.cs | 1266 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Run-Upgrades | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/RunUpgradeGameContentAuthoringProvider.cs | 575 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Run-Upgrades | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/RunUpgradesCore.cs | 539 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Selection-Suite | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Simultria-API | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Simultria-Viewer-Connection | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Simultria-Viewer-Connection | MissingSharedArchitectureValidation | SetupRequired | .github/workflows |  |  | Run the shared Deucarian package validator in continuous integration. |
| Simultria-Viewer-Connection | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SimultriaViewerDevelopmentWindow.cs | 720 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Simultria-Viewer-Connection | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SimultriaViewerEditorAuthenticationWorkspace.cs | 680 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Simultria-Viewer-Connection | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Authentication/SimultriaViewerConnectionAuthentication.cs | 612 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/IdleAutoDefenseTemplate.cs | 6890 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefenseContentEditingMappings.cs | 1820 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentSetProviderV2.cs | 1778 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefenseContentPackIndex.cs | 1758 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentPackProviderV2.cs | 1301 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefenseTemplateSetupWizard.cs | 1131 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/IdleAutoDefensePlayerExperienceController.Ui.cs | 1081 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefenseContentEditSession.cs | 976 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefenseContentEditingBackend.cs | 865 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/IdleAutoDefensePlayableContentAuditMenu.cs | 761 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/GameContentSetValidation.cs | 677 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/GameContentSetGameContentAuthoringProvider.cs | 648 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/IdleAutoDefensePlayerExperienceController.cs | 640 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/IdleAutoDefenseAuthoredCoreValidation.cs | 547 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Idle-Auto-Defense | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/IdleAutoDefenseRewardDraftCatalog.cs | 539 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Movement-FPS | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Template-Game-Movement-FPS | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Movement/WallrunnerMotor.cs | 3536 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Movement-FPS | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Bootstrap/MovementFpsTemplateController.cs | 922 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Movement-FPS | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Actors/MovementFpsPlayerController.cs | 587 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsTemplateController.cs | 15821 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsContentValidation.cs | 4485 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/BasicSurvivorsGame.cs | 2707 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsAuthoredContent.cs | 2464 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SurvivorsContentEditSource.cs | 1950 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SurvivorsLosslessJson.cs | 1642 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsWeaponArchetypes.cs | 1309 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SurvivorsContentPackIndex.cs | 1179 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsMetaProgression.cs | 945 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/SurvivorsContentEditSession.cs | 941 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsUiTheme.cs | 739 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsPayloadWeapons.cs | 688 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Game-Survivors | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/SurvivorsRunFlow.cs | 553 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Viewer-Web | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Template-Viewer-Web | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/WebViewerBootstrap.cs | 702 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Template-Viewer-Web | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/WebViewerApplication.cs | 676 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianThemeManagerWindow.cs | 2531 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianDefaultThemeAssetFactory.cs | 1978 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianThemingMenuActions.cs | 1795 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianThemePackAssetFactory.cs | 905 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianThemeManagerWorkflow.cs | 818 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Core/DeucarianThemeProvider.cs | 622 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Theming | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/Core/DeucarianThemingInspectorListFilter.cs | 582 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| UI | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/UIToolkit/DeucarianIconButtonStyle.cs | 527 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| UI-Binding | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| UI-FLow | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| UI-FLow | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Navigation/UIFlowHost.cs | 984 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| UI-FLow | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Navigation/UIFlowNavigator.cs | 966 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| UIBinding-CoreState-Integration | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Viewer-Authentication | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Viewer-Authentication | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/AuthenticationWindow.cs | 1390 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Viewer-Navigation | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Viewer-Rendering | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Viewer-Rendering | MissingSharedArchitectureValidation | SetupRequired | .github/workflows |  |  | Run the shared Deucarian package validator in continuous integration. |
| Viewer-Shell | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Viewer-Shell | MissingSharedArchitectureValidation | SetupRequired | .github/workflows |  |  | Run the shared Deucarian package validator in continuous integration. |
| Weapon-Systems | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| Weapon-Systems | ProductionFileExceedsLineLimit | RefactorBacklog | Editor/WeaponProviderV2.cs | 967 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| Web-Viewer-Suite | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| WebGL-Template | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| WebGL-Template | MissingSharedArchitectureValidation | SetupRequired | .github/workflows |  |  | Run the shared Deucarian package validator in continuous integration. |
| World-Navigation | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| World-Spawning | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| World-Spawning | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/WorldSpawningCore.cs | 572 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
| XR-UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Controls/CustomPressableSurface.Hierarchy.cs | 1314 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Controls/CustomButtonSettings.cs | 972 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Controls/CustomSelectableFeedback.cs | 930 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/Controls/CustomPressableSurface.cs | 826 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI | ProductionFileExceedsLineLimit | RefactorBacklog | Runtime/XrUiColorPalette.cs | 536 | 500 | Extract responsibilities until the production file is at most 500 lines. |
| XR-UI-Theming-Integration | MissingCanonicalArchitectureReference | SetupRequired | AGENTS.md |  |  | Reference https://github.com/Deucarian/Package-Registry/blob/main/ARCHITECTURE.md from the repository agent guidance. |
