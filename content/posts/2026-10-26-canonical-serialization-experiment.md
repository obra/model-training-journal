---
title: "A controlled test of training tool serialization"
date: "2026-10-26"
slug: "canonical-serialization-experiment"
phase: "Experiment"
summary: "The canonical 500K-label experiment starts from the preserved base with matched configuration and assistant targets. This launch snapshot makes no completed-performance claim."
order: 18
---

The finite canonical-serialization run began at **09:44:58 UTC on 26 October 2026**. This entry preserves its launch plan and early progress; [the completed results](/model-training-journal/2026/10/26/canonical-serialization-results/) are a separate record.

## Change one representation

The intervention changes only tool-message key order in the training corpus, aligning it with the frozen runtime. It retains the previous broader pilot's configuration bytes, preserved 100M-token base, fresh optimizer, seed, example order, tokenizer, context 1,536 and precision. All 3,000 conversations passed saved-runtime replay and token-bound checks before launch, with assistant targets unchanged and no discarded records.

The exact planned exposure is **499,839 assistant labels over 3,368 optimizer steps**. Complete-conversation stopping leaves 161 labels unused below the nominal 500,000 cap. The corpus still provides 444,537 assistant labels in a unique pass, so this is repeated exposure to the same material rather than more unique training data.

## Keep the comparison finite

The trainer has a 3,600-second limit and an enclosing 3,780-second job limit. Checkpoints are scheduled every 100K labels or 300 seconds. The independent project deadline remains **31 October 2026 at 04:12 UTC**; this experiment does not extend it.

Four evaluations on the two known development suites follow training, with original accepted-state scores kept separate from protocol, requested-outcome and suggestion/date checks. The same 64 training IDs will support a fitting diagnostic. No final-holdout evaluation is part of this comparison.

At the **09:46:23 UTC** progress snapshot, the run had processed 162,906 labels at approximately 1,953 labels per process-wall second and saved its first 100K checkpoint. Those were interim counters, not a final fit or generalization result.

A corrected passive memory observer began during training after an earlier device-selection defect. Earlier memory maxima remain unavailable. Later device-wide samples cannot establish tensor-allocator peaks or capture work before observation began.

The hypothesis is narrow: removing a demonstrated token-sequence mismatch should make the remaining training-fit failures interpretable. It does not predict that the model will learn reliable planning. This AI-assisted launch account was checked against launch metadata, matched budgets, configuration and the canonical-data manifest.
