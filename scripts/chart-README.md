# Reproducing the frozen checkpoint charts

Sanitized input: `assets/checkpoint-history.json`; SHA256 `3a854fc18127fd1083ded21773e43d9e58cdb828cff8c522ddb759c5ecfef4f9`.

Data freeze: 2026-10-29T18:33:03.713598+00:00. Latest saved-checkpoint observation:2026-10-29T18:31:32.221751+00:00. Observation/freeze timestamps are not checkpoint creation times. This revises the initial October29 publication at commit f23b61ee9f41749eef14ff1953911b862fa1d237.

Use Python3.13 and the existing versions in `chart-requirements.txt`. Run `python3 scripts/build_charts.py` from the site root. Generation performs no installation or network activity. The SVG sanitizer, fixed hash salt, font paths, passive tag/attribute profile and local glyph/clip references are unchanged.

The downloads contain33 evaluation rows (31 narrow CFR and2 historical broader-panel rows),27 global checkpoint identities,21 separate observational metadata rows, and4 unchanged completed-run timing rows. Repeated checkpoint observations remain distinct and are never averaged. Missing x values are omitted; null/unrun results remain missing. The five saved stage2 checkpoints are664,1327,1990,2653,3316 plus a repeated parent baseline. The checkpoint1990 regression remains visible; the last observed PPL is39.64829262191972. No terminal, broader-panel or fixed32 result is inferred for the current phase. CFR is a cheap narrow development metric, not reasoning or a universal perplexity target.

Physical and model-lineage clocks remain separate; phase-local clocks reset. Private source paths, host/job details and source-receipt pins are excluded; actual checkpoint, sidecar, report, evaluator, evaluation-manifest and tokenizer hashes remain.

## checkpoint-perplexity.svg

Narrow CFR development evaluation only:7,057 scored labels per report under one unchanged contract. Left:cumulative model-lineage valid labels in millions. Right:phase-local valid labels. Hollow markers retain baseline observations without averaging repeated checkpoints. Of 31 evaluated rows, the cumulative panel plots 26 and omits five unknown x values; the phase-local panel plots 30 and omits one early baseline. Missing values are never plotted at zero. Broad-panel and fixed32 results are separate. Stage2 has five saved checkpoints, not a terminal result. Checkpoint1990 PPL42.54301119340581 regressed from41.64221987947464 at checkpoint1327; checkpoint2653 reached40.75655881589883 and latest checkpoint3316 reached39.64829262191972, below parent43.77612727431155. Latest observation:2026-10-29T18:31:32.221751+00:00; checkpoint creation time unavailable.

SHA256 `233c36d7b2764efde0204ecf1888dbc5d90dcd63f52ddc8c7ac298e6948731ad`; 116,482 bytes.

Counts: `{"baseline_markers_per_panel": 4, "baseline_observations_total": 5, "evaluated_rows": 31, "omitted_unknown_cumulative_x": 5, "omitted_unknown_phase_x": 1, "plotted_cumulative_rows": 26, "plotted_phase_local_rows": 30, "unique_checkpoint_identities": 27}`.

## broader-panel.svg

Historical mixed-source development panel:130,209 scored labels. Only the parent and science-terminal aggregate checkpoints are available. Source slices keep arXiv45,516, StackExchange38,590 and Wikimedia46,103 labels separate. Not merged with the7,057-label CFR contract; not a current-stage or reasoning result.

SHA256 `4b1a105b4e66dcb9b2a9271580d4f5475fe53ed29cbf01469d17f2e20ba4fc85`; 75,797 bytes.

Counts: `{"aggregate_points": 2, "aggregate_scored_labels": 130209, "source_denominators": {"arxiv": 45516, "stackexchange": 38590, "wikimedia": 46103}, "source_slice_points": 6}`.

## training-throughput.svg

Four completed runs; actual phase-local valid labels divided by named guard-wall, worker-elapsed or training-loop seconds. Rates are thousands of valid labels per second. Guard wall is approximate where available. Two missing denominator values are omitted, not zero-filled. No GPU-kernel throughput claim.

SHA256 `5c83a5691fc2afa35df4351ada1a65b3bd6885cb6bddc2b6b66152e44e4b99dd`; 71,453 bytes.

Counts: `{"actual_bars": 10, "completed_runs": 4, "omitted_missing_denominators": [{"denominator": "Guard wall (approximate)", "stage": "science_104521471"}, {"denominator": "Worker elapsed", "stage": "filtered_96012838"}]}`.

## checkpoint-overhead.svg

Four completed runs. Checkpoint and evaluation full-boundary hook seconds are divided separately by matching training-loop seconds and stacked. Totals approximately1.330%,1.391%,0.989%,1.923%. The10% engineering reference ceiling is not a new timing measurement. Reserved or campaign-wide evaluation charges are not substituted for actual phase hooks.

SHA256 `a435686def4e2b084254e8f63414f3bb1f9e017efc22b56a826395e82b5a1efc`; 65,523 bytes.

Counts: `{"actual_hook_components": 8, "completed_runs": 4, "missing_hook_values": 0, "reference_ceiling_percent": 10}`.

No publication action is performed by the generator. The10% overhead line is an engineering reference. Timing denominators retain guard wall, worker elapsed and training loop; they are not GPU-kernel rates.
