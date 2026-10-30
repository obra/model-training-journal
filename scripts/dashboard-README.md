# Plain-language companions and shared measurement dashboard

This extends the existing static builder. It adds no framework, service, analytics,
external fonts, translation API or new browser script. Source post charts remain
frozen. The dashboard is a reviewed publication snapshot, not live telemetry.

## Translation schema (version 1)

Every `content/posts/<name>.md` requires
`content/translations/<front-matter-slug>.json` with exactly these fields:

- `schema`: integer `1`.
- `source`: the Markdown path relative to the repository.
- `source_sha256`: SHA-256 of the exact Markdown bytes, including front matter.
- `blocks`: ordered records, one for every substantive top-level rendered block.
  Each has `id` (`passage-001`, then sequential), `source_kind` (HTML tag),
  `source_text_sha256`, and nonempty plain-text `text`.

`source_text_sha256` hashes UTF-8 text extracted by `legibility.split_blocks`,
with text fragments joined by spaces and whitespace collapsed. Headings and
horizontal rules stay shared; paragraphs, lists, tables and figures get pairs.
Original HTML slices are preserved without reserialization. Companion text is
escaped, never interpreted as HTML. Blank lines create companion paragraphs.

The builder rejects missing, extra, stale, reordered or empty companions. Changing
an original requires editorial review of its companion, not merely refreshing a
hash. No automatic translation fallback is permitted. Preserve dates, numbers,
denominators, uncertainty, failures, and the difference between a person's
permission and scientific evidence. Explain unfamiliar terms in the passage;
the optional glossary is a backup, not a substitute. Aim for short sentences and
an eighth-grade reading level without removing technical facts.

## Dashboard schema (version 1)

`content/dashboard.json` specifies:

- `schema`: integer `1`.
- `verified_at_utc`: reviewed snapshot time, not checkpoint creation time.
- `history_source`: local public aggregate history JSON path.
- `later_slices_source`: local public V4/V5 checkpoint JSON path.
- `terminal_v5`: reviewed terminal status, verification time, nullable exact
  checkpoint time, checkpoint SHA-256, updates, valid labels, processed input
  tokens, perplexity, mean NLL in nats per target, scored-label denominator,
  measured save-and-evaluation percentage of loop time, source URL and precision
  note. Positive counts and finite nonnegative measurements are validated.
- `unrun`: records with `id`, `title`, explicit `status` (`not_run` or
  `blocked_before_trial`), `value: null`, and an explanatory `note`.

`dashboard.load_dashboard` compiles these sources, their exact SHA-256 hashes,
all original post tables with source hashes, the terminal addition, and one shared
summary. `assets/dashboard-data.json` is generated, not edited. Both the homepage
cards and dashboard render this same model. The raw historical arrays and their
contracts remain available in the compiled download. No null is changed to zero.

`chart_definitions` specifies each series' population, stage/clock, units, rows and
notes. Separate stages and populations stay separate. Repeated baselines and
regressions remain. A source-snapshot time is not an observation or a save time.
Rows with unknown coordinates stay in the table but not chart geometry; nulls
break lines. Full reported float precision is retained in tables/JSON; tick labels
are compact. Cumulative timings overlap and must not be added. Training counts,
reserved charges and completed work are different measures, not quality scores.

Historical post tables are extracted directly from Markdown-rendered originals.
Strict scalar/fraction parsing excludes versions, ranges and proposed percentage
thresholds from measurement bars. Different denominators are not pooled. Missing
or nonnumeric cells have no bar; a measured zero is retained. Each comparison
keeps its dated source and caveats. The source table is authoritative.

## Update procedure

1. Add reviewed public evidence with population/scorer/tokenizer identity,
   denominator, units, stage, status and provenance. Do not import private logs.
2. Keep historical source assets frozen. Add a separately reviewed new aggregate
   or extend the explicit current-data contract. A future stage requires an
   intentional schema/series update; do not append it under V5's identity.
3. Update dated status prose and companions together. The installed guard cutoff
   is not changed by a planning-horizon extension.
4. Run `python scripts/build.py`, then
   `python -m unittest discover -s tests -v` using the repository environment.
5. Run the existing complete privacy/publication validator with the publisher's
   private-terms file. Review all generated/source changes, not only HTML.
6. Check desktop, mobile, keyboard, zoom and no-JavaScript rendering before the
   existing reviewed publication procedure in `PUBLISHING.md`.

New SVGs use an exact named-file allowlist. Only those dashboard files additionally
allow bounded, leaf-only text labels; frozen chart files retain their old passive
profile. Scripts, external resources, inline SVG/styles/events, foreign objects,
unknown attributes and external references remain rejected. The only browser
JavaScript remains the existing snapshot-age/cutoff clock.

## Accessibility contract

DOM order is original passage, then matching plain-language passage. Desktop uses
two columns; mobile stacks each pair. Numbered crosslinks work without JavaScript.
Native details disclose the glossary and long evidence sections. Charts have text
alternatives, visible scales, exact captioned tables and keyboard-focusable scroll
regions. Color is not the sole carrier of meaning. Small screens may scroll a
chart horizontally rather than shrink its labels into unreadable text.
