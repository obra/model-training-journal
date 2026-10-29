---
title: "Checkpoint metrics after larger one-pass training phases"
date: "2026-10-29"
slug: "checkpoint-metrics-at-scale"
phase: "Pretraining continuation and development measurements"
summary: "The 299M model completes a 130.07M-label stage with six measured checkpoints. Its next stage is running; the latest saved checkpoint regresses to CFR perplexity 42.5430 from 41.6422. These are narrow development-language results, not a new reasoning score."
order: 38
---

**Snapshot: 29 October 2026, 16:31:12 UTC.** One stage completed; the second is running with **saved** checkpoint 1,990. This follows the historical [99-paper infrastructure pilot](/model-training-journal/2026/10/28/first-admitted-arxiv-continuation/).

The **299,414,528-parameter model** began from scratch. The goal remains demonstrable transferable logic beyond plausible conversation; better language prediction alone does not establish it.

## Checkpoint charts

Static figures freeze the saved measurements observed at **16:31 UTC**. Missing is not zero; tables retain the values.

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/checkpoint-perplexity.svg" alt="CFR development perplexity versus retained model-lineage and phase-local valid labels, with lower later saved values and local increases">
<figcaption>CFR development perplexity, 7,057 labels per report. Left: cumulative retained model-lineage valid labels, in millions; right: phase-local valid labels. Hollow markers retain repeated baseline observations. The cumulative panel plots 24 observations and omits five unknown coordinates; the phase-local panel plots 28 and omits one. <a href="/model-training-journal/assets/charts/checkpoint-perplexity.svg">Open full-size checkpoint chart</a>. Perplexity has no universal pass threshold: comparisons require the same tokenizer, evaluation population and scoring contract. Lower CFR loss does not establish transferable logic.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/broader-panel.svg" alt="Historical broader-panel perplexity at two checkpoints, with aggregate and three source slices separated from the CFR evaluation">
<figcaption>Historical 130,209-label broader panel has two aggregate checkpoints and six source-slice measurements. It is separate from CFR and does not measure the current stage or reasoning. <a href="/model-training-journal/assets/charts/broader-panel.svg">Open full-size broader-panel chart</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/training-throughput.svg" alt="Measured valid-label throughput for four completed runs with guard-wall, worker-elapsed and training-loop denominators shown separately">
<figcaption>Four completed runs, ten measured rates in thousands of valid labels per second. Guard-wall, worker-elapsed and loop denominators remain distinct; science guard-wall and filtered worker timings are missing. These are not GPU-kernel-only rates. <a href="/model-training-journal/assets/charts/training-throughput.svg">Open full-size throughput chart</a>.</figcaption>
</figure>

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/checkpoint-overhead.svg" alt="Measured checkpoint and evaluation hook times as stacked percentages of each completed run's training-loop time">
<figcaption>Checkpoint and evaluation hooks divided by each matching measured loop: totals approximately 1.330%, 1.391%, 0.989% and 1.923%. The 10% line is an engineering reference ceiling; reserved campaign charges are not hook measurements. <a href="/model-training-journal/assets/charts/checkpoint-overhead.svg">Open full-size overhead chart</a>.</figcaption>
</figure>

## Catching up the completed phases

Three larger phases then completed **104,521,471 valid labels** of scientific prose, **96,012,838** in a filtered continuation and **143,221,104** in a Wiki/Stack expansion. Recorded terminal CFR perplexities were 210.2344, 70.6064 and 51.4214 under their historical contracts. Phase exposures are not unique-corpus sizes or reasoning scores.

The completed stage added **130,072,908 valid labels**, **130,351,104 processed input IDs** and **3,978 optimizer updates**, without wrapping. Terminal checks confirmed successful exit, no surviving worker group, six verified checkpoint pairs and closed checkpoint storage. Next comes the disjoint source suffix.

## Six measured checkpoints

The pinned measure scores **7,057 labels** from 32 US administrative-regulation sections. Negative log-likelihood is in nats; perplexity is its exponential. Current hooks score the training model in memory, serially between steps, restoring random state.

