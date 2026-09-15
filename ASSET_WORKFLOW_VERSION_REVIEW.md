# Shared asset workflow version review — 2026-09-12

Editor 1.13.0 introduces public, reusable asset controls and discovery APIs.
Theming 1.9.0 introduces domain-owned deep customization of theme/audio assets.
Consumers declare these precise minimum versions to avoid compiling new menu code
against an earlier package version without those APIs.

Version-specific architecture allowances were reviewed against Editor develop
`4dc37ad56ce43c1fcff02e074b11b7e44f9e9592` and Theming develop
`e6e5e74f36cedbec9d6a7e1d39f4e54e775d3c8b`.
The following source files have no changes in this feature:
- Editor: `Editor/Definitions/DeucarianDefinitionImport.cs`,
  `Editor/DeucarianEditorAmbientGlass.cs`, `Editor/DeucarianEditorAppearance.cs`,
  `Editor/DeucarianToolHistory.cs`.
- Theming: `Runtime/Core/ThemeAudio.cs`,
  `Editor/Core/DeucarianThemeSceneApplication.cs`.

The same four Editor allowances (3, 2, 1, 1 mutable globals) and two Theming
allowances (1, 1) are retained for these exact versions. Existing version entries,
the baseline and policy thresholds are untouched. No allowance was increased.
The import queue, preferences, borrowed audio registration and repaint generation
retain the ownership and cleanup described in their existing reviews.

New asset field/catalog objects are instance-owned; panel attachment subscribes
to project changes and detach unsubscribes. Customization helpers carry no global
state and leave runtime activation to the owning domain workflow.

Validation: compare the six owners against the develop snapshots, run the syntax
metrics against both new package versions, and run the Registry Python tests.
No catalog or dependency graph change is involved, so Installer/Bootstrap
projections do not change. Develop only; no releases or main promotion.
