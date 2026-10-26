#!/usr/bin/env python3
"""Validate the complete public candidate, without reading the private notebook."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "/model-training-journal"
ROOT_FILES = {"README.md", "PUBLISHING.md", "requirements.txt", ".gitignore", "PRODUCT.md", "DESIGN.md"}
PUBLIC_DIRS = {"content", "templates", "assets", "scripts", "tests", "docs"}
LOCAL_DIRS = {".git", ".venv", ".impeccable", ".pytest_cache", ".review"}
EXTENSIONS = {".md", ".json", ".py", ".txt", ".html", ".css", ".xml"}
PROGRESS_SCRIPT_FILES = {"assets/progress.js", "docs/assets/progress.js"}
PROGRESS_SCRIPT_TAG = f'<script src="{BASE}/assets/progress.js" defer>'
MAX_BYTES = 1_000_000


class ValidationError(ValueError):
    pass


def allowed_path(name: str) -> bool:
    path = Path(name)
    return (not path.is_absolute() and ".." not in path.parts and
            (name in ROOT_FILES or (len(path.parts) > 1 and path.parts[0] in PUBLIC_DIRS)))


def private_terms(path: Path, root: Path = ROOT) -> list[str]:
    path = path.resolve()
    if path == root.resolve() or root.resolve() in path.parents:
        raise ValidationError("Private terms must be stored outside the public checkout")
    terms = [line.strip() for line in path.read_text().splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    if not terms or any(len(term) < 3 for term in terms):
        raise ValidationError("Supply nonempty private terms of at least three characters")
    return terms


def scan_text(text: str, name: str, terms: list[str]) -> None:
    patterns = {
        "credential token": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|xox[baprs]-[A-Za-z0-9-]{12,}|sk-[A-Za-z0-9_-]{24,})\b",
        "private key": r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----",
        "private absolute path": r"(?<![A-Za-z0-9])/(?:Users|home|root)/[A-Za-z0-9_.-]+(?:/|\b)",
        "personal email address": r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b",
        "internal task identifier": r"\b(?:source_" + r"(?:thread|orbit)_id|codex_" + r"delegation|transcript_" + r"evidence)\b",
        "embedded credential assignment": r"(?i)\b(?:password|api_key|access_token|auth_token|secret_key)\s*[:=]\s*[\"'][A-Za-z0-9_+/=-]{8,}[\"']",
    }
    for label, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if label == "personal email address":
            matches = [match for match in matches if match != "git@github.com" and
                       not match.endswith("@users.noreply.github.com")]
        if matches:
            raise ValidationError(f"{name}: possible {label}; review privately")
    for match in re.finditer(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", text):
        try:
            addr = ipaddress.ip_address(match.group())
        except ValueError:
            continue
        if addr.is_private or addr.is_loopback or addr.is_link_local:
            raise ValidationError(f"{name}: nonpublic network address")
    for term in terms:
        if re.search(r"(?<![\w])" + re.escape(term) + r"(?![\w])", text, re.IGNORECASE):
            raise ValidationError(f"{name}: private review term found; inspect locally")


def candidate(root: Path = ROOT, terms: list[str] | None = None) -> dict[str, str]:
    terms = terms or []
    hashes: dict[str, str] = {}
    paths = []
    for directory, subdirs, filenames in os.walk(root, followlinks=False):
        subdirs[:] = [name for name in subdirs if name != "__pycache__" and
                      not (Path(directory) == root and name in LOCAL_DIRS)]
        paths.extend(Path(directory) / name for name in subdirs + filenames)
    for path in sorted(paths):
        rel = path.relative_to(root)
        if rel.parts[0] in LOCAL_DIRS or "__pycache__" in rel.parts:
            continue
        if path.is_symlink():
            raise ValidationError(f"{rel}: symlinks cannot enter the public candidate")
        if path.is_dir():
            if len(rel.parts) == 1 and rel.parts[0] not in PUBLIC_DIRS:
                raise ValidationError(f"{rel}: unexpected directory in publishing checkout")
            continue
        name = rel.as_posix()
        if not allowed_path(name):
            raise ValidationError(f"{name}: not in the publication allowlist")
        if (path.suffix not in EXTENSIONS and path.name not in {".gitignore", ".nojekyll"}
                and name not in PROGRESS_SCRIPT_FILES):
            raise ValidationError(f"{name}: unexpected file type")
        data = path.read_bytes()
        if len(data) > MAX_BYTES or b"\0" in data:
            raise ValidationError(f"{name}: binary or oversized file")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError(f"{name}: not UTF-8 text") from exc
        scan_text(text, name, terms)
        if path.suffix == ".py":
            compile(text, name, "exec")
        hashes[name] = hashlib.sha256(data).hexdigest()
    if not hashes:
        raise ValidationError("The public candidate is empty")
    return hashes


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.problems: list[str] = []
        self.script_count = 0
        self._in_script = False
        self._text = text
        self._line_offsets = [0] + [match.end() for match in re.finditer("\n", text)]
        self.feed(text)
        self.close()
        if self._in_script:
            self.problems.append("unclosed progress script")

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.script_count += 1
            self._in_script = True
            # Keep this exception literal: alternate URLs, attributes, duplicate
            # attributes and unusual parsing forms all require a fresh review.
            if self.get_starttag_text() != PROGRESS_SCRIPT_TAG:
                self.problems.append("only the exact reviewed progress script tag is allowed")
            if self.script_count > 1:
                self.problems.append("multiple progress script tags")
        attrs = dict(attrs)
        if tag in {"iframe", "object", "embed", "form", "style", "svg"}:
            self.problems.append(f"unexpected active content: {tag}")
        if any(key.lower().startswith("on") for key in attrs):
            self.problems.append("inline event handler")
        if "style" in attrs:
            self.problems.append("inline style requires explicit review")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.problems.append("automatic page redirect")
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.problems.append("duplicate HTML id")
            self.ids.add(attrs["id"])
        for attr in ("href", "src", "srcset", "action", "xlink:href"):
            if attrs.get(attr):
                self.links.append(("anchor" if tag == "a" and attr == "href" else "resource", attrs[attr]))

    def handle_startendtag(self, tag, attrs):
        if tag == "script":
            self.problems.append("self-closing script tag")
        super().handle_startendtag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "script":
            line, column = self.getpos()
            offset = self._line_offsets[line - 1] + column
            if not self._in_script or not self._text.startswith("</script>", offset):
                self.problems.append("unexpected progress script closing tag")
            self._in_script = False

    def handle_data(self, data):
        if self._in_script and data.strip():
            self.problems.append("inline script content")


def validate_html(root: Path = ROOT) -> None:
    root = root.resolve()
    docs = (root / "docs").resolve()
    if not (docs / "index.html").is_file() or not (docs / ".nojekyll").is_file():
        raise ValidationError("Build must produce docs/index.html and docs/.nojekyll")
    pages = {path: Page(path.read_text()) for path in docs.rglob("*.html")}
    for path, page in pages.items():
        if page.problems:
            raise ValidationError(f"{path.relative_to(root)}: {', '.join(page.problems)}")
        for kind, href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                if url.scheme != "https" or not url.netloc:
                    raise ValidationError(f"{path.name}: unsafe or unsupported URL scheme")
                if kind != "anchor" and not (url.hostname == "obra.github.io" and url.path.startswith(BASE + "/")):
                    raise ValidationError(f"{path.name}: externally hosted resource")
                if url.hostname != "obra.github.io" or not url.path.startswith(BASE + "/"):
                    continue
            target_path = unquote(url.path)
            if target_path.startswith("/"):
                if not target_path.startswith(BASE + "/") and target_path != BASE:
                    raise ValidationError(f"{path.name}: local link omits project base path")
                target = docs / target_path[len(BASE):].lstrip("/")
            else:
                target = path.parent / target_path if target_path else path
            target = target.resolve()
            if target != docs and docs not in target.parents:
                raise ValidationError(f"{path.name}: link escapes the public site")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                raise ValidationError(f"{path.name}: broken local link {href}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValidationError(f"{path.name}: broken local anchor {href}")
    if any(page.script_count for page in pages.values()):
        source = root / "assets/progress.js"
        generated = docs / "assets/progress.js"
        if not source.is_file() or not generated.is_file():
            raise ValidationError("Progress script requires source and generated assets/progress.js files")
        if source.read_bytes() != generated.read_bytes():
            raise ValidationError("docs/assets/progress.js must exactly match assets/progress.js")
    for path in docs.rglob("*.css"):
        if re.search(r"@import\b", path.read_text(), re.I):
            raise ValidationError(f"{path.name}: CSS imports are not allowed")
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", path.read_text(), re.I):
            if urlsplit(match.group(1)).scheme or match.group(1).startswith("//"):
                raise ValidationError(f"{path.name}: externally hosted CSS resource")


def digest(hashes: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(root: Path = ROOT, terms: list[str] | None = None) -> dict[str, str]:
    hashes = candidate(root, terms)
    validate_html(root)
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-terms-file", type=Path, required=True)
    args = parser.parse_args()
    try:
        hashes = validate(terms=private_terms(args.private_terms_file))
    except (ValidationError, OSError, SyntaxError) as exc:
        parser.exit(1, f"Validation stopped: {exc}\n")
    print(f"Validated {len(hashes)} public files; SHA256 {digest(hashes)}")


if __name__ == "__main__":
    main()
