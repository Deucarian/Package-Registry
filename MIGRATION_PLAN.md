# Deucarian Migration Plan

Schema version: 2

This plan remains audit/governance-only. No production source, package dependencies, package versions, package READMEs, or main branches are changed.

## Next Safe Steps

1. Review `EXTRACTION_DECISIONS.md` before extracting any clone candidate.
2. Address Debug API findings from `DEBUG_API_AUDIT.md`; production/sample findings with policy disposition `Migrate` should move to `com.deucarian.logging` in a later source wave.
3. Review `UNITY_OBJECT_LIFETIME_AUDIT.md`; conclusion: Create com.deucarian.common.
4. Resolve `DOCUMENTATION_DRIFT.md` findings before dependency migrations.
5. Use `DEPENDENCY_USAGE_AUDIT.md` to decide which dependencies are required, editor-only, sample-only, optional-version-defined, missing hard dependencies, apparently unused, or review required.
6. Add architecture validation using `capabilities.json` and `dependency-rules.json`.

## Still Not Done

- No Common package.
- No Testing package.
- No Build Tools repository.
- No package dependency changes.
- No source migrations.
