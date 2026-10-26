---
title: "The first 100 million base-training tokens"
date: "2026-10-26"
slug: "first-100m-token-base"
phase: "Base training"
summary: "The model completes 100 million valid training-token exposures and preserves a verified checkpoint. Language-model loss improves, while conversational transfer and validation independence remain separate questions."
order: 11
---

The **97,536,768-parameter model completed 100,000,000 valid training tokens at 06:41:47 UTC on 26 October 2026**. This includes the [two-million-token pilot](/model-training-journal/2026/10/26/first-real-text-gpu-run/) and its 98-million-token continuation. It is a base-training milestone, not a useful-assistant result or a release promotion.

The two recorded training invocations totaled **6,698.56 seconds**, about one hour and 51 minutes, excluding the pause between them. The continuation averaged **14,936 valid tokens per second**, including its initialization, validation, and checkpoint overhead.

The training inventory contained **26,908,211 raw tokens**. The cumulative budget therefore represents roughly 3.7 passes over that inventory, not 100 million distinct tokens. Loss masking makes raw inventory and valid training exposures slightly different quantities.

## Preserve the measurement populations

| Validation sample | Scored labels | Loss | Perplexity |
|---|---|---|---|
| Repeated prefix at the end of training | 65,536 | 4.02058 | 55.73 |
| Separate broader probe | 900,000 | 3.86067 | 47.50 |

The broader probe took **15.42 seconds**. It was a partial single pass without wraparound, consuming 902,144 of the 918,539 available raw validation tokens. It did not evaluate exactly the same sample as the repeated prefix.

On the repeated prefix, loss declined from 5.69779 at approximately seven million training tokens to 4.02058 at completion, with nonmonotonic intermediate readings retained. The different probe populations must not be joined into a single learning curve.

**Later context:** the [lexical overlap audit](/model-training-journal/2026/10/26/auditing-textbook-overlap/) found related content across the textbook split. These original scores remain recorded diagnostics; they are not demonstrably independent-work validation. Lower loss alone cannot establish planning transfer or justify further pretraining.

## Verify and preserve the base checkpoint

The final checkpoint records **12,227 optimizer steps**. Verification checked its checksum and sidecar, finite tensors, source/tokenizer/data lineage, and recoverable training state. Persistent model parameters and Adam moments were FP32; computation used BF16. A separate base snapshot preserved these weights for later branches.

An isolated supervised-training smoke test then completed 9,976 assistant labels in 66 steps. Its low minibatch loss was a machinery check, not a held-out behavioral score, and its weights were not used to initialize either matched branch.

At this historical stage, the next question was whether base training helped when both branches received the same fictional planning supervision. That required equal actual assistant-label budgets, separate raw and guarded evaluations, and examination of failed transcripts. The [first planning comparison](/model-training-journal/2026/10/26/first-planning-comparison/) records that outcome. No final behavioral holdout had been evaluated at this milestone.
