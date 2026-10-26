---
title: "Broader supervision exposes scoring and input-format limits"
date: "2026-10-26"
slug: "broader-supervision-pilot"
phase: "Experiment"
summary: "The finite paired pilot finishes, but its apparent development gains do not establish correct plans. Follow-up checks find incomplete fitting and a tool-serialization mismatch."
order: 16
---

This is the completed record of the pilot launched at **08:26 UTC on 26 October 2026**, with follow-up checks through 09:25. Both arms started independently from the same preserved 100M-token base, using the same 97,536,768-parameter model, tokenizer, seed, context 1,536 and optimizer configuration. Original versus broader supervision was the intervention.

## Completed exposure and separate populations

| Measurement | Original-data control | Broader supervision |
|---|---|---|
| Unique conversations | 946 | 3,000 |
| Assistant labels per unique pass | 149,365 | 444,537 |
| Completed assistant labels | 499,871 | 499,839 |
| Optimizer steps | 3,170 | 3,368 |
| Training wall time | 234.32 seconds | 246.67 seconds |

Both arms stopped at complete-conversation boundaries below the 500K cap. Wall times include initialization and checkpointing. Checkpoint verification recorded recoverable state and FP32 persistent parameters and Adam tensors, with BF16 computation.

All eight development evaluations completed. The original 80-case suite used context 1,024; the newer 80-case composition suite used 1,536. Both retained greedy unconstrained replies, a 96-token reply limit and no JSON repair or prompt truncation. Raw and guarded modes are separate views of these cases, not extra independent trials.

| Original accepted-state score | Control | Broader supervision |
|---|---|---|
| Original development, each mode | 2/80 | 10/80 |
| New development, each mode | 0/80 | 11/80 |

## Why these are not counts of correct plans

The control's two original-suite passes happen to request the twenty-minute interval it writes in every scheduling attempt. The broader model's ten original-suite passes are truthful unavailable-tool acknowledgments after incorrectly specified booking attempts. Ten other successful writes change the requested title and date, followed by false completion claims that receipt checks miss.

On the new suite, all eleven broader-model passes follow the revocation path without writing after the delivered withdrawal. Their no-booking statements are supported, but **all eleven suggested intervals use the wrong date**; nine also have wrong duration. The original checker rewards no-write, intent and clarification presence without checking the suggested interval. These are narrow procedural passes, not eleven valid plans.

Only three of those eleven questions ask for missing duration. The simulator supplies duration after any clarification, including eight questions about an already supplied window. Separate review also finds eleven false generic completions on the new suite. Manual-review counts include unfamiliar wording and absent answers; they are not extra fabrication counts. No human ratings or final-holdout results exist here.

## Training fit and a representation mismatch

Separate source-specific 64-case training samples produced 59/64 accepted outcomes for control and 38/64 for breadth. These are exposed training diagnostics, not matched test inputs or holdouts. Teacher forcing found 59/64 versus 35/64 completely correct conversations, with 45/8,988 versus 44/9,601 incorrect assistant labels. High label accuracy concealed consequential value errors.

For the broader sample, 28 full histories matched exactly, 25 first differed in assistant output, and 11 first differed in a tool response. Saving the scenario had reordered JSON object keys without changing values. Seventeen teacher histories contained some such difference, but only eleven had it before the model's first divergence; seventeen is not a causal failure count.

A bounded same-checkpoint probe used two 501-token prefixes with identical tool values. Training key order yielded the correct interval; runtime key order yielded an incorrect interval. That establishes sensitivity in one case, not a universal explanation.

## Next decision

A separate canonical derivative changed only tool-message key order, preserving all 3,000 conversations, their order and assistant targets. All passed saved-history, semantic-value and token-bound checks; zero were rejected. The next experiment would isolate this serialization change before increasing training duration.

The resource observer's GPU memory counters were unavailable; no zero-memory or training-peak claim is supported. This AI-assisted summary was checked against paired budgets, separated development metrics, fit reports and independent reviews. [The repair record](/model-training-journal/2026/10/26/serialization-repair-and-launch-blocker/) explains the next controlled step.
