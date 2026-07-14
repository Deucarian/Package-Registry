# Third-party notices

This notice describes dependencies used by the Package Registry's governance and audit tooling. It does not replace the repository's [MIT license](LICENSE.md), and it does not grant rights to software installed separately.

## Review basis

The reviewed baseline is `origin/main` commit `f4f84e8032ffa72ea46b9093444b5a2fb7fa2dbf`, containing 47 tracked files. The inventory was checked for common vendor/third-party directories, compiled binaries and archives, Git submodules, Git LFS pointers, separate license markers, and media/font assets.

That inventory identified no files marked or located as vendored third-party source, no compiled binary/archive candidates, no submodules, no LFS pointers, and no media/font asset candidates. Tool dependencies are installed separately from `Tools/audit-requirements.txt`; they are not committed to this repository.

## Python tooling dependencies

| Distribution | Pinned version | Use | License / source |
|---|---:|---|---|
| `tree_sitter` | `0.25.2` | Python parser bindings used by authoritative audit generation | [MIT; PyPI release](https://pypi.org/project/tree-sitter/0.25.2/), [source license](https://github.com/tree-sitter/py-tree-sitter/blob/v0.25.2/LICENSE) |
| `tree_sitter_c_sharp` | `0.23.5` | C# grammar used by authoritative audit generation | [MIT; PyPI release](https://pypi.org/project/tree-sitter-c-sharp/0.23.5/), [source license](https://github.com/tree-sitter/tree-sitter-c-sharp/blob/v0.23.5/LICENSE) |

Python's standard library is used by the remaining tooling and is supplied by the host Python installation.

## Catalog and generated evidence

Entries in `packages.json` and repository URLs in governance documents are catalog references, not dependencies of this tooling and not bundled copies of the referenced packages. Each referenced package retains its own license and notices.

Committed audit JSON and Markdown files are generated summaries of repository metadata and source structure. The inventory did not identify copied package archives or compiled dependencies in those artifacts. Re-run the inventory and update this notice whenever tooling requirements or distributed content change.
