---
title: "Making the planning comparison fair"
date: "2026-10-26"
slug: "making-the-planning-comparison-fair"
phase: "Evaluation"
summary: "Exact supervised budgets, a stronger symbolic reference, a separate policy check, and a corrected context reserve prepare a comparison of random and base-trained weights."
order: 8
---

While the base model continued training on 26 October 2026, CPU preparation checked what the later planning comparison would measure. This is a historical preparation record: **no learned-model development or final evaluation had run at this stage**.

## Match the exposure, not just the requested budget

The two supervised branches would share architecture, tokenizer, conversations, seed, ordering, and optimization settings. Only their starting weights would differ: random initialization versus the verified base checkpoint. Both would reset optimizer and scheduler state.

The random-weight control still shares the corpus-trained tokenizer. This isolates weight pretraining, not every form of prior textual exposure.

| CPU budget calculation | Result |
|---|---|
| Complete training conversations | 946 |
| Assistant labels per unique pass | 149,365 |
| Requested label budget | 2,000,000 |
| Expected complete-conversation exposure | 1,999,931 labels |
| Expected optimizer steps | 12,672 |
| Unused budget | 69 labels |

The expected exposure is about 13.39 passes. Actual counts and stream positions must match before interpreting the branches; these calculations were not completed training results.

## Add a meaningful symbolic reference

The earlier phrase policy's 0/80 development result was insufficient as the sole symbolic comparator. A separate reference planner parses supported public constraints, reads mock tool state, and computes intervals with an independently tested solver. It receives no scenario identifiers, hidden initial-state object, or oracle answers.

The recorded reference achieved **80/80 development successes in each of raw and guarded modes**, with **160/160 valid tool actions per mode**. Its parser was deliberately developed using training and development language. The result shows that the supported development tasks can be executed; it is **not unseen-language generalization**.

The independent review records 21 reference-test passes, including 300 comparisons against a separate brute-force interval solver. Training calibration was a different population: **1,156/1,200**, retaining 44 acknowledgment-grounding proxy failures. No human ratings were performed.

## Keep consistency and policy checks separate from performance

A static validator found **80/80 development cases consistent**. Its training audit reported **1,178/1,200 supported passes and 22 unverified cases**, whose natural-language restrictions exceeded its parser. “Unverified” did not mean impossible or passed. This checker can inspect expected constraints, so it is neither model input nor an agent-performance baseline.

Review also found that the original end-state scorer could accept an authorized write without the preceding read required by the prompt. A separate transcript-policy report now measures that condition without changing the original scores. The raw reference report recorded zero violations among 80 write attempts. This checks a preceding successful read in the same collection, not freshness or arbitrary natural-language authorization.

## Correct the context reserve before observing model results

A 128-token reply reservation would reject **20/80 successful reference trajectories per mode**, although their complete conversations fit. Exact counting found a maximum prefix of 923 tokens and maximum full conversation of 976.

The shared reply cap became **96 tokens**: 923 + 96 = 1,019, within the 1,024-token context. The policy was selected before learned-model evaluation and applied to both branches and execution modes. No input was truncated, no JSON repaired, and no scenario weakened. Longer model-generated histories could still exceed the context bound.

The [next entry](/model-training-journal/2026/10/26/queueing-the-matched-comparison/) records how these conditions were incorporated into the bounded comparison. This AI-assisted summary preserves the distinction between preparation, symbolic calibration, and future model results.
