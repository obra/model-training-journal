---
title: "Twelve checkpoints close the scoring gap"
date: "2026-10-31"
slug: "twelve-checkpoints-close-the-scoring-gap"
phase: "Completed continuation and fixed-panel evaluation"
summary: "V6 and V7 now have twelve checkpoint scores on the same 7,057-target development panel. The final scores improve slightly, the curves remain uneven, and reasoning is still unmeasured."
order: 49
---

The [earlier update](/model-training-journal/2026/10/31/v6-complete-v7-running-without-new-scores/) stopped with V6 finished, V7 running, and neither stage scored. V7 has now completed, and a separate evaluation successfully scored **all twelve saved V6/V7 checkpoints**, with **zero failed scoring attempts or retries**. The last scoring job finished at **02:55:33 UTC on 31 October**. The earlier readiness failure remains part of the record.

V6's terminal perplexity is **34.18875627**; V7's is **33.88233562**, about **0.90% lower**. Every new score uses the same frozen **7,057-target CFR development panel**, tokenizer, scorer and numerical precision. Perplexity measures next-token prediction error; lower is better on this particular panel. This small descriptive change has no statistical significance result and does not establish transferable reasoning.

## The curves, including the reversals

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/dashboard-cfr-v6.svg" alt="V6 checkpoint perplexity rises and falls across six saves, ending at 34.1888. The horizontal axis counts usable training targets within V6.">
<figcaption>V6: all six saved checkpoints. Lower is better; the vertical scale is narrowed to show the reversals. The horizontal axis counts usable targets within V6. Exact values follow below. <a href="/model-training-journal/assets/charts/dashboard-cfr-v6.svg">Open the full-size V6 chart</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/dashboard-cfr-v7.svg" alt="V7 checkpoint perplexity rises to 34.5285 before falling near 33.88. Its terminal score is slightly higher than its preceding checkpoint.">
<figcaption>V7: all six saved checkpoints. Lower is better; the vertical scale is narrowed and differs from the V6 chart. The horizontal axis counts usable targets within V7. Exact values follow below. <a href="/model-training-journal/assets/charts/dashboard-cfr-v7.svg">Open the full-size V7 chart</a>.</figcaption>
</figure>

Both plots retain every saved checkpoint. Their horizontal axes restart at each stage and count **stage-local usable training targets**, not total model exposure. The charts add no extra zero-step baseline point; V7 starts from the V6 terminal model. V6's lowest sampled perplexity was at update 913; V7's was at update 1,148, just before its terminal save. A later checkpoint need not score better.

| Stage | Local update | Usable training targets in stage | CFR perplexity |
|---|---|---|---|
| V6 | 229 | 7,487,125 | 34.34509563 |
| V6 | 457 | 14,941,669 | 34.61300027 |
| V6 | 685 | 22,396,123 | 34.43284000 |
| V6 | 913 | 29,850,429 | 34.13229447 |
| V6 | 1,141 | 37,304,914 | 34.35973647 |
| V6 terminal | 1,369 | 44,759,442 | 34.18875627 |
| V7 | 230 | 7,519,912 | 34.30000254 |
| V7 | 460 | 15,039,700 | 34.29261710 |
| V7 | 689 | 22,526,917 | 34.33686575 |
| V7 | 919 | 30,046,835 | 34.52846650 |
| V7 | 1,148 | 37,534,104 | 33.87909412 |
| V7 terminal | 1,377 | 45,021,370 | 33.88233562 |

The [dashboard](/model-training-journal/dashboard/#cfr-v6) includes these separate curves, exact values and earlier experiments. The [aggregate JSON](/model-training-journal/assets/v6-v7-cfr-checkpoints.json) retains full reported precision, mean negative log-likelihood, checkpoint fingerprints and scoring identities. Evaluation completion times are recorded separately from model-save times, which are not inferred. This adds reviewed measurements, not a release of training code or weights.

## Training work and evaluation cost

V7 completed **1,377 updates**, **45,021,370 usable training targets** and **45,121,536 processed input tokens**. Its terminal model retains **1,070,817,348 targets** in its training lineage. Total physical campaign work is **1,073,475,742 targets**, including earlier discarded work; the budget has charged **1,089,764,398 targets**, including retained reservations. These three cumulative counts describe different things. None is the size of a unique-text collection or a quality score.

V7 spent **995.76 seconds saving checkpoints** in a **9,126.36-second training loop**: **10.91%**, exceeding the **10% overhead target**. That measurement includes full checkpoint-boundary work and excludes model loading. In-stage evaluation time was zero; the twelve scores above were collected afterward. The saving cost is a concrete issue to address before choosing another run's checkpoint schedule.

The later CPU preparation gate took **31.01 seconds**. The twelve scoring jobs' conservative guard durations totalled **131.66 seconds**; their inner scoring functions totalled **25.76 seconds**. The 25.76 seconds of inner scoring is included within the 131.66 seconds of scoring-job guard time. The separate CPU preparation gate adds 31.01 seconds. The budget keeps the full **3,600-second nonrefundable allocation**—twelve 300-second reservations—charged despite the shorter measured runtime. Combined charged evaluation time is **7,860 seconds**, including the prior **4,260 seconds**.

## What this still does not show

There is **no new reasoning, BLiMP or broader-panel result**. The last task check remains the earlier V3 **0/32 correct and 0/32 format-valid**, which limits what it can say about reasoning. The sealed final planning holdout remains untouched. CFR is a repeatedly used development panel, and its lexical screening does not prove absence of semantic overlap, overlap with other editions, or globally unseen source families. The next decision needs to weigh the small, uneven language change and checkpoint cost against complementary tests. This AI-assisted journal records the evidence and its limits; no checkpoint has established the project's target capability.
