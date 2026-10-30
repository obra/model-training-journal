#!/usr/bin/env python3
"""Validate the complete public candidate, without reading the private notebook."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import io
import ipaddress
import json
import math
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "/model-training-journal"
ROOT_FILES = {"README.md", "PUBLISHING.md", "requirements.txt", ".gitignore", "PRODUCT.md", "DESIGN.md"}
PUBLIC_DIRS = {"content", "templates", "assets", "scripts", "tests", "docs"}
LOCAL_DIRS = {".git", ".venv", ".impeccable", ".pytest_cache", ".review"}
EXTENSIONS = {".md", ".json", ".py", ".txt", ".html", ".css", ".xml"}
PROGRESS_SCRIPT_FILES = {"assets/progress.js", "docs/assets/progress.js"}
PROGRESS_SCRIPT_TAG = f'<script src="{BASE}/assets/progress.js" defer>'
CHART_SVG_NAMES = frozenset({"checkpoint-perplexity.svg", "broader-panel.svg",
                             "training-throughput.svg", "checkpoint-overhead.svg",
                             "v4-569-checkpoint-perplexity.svg", "v4-569-broader-lm.svg",
                             "v4-569-throughput.svg", "v4-569-overhead.svg",
                             "v4-1137-cfr-perplexity.svg",
                             "v4-2273-cfr-perplexity.svg"})
CHART_SVG_FILES = {f"{prefix}/{name}" for prefix in ("assets/charts", "docs/assets/charts")
                   for name in CHART_SVG_NAMES}
MAX_BYTES = 1_000_000
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"
MAX_SVG_NODES = 25_000
MAX_SVG_DEPTH = 64
SVG_ID = r"[A-Za-z_][A-Za-z0-9_.:-]{0,127}"
SVG_NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
SVG_PAINT_ATTRIBUTES = {"id", "transform", "fill", "stroke", "color", "stroke-width",
                        "stroke-linecap", "stroke-linejoin", "stroke-miterlimit",
                        "stroke-dasharray", "stroke-dashoffset", "fill-opacity",
                        "stroke-opacity", "opacity", "clip-path"}
SVG_ATTRIBUTES = {
    "svg": SVG_PAINT_ATTRIBUTES | {"width", "height", "viewBox", "version", "role",
                                    "aria-labelledby", "aria-describedby"},
    "g": SVG_PAINT_ATTRIBUTES,
    "defs": {"id"},
    "path": SVG_PAINT_ATTRIBUTES | {"d"},
    "rect": SVG_PAINT_ATTRIBUTES | {"x", "y", "width", "height"},
    "line": SVG_PAINT_ATTRIBUTES | {"x1", "y1", "x2", "y2"},
    "polyline": SVG_PAINT_ATTRIBUTES | {"points"},
    "polygon": SVG_PAINT_ATTRIBUTES | {"points"},
    "use": SVG_PAINT_ATTRIBUTES | {"href", "x", "y"},
    "clipPath": {"id"},
    "title": {"id"},
    "desc": {"id"},
}
SVG_XML_DECLARATION = re.compile(
    r'''<\?xml\s+version=(?:"1\.0"|'1\.0')'''
    r'''(?:\s+encoding=(?:"[Uu][Tt][Ff]-8"|'[Uu][Tt][Ff]-8'))?'''
    r'''(?:\s+standalone=(?:"(?:yes|no)"|'(?:yes|no)'))?\s*\?>''')


class ValidationError(ValueError):
    pass


def _svg_numbers(value: str, name: str) -> list[float]:
    if not re.fullmatch(SVG_NUMBER + r"(?:[\s,]+" + SVG_NUMBER + r")*", value.strip()):
        raise ValidationError(f"{name}: SVG geometry must contain only finite numbers")
    numbers = [float(item) for item in re.findall(SVG_NUMBER, value)]
    if any(not math.isfinite(item) or abs(item) > 1_000_000_000 for item in numbers):
        raise ValidationError(f"{name}: SVG coordinate exceeds the passive chart bounds")
    return numbers


def _svg_attribute(tag: str, key: str, value: str, name: str,
                   references: list[tuple[str, set[str]]]) -> None:
    if key == "id":
        valid = re.fullmatch(SVG_ID, value)
    elif key == "href":
        valid = re.fullmatch("#" + SVG_ID, value)
        if valid:
            references.append((value[1:], {"path"}))
    elif key == "clip-path":
        valid = re.fullmatch(r"url\(#(" + SVG_ID + r")\)", value)
        if valid:
            references.append((valid.group(1), {"clipPath"}))
    elif key in {"aria-labelledby", "aria-describedby"}:
        ids = value.split()
        valid = bool(ids) and all(re.fullmatch(SVG_ID, item) for item in ids)
        if valid:
            references.extend((item, {"title", "desc"}) for item in ids)
    elif key == "role":
        valid = value == "img"
    elif key == "version":
        valid = value == "1.1"
    elif key in {"fill", "stroke", "color"}:
        valid = (value in {"none", "transparent", "currentColor", "black", "white"} or
                 re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", value))
    elif key in {"stroke-linecap", "stroke-linejoin"}:
        valid = value in ({"butt", "round", "square"} if key == "stroke-linecap"
                          else {"miter", "round", "bevel"})
    elif key == "transform":
        end = 0
        valid = False
        arities = {"matrix": {6}, "translate": {1, 2}, "scale": {1, 2},
                   "rotate": {1, 3}, "skewX": {1}, "skewY": {1}}
        for match in re.finditer(r"(matrix|translate|scale|rotate|skewX|skewY)\s*\(([^()]*)\)", value):
            if value[end:match.start()].strip(" ,\t\r\n"):
                raise ValidationError(f"{name}: unsupported SVG transform")
            if len(_svg_numbers(match.group(2), name)) not in arities[match.group(1)]:
                raise ValidationError(f"{name}: incorrect SVG transform arguments")
            end = match.end()
            valid = True
        valid = valid and not value[end:].strip(" ,\t\r\n")
    elif key == "d":
        # Accept passive path commands and finite coordinates, never CSS or URLs.
        rest = re.sub(SVG_NUMBER + r"|[MmZzLlHhVvCcSsQqTtAa]|[\s,]", "", value)
        valid = not rest
        for number in re.findall(SVG_NUMBER, value):
            _svg_numbers(number, name)
    else:
        numeric = value
        if key in {"width", "height"} and tag == "svg":
            numeric = re.sub(r"(?:pt|px)$", "", value)
        if key == "stroke-dasharray" and value == "none":
            return
        numbers = _svg_numbers(numeric, name)
        valid = len(numbers) == 1
        if key == "viewBox":
            valid = len(numbers) == 4 and numbers[2] > 0 and numbers[3] > 0
        elif key == "points":
            valid = len(numbers) >= 4 and len(numbers) % 2 == 0
        elif key == "stroke-dasharray":
            valid = all(item >= 0 for item in numbers)
        elif key in {"width", "height", "stroke-width"}:
            valid = valid and numbers[0] >= 0
            if tag == "svg":
                valid = valid and numbers[0] <= 10_000
        elif key == "stroke-miterlimit":
            valid = valid and numbers[0] >= 1
        elif key in {"opacity", "fill-opacity", "stroke-opacity"}:
            valid = valid and 0 <= numbers[0] <= 1
    if not valid:
        raise ValidationError(f"{name}: unsupported passive SVG attribute value: {key}")


def validate_svg(text: str, name: str) -> None:
    """Accept only bounded passive chart markup with local glyph/clip references."""
    if name not in CHART_SVG_FILES:
        raise ValidationError(f"{name}: SVG path is not a reviewed chart")
    prolog = text.removeprefix("\ufeff")
    declaration = SVG_XML_DECLARATION.match(prolog)
    remainder = prolog[declaration.end():] if declaration else prolog
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.I) or "<?" in remainder:
        raise ValidationError(f"{name}: SVG declarations, entities or processing instructions are forbidden")
    nodes = []
    depth = 0
    try:
        parser = ET.iterparse(io.StringIO(text), events=("start", "end", "start-ns"))
        for event, item in parser:
            if event == "start-ns":
                if item[1] not in {SVG_NAMESPACE, XLINK_NAMESPACE}:
                    raise ValidationError(f"{name}: unknown SVG namespace")
            elif event == "start":
                depth += 1
                nodes.append(item)
                if len(nodes) > MAX_SVG_NODES or depth > MAX_SVG_DEPTH:
                    raise ValidationError(f"{name}: SVG node/depth limit exceeded")
            else:
                depth -= 1
    except ET.ParseError as exc:
        raise ValidationError(f"{name}: malformed SVG XML") from exc
    root = parser.root
    if root.tag != "{" + SVG_NAMESPACE + "}svg":
        raise ValidationError(f"{name}: exact SVG namespace/root required")
    ids: dict[str, str] = {}
    references: list[tuple[str, set[str]]] = []
    for node in nodes:
        prefix = "{" + SVG_NAMESPACE + "}"
        tag = node.tag.removeprefix(prefix)
        if not node.tag.startswith(prefix) or tag not in SVG_ATTRIBUTES or (tag == "svg" and node is not root):
            raise ValidationError(f"{name}: unexpected SVG element")
        if tag not in {"svg", "g", "defs", "clipPath"} and len(node):
            raise ValidationError(f"{name}: chart geometry and descriptions must be leaf elements")
        if tag == "clipPath" and any(child.tag not in {prefix + "rect", prefix + "path"}
                                     or "clip-path" in child.attrib for child in node):
            raise ValidationError(f"{name}: only nonrecursive path/rect clips are allowed")
        if ((tag not in {"title", "desc"} and node.text and node.text.strip()) or
                (node.tail and node.tail.strip())):
            raise ValidationError(f"{name}: SVG text is limited to title/desc")
        hrefs = 0
        for attribute, value in node.attrib.items():
            key = "href" if attribute == "{" + XLINK_NAMESPACE + "}href" else attribute
            if key not in SVG_ATTRIBUTES[tag]:
                raise ValidationError(f"{name}: unknown SVG attribute: {attribute}")
            hrefs += key == "href"
            _svg_attribute(tag, key, value, name, references)
        if (tag == "use" and hrefs != 1) or hrefs > 1:
            raise ValidationError(f"{name}: one local glyph reference is required per use")
        if "id" in node.attrib:
            identity = node.attrib["id"]
            if identity in ids:
                raise ValidationError(f"{name}: duplicate SVG id")
            ids[identity] = tag
    if any(identity not in ids or ids[identity] not in kinds for identity, kinds in references):
        raise ValidationError(f"{name}: unresolved or invalid local SVG reference")


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
                and name not in PROGRESS_SCRIPT_FILES and name not in CHART_SVG_FILES):
            raise ValidationError(f"{name}: unexpected file type")
        data = path.read_bytes()
        if len(data) > MAX_BYTES or b"\0" in data:
            raise ValidationError(f"{name}: binary or oversized file")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError(f"{name}: not UTF-8 text") from exc
        scan_text(text, name, terms)
        if name in CHART_SVG_FILES:
            validate_svg(text, name)
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
    for name in CHART_SVG_NAMES:
        source = root / "assets/charts" / name
        generated = docs / "assets/charts" / name
        if source.exists() or generated.exists():
            if not source.is_file() or not generated.is_file() or source.read_bytes() != generated.read_bytes():
                raise ValidationError(f"{name}: source and generated SVG chart must match exactly")
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
