# Publishing the journal

This checkout contains curated public content. The source notebook, training data,
raw logs, credentials and local review evidence stay outside it. GitHub Pages
serves `docs/` from `main`; a push publishes the already generated static files.

Publication after editorial checks is authorized. This is an agent-reviewed
process, with no timer, notebook mirror or unattended file synchronization.
Run it on the publishing Mac using its existing GitHub authentication. Never
copy credentials to the training machine or create a token for this workflow.

## Prepare and review an update

Discover candidates by listing Markdown files directly in the source notebook's
`posts/` directory and computing their SHA256 hashes. Preserve each source
basename for its curated copy in `content/posts/`. Keep a private publication
ledger outside this checkout with the source basename and hash, curated-file
hash, published commit and verified live URL. A new basename or changed source
hash requires review. A file is already published only when the ledger matches
the source revision, the curated file is present on `origin/main`, and its live
page was verified. An edited source should update the existing public slug;
do not create a duplicate entry merely because it changed.

1. Read only the relevant notebook entry and directly supporting results. Leave
   the notebook and training process untouched. Draft a curated Markdown copy in
   `content/posts/`, with `title`, `date`, `slug`, `phase` and `summary` front matter.
   Use an integer `order` when needed to preserve chronology within one date.
2. Verify every numerical and historical claim against the actual evidence.
   Separate completed diagnostics, planned runs and later outcomes. Identify this
   as AI-assisted engineering; do not imply personal authorship or assistant
   capability that the experiment has not demonstrated.
3. Remove personal names, machine names, private network addresses, local paths,
   internal identifiers, private messages and unrelated operational inventory.
   Keep raw logs and dataset text out. Confirm redistribution rights for any
   material actually included; a public download URL alone is not a license.
4. Build, run validation and inspect the changed pages on desktop and mobile.
   Check cited public links as well as the generated internal navigation. Read
   every candidate diff, including scripts and generated files. Source review is
   essential: pattern scanners cannot establish privacy, licensing or truth.

The private terms file is a local newline-separated list of private names,
hosts, locations and identifiers found in source evidence. Keep it **outside the
public checkout**. Empty lines and lines beginning with `#` are ignored. Use at
least three characters per term. Do not copy the file into this repository.

Run these commands from the checkout with its local virtual environment already
prepared. The clock behavior tests also require a local Node.js runtime; no npm
packages are needed:

```sh
.venv/bin/python scripts/build.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate.py --private-terms-file "$PRIVATE_TERMS_FILE"
git diff --stat
git diff
```

Inspect untracked candidate files too; `git diff` alone does not show them. The
validator rejects unknown top-level paths, non-text assets, symlinks, oversized
files, common credentials and private addresses, and checks generated internal
links. There is exactly one reviewed local script exception: UTF-8
`assets/progress.js` and its byte-identical generated copy at
`docs/assets/progress.js`. A page may include it once, using exactly
`<script src="/model-training-journal/assets/progress.js" defer></script>`.
Inline script content, other script tags or attributes, other JavaScript files
and externally hosted resources are rejected.

The progress script uses the visitor's local clock to update remaining time and
snapshot staleness once per minute. Published facts stay static; it performs no
network requests, storage or telemetry. This exception still requires manual
source and rendered-page review, and the review receipt binds both script copies
along with every other candidate file. CSS imports, inline styles and automatic
redirects remain excluded.

There is one narrow passive SVG exception: checkpoint-perplexity.svg,
broader-panel.svg, training-throughput.svg and checkpoint-overhead.svg under
assets/charts/, plus the four frozen V4 checkpoint569 chart names:
`v4-569-checkpoint-perplexity.svg`, `v4-569-broader-lm.svg`,
`v4-569-throughput.svg`, and `v4-569-overhead.svg` in the same directory,
with byte-identical copies under docs/assets/charts/. The frozen V4 checkpoint
1,137 chart `v4-1137-cfr-perplexity.svg` is also allowed in those two directories
under the same passive profile. The frozen V4 checkpoint
2,273 chart `v4-2273-cfr-perplexity.svg` is also allowed in those two directories
under the same passive profile. The frozen terminal V4 charts
`v4-terminal-cfr-perplexity.svg` and `v4-terminal-overhead.svg` are allowed
in those same two directories under that unchanged passive profile. The earlier four shared
chart assets and historical captions remain unchanged in this update. Other SVG
paths remain excluded. Each chart must be UTF-8, no larger than 1,000,000 bytes,
and pass the same privacy scan as every other public file. Its XML must use the
SVG namespace and only the reviewed passive geometry, glyph-path and title/desc
profile, bounded to 25,000 elements and depth 64. Glyph hrefs may reference only
existing local path IDs; clip-path may reference only existing local clipPath
IDs. Duplicate, unresolved or recursive references, external/data references,
unknown namespaces or attributes, styles, events, scripts, images, links,
foreignObject, animation, DTD/entity declarations and nonstandard processing
instructions are rejected. Only a standard XML declaration is allowed. Inline
SVG in HTML remains excluded.

Review the chart's numbers, captions, accessibility text, rights and actual
desktop/mobile rendering; the validator does not establish factual accuracy.
The publication receipt binds source and generated chart bytes with the whole
candidate. New chart names or changes to this passive profile require a deliberate
validator update and review.

