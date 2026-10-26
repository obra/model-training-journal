---
title: "More distinct supervision did not produce a better planning assistant"
date: "2026-10-26"
slug: "diversity-results-and-language-limits"
phase: "Results"
summary: "The matched diversity study finishes without a promoted checkpoint. Fresh examples improve one reused diagnostic but lose on the new set, training fit, and retained calendar behavior."
order: 29
---

The [diversity-versus-repetition study](/model-training-journal/2026/10/26/diversity-versus-repetition/) completed its evaluation queue at **16:36:52 UTC on 26 October 2026**. **Neither checkpoint was promoted.**

Both 97,536,768-parameter arms started from the same preserved 100M-token base with fresh optimizers. Each completed **13,338 steps and 1,999,822 assistant labels**. Replay used 100 repair anchors; fresh used 1,916. Canonical messages, per-step label counts, source positions, and learning-rate values matched. Input tokens differed by 328, and the shared shuffled order differed from the preceding experiment.

This study added owned programmatic supervision, not external text or language pretraining.

## New outcomes and fewer answers

The newly frozen diagnostic had **64 core cases and 32 stress cases**. Those populations share anchors and remain separate from the earlier binding diagnostic with its own 64 cases.

| New frozen diagnostic | Replay | Fresh |
|---|---|---|
| Exact requested states / strict successes | 28/96 | 26/96 |
| Core cases | 23/64 | 22/64 |
| Stress cases | 5/32 | 4/32 |
| False completion claims | 51 | 33 |
| Missing final answers | 17 | 37 |
| Applied wrong-object writes | 40 | 24 |
| Cases with unresolved requested-state / wrong-object scope | 5 | 0 |

Raw and guarded histories were identical within each arm; they are correlated views, not independent replications. Both arms failed all eight create requests and all reserved-year and joint stress cases. Only one repair control succeeded in both arms, too little to support a broad comparison of conditional transfer rates.

Of replay's 51 false claims, fresh corrected 13, replaced 23 with missing answers, and retained 15. Fresh also turned 12 previously correct cases into false claims. Every missing-answer case in this new set left the complete state unchanged, but still left the request unfinished. Some missing answers in older suites followed silent wrong writes, so the new-set observation cannot be generalized to every evaluation.

The five unresolved replay cases made no state change, but the audit retained unknown binding because they never obtained the required pre-write read. Genuine receipts and zero mock operation-permission violations did not establish correct requested outcomes.

## Fit, retention, and reused diagnostics disagree

On source-specific actual-training samples, replay reproduced **50/50 exact histories** and fresh **26/50**. Each sample contained fifty distinct histories, but the arms did not receive identical prompts. These were training-fit checks, not holdouts or matched-input tests.

Fresh prefixes through the first successful read matched their references. Its first writes had correct operation, date, and version fields in all fifty cases, but the correct target identifier in only 28.

On the common retained 64 cases, exact histories were **46/64 versus 44/64**, and correct calendar bookings were **9/23 versus 6/23**. Fresh lost three bookings and gained none. All 31 noncalendar histories stayed exact in both arms.

The **reused binding-development 64 cases** improved from **3/64 to 19/64** exact outcomes. That is a real result on those familiar diagnostic inputs, not the new 96-case result. The older structural and broader development sets still produced no correct requested plans, while the separate paired 80-case diagnostic declined from **44/80 to 40/80** exact states. These denominators must not be pooled into a synthetic success score.

## Readable output is not reliable conversation

Saved supervised output includes readable, template-like English alongside wrong intervals, wrong-object changes, and false completion claims. This text within the planning protocol does not establish open-ended chat competence or human-rated quality.

At this milestone, a frozen base-language probe was prepared but not yet measured. The next bounded failure-reflection diagnostic would treat the model's explanations as hypotheses to test, not privileged evidence of why it failed.

## The next plan is conditional on new data

The recorded direction is to stop serial narrow supervision variants and investigate broader base training at the **same model size**. The original base remains a control; any continued base would receive the same fixed conversational-supervision recipe for comparison.

The proposed ceiling is **200M additional training labels**, conditional on audited rights, provenance, overlap, and actual new-token yield. The full run calls for at least 100M eligible new unique tokens across both proposed source families, with at most two passes per document. A 50–100M-token yield would shrink the target; below 50M, the plan reports a data bottleneck instead of filling the budget with the old corpus. Candidate sources are not admitted data.

The original 100M exposures came from about 26.91M corpus tokens, and language-validation overlap risk remains. These results establish neither a parameter-capacity ceiling nor a reason to promise a 1B-parameter run. The final planning holdout remains excluded from training and unevaluated. See the [dated current plan](/model-training-journal/current-plan/) for subsequent verified status.

This AI-assisted account was checked against the notebook, training milestone, and independent outcome reviews. Raw transcripts, source text, and private runtime details are excluded.
