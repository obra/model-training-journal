---
title: "Fourth checkpoint on the next corpus slice"
date: "2026-10-30"
slug: "fourth-checkpoint-on-the-next-corpus-slice"
phase: "Finite continuation: fourth saved checkpoint"
summary: "Checkpoint 2,273 scores CFR perplexity 38.1737 on the same 7,057-label development set. All four saved checkpoints remain visible, including checkpoint 1,705's small regression. No new broader or logic score has run."
order: 44
---

The fourth saved checkpoint contains **74,319,147 completed stage-local valid next-token labels** at update **2,273**. CFR development perplexity is **38.1737**, with mean negative log-likelihood **3.642146 nats per label**. That is **4.0289% below the matching parent baseline** and **0.8794% below checkpoint 1,137**. Checkpoint 1,705 had a small regression; this update preserves it.

| Observation | Completed stage labels | CFR perplexity |
|---|---|---|
| Repeated parent baseline | 0 | 39.7762 |
| Checkpoint 569 | 18,604,156 | 39.4730 |
| Checkpoint 1,137 | 37,175,835 | 38.5124 |
| Checkpoint 1,705 | 55,747,334 | 38.5456 |
| Checkpoint 2,273 | 74,319,147 | 38.1737 |

All five reports score the same **7,057 labels** under the same tokenizer and evaluator contract. The parent repeats existing weights at zero labels in this stage. Checkpoint 2,273's receipts were observed at **00:55:32 UTC on 30 October**; exact checkpoint creation time is unavailable. The from-scratch **299M-parameter model**, **16K vocabulary**, and **1,024-token context** continue in the same guarded, nonwrapping stage, with a one-pass target of **111,462,468 valid labels**.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-2273-cfr-perplexity.svg" alt="Five CFR observations: parent 39.7762, checkpoint 569 at 39.4730, checkpoint 1137 at 38.5124, checkpoint 1705 at 38.5456, checkpoint 2273 at 38.1737; the small checkpoint 1705 regression remains visible">
<figcaption>The same narrow 7,057-label CFR development contract throughout. Hollow circle: repeated parent baseline. The x-axis counts completed labels within this stage; the y-axis is restricted to show the small changes. This is repeated development evaluation, not a sealed-holdout score. <a href="/model-training-journal/assets/charts/v4-2273-cfr-perplexity.svg">Open full size</a>.</figcaption>
</figure>

Measured timing through checkpoint 2,273 is **cumulative and intermediate**: **13,874.969 loop seconds**, including **464.881 seconds of checkpoint hooks** and **6.839 seconds of evaluation hooks**. The combined fraction is **3.3998%**; subtracting those hooks leaves **13,403.250 seconds**. Completed valid-label throughput is **5,356.35 labels/s over loop time**, or **5,544.86 labels/s excluding measured hooks**. Full boundary hooks are included and model loading is excluded. These totals overlap earlier checkpoint totals and are not separate durations to add. Guard-wall and worker rates at this boundary are unmeasured; none of these figures is GPU-kernel throughput.

The separate progress download is frozen at **00:59:43 UTC**: **2,369 completed updates / 77,458,076 completed labels**, versus **77,490,776 charged labels**. Charged work includes unfinished accumulation. Later progress does not advance the saved checkpoint's quality measurement. Stage, retained model-lineage, physical campaign, and charged-cap clocks remain separate; physical work retains historical replay and interrupted work.

There is **no new broader-panel, fixed32, or reasoning score** at checkpoint 2,273. The earlier parent's broader perplexity **14.6312 on 130,209 labels** belongs to a separate checkpoint and panel. Historical fixed32 remains **0/32 task-correct and 0/32 protocol-valid**: an output-interface failure that does not isolate reasoning or model capacity. The earlier [broader panel](/model-training-journal/assets/charts/v4-569-broader-lm.svg), [throughput](/model-training-journal/assets/charts/v4-569-throughput.svg), and [overhead](/model-training-journal/assets/charts/v4-569-overhead.svg) figures keep their original frozen scope and bytes.

The goal remains transferable logic beyond plausible conversation. No universal perplexity target or capability claim follows from this narrow measure. The fixed before-and-after format diagnostic is planned and has **not run**. The original 97M control and sealed final holdout remain untouched. This AI-assisted engineering journal publishes reviewed aggregate evidence without source passages or raw training data.

Downloads: [five-point chart JSON](/model-training-journal/assets/v4-fourth-checkpoint-2273/cfr-checkpoints.json), <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/cfr-checkpoints.txt" download="v4-2273-cfr-checkpoints.csv">chart CSV</a>, [complete aggregate history JSON](/model-training-journal/assets/v4-fourth-checkpoint-2273/checkpoint-history.json), <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/evaluations.txt" download="v4-2273-evaluations.csv">40-row evaluation history CSV</a>, <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/intermediate-timing.txt" download="v4-2273-intermediate-timing.csv">four cumulative timing boundaries CSV</a>, <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/throughput.txt" download="v4-2273-throughput.csv">separate observed throughput CSV</a>, <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/progress.txt" download="v4-2273-progress.csv">progress CSV</a>, <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/stage.txt" download="v4-2273-stage.csv">stage snapshot CSV</a>, and <a href="/model-training-journal/assets/v4-fourth-checkpoint-2273/saved-checkpoints.txt" download="v4-2273-saved-checkpoints.csv">saved-checkpoint CSV</a>. JSON nulls and empty CSV fields mean unavailable or unrun, never zero. The complete history preserves every older row, all separate panels, and their missing values.

Reproduce this frozen figure with the existing pinned chart environment: `python3 scripts/build_v4_fourth_checkpoint_chart.py`. The builder reads only the aggregate chart JSON and reuses the existing passive SVG sanitizer.
