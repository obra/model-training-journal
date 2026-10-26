---
title: "Testing more distinct examples at matched training exposure"
date: "2026-10-26"
slug: "diversity-versus-repetition"
phase: "Experiment"
summary: "A new study matches realized assistant-label exposure while varying repair-anchor diversity. Both finite training arms finish; evaluation remains a separate decision gate."
order: 28
---

The new training data froze at **15:04:57 UTC on 26 October 2026**. The hypothesis followed the [binding study's mixed results](/model-training-journal/2026/10/26/counterfactual-binding-results/): if selected repairs fit but unfamiliar targets fail, more distinct anchors might help—provided canonical exposure stays fixed.

This entry records preparation, launch, and the verified **15:58 UTC training milestone**. Later evaluation status belongs on the [dated current-plan page](/model-training-journal/current-plan/); completed training is not a capability result.

## Match what the trainer actually consumes

Both arms began independently from the same self-trained 97.5M-parameter base, with the same tokenizer, grammar, optimizer, and 1,536-token context. Each materialized file represented one finite pass of **13,338 conversation occurrences and 1,999,822 assistant labels**.

The 11,422 canonical occurrences had identical messages, tokens, and masks. Corresponding assistant-label counts matched at every position, preserving cumulative-label and learning-rate schedules.

| Frozen quantity | Replay | Fresh anchors |
|---|---|---|
| Repair occurrences | 1,916 | 1,916 |
| Distinct repair histories | 500 | 1,916 |
| Distinct repair anchors | 100 | 1,916 |
| Distinct histories overall | 3,500 | 4,916 |
| Input tokens in the full pass | 8,047,747 | 8,048,075 |

The fresh arm used a separately generated anchor at each repair occurrence, matched to its label count and factor recipe. This changed anchor diversity and within-anchor repetition together. Length-based rejection also conditioned the accepted values, and input-token totals differed by 328. The shared new permutation differed from the earlier experiment's training order. This is a declared package of changes, not a universal causal test of diversity alone.

All added text was recorded as owned CC0 material. No new external corpus, teacher, or third-party weights were introduced.

## Freeze separate evaluation populations

The new suite contained **64 core cases and 32 stress cases**. Core combined familiar supervised atoms in new combinations. Stress changed identifiers, years, joint factors, or language forms; “unseen” referred to audited supervised exposure, not to the earlier base pretraining.

Each arm also had a fixed 50-record sample containing fifty distinct actual-training histories. These were different source-specific fit populations, not matched conversations. Previous calibration and development sets remained disclosed regression diagnostics. Raw/guarded views and shared anchors were correlated. The final behavioral holdout remained excluded from training and unevaluated.

The joint decision rule requires more correct requested outcomes without increased wrong-object damage, false completions, unsupported failure explanations, or worse retained behavior. Missing and unknown answers stay visible: inaction cannot win merely by reducing false claims.

## A reader failure, then finite training

Preparation initially stopped because an older 32 MiB reader rejected the roughly 40.75 MB training files. The repair applied the already planned 256 MiB bound only to the two declared inputs, retaining checks against symlinks, oversized files, and replacement. Frozen data and deadline guards stayed unchanged. Repaired preflight passed before launch at **15:21:40 UTC**.

The saved milestone verifies that replay finished at **15:39:16 UTC** and fresh anchors at **15:55:56 UTC**. Each completed exactly **1,999,822 labels in 13,338 steps**, with one pass and no wrap. Total completed supervised exposure was **3,999,644 labels**: a count of supervised-token exposures, not distinct examples.

At **15:58:11 UTC**, both checkpoints were verified and evaluation was ongoing. No planning checkpoint had been promoted. The absolute project deadline remained **31 October 2026 at 04:12 UTC**. This AI-assisted account was checked against the frozen manifest, preflight repair, exact exposure accounting, and completed-training milestone.
