#!/usr/bin/env python3
"""Render the deliberately small, reviewed public journal to docs/."""
from datetime import date, datetime, timezone
from html import escape
import json
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
DEADLINE_UTC = "2026-10-31T04:12:00Z"


def utc_timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ValueError("Progress timestamps must use YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_progress(path=None):
    progress = json.loads((path or ROOT / "content/progress.json").read_text())
    required = {"schema", "model_parameters", "initialization", "experiment_state", "latest_result", "verified_at_utc", "deadline_utc"}
    if set(progress) != required or progress["schema"] != 1:
        raise ValueError("Unexpected progress snapshot schema")
    if type(progress["model_parameters"]) is not int or not 0 < progress["model_parameters"] < 1_000_000_000_000:
        raise ValueError("Model parameters must be a positive integer")
    if progress["initialization"] != "from scratch":
        raise ValueError("This journal records training from scratch")
    if progress["deadline_utc"] != DEADLINE_UTC:
        raise ValueError("The fixed 120-hour deadline must not move")
    utc_timestamp(progress["verified_at_utc"])
    result = progress["latest_result"]
    if not isinstance(result, dict) or set(result) != {"summary", "url"}:
        raise ValueError("Latest result requires summary and a public local URL")
    for value, limit in ((progress["experiment_state"], 240), (result["summary"], 360)):
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise ValueError("Progress text must be concise nonempty plain text")
    if not isinstance(result["url"], str) or not re.fullmatch(re.escape(BASE) + r"/[a-z0-9/-]*(?:#[a-z0-9-]+)?", result["url"]):
        raise ValueError("Latest result must link within the public journal")
    return progress


def remaining_at_snapshot(verified):
    seconds = max(0, int((utc_timestamp(DEADLINE_UTC) - verified).total_seconds()))
    if seconds == 0:
        return "Budget elapsed at snapshot"
    if seconds < 60:
        return "Less than 1 min remaining at snapshot"
    minutes = seconds // 60
    days, minutes = divmod(minutes, 1440)
    hours, minutes = divmod(minutes, 60)
    return f"{days}d {hours}h {minutes}m remaining at snapshot"


def render_progress(progress):
    verified = utc_timestamp(progress["verified_at_utc"])
    parameters = progress["model_parameters"]
    model = f"{parameters / 1_000_000:.1f}M parameters" if parameters >= 1_000_000 else f"{parameters:,} parameters"
    result = progress["latest_result"]
    return f'''<section class="progress" aria-label="Experiment progress" data-progress data-verified-at="{escape(progress['verified_at_utc'], quote=True)}" data-deadline="{DEADLINE_UTC}">
  <div class="progress-top"><p class="progress-model"><strong title="{parameters:,} trainable parameters">{model}</strong> · from scratch</p><a href="{BASE}/current-plan/">Current plan</a></div>
  <dl class="progress-facts">
    <div class="progress-state"><dt>Experiment state</dt><dd>{escape(progress['experiment_state'])}</dd></div>
    <div class="progress-result"><dt>Latest meaningful result</dt><dd><a href="{escape(result['url'], quote=True)}">{escape(result['summary'])}</a></dd></div>
    <div class="progress-budget"><dt>Installed guard cutoff</dt><dd><strong data-countdown>{remaining_at_snapshot(verified)}</strong><span class="progress-deadline">Cutoff <time datetime="{DEADLINE_UTC}">31 Oct 2026, 04:12 UTC</time></span></dd></div>
  </dl>
  <div class="progress-snapshot"><p><strong>Status snapshot</strong> · last verified <time datetime="{progress['verified_at_utc']}">{verified:%d %b %Y, %H:%M:%S} UTC</time>. Data do not refresh here.</p><p data-freshness role="status">Local clock unavailable; remaining time is shown at the snapshot.</p></div>
</section>'''


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
    progress = load_progress()
    progress_header = render_progress(progress)
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
            body=body, base=BASE, progress_header=progress_header,
            journal_current=' aria-current="page"' if section == "journal" else "",
            experiments_current=' aria-current="page"' if section == "experiments" else "",
            about_current=' aria-current="page"' if section == "about" else "",
            current_plan_current=' aria-current="page"' if section == "current-plan" else "",
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

    for filename, title in (("experiments", "Experiment index"), ("about", "About this journal"), ("current-plan", "Current plan")):
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
    print(f"Built {len(posts)} posts and 4 index/info pages in docs/")


if __name__ == "__main__":
    build()
