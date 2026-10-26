---
title: "A 120-hour plan for a small conversational model"
date: "2026-10-26"
slug: "autonomous-mission-and-120-hour-budget"
phase: "Planning"
summary: "A fixed five-day experiment proposes a fresh tokenizer, roughly 100 million base-training tokens, and separate tests of model behavior and guarded tool use. These are plans and release goals, not results."
order: 3
---

The [first GPU diagnostic](/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/) established that a 97.5-million-parameter model could execute a bounded training workload and pass mechanical correctness checks. The next question was more demanding: could a small model trained from random initialization become useful at a narrow set of conversational planning tasks?

This entry records the plan as of **04:20 UTC on 26 October 2026**. No production-length training run had launched. Production evaluation had not run, no production checkpoint was recorded, and production-token throughput was unknown. The diagnostic result was not evidence of conversational competence.

## A fixed experimental window

The program had a **120-hour wall-clock budget**, from **26 October 2026 at 04:12 UTC** to **31 October 2026 at 04:12 UTC**. Interruptions or disconnected sessions would not extend the deadline.

Before a long run, the plan called for testing a deadline safeguard and a finite-job supervisor. Where feasible, the system would save an atomic checkpoint before stopping the experiment's registered processes at the absolute deadline. This was a requirement to implement and test, not a completed capability at this snapshot.

The objective was the smallest useful experimental model for conversational planning, calibrated initiative, grounded acknowledgment, and respectful disagreement. Tool interactions would involve **fictional calendars, tasks, and notes**. A scientifically useful negative result was an acceptable outcome; the five-day window did not imply that a useful assistant would emerge.

## Define success before tuning behavior

The proposed narrow-domain release criteria were:

| Proposed criterion | Target |
|---|---|
| Task end-state success | At least 80% |
| Raw tool-call syntax validity | At least 95% |
| Unauthorized mock actions observed in release tests | Zero |
| Fabricated completion claims observed in release tests | Zero |

These were **evaluation goals, not measured scores**. No evaluation counts or uncertainty estimates were available in this planning record. “Zero observed” would describe a finite test result, not prove that a model could never make the error.

The plan called for development scenarios and a separately frozen final evaluation set before behavior tuning. Test counts and uncertainty would accompany the eventual results. Human conversational ratings would be reported only if they were actually collected.

## Separate the model from its guardrails

Two evaluation views were planned: raw model behavior and behavior behind a guard that controlled mock tool actions. Keeping them separate would make it possible to see whether the model itself produced valid, appropriate actions or whether the surrounding system prevented mistakes.

The planned comparisons were a randomly initialized model followed by supervised fine-tuning, a model given base training before supervised fine-tuning, and a scripted baseline. These comparisons had not yet produced results. They were intended to test whether base training added useful behavior and whether a learned model offered an advantage over a simpler scripted approach.

## Data and tokenizer work came first

Marin's catalog and pinned recipes were the proposed starting pool for source selection. Each selected upstream source and document still required a rights and provenance review. Permission to train and permission to redistribute would be recorded separately; inclusion in a catalog alone would not settle either question.

A fresh **16K BPE tokenizer** was planned to replace the temporary byte mapping used in the diagnostic. The first finite base-training target was approximately **100 million tokens**. Learning curves and evaluation evidence would inform later allocation within the same deadline.

The diagnostic's byte-token rate could not be treated as production-token throughput. A trained tokenizer changes the unit being counted, and production data processing, checkpointing, and evaluation add work that the short diagnostic did not measure.

## What remained untested

At this snapshot, the next steps were to test the deadline safeguard, freeze the final evaluation, audit the first corpus tranche, and prepare a resumable trainer. Useful conversational behavior, raw tool-call reliability, guarded task success, and the proposed release thresholds were all still untested.

This AI-assisted journal entry is a sanitized account of that planning state. It publishes no training data or third-party text excerpts. Later results must be read as evidence against this plan, not inferred from its ambitions.
