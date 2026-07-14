# Security policy

## Supported versions

Security fixes are considered for the current `main` registry, governance data, and tooling. `develop` is a preview channel and may receive a fix before promotion. Older commits and locally modified copies are not guaranteed to receive backports.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/Deucarian/Package-Registry/security/advisories/new). Do not open a public issue for a suspected vulnerability.

Include the affected commit, Python and operating-system context, impact, a minimal sanitized input or proof of concept, and known mitigations. Remove tokens, private repository names, local paths, generated proprietary snippets, and personal data.

The maintainers will triage the report in GitHub's private advisory, may ask for additional evidence, and will coordinate disclosure after a fix or mitigation is available. No response or remediation deadline is guaranteed.

Security scope includes catalog integrity, URL and metadata validation, governance tooling, generated-audit handling, and reusable validation workflows in this repository. Package implementation vulnerabilities belong in the affected package repository.
