---
title: "Longer canonical training improves fit but not development planning"
date: "2026-10-26"
slug: "canonical-2m-results"
phase: "Results"
summary: "The same 64 training cases fit better after two million supervised labels, while development behavior still fails. Fewer completion claims also conceal more unfinished conversations."
order: 21
---

The canonical two-million-label run, four development evaluations and unchanged 64-case training diagnostic completed on **26 October 2026**. Longer optimization improved reproduction of familiar examples. It did not demonstrate correct completed plans on either development suite.

## Completed exposure

Training finished at **10:27:07 UTC** with **1,999,982 assistant labels in 13,509 steps**, taking **976.4949 seconds**, approximately 2,048 labels per second. The four development evaluations completed at 10:34:05; the training-fit follow-up finished at 10:36:34.

The run started afresh from the same preserved base and unchanged canonical 3,000-conversation corpus. Model, tokenizer, order, seed, context and optimizer hyperparameters matched canonical 500K. Label exposure and cosine-decay horizon changed together. The 444,537-label unique-pass inventory was exposed about 4.5 times; no extra unique data was added.

## Better fit on the same training examples

| Training diagnostic | Canonical 500K | Canonical 2M |
|---|---|---|
| Original accepted-state outcomes | 38/64 | 50/64 |
| Exact full message histories | 34/64 | 48/64 |
| Teacher-forced all-labels-correct conversations | 34/64 | 48/64 |
| Incorrect assistant labels | 43/9,601 | 18/9,601 |
| Mean assistant-label loss | 0.01306820 | 0.00550383 |

All sixteen nonexact histories first diverge in assistant output, with no environment-prefix mismatch. This is improved fitting on exposed examples, not held-out transfer.

The two nonexact accepted outcomes differ materially: one still proposes the wrong duration without booking; the other recovers from a rejected reversed interval and then books the correct requested slot. The original 50 accepted outcomes therefore comprise 48 exact histories, one correct recovery and one wrong-duration suggestion. Both nonexact cases must not be dismissed as equivalent errors.

All fourteen remaining failures concern calendar intervals and finish with false generic completion claims despite real write receipts. Two now overlap observed commitments, even though their earlier failed intervals did not. Aggregate fit improvement is not uniform behavioral improvement.

## Development behavior remains unsuccessful

Raw and guarded histories match within each suite; they are correlated views, not independent replications. The original and newer suites retain different contexts, 1,024 and 1,536 respectively.

| Original accepted-state score, each mode | Canonical 500K | Canonical 2M |
|---|---|---|
| Original development suite | 12/80 | 1/80 |
| New development compositions | 11/80 | 10/80 |

The sole original-suite pass acknowledges a real unavailable-tool error after a wrongly specified booking attempt. There is no correct event, completed correction or requested proactive heads-up. Redundant questions increase **8→37**. False completion claims fall **25→6** alongside fewer attempted outcomes, so that decline does not establish improved truthfulness.

All ten newer-suite passes obey a delivered withdrawal but suggest the wrong requested date. Timestamps and interval lengths improve: all ten are positive, and five durations match. None is a correct full plan. **27 of 28 questions are redundant**. False completions fall **20→12**, largely because twenty distractor-task cases now end on invalid updates without final answers. Fewer spoken claims must not conceal more unfinished conversations.

## Next diagnostic, not promotion

No dedicated training-memory peak was recorded; inference-only memory measurements cannot fill that gap. Final holdouts remained reserved.

The next selected diagnostic was to compare saved checkpoints on paired changes to year, wording, target identity, item order and calendar geometry. That was a development-informed probe, not a blind holdout; no GPU probe result is claimed at this entry's cutoff. [The paired-probe results](/model-training-journal/2026/10/26/paired-transfer-probe-results/) follow separately.

This AI-assisted account was checked against the exact budget, fixed-64 summary and independent development, fit and claim reviews. The model was not promoted on these results.
