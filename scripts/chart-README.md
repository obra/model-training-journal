# Reproducing the frozen checkpoint charts

Sanitized input: `assets/checkpoint-history.json`; SHA256 `0fe801b9c69aa119266bd3aeabcf3efdce425d8c93d4409750203bb347789761`.

Source freeze: 2026-10-29T16:39:28.277512+00:00. Latest saved-checkpoint observation:2026-10-29T16:31:12.990416+00:00. These are observation/freeze timestamps, not checkpoint creation times.

Use Python3.13 and the already available package versions in `chart-requirements.txt`. From the site root:

```sh
python3 scripts/build_charts.py
```

Generation performs no installation or network activity. Matplotlib uses fixed `svg.hashsalt`, DateNone metadata and glyph paths. XML processing removes the DTD, metadata and CSS; style declarations become bounded presentation attributes. References point only to local glyph paths or clip paths. Each file has accessible title/description and roleimg. The sanitizer/profile is unchanged from the previous snapshot; only frozen data and its captions/annotations changed.

The downloads `assets/checkpoint-history.txt` and `assets/training-throughput.txt` contain31 actual evaluation rows and4 completed-run timing rows. CFR7057, broad130209 and historical fixed32 are distinct contracts. Unknown x values are omitted, not zero-filled; baselines are preserved as repeated observations rather than averaged.

## Frozen charts

### checkpoint-perplexity.svg

Narrow CFR development evaluation only:7,057 scored labels per report under one unchanged contract. Left:cumulative model-lineage valid labels in millions. Right:phase-local valid labels. Hollow markers retain baseline observations without averaging repeated checkpoints. Of 29 evaluated rows, the cumulative panel plots 24 and omits five unknown x values; the phase-local panel plots 28 and omits one early baseline. Missing values are never plotted at zero. Broad-panel and fixed32 results are separate. Stage2 has three saved checkpoints, not a terminal result. The latest PPL42.54301119340581 regresses from41.64221987947464 at checkpoint1327, while below parent43.77612727431155.

SHA256 `6ba48f2f34664e6db9c79d22797d635d14aade5f175936865a786c1fcdf76cab`; 114,914 bytes.

Counts: `{"baseline_markers_per_panel": 4, "baseline_observations_total": 5, "evaluated_rows": 29, "omitted_unknown_cumulative_x": 5, "omitted_unknown_phase_x": 1, "plotted_cumulative_rows": 24, "plotted_phase_local_rows": 28, "unique_checkpoint_identities": 25}`.

### broader-panel.svg

Historical mixed-source development panel:130,209 scored labels. Only the parent and science-terminal aggregate checkpoints are available. Source slices keep arXiv45,516, StackExchange38,590 and Wikimedia46,103 labels separate. Not merged with the7,057-label CFR contract; not a current-stage or reasoning result.

SHA256 `4b1a105b4e66dcb9b2a9271580d4f5475fe53ed29cbf01469d17f2e20ba4fc85`; 75,797 bytes.

Counts: `{"aggregate_points": 2, "aggregate_scored_labels": 130209, "source_denominators": {"arxiv": 45516, "stackexchange": 38590, "wikimedia": 46103}, "source_slice_points": 6}`.

### training-throughput.svg

Four completed runs; actual phase-local valid labels divided by named guard-wall, worker-elapsed or training-loop seconds. Rates are thousands of valid labels per second. Guard wall is approximate where available. Two missing denominator values are omitted, not zero-filled. No GPU-kernel throughput claim.

SHA256 `5c83a5691fc2afa35df4351ada1a65b3bd6885cb6bddc2b6b66152e44e4b99dd`; 71,453 bytes.

Counts: `{"actual_bars": 10, "completed_runs": 4, "omitted_missing_denominators": [{"denominator": "Guard wall (approximate)", "stage": "science_104521471"}, {"denominator": "Worker elapsed", "stage": "filtered_96012838"}]}`.

### checkpoint-overhead.svg

Four completed runs. Checkpoint and evaluation full-boundary hook seconds are divided separately by matching training-loop seconds and stacked. Totals approximately1.330%,1.391%,0.989%,1.923%. The10% engineering reference ceiling is not a new timing measurement. Reserved or campaign-wide evaluation charges are not substituted for actual phase hooks.

SHA256 `a435686def4e2b084254e8f63414f3bb1f9e017efc22b56a826395e82b5a1efc`; 65,523 bytes.

Counts: `{"actual_hook_components": 8, "completed_runs": 4, "missing_hook_values": 0, "reference_ceiling_percent": 10}`.

Latest stage2 checkpoint1990 has PPL42.54301119340581, worse than checkpoint1327 at41.64221987947464 and below parent43.77612727431155. The publication snapshot stops here; later checkpoints are intentionally excluded.

The10% overhead line is an engineering reference, not a measured extra point. Throughput denominators remain guard wall, worker elapsed and training loop; no GPU-kernel throughput claim. No publication action is performed by the generator.
