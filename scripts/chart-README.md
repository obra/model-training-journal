# Reproducing the terminal checkpoint charts

Sanitized input: `assets/checkpoint-history.json`; SHA256 `6a43c0f3126635369415b29834688dda4b74ce3c97f8ecd2afb858798406d590`.

Run `python3 scripts/build_charts.py` from the site root with Python3.13 and the existing pinned `chart-requirements.txt` environment. No installation or network activity is performed by the builder. The fixed SVG hash salt, font paths, sanitizer, passive tag/attribute profile and local glyph/clip references are unchanged.

The frozen download contains35 LM evaluation rows:32 narrow CFR and3 broader-panel rows,28 global checkpoint identities,22 separate stage2 observations and5 completed-run timings. Three fixed32 summaries are separate from LM scores. Only the current terminal broader/fixed32 unrun markers have been resolved;26 other unrun markers remain. Unknown coordinates are omitted; missing checkpoint creation times remain null. Physical and model-lineage clocks retain their replay gap. Repeated observations are not new unique checkpoints.

CFR terminal PPL39.7762 slightly regresses from39.6483, remaining below parent43.7761. Broader-panel PPL14.6312 versus historical62.1032 compares the same130209-label panel across many phases. Fixed32 remains an output-interface failure, not a capacity ceiling. These are scoped development measurements, not sealed holdout results or globally unseen-source claims. Timing denominators remain distinct; no GPU-kernel throughput claim is made.

Private source paths, hosts/jobs and source-receipt pins are excluded using the established public-field allowlist. Checkpoint, sidecar, report, evaluator, evaluation-manifest and tokenizer identities remain under that same contract. No historical post body is changed by this candidate.

## checkpoint-perplexity.svg

Narrow CFR development evaluation only:7,057 scored labels per report under one unchanged contract. Left:cumulative model-lineage valid labels in millions. Right:phase-local valid labels. Hollow markers retain baseline observations without averaging repeated checkpoints. Of 32 evaluated rows, the cumulative panel plots 27 and omits five unknown x values; the phase-local panel plots 31 and omits one early baseline. Missing values are never plotted at zero. Broad-panel and fixed32 results are separate. Stage2 completed six scheduled checkpoints. Terminal PPL39.776214231484126 slightly regressed from39.64829262191972 at checkpoint3316, below parent43.77612727431155. The checkpoint1990 regression remains visible. Terminal observation:2026-10-29T19:27:22.274377+00:00; checkpoint creation time unavailable.

SHA256 `8ded85873446c9b75d13005d94308447f9c9ba47283cd8c150bf72ec5497e06e`; 116,739 bytes. Counts: `{"baseline_markers_per_panel": 4, "baseline_observations_total": 5, "evaluated_rows": 32, "omitted_unknown_cumulative_x": 5, "omitted_unknown_phase_x": 1, "plotted_cumulative_rows": 27, "plotted_phase_local_rows": 31, "unique_checkpoint_identities": 28}`.

## broader-panel.svg

Mixed-source development panel:130,209 scored labels at three checkpoints, with nine separate source slices. Science-terminal PPL62.10324143003107 at133411556 retained labels versus current-terminal14.631154356930713 at632823676 spans multiple phases; not an isolated phase effect. Source denominators:arXiv45516, StackExchange38590, Wikimedia46103. Separate from CFR; no reasoning or sealed-holdout claim.

SHA256 `7090a597c3aab86cdff5069652b10ca5114113bd0eec5e8166153a3f93c64560`; 82,839 bytes. Counts: `{"aggregate_points": 3, "aggregate_scored_labels": 130209, "source_denominators": {"arxiv": 45516, "stackexchange": 38590, "wikimedia": 46103}, "source_slice_points": 9}`.

## training-throughput.svg

Five completed runs; actual phase-local valid labels divided by named guard-wall, worker-elapsed or training-loop seconds. Rates are thousands of valid labels per second. Guard wall is approximate where available. Two missing denominator values are omitted, not zero-filled. No GPU-kernel throughput claim.

SHA256 `c7a123874abcf943b0a491c0ce72405c00f06923d0f38a77034ebaec6340003f`; 74,597 bytes. Counts: `{"actual_bars": 13, "completed_runs": 5, "omitted_missing_denominators": [{"denominator": "Guard wall (approximate)", "stage": "science_104521471"}, {"denominator": "Worker elapsed", "stage": "filtered_96012838"}]}`.

## checkpoint-overhead.svg

Five completed runs. Checkpoint and evaluation full-boundary hook seconds are divided separately by matching training-loop seconds and stacked. Totals approximately1.330%,1.391%,0.989%,1.923%,2.120%. The10% engineering reference ceiling is not a new timing measurement. Reserved or campaign-wide evaluation charges are not substituted for actual phase hooks.

SHA256 `855be181244c4c3903bf7a22d3fa62aa23064d4dcfc134edea7a7b05b30ac77f`; 67,849 bytes. Counts: `{"actual_hook_components": 10, "completed_runs": 5, "missing_hook_values": 0, "reference_ceiling_percent": 10}`.
