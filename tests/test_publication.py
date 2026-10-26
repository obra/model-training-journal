"""Regression checks for the publication boundary, using synthetic fixtures."""
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import ValidationError, candidate, digest, scan_text, validate_html
from review import terms_digest, verify_receipt
from publish import ORIGIN, PUBLIC_EMAIL, PUBLIC_NAME, commit_environment, git_preflight, publish, verify_committed, verify_staged


class PublicationTests(unittest.TestCase):
    def test_secret_and_private_identifiers_are_rejected(self):
        examples = [
            "ghp_" + "a" * 30,
            "10" + ".24.3.4",
            "/" + "home/fixture/person.txt",
            "private.person" + "@example.org",
            "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
            "source_" + "thread_id",
            'api_key="' + "a" * 20 + '"',
        ]
        for example in examples:
            with self.subTest(example=example[:6]):
                with self.assertRaises(ValidationError):
                    scan_text(example, "content/post.md", [])

    def test_private_terms_are_case_insensitive_and_word_bounded(self):
        with self.assertRaises(ValidationError):
            scan_text("Recorded on FIXTURE-HOST.", "content/post.md", ["fixture-host"])
        scan_text("unrelated hostnameprefix", "content/post.md", ["hostname"])

    def test_public_versions_and_statistics_are_allowed(self):
        scan_text("PyTorch 2.14.0; 11,697.79 tokens/s; 2.164 GiB; https://example.org/reference", "content/post.md", [])

    def test_symlink_and_unknown_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "content").mkdir()
            (root / "content/post.md").symlink_to(root / "README.md")
            with self.assertRaises(ValidationError):
                candidate(root)
            (root / "content/post.md").unlink()
            (root / "raw.log").write_text("raw output")
            with self.assertRaises(ValidationError):
                candidate(root)

    def test_html_checks_links_anchors_and_external_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / ".nojekyll").touch()
            page = docs / "index.html"
            page.write_text('<main id="main"><a href="#main">Read</a></main>')
            validate_html(root)
            for bad in ['<a href="/wrong/">x</a>', '<a href="#missing">x</a>',
                        '<img src="https://example.org/pixel">', '<script>alert(1)</script>',
                        '<style>body{}</style>', '<p style="color:red">x</p>',
                        '<meta http-equiv="refresh" content="0;url=https://example.org">']:
                page.write_text(bad)
                with self.assertRaises(ValidationError):
                    validate_html(root)

    def test_css_imports_and_vector_assets_require_explicit_future_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / ".nojekyll").touch()
            (docs / "index.html").write_text("<p>Journal</p>")
            (docs / "site.css").write_text('@' + 'import "https://example.org/font.css";')
            with self.assertRaises(ValidationError):
                validate_html(root)
            (docs / "site.css").unlink()
            (docs / "chart.svg").write_text("<svg></svg>")
            with self.assertRaises(ValidationError):
                candidate(root)

    def receipt(self, hashes, terms):
        return {"schema": 1, "repository": "obra/model-training-journal", "files": hashes,
                "candidate_sha256": digest(hashes), "private_terms_sha256": terms_digest(terms),
                "reviewed_utc": datetime.now(timezone.utc).isoformat(),
                "checks": {"privacy": True, "factual_accuracy": True, "licensing": True, "rendered_pages": True},
                "note": "Compared source evidence, rights and rendered output."}

    def test_receipt_rejects_changed_bytes_missing_checks_and_expiry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            receipt = Path(tmp) / "review.json"
            hashes = {"README.md": "a" * 64}
            terms = ["fixture-host"]
            data = self.receipt(hashes, terms)
            receipt.write_text(json.dumps(data))
            verify_receipt(receipt, hashes, terms, root)
            with self.assertRaises(ValidationError):
                verify_receipt(receipt, {"README.md": "b" * 64}, terms, root)
            data["checks"]["licensing"] = False
            receipt.write_text(json.dumps(data))
            with self.assertRaises(ValidationError):
                verify_receipt(receipt, hashes, terms, root)
            data = self.receipt(hashes, terms)
            data["reviewed_utc"] = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
            receipt.write_text(json.dumps(data))
            with self.assertRaises(ValidationError):
                verify_receipt(receipt, hashes, terms, root)

    def test_invalid_candidate_stops_before_any_git_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "README.md").write_text("ghp_" + "b" * 30)
            terms = Path(tmp) / "terms.txt"
            terms.write_text("fixture-host")
            with patch("publish.git") as git, patch("publish.subprocess.run") as run:
                with self.assertRaises(ValidationError):
                    publish(Path(tmp) / "review.json", terms, "Publish reviewed entry", root)
                git.assert_not_called()
                run.assert_not_called()

    def test_stale_review_stops_before_fetch_stage_commit_or_push(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "README.md").write_text("Safe journal candidate")
            terms = Path(tmp) / "terms.txt"
            terms.write_text("fixture-host")
            receipt = Path(tmp) / "review.json"
            receipt.write_text(json.dumps(self.receipt({"README.md": "old"}, ["fixture-host"])))
            with patch("publish.git_preflight", return_value=[]), patch("publish.subprocess.run") as run, \
                 patch("publish.validate", return_value={"README.md": "new"}), patch("publish.git") as git:
                with self.assertRaises(ValidationError):
                    publish(receipt, terms, "Publish reviewed entry", root)
                run.assert_not_called()
                git.assert_not_called()

    def test_staged_blob_must_equal_reviewed_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "README.md").write_text("Safe staged bytes")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
            with self.assertRaises(ValidationError):
                verify_staged({"README.md": "wrong"}, [], root)

    def test_multiple_push_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True)
            subprocess.run(["git", "remote", "add", "origin", ORIGIN], cwd=root, check=True)
            subprocess.run(["git", "config", "--add", "remote.origin.pushurl", ORIGIN], cwd=root, check=True)
            subprocess.run(["git", "config", "--add", "remote.origin.pushurl", "https://example.org/other.git"], cwd=root, check=True)
            with self.assertRaises(ValidationError):
                git_preflight(root)

    def test_commit_hook_cannot_publish_different_bytes(self):
        calls = [b"100644 blob abc\tREADME.md\0", b"Changed by a hook"]
        with patch("publish.git", side_effect=calls):
            with self.assertRaises(ValidationError):
                verify_committed("commit", {"README.md": "reviewed-hash"}, [])

    def test_unreviewed_parent_history_is_refused(self):
        with patch("publish.git", return_value="tip other-parent"):
            with self.assertRaises(ValidationError):
                verify_committed("tip", {}, [], base="reviewed-base")

    def test_inherited_personal_git_identity_is_overridden(self):
        with patch.dict("publish.os.environ", {"GIT_AUTHOR_NAME": "Fixture Private", "GIT_COMMITTER_EMAIL": "fixture" + "@example.org"}):
            env = commit_environment()
            self.assertEqual(env["GIT_AUTHOR_NAME"], PUBLIC_NAME)
            self.assertEqual(env["GIT_COMMITTER_EMAIL"], PUBLIC_EMAIL)


if __name__ == "__main__":
    unittest.main()
