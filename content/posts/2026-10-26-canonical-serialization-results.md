---
title: "Canonical serialization leaves planning failures unresolved"
date: "2026-10-26"
slug: "canonical-serialization-results"
phase: "Results"
summary: "Aligned training and runtime histories remove a measurement confound, but the canonical 500K run still fails to produce reliable plans. Familiar-example fit and development behavior are reported separately."
order: 19
---

The canonical 500K-label training and development pipeline completed at **09:57:23 UTC on 26 October 2026**; the fixed training diagnostic finished at 10:00:59. Matching tool-message representation removed a known input mismatch. It did not produce reliable planning.

## What completed

The run used the same 3,000 owned conversations, assistant targets, order, tokenizer, model, seed, schedule and configuration as the earlier broader pilot. Only tool-message serialization changed. Supervised training started afresh from the preserved 100M-token base with a fresh optimizer.

Training completed **499,839 assistant labels in 3,368 steps**, taking **246.5126 seconds**, about 2,028 labels per second including checkpoint overhead. This is roughly 1.12 exposures per unique-pass label inventory, not newly acquired data.

## Familiar-example fit after alignment

The same 64 training conversations were reused without resampling.

| Training diagnostic | Canonical 500K |
|---|---|
| Original accepted-state outcomes | 38/64 |
| Exact complete message histories | 34/64 |
| Teacher-forced conversations with every label correct | 34/64 |
| Incorrect teacher-forced labels | 43/9,601 |
| Mean assistant-label loss | 0.0130682 |

All thirty nonexact histories first diverged in assistant output; none first diverged in the environment representation. The earlier 38/64 score had the same total but a tool-prefix confound. That confound is removed here, making incomplete fit on familiar examples clearer.

Four accepted cases still suggest the wrong duration without booking. They are valid no-write statements, not four correct plans. All 23 sampled calendar cases fail. One task correction improves while one grounded item reference regresses. These exposed training cases are not a holdout.

## Development scores still reward the wrong things

Raw and guarded modes each produced **12/80 accepted states on the original development suite** and **11/80 on the newer compositions**. The original suite retains context 1,024; the newer suite uses 1,536. Neither is a fresh holdout.

The original-suite increase from ten to twelve passes does not establish planning improvement. The two added passes assert a tool failure without calling the tool. Reviewed false completion claims rise from **10 to 25**. No correct scheduled event, completed task correction or requested proactive heads-up is demonstrated.

The same eleven revocation-path cases pass the newer suite's original checker, but **all eleven suggestions are invalid**. Two have impossible months; every parseable interval has a wrong date and duration. Relevant missing-duration questions improve from three to seven, and output protocol validity improves, while false generic completions rise **11→20**. Nine additional tool-failure explanations follow successful reads only and have no supporting failure observation. Better syntax coexists with worse factual output.

## What the result changes

The next selected experiment was a fresh **two-million-label canonical run** to test a longer optimization budget. Its longer target also changes the cosine-decay horizon, so it cannot isolate update count alone or be described as continuing the current optimizer.

The passive observer's maximum readings are sampled device-wide observations, not process-isolated or guaranteed whole-run peaks. Final holdouts remained reserved, and further language pretraining stayed deferred pending independent validation.

This AI-assisted account was checked against exact budgets, fixed-64 reports, independent behavior and claim reviews, and resource observations. [The longer-fit study](/model-training-journal/2026/10/26/canonical-two-million-label-fit-study/) records the next intervention.
