---
title: "Varied training years did not produce date transfer"
date: "2026-10-26"
slug: "year-diversity-results"
phase: "Results"
summary: "The year-diversity candidate still fails unseen years and loses retained behavior. Valid tool syntax and some improved date fields do not justify promotion."
order: 24
---

The year-diversity training and main development queue completed at **12:08 UTC on 26 October 2026**; the separate fit and retention checks completed at **12:13 UTC**. **The candidate was not promoted.**

The [matched intervention](/model-training-journal/2026/10/26/year-diversity-experiment/) varied supervised years while keeping the model, tokenizer, seed, ordered conversations, and optimization schedule fixed. It completed **1,999,982 assistant labels in 13,509 steps**, taking **976.672 seconds**, or about **2,047.75 labels/second** including process overhead.

## Fresh years remain unsolved

The 48-case diagnostic contained 16 anchors at three years each. These cases were frozen before training, but used known grammar and related anchors. They were not the final behavioral holdout.

| Fresh 48-case diagnostic | Canonical 2M | Varied years |
|---|---|---|
| Exact requested states | 10/48 | 8/48 |
| Successful 2028 controls | 10/16 | 8/16 |
| Transfer to 2000 among successful controls | 0/10 | 0/8 |
| Transfer to 2044 among successful controls | 0/10 | 0/8 |
| False generic completion claims | 38/48 | 40/48 |

On the **eight controls both checkpoints solved**, each scored zero successes for either unseen year. The varied-year checkpoint used 2032 in 29 of its 32 unseen-year targets and 2036 in the other three, never the requested 2000 or 2044. This is consistent with a preference for supervised years, not proof of an internal mechanism.

Some fields improved while full outcomes worsened. Unseen-year task month/day matches rose from 5/16 to 16/16. Calendar earliest-start matches on the 2028 controls rose from 4/8 to 8/8, while duration matches fell from 2/8 to zero. Two previously correct calendar controls were lost. Both models nevertheless produced valid protocol envelopes throughout this diagnostic.

## Other populations expose different problems

On the **original 80 development cases**, raw and guarded execution each scored 0/80. On the **broader 80-case set**, both retained ten proxy passes, but all ten suggested plans were invalid. The varied-year model also overwrote unrelated tasks in all twenty relative-task cases. False generic completions on that broader set rose from 12 to 25 despite zero original receipt flags. Real API receipts did not establish correct requested outcomes.

These raw and guarded histories were identical within the experiment; they are correlated views, not independent replications. The fresh 48-case scores and the two 80-case development scores must not be pooled.

## Training fit and retention also deteriorate

The fixed-64 checks distinguished transformed training examples from their original forms. Neither population was a holdout.

| Fixed-64 measure | Canonical 2M | Varied-year fit | Original-form retention |
|---|---|---|---|
| Exact reference histories | 48/64 | 42/64 | 42/64 |
| Wrong teacher-forced labels, out of 9,601 | 18 | 29 | 31 |
| Correct calendar bookings | 9/23 | 5/23 | 5/23 |

All 22 nonexact histories in each new cohort first diverged at an assistant output, with no preceding environment mismatch. Small label-error totals still produced consequential wrong arguments. Equal aggregate fit and retention counts also concealed different successful cases.

The next selected direction was [input-to-action binding with a repetition control](/model-training-journal/2026/10/26/contrastive-binding-plan/), rather than more year-only cycles or model growth. Further language pretraining remained deferred because independently sourced validation was still needed. The final holdout remained unevaluated, and these fictional-world checks supplied no human conversational rating.

This AI-assisted account was checked against the requested-outcome audit, independent development reviews, and completed fit/retention summary.
