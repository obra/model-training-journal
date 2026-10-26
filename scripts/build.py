#!/usr/bin/env python3
"""Render the deliberately small, reviewed public journal to docs/."""
from datetime import date
from html import escape
from pathlib import Path
from string import Template
import re
import shutil
import xml.etree.ElementTree as ET

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = "/model-training-journal"
ORIGIN = "https://obra.github.io"
TITLE = "Model Training Journal"


def load_posts():
    posts = []
    for source in sorted((ROOT / "content/posts").glob("*.md")):
        text = source.read_text()
        if not text.startswith("---\n"):
            raise ValueError(f"Missing front matter: {source.name}")
        _, front, body = text.split("---", 2)
        meta = yaml.safe_load(front)
        for key in ("title", "date", "slug", "phase", "summary"):
            if not meta.get(key):
                raise ValueError(f"Missing {key}: {source.name}")
        meta["date"] = date.fromisoformat(str(meta["date"]))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["slug"]):
            raise ValueError(f"Unsafe slug: {source.name}")
        meta["path"] = f"{meta['date']:%Y/%m/%d}/{meta['slug']}/"
        meta["url"] = f"{BASE}/{meta['path']}"
        meta["html"] = markdown.markdown(body.strip(), extensions=["tables", "fenced_code", "toc"])
        meta["html"] = meta["html"].replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
        meta["read_minutes"] = max(1, round(len(body.split()) / 220))
        posts.append(meta)
    posts.sort(key=lambda post: (post["date"], post.get("order", {"Setup": 1, "Diagnostic": 2}.get(post["phase"], 3)), post["slug"]))
    if not posts or len({post["path"] for post in posts}) != len(posts):
        raise ValueError("Need nonempty posts with unique URLs")
    return posts


def build():
    posts = load_posts()
    template = Template((ROOT / "templates/layout.html").read_text())
    output = ROOT / "docs"
    # Only generated output is replaced. Public sources are never imported remotely.
    if output.is_symlink():
        raise ValueError("docs must not be a symlink")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    shutil.copytree(ROOT / "assets", output / "assets")
    (output / ".nojekyll").write_text("")
    paths = []

    def render(path, title, description, body, section="journal"):
        file = output / path / "index.html" if path else output / "index.html"
        file.parent.mkdir(parents=True, exist_ok=True)
        canonical = f"{ORIGIN}{BASE}/{path}"
        file.write_text(template.substitute(
            title=escape(f"{title} · {TITLE}" if title != TITLE else TITLE),
            description=escape(description, quote=True), canonical=canonical,
            body=body, base=BASE,
            journal_current=' aria-current="page"' if section == "journal" else "",
            experiments_current=' aria-current="page"' if section == "experiments" else "",
            about_current=' aria-current="page"' if section == "about" else "",
        ))
        paths.append(canonical)

    entries = []
    for post in reversed(posts):
        entries.append(f'''<li class="entry">
<div class="entry-meta"><time datetime="{post['date']}">{post['date']:%d %b %Y}</time><span>{escape(post['phase'])}</span></div>
<div><h3><a href="{post['url']}">{escape(post['title'])}</a></h3>
<p>{escape(post['summary'])}</p><a class="read-link" href="{post['url']}">Read entry · {post['read_minutes']} min</a></div></li>''')
    render("", TITLE, "An AI-assisted engineering journal about training a small language model from scratch: methods, measurements, failures, and open questions.", f'''
<section class="intro" aria-labelledby="journal-title">
<div><h1 id="journal-title">Small models.<br>Measured progress.</h1>
<p>An engineering journal about training a small language model from scratch. The questions, the experiments, and what the evidence actually supports.</p></div>
<aside><strong>A record of the work</strong><p>AI-assisted notes, curated from a local experiment notebook. Completed diagnostics and future plans are kept distinct.</p><a href="{BASE}/about/">About the journal</a></aside>
</section>
<section aria-labelledby="entries-heading"><div class="section-heading"><h2 id="entries-heading">Journal entries</h2><span>Latest first · {len(posts)} entries</span></div><ol class="entries">{''.join(entries)}</ol></section>
''')

    for i, post in enumerate(posts):
        prev = f'<a href="{posts[i-1]["url"]}">Earlier: {escape(posts[i-1]["title"])}</a>' if i else f'<a href="{BASE}/">All journal entries</a>'
        next_link = f'<a href="{posts[i+1]["url"]}">Next: {escape(posts[i+1]["title"])}</a>' if i + 1 < len(posts) else f'<a href="{BASE}/experiments/">Experiment index</a>'
        body = f'''<article class="page"><header class="article-header"><h1>{escape(post['title'])}</h1><p class="dek">{escape(post['summary'])}</p><p class="article-meta"><time datetime="{post['date']}">{post['date']:%d %B %Y}</time> · {escape(post['phase'])} · {post['read_minutes']} min read</p></header><div class="prose">{post['html']}</div><nav class="post-nav" aria-label="Article navigation">{prev}{next_link}</nav></article>'''
        render(post["path"], post["title"], post["summary"], body)

    for filename, title in (("experiments", "Experiment index"), ("about", "About this journal")):
        source = (ROOT / f"content/{filename}.md").read_text()
        html = markdown.markdown(source, extensions=["tables", "fenced_code", "toc"])
        html = html.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
        render(filename + "/", title, source.splitlines()[0], f'<article class="page"><h1>{title}</h1><div class="prose">{html}</div></article>', section=filename)

    render("404/", "Page not found", "This page could not be found.", f'<article class="page"><h1>Page not found</h1><p>Return to the <a href="{BASE}/">journal</a> or the <a href="{BASE}/experiments/">experiment index</a>.</p></article>')
    shutil.copyfile(output / "404/index.html", output / "404.html")
    ns = "http://www.w3.org/2005/Atom"
    ET.register_namespace("", ns)
    feed = ET.Element(f"{{{ns}}}feed")
    def elem(parent, tag, text):
        ET.SubElement(parent, f"{{{ns}}}{tag}").text = text
    elem(feed, "title", TITLE)
    elem(feed, "id", ORIGIN + BASE + "/")
    elem(feed, "updated", f"{posts[-1]['date']}T00:00:00Z")
    ET.SubElement(feed, f"{{{ns}}}link", href=ORIGIN + BASE + "/feed.xml", rel="self")
    ET.SubElement(feed, f"{{{ns}}}link", href=ORIGIN + BASE + "/")
    author = ET.SubElement(feed, f"{{{ns}}}author")
    elem(author, "name", "Model Training Journal")
    for post in reversed(posts):
        entry = ET.SubElement(feed, f"{{{ns}}}entry")
        for tag, text in (("title", post["title"]), ("id", ORIGIN + post["url"]), ("updated", f"{post['date']}T00:00:00Z"), ("summary", post["summary"])):
            elem(entry, tag, text)
        ET.SubElement(entry, f"{{{ns}}}link", href=ORIGIN + post["url"])
    ET.ElementTree(feed).write(output / "feed.xml", encoding="utf-8", xml_declaration=True)
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in paths:
        if not path.endswith("/404/"):
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = path
    ET.ElementTree(sitemap).write(output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Built {len(posts)} posts and 3 index/info pages in docs/")


if __name__ == "__main__":
    build()
