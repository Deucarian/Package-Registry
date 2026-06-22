# Deucarian Migration Plan

Schema version: 2

This plan records the completed Common extraction and the remaining governance follow-ups. Existing repository main branches remain unchanged by the audit wave.

## Next Safe Steps

1. Git-only stable distribution is active.
2. npm/scoped-registry publication is deferred.
3. Optional future release wave: manual tags/releases and manual npm/scoped-registry publication.
4. Future package feature work can resume on develop.
5. Remaining reviewed extraction candidates can be handled only after audit-backed decisions.

## Still Not Done

- No Testing package.
- No Build Tools repository.
- No broad utility expansion beyond `UnityObjectUtility.DestroySafely`.
