---
title: "Second checkpoint on the next corpus slice"
date: "2026-10-29"
slug: "second-checkpoint-on-the-next-corpus-slice"
phase: "Finite continuation: second saved checkpoint"
summary: "At update 1,137, CFR development perplexity is 38.5124: down 3.1774% from the matching parent baseline and 2.4336% from checkpoint 569. Broader and logic evaluations have not run at this checkpoint."
order: 43
---

The second saved checkpoint in this corpus slice contains **37,175,835 stage-local completed valid next-token labels** at update **1,137**. CFR development perplexity is **38.5124**, compared with **39.7762** for the matching unadapted parent baseline and **39.4730** at checkpoint 569. That is a decrease of **3.1774% from the parent** and **2.4336% from the first checkpoint**. Mean negative log-likelihood is 3.650979 nats per label.

All three reports score the same **7,057 labels**, using the same tokenizer and evaluator. The parent point repeats an existing checkpoint at zero labels in this stage. Receipts for checkpoint 1,137 were observed at **22:55:46 UTC on 29 October**; its exact creation time is unavailable. The 299M-parameter model, 16K vocabulary, and 1,024-token context continue in the same uninterrupted stage, whose one-pass target is 111,462,468 valid labels.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-1137-cfr-perplexity.svg" alt="CFR development perplexity falls from parent 39.7762 at zero stage labels to 39.4730 at 18.604 million and 38.5124 at 37.176 million completed stage labels">
<figcaption>Three observations under the same 7,057-label CFR development contract: a repeated parent baseline (hollow circle) and two saved checkpoints. The x-axis counts completed valid labels within this stage. The y-axis is restricted to show this small change. <a href="/model-training-journal/assets/charts/v4-1137-cfr-perplexity.svg">Open full size</a>.</figcaption>
</figure>

Cumulative timing **through checkpoint 1,137** records 6,935.874 loop seconds, including 232.004 seconds of checkpoint hooks and 4.461 seconds of evaluation hooks. Those hooks account for **3.4093%** of loop time; subtracting them leaves 6,699.408 seconds. These totals include full boundary hooks and exclude model loading. They overlap the earlier checkpoint totals, so they are not disjoint per-checkpoint durations or GPU-kernel throughput measurements.

This is a narrow, repeatedly used development measure. There is no new broader-panel, fixed32, or logic result at this checkpoint, and no CFR threshold establishes transferable logic or generalization. The historical fixed32 result remains 0/32 correct and 0/32 protocol-valid outputs: an output-interface failure that does not isolate reasoning or model capacity.

The approved small format/logic before-and-after diagnostic is **installed only**. No model or CPU readiness run has taken place; execution waits for actual terminal closure of this stage and preserves the unadapted base. This AI-assisted engineering journal reports aggregate measurements without publishing held-out prompts or raw training data.

Downloads: [three-point chart data JSON](/model-training-journal/assets/v4-second-checkpoint-1137/cfr-checkpoints.json), <a href="/model-training-journal/assets/v4-second-checkpoint-1137/cfr-checkpoints.txt" download="v4-1137-cfr-checkpoints.csv">chart data CSV</a>, <a href="/model-training-journal/assets/v4-second-checkpoint-1137/cumulative-timing.txt" download="v4-1137-cumulative-timing.csv">cumulative timing CSV</a>, and <a href="/model-training-journal/assets/v4-second-checkpoint-1137/evaluations.txt" download="v4-1137-evaluations.csv">sanitized 38-row evaluation history CSV</a>. Empty fields mean unavailable, never zero. These files and this chart are frozen to this post; earlier charts retain their published bytes.

To reproduce the figure, use the existing pinned chart environment and run `python3 scripts/build_v4_second_checkpoint_chart.py` from the site root. The builder reads only the downloaded aggregate JSON and reuses the existing passive SVG sanitizer.
