"""Regression checks for the single reviewed local progress script exception."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import ValidationError, candidate, validate, validate_html


SCRIPT_URL = "/model-training-journal/assets/progress.js"
SCRIPT_TAG = f'<script src="{SCRIPT_URL}" defer></script>'
SCRIPT_BYTES = b'"use strict";\n'


class ProgressValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "assets/progress.js"
        self.generated = self.root / "docs/assets/progress.js"
        self.source.parent.mkdir(parents=True)
        self.generated.parent.mkdir(parents=True)
        self.source.write_bytes(SCRIPT_BYTES)
        self.generated.write_bytes(SCRIPT_BYTES)
        (self.root / "docs/.nojekyll").touch()
        self.page = self.root / "docs/index.html"
        self.page.write_text(SCRIPT_TAG, encoding="utf-8")

    def test_reviewed_local_script_and_copy_are_allowed(self):
        hashes = validate(self.root)
        self.assertIn("assets/progress.js", hashes)
        self.assertEqual(hashes["assets/progress.js"], hashes["docs/assets/progress.js"])

    def test_whitespace_inside_script_is_allowed(self):
        self.page.write_text(SCRIPT_TAG.replace("></script>", "> \n\t</script>"), encoding="utf-8")
        validate(self.root)

    def test_pages_without_script_remain_allowed(self):
        self.page.write_text("<p>Static journal</p>", encoding="utf-8")
        self.source.unlink()
        self.generated.unlink()
        validate(self.root)

    def test_one_script_on_each_page_is_allowed(self):
        (self.root / "docs/another.html").write_text(SCRIPT_TAG, encoding="utf-8")
        validate(self.root)

    def test_alternative_script_urls_are_rejected(self):
        alternatives = [
            "https://example.org/progress.js",
            "https://obra.github.io" + SCRIPT_URL,
            "//obra.github.io" + SCRIPT_URL,
            "assets/progress.js",
            "/assets/progress.js",
            "/model-training-journal/assets/other.js",
            "/model-training-journal/assets/../assets/progress.js",
            "/model-training-journal/assets/%70rogress.js",
            SCRIPT_URL + "?v=1",
            SCRIPT_URL + "#clock",
        ]
        for url in alternatives:
            with self.subTest(url=url):
                self.page.write_text(f'<script src="{url}" defer></script>', encoding="utf-8")
                with self.assertRaises(ValidationError):
                    validate_html(self.root)

    def test_extra_missing_or_duplicate_script_attributes_are_rejected(self):
        alternatives = [
            f'<script src="{SCRIPT_URL}" defer async></script>',
            f'<script src="{SCRIPT_URL}" defer type="text/javascript"></script>',
            f'<script src="{SCRIPT_URL}" defer data-clock="yes"></script>',
            f'<script src="{SCRIPT_URL}"></script>',
            f'<script src="{SCRIPT_URL}" defer="false"></script>',
            f'<script src="{SCRIPT_URL}" src="{SCRIPT_URL}" defer></script>',
            f'<script src="https://example.org/other.js" src="{SCRIPT_URL}" defer></script>',
            f'<script src="{SCRIPT_URL}" defer defer></script>',
            f'<script src="{SCRIPT_URL}" defer onload="alert(1)"></script>',
        ]
        for markup in alternatives:
            with self.subTest(markup=markup):
                self.page.write_text(markup, encoding="utf-8")
                with self.assertRaises(ValidationError):
                    validate_html(self.root)

    def test_inline_script_content_is_rejected(self):
        for content in ["alert(1)", "<!-- comment -->", "// comment", "&#32;", "<script></script>"]:
            with self.subTest(content=content):
                self.page.write_text(SCRIPT_TAG.replace("></script>", f">{content}</script>"), encoding="utf-8")
                with self.assertRaises(ValidationError):
                    validate_html(self.root)

    def test_malformed_or_multiple_script_tags_are_rejected(self):
        alternatives = [
            f'<script src="{SCRIPT_URL}" defer/>',
            f'<script src="{SCRIPT_URL}" defer /></script>',
            f'<script src="{SCRIPT_URL}" defer>',
            SCRIPT_TAG + SCRIPT_TAG,
            SCRIPT_TAG + "<script></script>",
            SCRIPT_TAG + "</script>",
            SCRIPT_TAG.replace("</script>", "</script ignored>"),
            SCRIPT_TAG.replace("</script>", "</script/>"),
        ]
        for markup in alternatives:
            with self.subTest(markup=markup):
                self.page.write_text(markup, encoding="utf-8")
                with self.assertRaises(ValidationError):
                    validate_html(self.root)

    def test_only_exact_javascript_file_paths_are_allowed(self):
        for name in ["assets/other.js", "docs/assets/other.js", "scripts/progress.js",
                     "content/progress.js", "assets/nested/progress.js", "docs/progress.js",
                     "assets/progress.mjs", "assets/other.JS"]:
            with self.subTest(name=name):
                extra = self.root / name
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_bytes(SCRIPT_BYTES)
                with self.assertRaises(ValidationError):
                    candidate(self.root)
                extra.unlink()

    def test_script_path_case_must_match(self):
        # Remove first so this also tests case-insensitive filesystems.
        self.source.unlink()
        self.source.with_suffix(".JS").write_bytes(SCRIPT_BYTES)
        with self.assertRaises(ValidationError):
            candidate(self.root)

    def test_script_files_must_still_be_utf8_and_pass_privacy_checks(self):
        for data in [b"\xff", b"\x00", ("ghp_" + "a" * 30).encode()]:
            with self.subTest(data=data[:4]):
                self.source.write_bytes(data)
                with self.assertRaises(ValidationError):
                    candidate(self.root)
        self.source.write_text("fixture-private-term", encoding="utf-8")
        with self.assertRaises(ValidationError):
            candidate(self.root, ["fixture-private-term"])

    def test_referenced_script_requires_exact_generated_copy(self):
        self.generated.write_bytes(SCRIPT_BYTES + b"// changed\n")
        with self.assertRaises(ValidationError):
            validate_html(self.root)

    def test_referenced_script_requires_source_and_generated_files(self):
        for path in [self.source, self.generated]:
            with self.subTest(path=path.relative_to(self.root)):
                path.unlink()
                with self.assertRaises(ValidationError):
                    validate_html(self.root)
                path.write_bytes(SCRIPT_BYTES)

    def test_new_reviewed_script_bytes_are_not_pinned_to_a_hash(self):
        for path in [self.source, self.generated]:
            path.write_bytes(b'"use strict";\n// A reviewed revision.\n')
        validate(self.root)


if __name__ == "__main__":
    unittest.main()
