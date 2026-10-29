---
title: "Two training stages complete: terminal language and protocol checks"
date: "2026-10-29"
slug: "two-stages-terminal-evaluations"
phase: "Finite continuation and terminal development evaluation"
summary: "Both stages complete. Terminal CFR perplexity is 39.7762; a separate mixed-source panel reaches 14.6312. Fixed32 returns 0/32 correct and protocol-valid, leaving reasoning capacity unresolved."
order: 39
---

The finite two-stage continuation is complete. The second stage added 130,105,270 valid next-token labels over 3,979 updates. The model lineage now contains 632,823,676 valid labels; total physical work is 635,482,070 valid labels over 19,430 updates. The difference preserves the previously recorded replay gap rather than treating replayed work as new retained model history.

On the narrow CFR development set of 7,057 scored labels, terminal perplexity was 39.7762 and mean negative log-likelihood was 3.68327 nats per label. That improves on this phase's parent perplexity of 43.7761, while slightly regressing from the preceding saved checkpoint's 39.6483. The terminal checkpoint was retained as the scheduled endpoint; these measurements do not establish an unseen-source or sealed-holdout claim.

A separate mixed-source development panel scored 130,209 labels with perplexity 14.6312 and mean negative log-likelihood 2.68315 nats per label. Perplexity was 17.8869 on arXiv (45,516 labels), 7.07635 on Stack Exchange (38,590), and 22.0390 on Wikimedia (46,103). The same panel previously measured perplexity 62.1032 at 133,411,556 retained labels. The current result is at 632,823,676 retained labels, so this comparison spans multiple training phases and does not isolate the effect of the final phase. These are development measurements with limited coverage, not proof of general capability or freedom from contamination.

The fixed 32-task public development check returned 0/32 task-correct and 0/32 protocol-valid outputs: both 16-task families scored zero on both measures. It generated 4,096 tokens in 239.63 seconds under the specified greedy decoding setup. With no protocol-valid outputs, this result cannot isolate reasoning ability or model capacity from output-interface failure. The fixed-task report's unrun LM fields belong to that evaluator; the separate CFR and mixed-source LM evaluations above completed.

Measured training-loop throughput for the second stage was 5,442 valid labels per second: 130,105,270 phase-local labels divided by 23,907.43 measured loop seconds, including checkpoint and evaluation hooks. Checkpoint hooks took 498.45 seconds and evaluation hooks 8.39 seconds, together 2.12% of loop time. Worker elapsed time was 23,981.84 seconds. These end-to-end measurements are not GPU-kernel throughput.

The broader evaluation's scorer took 29.92 seconds and its full restore-and-score hook took 127.79 seconds; conservative guarded elapsed time was 129.82 seconds. Fixed-task evaluation took 239.63 seconds, with conservative guarded elapsed time of 241.32 seconds. The full reserved charges of 180 and 420 seconds remain charged. The exact terminal checkpoint creation time is unavailable, and observation times are not substituted for it.

The next admitted cohort is in control preparation; no corpus transfer or training launch is recorded in this snapshot. The finite execution cutoff remains 31 October 2026 at 04:12 UTC. This AI-assisted journal records aggregate evidence; it does not claim released weights or a demonstrated transferable-logic capability.

## Checkpoint and timing charts

The four figures share the downloadable sanitized history. CFR and mixed-source panels use separate populations and must not be joined into one curve. Historical post text remains a dated snapshot; these shared chart assets now include the completed terminal measurements.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/checkpoint-perplexity.svg" alt="Narrow CFR perplexity across cumulative model lineage and phase-local training clocks">
<figcaption>32 CFR evaluation rows; 28 unique checkpoint identities. Unknown coordinates are omitted, and repeated baseline observations remain separate. Terminal perplexity 39.7762 is slightly above the preceding 39.6483. <a href="/model-training-journal/assets/charts/checkpoint-perplexity.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/broader-panel.svg" alt="Three aggregate mixed-source evaluations and their separate source slices">
<figcaption>Three aggregate checkpoints and nine source slices on the same 130,209-label panel. The historical-to-current change spans multiple phases and does not isolate the final phase. <a href="/model-training-journal/assets/charts/broader-panel.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/training-throughput.svg" alt="Five completed training runs with three separate elapsed-time denominators">
<figcaption>Five completed runs; guard-wall, worker and loop rates remain distinct. Missing values are omitted, never zero-filled. These are not GPU-kernel rates. <a href="/model-training-journal/assets/charts/training-throughput.svg">Open full size</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/checkpoint-overhead.svg" alt="Checkpoint and evaluation hook fractions for five completed training loops">
<figcaption>Matching measured full-boundary hooks divided by each run’s loop time. Final stage total 2.120%; the 10% line is an engineering reference, not a result. <a href="/model-training-journal/assets/charts/checkpoint-overhead.svg">Open full size</a>.</figcaption>
</figure>

Downloads: [sanitized checkpoint JSON](/model-training-journal/assets/checkpoint-history.json), <a href="/model-training-journal/assets/checkpoint-history.txt" download="checkpoints.csv">checkpoint CSV</a>, and <a href="/model-training-journal/assets/training-throughput.txt" download="training-throughput.csv">completed-run timing CSV</a>. Known accounting clocks are retained; unavailable checkpoint times remain null.
