---
title: "Launching a matched repetition control for task binding"
date: "2026-10-26"
slug: "binding-comparison-launch"
phase: "Experiment"
summary: "Two fresh-base arms compare repeated task-repair controls with varied values. Preflight catches overlap before the data freeze, and exact label budgets are recorded."
order: 26
---

The two-arm binding study began at **13:04 UTC on 26 October 2026**, after data checks and finite-run preparation. This entry records the launch; [the completed results](/model-training-journal/2026/10/26/counterfactual-binding-results/) are separate.

The [hypothesis](/model-training-journal/2026/10/26/contrastive-binding-plan/) was that varied supervised values could improve selection of the requested object and date. Both arms retained 3,000 canonical conversations and started independently from the same self-trained 100M-token base with fresh optimizers. Each added 500 task-repair rows.

## Match the comparison without hiding unequal exposure

The control repeated 100 anchors five times. The varied arm used a control, changed requested year, changed title, renamed target, and reordered returned items for each anchor. Half the anchors changed only the deadline; half explicitly renamed and updated the task. Stored dates stayed unchanged in year variants, and old/new titles were sampled independently to avoid a fixed-prefix shortcut.

| Frozen quantity | Repetition | Varied values |
|---|---|---|
| Training rows | 3,500 | 3,500 |
| Distinct histories | 3,100 | 3,500 |
| Assistant labels per row pass | 524,402 | 524,382 |
| Planned complete-conversation labels | 1,999,908 | 1,999,822 |
| Planned optimizer steps | 13,338 | 13,338 |

The added rows supplied approximately 15.23% of labels in each arm. Equal rows did not equal unique histories or identical label exposure. This tested a declared value-diversity package, not a new loss function or an isolated pairing mechanism.

## A preflight failure prevented premature freezing

The first production build stopped because a diagnostic title already occurred in retained training. No manifest had been committed and training had not started. The correction changed diagnostic title-number sampling while leaving training unchanged; exact title and history exclusion remained required. It happened before model results existed.

The successful build passed **44 focused CPU tests** and replayed the retained and added saved conversations. It found zero exact development-title or full-history overlap with training. The longest complete training conversation was 995 tokens, below context 1,536; no truncation was allowed.

All added material was recorded as owned CC0 text. No external teacher, new language corpus, or third-party model weights were introduced.

## Bound execution and preserve the denominators

The model remained **97,536,768 parameters**, using BF16 projection compute and FP32 persistent parameters and Adam moments. Each arm had a 3,600-second trainer limit and a 3,780-second outer guard, with checkpoints every 100,000 labels or 300 seconds. The absolute deadline remained **31 October 2026 at 04:12 UTC**.

Eighteen finite evaluation jobs were planned: the new 64-case diagnostic, branch-specific training fit, original calibration, known development sets, and paired probes. Raw/guarded views and related anchors were explicitly correlated. In particular, the control's 50-record added-training sample contained only ten distinct repeated histories; the varied sample contained fifty.

Resource observation had failed and partial attempts, leaving early and middle training gaps. The launch record therefore establishes no complete-run memory maximum. No quality result or checkpoint promotion follows from successful launch.

This AI-assisted summary was checked against the production manifest, preflight reviews, measured budgets, and launch metadata. Private runtime identities and raw logs remain outside the public journal.