The charts are generated separately from publication. See `scripts/chart-README.md`
for the fixed data input, pinned optional plotting requirements and reproducible
build command. The normal site build copies the reviewed SVG bytes; it does not
fetch data or regenerate them. The additional reviewed
`v4-v5-cfr-perplexity.svg` is an offline, passive SVG with an exact copy
under `docs/assets/charts/`; its standard-library builder reads only
`assets/v4-v5-cfr-checkpoints.json`.

The later dashboard addition explicitly allows `dashboard-cfr-v6.svg` and
`dashboard-cfr-v7.svg` under `assets/charts/`, with exact generated copies under
`docs/assets/charts/`. They use the existing passive dashboard SVG profile with
bounded text labels, without expanding active-content permissions. Their source
is the reviewed aggregate `assets/v6-v7-cfr-checkpoints.json`; the normal offline
site build generates them without reading private evidence or fetching data.

The V8 addition allows `dashboard-cfr-v8.svg` under those same two chart
directories and passive profile. Its source is the reviewed, separately pinned
`assets/v8-cfr-checkpoints.json`, which retains the repeated V7 baseline and
both V8 saves. No active-content permission changes accompany this chart.

## Refresh the progress snapshot

Review the latest notebook status and directly supporting stage results before
changing `content/progress.json` or `content/current-plan.md`. Old status fields
can survive newer stages: use timestamps and completed-stage evidence, and keep
each evaluation population separate. Record the UTC verification timestamp,
actual experiment state, one qualified result, and the next decision. Planned
work must not be presented as launched or completed.

The currently installed training cutoff is `2026-11-07T04:12:00Z`; content and the local clock script must match this reviewed installed setting.
The prior 31 October cutoff is preserved in dated history. A later project cutoff
does not extend the separate finite guard of an active run. This is an installed guard setting, not
a fixed user deadline for the research. Research proceeds through finite runs
with measured progress and separately reviewed run budgets. The browser updates only countdown and snapshot age. It
shows a stale warning after 60 minutes and never fetches training telemetry. With
JavaScript disabled, remaining time is explicitly labeled as measured at the
snapshot. Include the progress JSON, plan Markdown, generated pages and clock
script in the same factual, privacy and rendered-page review as the posts.

## Record the completed review and publish

After the editorial and rendered-page review is actually complete, choose a
**new external receipt path** and record that fact explicitly:

```sh
.venv/bin/python scripts/review.py \
  --private-terms-file "$PRIVATE_TERMS_FILE" \
  --reviewed \
  --note "Compared claims with source results; reviewed privacy, rights and desktop/mobile output." \
  --output "$REVIEW_RECEIPT"

.venv/bin/python scripts/publish.py \
  --private-terms-file "$PRIVATE_TERMS_FILE" \
  --review "$REVIEW_RECEIPT" \
  --message "Publish reviewed experiment update"
```

The receipt contains exact SHA256 hashes of **every public candidate file** and
the private-term-list digest, plus the review assertions and time. It is local
review evidence, not public content. Receipts expire after 24 hours. Any source,
style, script or generated HTML change invalidates the receipt; review the new
candidate and create a fresh one. `--reviewed` is an assertion by the reviewer,
not an automated factual or licensing check.

The publisher requires `main`, an empty staging area and this exact SSH origin:
`git@github.com:obra/model-training-journal.git`. It rebuilds, validates, runs the
tests, verifies the receipt, fetches `main`, and requires local `HEAD` to equal
remote `main`. It stages only allowlisted paths and verifies the staged bytes
again before an ordinary commit and push. Existing commit hooks remain active;
the actual committed tree and message are checked again before pushing the exact
commit to the single authorized repository. It also requires that this commit's
sole parent is the fetched base, so unexpected intervening history is not sent.
Automatic tag following is disabled
for this push. Commits use an explicit generic
automation identity with a no-reply address to avoid publishing a local personal
email. No credential or permission settings are changed.

## Verify deployment

```sh
gh run list --repo obra/model-training-journal --limit 5
gh api repos/obra/model-training-journal/pages
git rev-parse HEAD
```

Wait for GitHub's Pages deployment to succeed for the pushed commit. Open
<https://obra.github.io/model-training-journal/> and every newly published post;
verify the real content loads. Report the commit and verified live URLs only
after this check. A successful push alone is not proof of a live deployment.
Then update the external publication ledger with the source snapshot actually
reviewed and the verified public commit. The publisher does not copy or inspect
the private source notebook and does not update this ledger itself.

## When a check stops publication

Inspect the reason locally and fix only the intended journal change. Never
force-push, auto-reset, delete unrelated content, broaden OAuth permissions or
silently refresh authentication. If remote history changed, fetch and reconcile
it with a normal history-preserving workflow, then review the resulting files.

If staging or commit succeeded but push failed, leave the work intact and inspect
both local and remote commit IDs before retrying. Do not blindly rerun the
publisher: it deliberately refuses preexisting staged changes or local commits
ahead of the remote. A network timeout can leave a push outcome uncertain;
first check whether the exact reviewed commit reached `main`. Report any access
or approval blocker to the coordinating task.