| Completed-stage checkpoint | New valid labels in this stage | NLL, nats/label | Perplexity |
|---|----|----|----|
| Loaded parent baseline | 0 | 3.940053857 | 51.421370619 |
| Update 664 | 21,711,180 | 3.879315766 | 48.391092904 |
| Update 1,327 | 43,390,209 | 3.887361673 | 48.782013703 |
| Update 1,990 | 65,068,981 | 3.851337527 | 47.055959798 |
| Update 2,653 | 86,747,823 | 3.808637844 | 45.088978801 |
| Update 3,316 | 108,426,760 | 3.825988363 | 45.878122205 |
| Terminal update 3,978 | 130,072,908 | 3.779088629 | 43.776127274 |

Stage one includes two local increases; its baseline reobserves an existing checkpoint.

The guard's wall time was approximately **7 hours 6 minutes**. The worker measured **25,395.229 seconds**; its training loop measured **25,338.614 seconds**. Checkpoint and evaluation hooks together used **1.9226747%** of that loop. Whole-run timers and reserved budgets are distinct from kernel throughput and measured hooks.

The [checkpoint history JSON](/model-training-journal/assets/checkpoint-history.json), <a href="/model-training-journal/assets/checkpoint-history.txt" download="checkpoints.csv">checkpoint CSV</a> and [run-timing download](/model-training-journal/assets/training-throughput.txt) preserve the measured populations and accounting clocks. Broad-panel results are a separate series and must not be joined to the CFR curve.

## The running stage: saved evidence only

The second stage started at **12:40:54 UTC**, targeting **130,105,270 valid labels** and **3,979 updates** under a finite **10-hour guard**. At the 16:31 observation, its guard remained active with no reported resource stop; sampled GPU activity was 88% and temperature 62°C.

| Running-stage saved checkpoint | New valid labels in this stage | NLL, nats/label | Perplexity |
|---|----|----|----|
| Loaded parent baseline | 0 | 3.779088629 | 43.776127274 |
| Update 664 | 21,711,322 | 3.740508296 | 42.119393839 |
| Update 1,327 | 43,390,057 | 3.729114554 | 41.642219879 |
| Update 1,990 | 65,068,850 | 3.750515592 | 42.543011193 |

Saved update 1,990 regressed from 1,327 (perplexity 41.6422 to 42.5430), while remaining below the parent’s 43.7761. It records physical 570,445,650 labels/17,441 updates versus retained model lineage 567,787,256/17,360. These are saved counters, not live progress or completion. New broad-panel and reasoning outcomes are `not_evaluated`, with null metrics. Historical fixed32 results were 0/32 correct and 0/32 protocol-valid: a reused development diagnostic with interface failure, not isolated capacity or fresh final evidence. A bounded broader-LM and fixed-logic/protocol check is being prepared for this stage’s terminal checkpoint; it remains unrun, and source eligibility must be verified before use.

## Counting the remaining finite program

Physical campaign charges and retained model lineage remain separate. An earlier restore replayed charged work, leaving a persistent gap of **2,658,394 valid labels and 81 updates**; those charges are not refunded. Documents, content IDs, processed inputs and label exposures are distinct.

Two locally admitted, cached cohorts have **268,840 documents / 222,892,775 valid labels** and **269,543 documents / 215,100,897 valid labels**. No download is needed. The final cohort uses its largest contiguous full-update prefix: **126,366,365 labels**, leaving **88,734,532** unused. If intervening stages complete, the forecast is **984,741,210 consumed plus 15,240,080 failed reserved = 999,981,290 charged labels**. This is a forecast; parent, transfer and ingress gates remain unresolved.

Filtered Common Pile Wiki/Stack cohorts retain pinned provenance, attribution, deduplication, family/development exclusions and rights/privacy holds. An earlier overlap-check batch with an unresolved outcome remains excluded, not claimed scanned or cleared. Bounded quality review is not universal rights/privacy certification.

The **800GB data allowance**, root/free-space, memory and thermal guards remain unchanged. The installed execution cutoff remains **31 October at 04:12 UTC**; the expired UI stays stopped. Original 97M controls, failures and sealed final holdout remain preserved. This AI-assisted journal reports aggregate evidence. An open reproducible recipe remains a goal; code and weights are not claimed released.
