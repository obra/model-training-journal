---
title: "Repairing tool serialization before the next run"
date: "2026-10-26"
slug: "serialization-repair-and-launch-blocker"
phase: "Engineering"
summary: "A separate training derivative aligns tool-message representation with the runtime. Stronger date and outcome audits qualify the earlier proxy scores before more compute."
order: 17
---

At **09:38 UTC on 26 October 2026**, the next finite experiment was prepared but had not launched. The completed work was a verified training-data correction and stronger measurement—not a new model result. The [subsequent launch record](/model-training-journal/2026/10/26/canonical-serialization-experiment/) describes the later run.

## Isolate the representation change

The earlier pilot exposed a discrepancy between stored training tool messages and runtime tool messages. Their JSON values matched, but object-key order differed. In one same-checkpoint probe, semantically identical 501-token prefixes produced different scheduling answers: the training representation produced the correct interval and the runtime representation did not.

The correction is a **new, separate derivative** of the same owned CC0 conversations. It replays the stored assistant outputs against saved and reloaded training scenarios. All **3,000 conversations** passed exact saved-history, assistant-byte-identity, semantic tool-value and actual-tokenizer checks; none were rejected.

Only tool key order changed, in **875 messages across 750 conversations**. The example order and **444,537 assistant labels per unique pass** remained unchanged. No external teacher, corpus or pretrained weights were added. This isolates an avoidable input-format inconsistency without rewriting earlier results.

## Correct the measurement before interpreting gains

A supplemental suggestion/date audit recorded 58 focused and related test passes and re-examined the four completed new-development reports. In each broader-model mode, all eleven original proxy passes had wrong requested dates, nine had wrong durations and one interval ran backward.

The auditor uses information visible before each output. It does not apply a future clarification answer or withdrawal that the model never received. Unsupported language and missing evidence remain unknown. These checks qualify the old metric; they do not create a replacement global “success” score or certify general safety.

## Match the next run

The prepared serialization experiment retained the earlier broader arm's exact configuration, model, tokenizer, seed, context 1,536 and learning-rate schedule. It would start afresh from the same preserved base with a fresh optimizer. Whole-conversation preparation gave **499,839 labels in 3,368 steps**, leaving 161 labels unused under the 500K cap.

Four known-development evaluations and the same 64 training-fit IDs were planned. Final holdouts remained reserved. At this entry's cutoff, preparation established neither training completion nor improved planning.

This AI-assisted account was checked against the canonical manifest, matched budget, suggestion-audit evidence and implementation review. Data, transcripts and operational details remain outside the public copy.
