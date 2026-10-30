---
title: "A completed slice and an uneven loss curve"
date: "2026-10-30"
slug: "a-completed-slice-and-an-uneven-loss-curve"
phase: "Finite continuation: completed first V4 slice"
summary: "The first V4 slice completed 111.46M valid labels. Terminal CFR perplexity 37.7860 is below the parent but worse than the preceding checkpoint. The next slice is running; a format diagnostic stopped at its CPU readiness gate."
order: 45
---

The first V4 corpus slice has completed **111,462,468 valid next-token labels**, **111,706,112 processed positions**, and **3,409 optimizer updates**. Its terminal checkpoint scores CFR development perplexity **37.7860** on the same **7,057 labels**, versus the matching parent **39.7762**. The terminal score is **5.0035% lower than the parent**, but **1.2598% higher than checkpoint 2,841's 37.3159**. Lower perplexity is better. The best observed checkpoint and the terminal checkpoint are different; the curve below preserves that regression.

| Observation | Completed slice labels | CFR perplexity |
|---|---|---|
| Repeated parent | 0 | 39.7762 |
| Checkpoint 569 | 18,604,156 | 39.4730 |
| Checkpoint 1,137 | 37,175,835 | 38.5124 |
| Checkpoint 1,705 | 55,747,334 | 38.5456 |
| Checkpoint 2,273 | 74,319,147 | 38.1737 |
| Checkpoint 2,841 | 92,890,868 | 37.3159 |
| Terminal 3,409 | 111,462,468 | 37.7860 |

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-terminal-cfr-perplexity.svg" alt="Seven same-panel CFR observations: parent 39.7762; checkpoint 569: 39.4730; 1137: 38.5124; 1705: 38.5456; 2273: 38.1737; 2841: 37.3159; terminal 3409: 37.7860. Both regressions remain visible.">
<figcaption>CFR development evaluation only, 7,057 labels under the same tokenizer and evaluator. Hollow marker: repeated parent at zero labels within this slice. The restricted y-axis shows small changes. Repeated development evaluation is neither a sealed-holdout result nor evidence of transferable logic. <a href="/model-training-journal/assets/charts/v4-terminal-cfr-perplexity.svg">Open full size</a>.</figcaption>
</figure>

Terminal mean negative log-likelihood is **3.631939 nats per label**. Completion was verified separately from the saved-checkpoint evaluation. The terminal receipts were copied at **03:47:48 UTC** and bound to fresh closed-stage metadata at **03:49:55 UTC on 30 October**. The final genuine live progress sample remains **02:45:48 UTC**. These are observation times; exact checkpoint creation time is unavailable. An ended process alone would not establish successful completion.

The cumulative timing panel includes all checkpoint and evaluation boundary hooks through the terminal checkpoint: **698.850 checkpoint seconds** plus **9.251 evaluation seconds**, within **20,821.276 loop seconds**. Combined overhead is **3.40085%**; subtracting those hooks gives **20,113.175 seconds**. Model loading is excluded. These cumulative checkpoint totals overlap, so they must not be added together. They are not guard-wall, worker-startup or GPU-kernel timings. The downloadable history deliberately keeps these measurements in its intermediate-boundary schema; the separate completion verification establishes stage status.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-terminal-overhead.svg" alt="Six cumulative checkpoint and evaluation hook fractions, each approximately 3.4 percent of loop time. These are overlapping totals, not per-interval durations.">
<figcaption>A separate timing panel: cumulative checkpoint plus evaluation fraction at each saved boundary. Full boundary hooks included; model load excluded. The axis starts at zero. The measured terminal fraction is 3.40085%, below the existing 10% limit. <a href="/model-training-journal/assets/charts/v4-terminal-overhead.svg">Open full size</a>.</figcaption>
</figure>

The clocks measure different things. Completed slice work is **111,462,468 valid labels /111,706,112 processed positions /3,409 updates**. The terminal checkpoint's retained model lineage is **744,286,144 valid labels /745,734,144 positions /22,758 updates**. Physical campaign totals are **746,944,538 valid labels /748,396,544 positions /22,839 updates**, retaining replay and interrupted work. These clocks are not interchangeable. Historical failed reservations remain charged; the new stage does not reset them.

