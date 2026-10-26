---
title: "Reflect on saved failures, then test broader pretraining"
date: "2026-10-26"
slug: "reflection-then-broader-pretraining"
phase: "Planning"
summary: "A bounded reflection diagnostic will test possible repairs to three saved failures before a conditional comparison of broader base training. Neither intervention has results at this planning milestone."
order: 30
---

After the [completed diversity study](/model-training-journal/2026/10/26/diversity-results-and-language-limits/), the next sequence recorded on **26 October 2026** was a short failure-reflection diagnostic followed by a broader-pretraining comparison. At this entry, the prior evaluation queue was complete and the reflection implementation was being checked. No reflection result, broader download, or additional pretraining run was yet claimed.

The sequence tests two different possibilities: whether explicit feedback and instructions can repair selected failures, and whether a broader language foundation can improve later supervised behavior. Neither is a promise that the model will become a useful assistant.

## Three saved failures, with controlled feedback

The initial diagnostic selects three observed mistakes: updating the wrong task, suggesting a 20-minute interval when 35 minutes were requested after permission withdrawal, and claiming completion without a write.

Each reflection will preserve the history actually delivered to the model, including tool results. Later corrections that were never delivered during the failed rollout remain hidden. When a reflection prompt identifies an error, that feedback is additional supplied information; the model has not independently discovered it.

The model will be asked why its answer might be wrong and what information or instruction could help. Its explanation may be incoherent or a plausible rationalization. An explanation alone is not evidence of the internal cause of the mistake, and unsupported rationalizations will not become training targets.

The three short reflections will be followed by bounded checks on the same cases: the original baseline, generic rechecking, independent procedural instructions, and model-suggested changes only when the model supplies a coherent, actionable suggestion. Raw output, protocol validity, correct requested outcomes, and unsupported completion claims will be recorded separately.

An intervention that supplies the answer is a correction test. Success there would not establish transfer to fresh cases. Fresh evaluations and the final holdout remain reserved. The combined initial diagnostic has a **900-second guarded budget and no training step**.

## Preserve the original base as a control

The next proposed training comparison keeps the **97.5M-parameter architecture**. It would compare the preserved base trained on 100M token exposures with a separate continuation on **up to 200M additional token exposures** of broader, audited text. Both base checkpoints would then receive identical conversational supervision and fixed task evaluation.

This preserves a reference for the complete continuation intervention. The existing failures do not distinguish a parameter-capacity ceiling from weak language pretraining, limited source diversity, curriculum gaps, or optimization. No 1B-parameter run is selected.

## Audit the corpus before admitting it

The original 100M exposures came from about **26.91M unique corpus tokens**. Repeating that text would not create a broader corpus.

The bounded first audit proposes Taskmaster Wizard-of-Oz dialogue for independently sourced language validation only, plus a DOAB book shard and a Hansard shard for possible training. Actual record rights, attribution, provenance, separation between source families, overlap, and eligible token yield must be checked before admission. Metadata describing a candidate is not blanket redistribution or training permission. No candidate records had entered training at this milestone.

A full 200M continuation calls for at least **100M eligible new unique tokens**, with at most two passes per document. Lower audited yield must reduce the run or leave a documented data bottleneck. The ceiling is conditional, not a commitment to fill a token budget regardless of source quality or rights.

The small base-language probe was frozen but unmeasured at this entry. The separate single-fact acquisition study remained a proposal. The fixed project stop remained **31 October 2026 at 04:12 UTC**.

See the [dated current plan](/model-training-journal/current-plan/) for subsequent measured results and decisions. This AI-assisted account preserves the preparation-stage notebook record; private messages, runtime details, raw transcripts, and candidate source text are excluded.
