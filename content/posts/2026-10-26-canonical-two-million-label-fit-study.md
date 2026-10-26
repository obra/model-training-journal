---
title: "Testing a longer optimization budget on canonical supervision"
date: "2026-10-26"
slug: "canonical-two-million-label-fit-study"
phase: "Experiment"
summary: "A fresh two-million-label run tests whether more optimization improves familiar-example fit. Exposure and schedule change together; no new development result is claimed at launch."
order: 20
---

This launch record is dated **10:10:39 UTC on 26 October 2026**. The new canonical run was underway; its [completed results](/model-training-journal/2026/10/26/canonical-2m-results/) are recorded separately.

The preceding serialization correction aligned training and runtime inputs but did not produce useful development planning. On the same 64 exposed training cases, only 34 complete histories were exact. All thirty first divergences were model outputs after matching prefixes. That incomplete fit motivated a bounded optimization study rather than a claim that low token loss was enough.

## Exposure and schedule change together

The run starts afresh from the same preserved 100M-token base. It retains the canonical 3,000-conversation corpus, tokenizer, architecture, context, seed, example order, precision and optimizer hyperparameters.

The nominal target increases from 500K to **two million assistant labels**, and the cosine-decay horizon increases with it. This is a **combined exposure-and-schedule intervention**, not a pure update-count experiment and not a continuation of the 500K optimizer.

Whole-conversation preparation gives **1,999,982 labels in 13,509 steps**, leaving eighteen labels unused. A unique pass still contains 444,537 labels, so the exposure is about 4.5 passes over the same data. No new corpus or external teacher is introduced.

## Bound the run and preserve the diagnostics

The trainer and enclosing job limits remain 3,600 and 3,780 seconds. Checkpoints are scheduled every 100K labels or 300 seconds, under the fixed project deadline of **31 October 2026 at 04:12 UTC**.

The finite queue evaluates the same two known development suites in raw and guarded modes, preserving separate protocol, requested-outcome, completion-claim and suggestion/date checks. The unchanged 64 training IDs support a subsequent fit diagnostic. Final holdouts remain reserved.

At **10:13 UTC**, the snapshot recorded 279,144 labels and a saved 200K checkpoint. Those interim counters establish execution, not a final outcome. The decision criterion is whether actual values, plans and claims improve alongside familiar-example fit; lower loss alone will not select a model.

This AI-assisted account was checked against the exact exposure budget, configuration, launch metadata and experiment handoff. Operational identities and raw logs are omitted.
