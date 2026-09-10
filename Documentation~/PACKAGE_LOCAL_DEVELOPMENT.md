# Package-local development

Package Installer's existing `package-management` capability includes connecting
a consuming Unity project to an explicitly selected package repository, tracking
that local-development session, and package-scoped Git changes. Editor owns the
shared presentation, including change lists, diffs, history and responsive forms.
No new capability owner, Git-client package or runtime dependency is introduced.

## Repository boundary

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
