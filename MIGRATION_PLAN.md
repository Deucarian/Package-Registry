# Deucarian Migration Plan

Generated: 2026-06-22

This plan starts the requested migration but deliberately stops before extraction because the inventory and audit artifacts must exist first.

## Wave 1: Governance And Audit Baseline

Status: started in Package Registry on `develop`.

Artifacts created:

- `REUSE_AUDIT.md`
- `PACKAGE_CAPABILITY_MATRIX.md`
- `DEPENDENCY_GRAPH.md`
- `DUPLICATION_REPORT.json`
- `capabilities.json`
- `dependency-rules.json`

## Required Follow-Up Order

1. Review `DUPLICATION_REPORT.json` clone groups and classify each candidate against the extraction thresholds.
2. Run the dedicated DestroyUnityObject migration review. Current lifetime/destruction hits: 57.
3. Review direct Debug API hits. Current non-allowlisted baseline hits: 37.
4. Resolve documentation and version drift before changing dependencies.
5. Decide whether Build Tools or a `.github` governance repository owns reusable validation and workflows.
6. Only then begin owner-package extraction waves.

## Initial High-Confidence Work Items

- Add architecture validation for direct Debug usage using `capabilities.json`.
- Add registry/package dependency consistency checks from `dependency-rules.json`.
- Keep Package Registry dependency consistency enforced; the initial audit found no registry dependency drift.
- Review `Logging -> Editor` as an explicit dependency exception before allowing Editor to consume Logging.
- Preserve Bootstrap self-containment; documentation changes are allowed but dependency adoption is not.

## Items Intentionally Not Done In This Wave

- No `com.deucarian.common` package was created.
- No `com.deucarian.testing` package was created.
- No source call sites were migrated.
- No package dependencies or asmdef references were changed.
- No README files outside Package Registry were rewritten.
- No main branch was modified.

## Validation Needed Before Dependency Migration

- Compile/test each owner package after any extracted API is added.
- Compile/test every consumer after dependency adoption.
- Build an integration validation project resolving all develop package URLs.
- Run architecture validation against the baseline and remove exceptions intentionally.
