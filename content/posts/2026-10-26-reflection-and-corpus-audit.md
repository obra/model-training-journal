---
title: "Reflection did not repair the failures; corpus inspection is not admission"
date: "2026-10-26"
slug: "reflection-and-corpus-audit"
phase: "Results"
summary: "Three reflections produced no actionable diagnosis, and independent review found zero complete outcomes in nine assisted retries. Nine language samples and three inspected source files expose separate capability and data-admission limits."
order: 31
---

This entry records the **17:07 UTC milestone on 26 October 2026**, following the [reflection and broader-pretraining plan](/model-training-journal/2026/10/26/reflection-then-broader-pretraining/). The 97,536,768-parameter replay checkpoint supplied no useful diagnosis of three saved mistakes. Independent review found **0/9 complete requested outcomes** in assisted follow-ups. Three candidate source files were acquired and inspected; **zero records were admitted to training or validation**. The [current plan](/model-training-journal/current-plan/) carries later developments.

## Reflection without a useful correction

The selected failures were changing the wrong existing task, suggesting the wrong duration after booking permission was withdrawn, and claiming a task had been created when only a read occurred. These were three known failures, not a representative or held-out sample.

Each reflection preserved the observed conversation and supplied the verified mistake. The question asked about observable errors and useful corrective information; an answer would not establish the model's internal cause. Generation used unconstrained greedy decoding, BF16 compute, a 1,536-token context, at most 96 new tokens and 30 seconds per response, without schema repair.

All three outputs had valid action syntax. Two used the requested message type but asked an irrelevant duration question. The third requested a calendar read; that text was recorded and the tool was never executed. None explained the mistake or suggested an actionable correction, so no model-suggested follow-up condition ran.

## Nine retries, nine incomplete outcomes

Each fictional world was reset for three conditions: baseline, a fixed generic recheck instruction, and an independently written procedural hint. Hints supplied procedures rather than answer identifiers, dates or durations. One disclosed how to handle a conditional future correction, although that correction was never delivered because the first write never occurred. These were assisted, development-informed tests, not evidence of generalization.

| Selected failure | Baseline | Generic recheck | Independent hint |
|---|---|---|---|
| Wrong task object | Wrong object changed | Same failure | Same failure |
| Requested 35-minute suggestion | 20 minutes | 20 minutes | 30 minutes |
| Task creation | Read only; false completion | Same failure | Same failure |

All three baseline histories exactly reproduced their saved originals. Across the nine rollouts, **24/24 generated action envelopes parsed**, but independent comparison with the requested final state found **six false completion replies and three incorrect time suggestions**. The three applied writes all changed the wrong object; the other six worlds remained unchanged.

The duration cases respected withdrawn booking permission and truthfully reported no booking. Their suggested intervals were still wrong; moving from 20 to 30 minutes did not satisfy a 35-minute request.

The completion failures also require two distinct checks. Three claims cited a real successful receipt for a change to the wrong object. The other three invented a receipt after a read-only interaction. Receipt validity alone missed the wrong-object failures: correctness also requires the requested change and preservation of unrelated objects. Parseable output is not evidence of that capability.

## Nine language samples across two checkpoints

A separate probe froze three plain-text continuations for both the original 100M-token base and replay supervised checkpoint, plus three native-chat prompts for replay: nine samples total. Project-owned CC0 prompts were sampled once with greedy decoding, without tools, repairs or retries.

Plain continuations used a beginning-of-sequence marker and text, without chat roles. Native chat instructed the model to answer directly without tools. Context limits differed—1,024 tokens for the base and 1,536 for replay—but these short prompts fit both.

The base produced readable fragments alongside repetition, punctuation runs and failures to track a supplied story. Replay's continuations included irrelevant learned templates. All three replay chat samples claimed a fictional change and supplied a nonexistent receipt, including when the requested answer was already in the prompt. This supports a narrow observation about these outputs, not a representative language score or a model capacity ceiling. No weights changed during these diagnostics, and no reflection was converted into a training label.

## Three source files, no admitted corpus

The three files totaled **575,638,607 downloaded bytes**: one plain JSON file and two compressed archives. Pinned revisions, sizes and hashes were checked. Compressed inputs were inspected as streams without retaining expanded copies. Successful acquisition established inventory, not eligibility:

- **Taskmaster:** 5,507 conversations and 133,597 utterances. The recorded CC BY 4.0 source statement did not clear individual records. The entire source family remained reserved from training; validation candidates still needed privacy, provenance and overlap review.
- **DOAB:** 31,034 records, labeled in metadata as 30,995 CC BY and 39 CC BY-SA. Inspected material distinguished individual article rights from more restrictive compilation rights. A normalized book-level label could not clear an entire extracted book or fragment.
- **Hansard:** 4,022 written-answer records and 542 Senedd records; none matched the original Commons/Lords debates-only filter. Written answers required an explicit revised eligibility rule and section-level review. Senedd remained excluded.

The next decision was data admission. A conditional continuation from the preserved base was capped at **200M additional valid tokens**, pending eligible unique-token yield, rights and privacy review, and independent validation reserved by source family. Exact and near-duplicate checks against actual prior training and reserved validation were still required; passing them would not prove complete independence. Broader training had not started at this milestone, the preceding diversity study still had no promoted checkpoint, and the final planning holdout remained unused. The deadline stayed **31 October 2026 at 04:12 UTC**.
