---
title: "Testing whether varied training years improve date transfer"
date: "2026-10-26"
slug: "year-diversity-experiment"
phase: "Experiment"
summary: "A matched supervised-training experiment varies years while preserving token counts and conversation order. Fresh year diagnostics are frozen before training."
order: 23
---

At **11:22 UTC on 26 October 2026**, preparation completed for a focused response to the [paired date failures](/model-training-journal/2026/10/26/paired-transfer-probe-results/). The hypothesis was that supervision using only 2028 encouraged familiar-year output instead of conditioning on the requested date.

This was another supervised-training experiment on the same **97,536,768-parameter** base. It was not additional language pretraining or a larger model.

## Change years without silently changing the training budget

The intervention changed years in the same 3,000 owned CC0 training conversations. Of 2,000 dated records, 667 used 2028, 667 used 2032, and 666 used 2036. The other 1,000 records stayed byte-identical. Both the candidate and its canonical comparison started afresh from the preserved 100M-token base, with fresh optimizers.

Model, tokenizer, seed, ordering, context, optimizer, and nominal two-million-label schedule remained fixed. An initial 2024 candidate was rejected before freezing because its BPE encoding changed the length.

The selected transformation passed checks for date meaning, inverse transformation, unchanged non-date values and permissions, and replay of saved tool histories. All **3,000 full-conversation token counts and assistant-label counts matched** their canonical parents. No record was filtered or truncated. The corpus retained **444,537 assistant labels per unique pass**; its longest complete conversation was 995 tokens within the 1,536-token context.

Matching token counts reduces one confound. It does not establish that year substitution has no other effect, or that a single-seed result represents the general effect of augmentation.

## Freeze a fresh diagnostic first

The new diagnostic contained **48 cases**: 16 anchors, each with a 2028 control and otherwise transformed 2000 and 2044 versions. It covered scheduling, stale writes, existing-task repair, and creation followed by correction. Both the prior canonical checkpoint and the new checkpoint would receive the same cases.

Overlap checks covered prompts, states, goals, and histories, including changes concealed by renaming identifiers or substituting years. These remained development-informed cases in known grammar, not the reserved final evaluation. Held-out year strings could also have different BPE lengths; those counts were recorded.

Separate fixed-64 diagnostics were planned for fit to the transformed training examples and retention of their original forms. Protocol validity, requested outcomes, and false completion claims would remain distinct measurements.

## A finite launch

The bounded training run began at **11:35:50 UTC**. Exact preparation specified **1,999,982 assistant labels in 13,509 optimizer steps**, leaving 18 nominal labels unused at a whole-conversation boundary. The trainer limit was 3,600 seconds, enclosed by a 3,780-second guard and the unchanged absolute deadline of **31 October 2026 at 04:12 UTC**.

This launch record establishes the method and budget, not its effectiveness. The [completed year-diversity results](/model-training-journal/2026/10/26/year-diversity-results/) record the outcome. No external teacher, new source text, or third-party model weights were added.

This AI-assisted summary was checked against the frozen training manifest, diagnostic metadata, measured budget, and preparation and launch records.
