# Deucarian Distribution Policy

## Current Channels

Stable Deucarian Unity packages are distributed by Git URL pinned to the `main` branch:

```text
https://github.com/Deucarian/<Repo>.git#main
```

Development packages are distributed by Git URL pinned to the `develop` branch:

```text
https://github.com/Deucarian/<Repo>.git#develop
```

`packages.json` is the source of truth for stable and development Git URLs. The Package Installer consumes the remote registry from `main` and keeps a bundled fallback catalog for offline or recovery flows.

GitHub (`github.com`) and Bitbucket Cloud (`bitbucket.org`) are supported package
hosts. A channel may use credential-free HTTPS, full SSH or Git's SSH shorthand:

```text
https://bitbucket.org/<workspace>/<repo>.git#develop
ssh://git@bitbucket.org/<workspace>/<repo>.git#develop
git@bitbucket.org:<workspace>/<repo>.git#develop
```

The same forms are accepted for GitHub. Stable channels still require `#main`
and development channels `#develop`. URLs must identify a repository root;
embedded HTTPS usernames/passwords/tokens, query strings, custom hosts and
Bitbucket Data Center URLs are not supported catalog channels. Keep existing
GitHub URLs until actual migration destinations and refs have been verified;
provider support alone does not migrate a repository or change consumer pins.

## Private package access

Set `sourceVisibility: private` for private source repositories on either host.
Authentication stays in the user's existing Git credential helper or SSH setup;
catalogs, package manifests and fallback catalogs must never contain credentials.
The remote-ref validation gate uses native `git ls-remote`, including configured
Git authentication, and must pass in an authorized environment before promotion.
See [Bitbucket clone and authentication guidance](https://support.atlassian.com/bitbucket-cloud/docs/clone-a-repository/).

Private source remains excluded from credential-free organization audit
provisioning. Registry metadata validation still applies, and authenticated
package CI must run the canonical validators, architecture/AOT checks and Unity
tests without publishing private source. This provider support does not migrate
the Registry/Bootstrap repositories, registry feed or GitHub reusable workflows
to Bitbucket Pipelines. CI migration requires explicit repository destinations,
equivalent checks and appropriate runner authentication before retiring the
existing workflows. Public audit checkout names must remain unique across hosts.

## Review-only catalog entries

A registry feature branch may carry planned channel URLs so Package Installer and Bootstrap catalog projections can be reviewed before publication. Those entries are not distributable and the planned URLs are not evidence that either branch is reachable.

Do not promote a review-only entry to `develop` or `main` until all of the following are true:

- The package repository exists and contains the reviewed source.
- Its `develop` and `main` refs exist as required by the target channel.
- `deucarian_package_validator.py --check-remote-urls` passes for the registry.
- A clean consumer checkout resolves the package without workspace-relative sources.

Until that gate passes, generated fallback catalogs may be committed only on matching review branches and must not be described as installable or published.

## Deferred Channels

npm/scoped-registry publication is deferred. Do not publish Deucarian packages to npm as part of normal branch promotion.

Git tags and GitHub releases are also deferred. They are not required for the current stable Git workflow and must not be created automatically from branch promotion.

## Future Release Waves

Future npm/scoped-registry publication, Git tag creation, or GitHub release creation must happen through a separate deliberate release wave with explicit validation and manual approval.

Release-capable workflows must remain manual-only and guarded while Git-only distribution is active.
