# Model Training Journal

An AI-assisted engineering journal about training a small language model from scratch. Public entries distinguish observed results from plans, preserve failures and limitations, and omit private operational details.

Read the journal at **https://obra.github.io/model-training-journal/**.

## Structure

- `content/posts/`: curated public Markdown entries with title, date, slug, phase and summary front matter.
- `content/`: experiment index, editorial method, reviewed dashboard additions and hash-bound plain-language companions.
- `templates/` and `assets/`: shared HTML and restrained, responsive styling.
- `scripts/`: local builder and publication checks.
- `docs/`: generated static HTML served by GitHub Pages from `main`.

No notebook mirror, raw logs, model weights, dataset copies or credentials belong in this repository.

## Build

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build.py
```

The build is local and deterministic. It uses no CDN, remote fonts or tracking.
The only browser JavaScript is the reviewed local snapshot-age and cutoff clock;
charts are static SVG images. The generated pages are committed so they can be reviewed before publication. GitHub Pages serves `main:/docs` with `.nojekyll`.

See [PUBLISHING.md](PUBLISHING.md) for the review-and-publish procedure. Publication needs an existing authorized GitHub login; this project neither creates nor transfers credentials.

## Rights and provenance

The entries summarize project observations and cite external sources. No third-party dataset or text excerpt is distributed. Software and data license observations in articles describe the original experiment; they are not a license grant for external materials. Do not add copied material without verifying and recording redistribution rights.

## Reader access and measurements

Every post pairs the original with a plain-language companion. The homepage and
[dashboard](https://obra.github.io/model-training-journal/dashboard/) share one
compiled evidence model. See [the schema and update guide](scripts/dashboard-README.md)
for correspondence checks, missing-data rules and adding future measurements.
