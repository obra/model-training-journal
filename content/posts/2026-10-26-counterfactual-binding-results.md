---
title: "More correct task fields, but more wrong-object writes"
date: "2026-10-26"
slug: "counterfactual-binding-results"
phase: "Results"
summary: "Varied task values improve nine of 64 requested outcomes versus three for repetition, but increase wrong-object writes and false claims. Neither checkpoint is promoted."
order: 27
---

Both training arms and all 18 evaluations completed by **14:25:53 UTC on 26 October 2026**. The [binding experiment](/model-training-journal/2026/10/26/binding-comparison-launch/) improved some fields and ordering behavior while worsening other outcomes. **Neither checkpoint was promoted.**

The 1,284 evaluated episodes included correlated raw/guarded views and related probes. They were not 1,284 independent tasks.

## Completed training, limited transfer

The repetition and varied-value arms started from the same preserved base. Both retained the canonical supervised data and added 500 repair rows, but had 3,100 and 3,500 distinct histories respectively.

| Training measurement | Repetition | Varied values |
|---|---|---|
| Completed assistant labels | 1,999,908 | 1,999,822 |
| Optimizer steps | 13,338 | 13,338 |
| Process wall time | 976.796 seconds | 977.160 seconds |

On the selected added-training sample, repetition reproduced 50/50 histories, representing only **ten distinct histories repeated five times**. Varied values reproduced 49/50 distinct histories. Both solved the ten shared controls. These were training-fit measurements, not generalization results.

## The fresh 64-case diagnostic

This diagnostic combined eight repair anchors with six variants each and eight create/update pairs. Its independent checker used visible requests and reads to verify requested state, preserved unrelated objects, intermediate actions, and claims.

| Per-mode result, 64 cases | Repetition | Varied values |
|---|---|---|
| Exact requested outcomes / strict successes | 3 | 9 |
| False completion claims | 28 | 40 |
| Cases with wrong-object applied writes | 21 | 29 |
| Unknown-wording final answers | 4 | 1 |
| Missing final answers | 29 | 14 |

Raw and guarded histories matched within each arm, so they are not independent replications. The runtime allowed the update operation globally, but applying it to the wrong object still violated the requested scope. Successful receipts did not establish successful requested actions.

Neither arm solved any of the eight repair controls. Conditional-transfer denominators were therefore zero, including their common-control intersection. Nine total successes must not be described as successful transfer from working repair controls.

The varied arm made progress on some date fields but more often selected a distractor object. Of its 40 false completions, 38 followed successful wrong-result writes and two followed rejected calls. Missing answers and unfamiliar noncompletion wording remained separate categories.

## Retention and regression checks change the interpretation

On the original 64 calibration examples, exact reference histories fell from **48/64** at canonical 2M to **42/64** for repetition and **40/64** for varied values. Correct calendar bookings fell from **9/23** to **4/23** and **2/23**. These were fresh-base mixed-data runs with reduced canonical exposure, so describing the change as forgetting during continuation would be misleading.

The original 80-case development set gave proxy passes of 9 and 10, but none represented a correct requested plan or task correction. The broader 80-case set gave ten proxy passes per arm, all invalid suggestions. Fewer false completions in that broader set were accompanied by unsupported failure explanations and more cases abandoning work; that is not demonstrated recovery.

On the distinct paired 80-case regression set, exact states rose from 39 to 42. Item-order transfer improved from 0/8 to 8/8, while year transfer fell from 4/5 to 0/5 and identifier transfer remained 0/8. False completions rose from 22 to 31. These populations cannot be pooled with the fresh 64 cases.

## Next decision: hold realized exposure fixed

The selected follow-up was [diversity versus repetition at matched exposure](/model-training-journal/2026/10/26/diversity-versus-repetition/): more distinct repair anchors while preserving actual canonical labels, tokens, and masks. Its decision rule would include missing answers and unsupported failure explanations alongside correct outcomes and damage.

The final holdout remained reserved. These fictional-world results establish neither a useful assistant nor broad safety. This AI-assisted account was checked against completed training records and independent outcome, fit, retention, and regression reviews.
