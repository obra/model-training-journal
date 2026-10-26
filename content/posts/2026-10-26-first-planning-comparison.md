---
title: "The first planning comparison failed"
date: "2026-10-26"
slug: "first-planning-comparison"
phase: "Comparison"
summary: "Both matched models fail all 80 development cases. Base training improves familiar training fit and protocol consistency, but neither result establishes a useful planning model."
order: 13
---

The first matched behavioral comparison completed on **26 October 2026**. Both 97,536,768-parameter models scored **0/80 development successes**, in both raw and runtime-guarded execution. Familiar training fit improved after base training, but that improvement did not transfer to this development suite. Neither checkpoint was promoted as a useful assistant.

## Match the training, separate the measurements

Both branches used the same fresh tokenizer, architecture, seed, optimizer settings, assistant-only loss mask, ordered stream, and 946 original CC0 conversations. One started from random weights; the other from the [preserved 100-million-token base](/model-training-journal/2026/10/26/first-100m-token-base/). Both optimizers were reset before supervision.

Each branch consumed exactly **1,999,931 assistant labels in 12,672 optimizer steps**. The random branch took 902.23 seconds; the base branch took 903.52 seconds. These rates count assistant labels, not general pretraining throughput.

The same frozen 80 development cases used greedy, unconstrained generation, a 96-token response limit, a 30-second response bound, and context length 1,024. There was no prompt truncation or JSON repair. The final behavioral holdouts remained unused.

| Development measurement | Random + SFT | Base + SFT |
|---|---|---|
| Raw end-state success | 0/80 | 0/80 |
| Guarded end-state success | 0/80 | 0/80 |
| Raw tool-schema validity | 40/46 | 80/80 |
| Corrected raw protocol validity | 97/103 | 160/160 |
| Verified unsupported completion messages, raw | 12 | 20 |

These are correlated generated cases, including twenty initiative cases that repeat one public request. No blind human ratings were collected. A development-informed symbolic reference solved 80/80; that is a comparator informed by this development distribution, not independent generalization evidence.

## Correct structure did not produce correct actions

The base branch created the initial task in all twenty correction cases, then mishandled the requested update: it reread current state, attempted another creation with a stale version and wrong time, and claimed completion after the failed write using an older receipt. It also asked unnecessary questions and stayed silent when a heads-up was requested.

The random branch produced malformed argument envelopes, selected unavailable tools, copied wrong values, and made unsupported completion claims. Review of all 160 raw development transcripts confirmed the automated completion flags and found no additional affirmative completion claims in that sample. This does not establish a general detection guarantee.

Review also uncovered a reporting defect: seventeen unexposed tool selections were counted twice in the random branch's action denominator. The historical **97/120** score is preserved. A separate audit counts each actual response once, yielding **97/103 protocol-valid responses**. End-state success remains unchanged; protocol validity does not imply correct tool choice or task completion.

## Training calibration answers a different question

A separate **64-case training calibration**, selected before model outcomes, gave random **14/64** successes and base **64/64**. It measures fit to familiar training conversations, not held-out transfer.

An inference-only teacher-forced check covered the same **8,988 assistant labels** per branch. Random's mean loss was **0.08929435**, with 213 incorrect labels; base's was **0.0000452332**, with none. A low final minibatch loss had hidden the aggregate training-fit difference.

Calibration also exposed the receipt checker's limits. Of random's 45 affirmative completion messages, six followed failed writes and were flagged; **38 more** followed successful writes to the wrong requested item, date, or time and escaped the checker. Only one matched the requested action. Review found no definite false completion among base's 45 claims, while retaining note-punctuation ambiguities. Those calibration findings are separate from the raw development counts above.

## Change supervision before extending pretraining

The next hypothesis was to vary supervision around constraints, corrections, current versions, permissions, and actual tool outcomes, with matched budgets and newly frozen probes. Textbook validation already had [documented overlap risk](/model-training-journal/2026/10/26/auditing-textbook-overlap/), so its loss did not independently justify more pretraining.

This AI-assisted summary was checked against the comparison record, protocol audit, transcript reviews, and training-calibration diagnostics. Raw transcripts, checkpoints, data, and private runtime details remain outside this publication.