The **second V4 slice launched at 03:39 UTC**. Its verified **03:54:02 UTC** snapshot has **81 completed updates**, **2,648,353 completed valid labels**, and **2,654,208 processed positions**. Its finite target is **111,430,307 valid labels /111,673,344 processed positions /3,408 updates**. There is **no new scored saved checkpoint from this slice yet**; the repeated parent baseline is not a new checkpoint. Progress does not advance a quality score, and these new-stage counters do not extend the completed first-slice chart.

The format diagnostic stopped at its **CPU readiness gate**: an incompatible device-visibility setting caused an abort before the actual before-and-after trial. That is an infrastructure failure, not a result about formatting or reasoning. A source-only repair is prepared; no successful replacement run or diagnostic improvement is claimed in this snapshot. The next diagnostic still needs its own reviewed admission and successful readiness check. The existing diagnostic eligibility check is tied to the completed first slice, while continuation has moved to the second slice. A visibility-mask repair does not resolve that stage mismatch; the diagnostic remains blocked under its current contract.

No new broader-panel, fixed32 or reasoning score belongs to these V4 checkpoints. The older broader-panel perplexity **14.6312 on 130,209 labels** stays in its own frozen panel. Historical fixed32 remains **0/32 task-correct and 0/32 protocol-valid**, an interface failure that does not isolate reasoning ability or model capacity. The earlier [broader panel](/model-training-journal/assets/charts/v4-569-broader-lm.svg), [throughput panel](/model-training-journal/assets/charts/v4-569-throughput.svg), and [overhead panel](/model-training-journal/assets/charts/v4-569-overhead.svg) retain their original scope and bytes. Null or blank measurements remain unavailable, never zero.

This remains AI-assisted engineering toward transferable logic beyond plausible conversation. The model was trained from scratch, has 299M parameters, a 16K vocabulary and 1,024-token context; none of those facts establishes assistant capability. There is no universal perplexity target. The original control and sealed final holdout remain untouched. This journal shares reviewed aggregate observations, not source passages, private logs, data, credentials or claims that code and weights have been released.

Downloads: [seven-point CFR JSON](/model-training-journal/assets/v4-terminal-tranche1/cfr-checkpoints.json), <a href="/model-training-journal/assets/v4-terminal-tranche1/cfr-checkpoints.txt" download="v4-terminal-cfr-checkpoints.csv">CFR chart CSV</a>, [complete 42-row aggregate history JSON](/model-training-journal/assets/v4-terminal-tranche1/checkpoint-history.json), <a href="/model-training-journal/assets/v4-terminal-tranche1/evaluations.txt" download="v4-terminal-evaluations.csv">evaluation CSV</a>, [cumulative timing JSON](/model-training-journal/assets/v4-terminal-tranche1/cumulative-overhead.json), <a href="/model-training-journal/assets/v4-terminal-tranche1/intermediate-timing.txt" download="v4-terminal-cumulative-timing.csv">cumulative timing CSV</a>, <a href="/model-training-journal/assets/v4-terminal-tranche1/progress.txt" download="v4-terminal-progress.csv">first-slice progress CSV</a>, <a href="/model-training-journal/assets/v4-terminal-tranche1/throughput.txt" download="v4-terminal-throughput.csv">observed throughput CSV</a>, <a href="/model-training-journal/assets/v4-terminal-tranche1/stage.txt" download="v4-terminal-stage.csv">first-slice stage snapshot CSV</a>, <a href="/model-training-journal/assets/v4-terminal-tranche1/saved-checkpoints.txt" download="v4-terminal-saved-checkpoints.csv">saved checkpoints CSV</a>, and [separate new-stage progress JSON](/model-training-journal/assets/v4-terminal-tranche1/continuation-status.json).

Reproduce the new passive figures with the existing pinned plotting environment: `python3 scripts/build_v4_terminal_charts.py`. The builder reads only sanitized aggregate JSON; it performs no training, telemetry fetch or evaluation.
