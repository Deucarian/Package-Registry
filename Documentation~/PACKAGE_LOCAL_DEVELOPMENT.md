# Package-local development

Package Installer's existing `package-management` capability includes connecting
a consuming Unity project to an explicitly selected package repository, tracking
that local-development session, and package-scoped Git changes. Editor owns the
shared presentation, including change lists, diffs, history and responsive forms.
No new capability owner, Git-client package or runtime dependency is introduced.

## Repository boundary

The default clone destination is `<project>/.deucarian/checkouts/<package-id>`.
Cloning there is an explicit action that adds a narrowly scoped local ignore
rule to the consumer repository's Git `info/exclude`, preserving existing rules.
It does not edit `.gitignore`, stage consumer files, or change consumer commits.
Already tracked files, junctions in local storage, consumer Git metadata used as
package metadata, and other nested checkout locations are rejected. A separate
external repository remains supported. Page opening never creates directories
or edits exclusions. The clone retains its own independent Git repository.

Connecting still modifies the consumer manifest and may cause Unity to update
the lockfile. These tracked changes are never hidden using ignore rules, index
flags or lockfile rewriting. Show **Local development active**, the checkout and
branch, and **Project connection temporarily changed**. **Restore installed
version** restores the original reference while preserving local source, edits
and commits. Do not describe an active local connection as a clean project.

Every mutation must validate the package ID, canonical working-tree root, common
Git directory, expected remote and selected branch. Consumer repositories,
ancestor repositories, PackageCache and aliases of those paths are forbidden
mutation targets. A manifest source change belongs to the consuming project's
recoverable session; its files must never enter the package's staging list.

Opening a page performs no Git mutations. Staging, branch changes, commits, fetch
and push require explicit actions showing their package scope. Existing staging
must be preserved; ambiguous index drift requires external review. Protected
branches, force pushes, resets, cleans, merges and rebases are outside this UI.
Use existing Git authentication and hooks. Do not collect credentials or expose
raw process diagnostics, application payloads or secrets in status snapshots.

## Git hosts and pull requests

GitHub and Bitbucket Cloud package repositories use the same local workflow:
connect the package checkout, edit and test in Unity, commit and push the feature
branch, then open the provider's pull-request page in the browser. Existing Git
tools remain valid for editing, branches, commits and pushes. Installer owns the
source connection and safe restoration; it does not need to become a complete
Git client or pull-request review tool.

The browser handoff is an explicit action against the verified package remote
and selected source/destination branches. Browser login, PR submission, reviewers,
checks and merging stay with the provider. Opening the page must not submit a PR,
push a branch or merge it. Do not collect provider tokens to build this handoff.

Private GitHub and Bitbucket Cloud packages reuse configured Git credentials or
SSH authentication for package access. Credential-free HTTPS and `git` SSH
remote forms identify the same repository on each host; a host or workspace
change is still a different repository and requires explicit verification.
Private packages remain subject to the [distribution policy](../DISTRIBUTION_POLICY.md)
and authenticated package validation. Bitbucket Data Center is outside this scope.

After testing, restore the original package reference before committing consumer
configuration. The package checkout and its work remain available for review.
Merging the package PR does not silently update applications: install the chosen
updated revision through Installer as a separate deliberate consumer change.

## Disposable source-switching fixtures

Installer implementation, review and validation hosts continue to consume
Installer, Editor and other supporting Deucarian packages through canonical Git
URLs. Unmerged implementation must first be pushed to a feature branch and the
host pinned to the exact candidate commit.

The explicitly requested local-source feature needs a narrowly scoped exception:
an isolated, disposable **target package fixture** may temporarily use a `file:`
reference while testing connect, resolution, editing, staging, commit, push and
restoration. The fixture repository and bare remote are local, contain synthetic
data, and never push to production package remotes. Installer and Editor remain
Git-pinned throughout. Record original and restored manifest/lock evidence,
consumer Git immutability, reload recovery and cancellation/failure outcomes.
This exception does not permit changing real application projects or validating
Installer/Editor from file references or embedded sources.

Local absolute paths are unavoidable in a Unity local package reference. Session
state is machine-local, and the user must restore the original reference before
committing consumer configuration. Disconnecting preserves the repository and
its uncommitted files and commits. Never silently replace a managed session via
an ordinary update, reinstall, remove or update-all operation.
