import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from trust_metadata_validator import validate_repository


class TrustMetadataValidatorTests(unittest.TestCase):
    def _write(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _make_package(self, root: Path, dependency: bool = True) -> None:
        repo = "Example"
        dependencies = {"com.deucarian.common": "0.2.0"} if dependency else {}
        manifest = {
            "name": "com.deucarian.example",
            "version": "1.0.0",
            "repository": {"type": "git", "url": f"https://github.com/Deucarian/{repo}.git"},
            "documentationUrl": f"https://github.com/Deucarian/{repo}/blob/main/README.md",
            "changelogUrl": f"https://github.com/Deucarian/{repo}/blob/main/CHANGELOG.md",
            "licensesUrl": f"https://github.com/Deucarian/{repo}/blob/main/LICENSE.md",
            "dependencies": dependencies,
        }
        self._write(root, "package.json", json.dumps(manifest))
        self._write(root, "README.md", "readme")
        self._write(root, "CHANGELOG.md", "changelog")
        self._write(root, "LICENSE.md", "license")
        self._write(root, "SUPPORT.md", f"https://github.com/Deucarian/{repo}/issues")
        self._write(
            root,
            "SECURITY.md",
            f"https://github.com/Deucarian/{repo}/security/advisories/new\n"
            "Do not open a public issue",
        )
        if dependency:
            notice = (
                "## Review basis\n"
                "## Deucarian dependencies (not third-party)\n"
                "`com.deucarian.common` `0.2.0`"
            )
        else:
            notice = "## Review basis\nThe reviewed package.json declares no direct package dependencies."
        self._write(root, "THIRD_PARTY_NOTICES.md", notice)

    def test_accepts_complete_package_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_package(root)
            self.assertEqual([], validate_repository(root))

    def test_accepts_dependency_free_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_package(root, dependency=False)
            self.assertEqual([], validate_repository(root))

    def test_rejects_missing_dependency_notice(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_package(root)
            self._write(root, "THIRD_PARTY_NOTICES.md", "## Review basis")
            errors = validate_repository(root)
            self.assertTrue(any("does not record com.deucarian.common 0.2.0" in error for error in errors))

    def test_rejects_unverified_deucarian_email(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_package(root)
            self._write(
                root,
                "SUPPORT.md",
                "https://github.com/Deucarian/Example/issues support@deucarian.com",
            )
            errors = validate_repository(root)
            self.assertTrue(any("unverified Deucarian email" in error for error in errors))

    def test_accepts_registry_tooling_pins(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "SUPPORT.md", "https://github.com/Deucarian/Package-Registry/issues")
            self._write(
                root,
                "SECURITY.md",
                "https://github.com/Deucarian/Package-Registry/security/advisories/new\n"
                "Do not open a public issue",
            )
            self._write(
                root,
                "THIRD_PARTY_NOTICES.md",
                "## Review basis\n`tree_sitter` `0.25.2`",
            )
            self._write(root, "Tools/audit-requirements.txt", "tree_sitter==0.25.2\n")
            self.assertEqual(
                [], validate_repository(root, repository_name="Package-Registry")
            )


if __name__ == "__main__":
    unittest.main()
