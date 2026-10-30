---
title: "V6 begins with a saved checkpoint, not a new quality score"
date: "2026-10-30"
slug: "v6-first-saved-checkpoint"
phase: "Finite continuation: checkpoint evidence"
summary: "V5 is complete. V6 has a first saved checkpoint after 7,487,125 valid labels; no new language or reasoning score has been measured."
order: 47
---

V5 completed **3,833 updates** and **125,320,085 valid next-token labels**. Its terminal **34.2885 perplexity** belongs to the fixed **7,057-label CFR development panel**. That measured result remains separate from the newly launched V6 continuation. The [V5 completion record](/model-training-journal/2026/10/30/a-second-completed-slice-and-v5-checkpoints/#ledger-correction-and-terminal-update) and [dashboard](/model-training-journal/dashboard/) retain its result and the earlier regressions.

V6 started at **20:44:02 UTC on 30 October 2026** from V5's terminal saved model. Its first new checkpoint was committed at **21:17:29.743755 UTC**, after **229 stage-local updates** and **7,487,125 stage-local valid labels**. The save is verified; **its perplexity has not been evaluated**. The checkpoint's SHA-256 is `29062fdc6cca6ef398d69f3eddd714ebd4145a80cf6afac7f2d4e96762c86d99`. A durable save establishes recoverable training progress, not model quality.

| Run | Evidence boundary | Stage-local completed updates | Stage-local valid labels | Quality status |
|---|---|---|---|---|
| V5 | terminal | 3,833 | 125,320,085 | CFR perplexity 34.2885 on 7,057 labels |
| V6 | saved checkpoint, 21:17:29.743755 UTC | 229 | 7,487,125 | Not evaluated |
| V6 | live ledger, 21:18:13 UTC | 236 | 7,716,009 | Not evaluated; live progress is not another saved checkpoint |

These are separate run-local clocks. Do not add a live ledger row to its earlier saved-checkpoint row: they describe successive states of the same run. The dashboard's new dated table preserves this distinction; historical score charts retain their original populations and boundaries. No line connects V5's measured perplexity to an invented V6 score.

The installed project cutoff is now **7 November 2026 at 04:12 UTC**, following a separately reviewed extension. V6 itself remains a finite run with an earlier guard ending **31 October 2026 at 02:44:02 UTC**. A later project cutoff does not authorize an indefinite run or establish completion of this slice.

**No new reasoning benchmark has run.** V6 has no new CFR, broader-panel, task, or reasoning score in this snapshot. BLiMP remains unrun, the earlier format diagnostic stopped before its trial, and the sealed final planning holdout remains untouched. The historical **0/32 correct and 0/32 protocol-valid** task result belongs to an earlier V3 checkpoint and includes an output-interface failure. Training progress does not change that result or prove transferable reasoning. This AI-assisted journal publishes reviewed aggregates and an evolving reproducible method; it does not redistribute training text or claim a model-weights release.
