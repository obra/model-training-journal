---
title: "First checkpoint on the next corpus slice"
date: "2026-10-29"
slug: "first-checkpoint-on-the-next-corpus-slice"
phase: "Finite continuation: first saved checkpoint"
summary: "The first V4 checkpoint scores CFR perplexity 39.4730 versus the matching parent baseline of 39.7762. Intermediate checkpoint and evaluation hooks occupy 3.413% of loop time; transferable logic remains unestablished."
order: 42
---

The next finite corpus slice has produced its first saved and scored checkpoint. At update 569 it contains 18,604,156 new valid next-token labels. CFR development perplexity is **39.4730**, down from the matching in-memory parent baseline of **39.7762**: a decrease of 0.30325, or 0.7624%. Mean negative log-likelihood moved from 3.683269 to 3.675616 nats per label.

Both reports score the same 7,057 labels with the same tokenizer and scorer. The baseline repeats the previous terminal checkpoint; it adds no unique checkpoint. The new save adds one checkpoint identity. Its model lineage contains 651,427,832 valid labels; total physical completed work is 654,086,226 labels over 19,999 updates. The previously recorded replay gap remains separate.

This is an encouraging small change on a repeatedly used development set. It is not a sealed test or evidence of globally unseen source families, and it does not establish transferable logic. The previous parent's mixed-source perplexity of 14.6312 and fixed-task result of 0/32 correct and 0/32 protocol-valid outputs remain previous-parent measurements. Neither evaluation has run on this new checkpoint. Zero protocol-valid outputs in that earlier check also prevented isolating reasoning from output-interface failure. There is no universal perplexity threshold that settles those questions.

The saved-checkpoint receipts were observed at **21:58:47 UTC on 29 October**; exact checkpoint creation time is unavailable. A separate live progress observation at **22:01:03 UTC** records 612 completed updates and 20,010,132 applied labels in this phase. Charged exposure is slightly ahead: 20,027,502 labels across 19,601 microbatches, including unfinished accumulation. Those live counters do not move the saved checkpoint's quality result forward. The finite slice allows 111,462,468 valid labels over 3,409 updates; it was still running at that observation, with the next scheduled checkpoint at update 1,137.

Through checkpoint 569, the measured training loop took 3,471.963 seconds, including 115.920 seconds for checkpoint hooks and 2.569 seconds for evaluation hooks. Evaluation includes the parent baseline and this checkpoint. Their combined share is **3.41275%** of loop time. Subtracting those measured hooks leaves 3,353.474 seconds. These are intermediate measurements, include full boundary hooks, and exclude model loading.

Dividing the same 18,604,156 labels by those two clocks gives **5,358 labels/s including hooks**, or **5,548 labels/s excluding the measured hooks**. A different, startup-inclusive observation divides all charged labels by elapsed guard wall time: 4,941 labels/s at 22:01:03. The latest observed 30-second interval charged 5,586 labels/s. These rates have different numerators and time windows; none is GPU-kernel throughput or a final-run rate.

The project goal remains transferable logic. A revised probe is approved but only prepared, with eight complete samples planned at a safe boundary; no result from it is reported here. This AI-assisted engineering journal records aggregate evidence and the limits of what it supports.

## Checkpoint and timing charts

These figures and downloads are frozen to this post. Earlier shared charts and captions retain their previous bytes. CFR, mixed-source evaluation, live exposure, and timing use separate panels and clocks.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-569-checkpoint-perplexity.svg" alt="CFR perplexity across the training lineage with a close view of the V4 parent baseline and first saved checkpoint">
<figcaption>34 CFR evaluation rows, 29 unique checkpoint identities. The V4 inset shows the repeated parent baseline and one new saved checkpoint at 18.604 million phase labels. Unknown coordinates are omitted. <a href="/model-training-journal/assets/charts/v4-569-checkpoint-perplexity.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-569-broader-lm.svg" alt="Three earlier mixed-source checkpoint evaluations and their source slices, with no new V4 result">
<figcaption>Frozen earlier results: three aggregate checkpoints and nine source slices on a separate 130,209-label panel. The most recent is the previous V4 parent, not checkpoint 569. <a href="/model-training-journal/assets/charts/v4-569-broader-lm.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-569-throughput.svg" alt="Five completed runs and intermediate V4 throughput with separately named elapsed-time denominators">
<figcaption>Five completed phases and the intermediate V4 boundary through update 569. Loop time and time excluding measured hooks remain distinct. Missing guard-wall and worker denominators are omitted. Startup-inclusive live rates are in the separate progress download. <a href="/model-training-journal/assets/charts/v4-569-throughput.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-569-overhead.svg" alt="Measured checkpoint and evaluation hook shares for five completed runs and the intermediate V4 checkpoint boundary">
<figcaption>V4's intermediate total is 3.413% through checkpoint 569, including baseline and checkpoint evaluation but excluding model load. The 10% line is an engineering reference. <a href="/model-training-journal/assets/charts/v4-569-overhead.svg">Open full size</a>.</figcaption>
</figure>

Downloads: [sanitized checkpoint history JSON](/model-training-journal/assets/v4-first-checkpoint-569/checkpoint-history.json), <a href="/model-training-journal/assets/v4-first-checkpoint-569/checkpoints.txt" download="v4-checkpoints.csv">checkpoint CSV</a>, <a href="/model-training-journal/assets/v4-first-checkpoint-569/intermediate-timing.txt" download="v4-intermediate-timing.csv">intermediate timing CSV</a>, and <a href="/model-training-journal/assets/v4-first-checkpoint-569/live-progress.txt" download="v4-live-progress.csv">observed progress CSV</a>. Empty fields mean unavailable or unrun, never zero. Checkpoint hashes and scientific stage names identify the measurements; no model weights are included.
