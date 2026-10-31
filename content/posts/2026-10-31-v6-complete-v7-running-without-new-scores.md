---
title: "V6 completes; V7 starts while quality remains unmeasured"
date: "2026-10-31"
slug: "v6-complete-v7-running-without-new-scores"
phase: "Finite continuation: completion and evaluation failure"
summary: "V6 finished 44,759,442 valid labels. Completion recovery passed, but the CFR readiness gate failed before scoring. V7 is running; no new quality or reasoning result exists."
order: 48
---

V6 finished at **23:23:14 UTC on 30 October 2026**, with exit code **0**, **1,369 completed training updates**, and **44,759,442 valid next-token labels** in the run. Its terminal saved checkpoint is `3c22c967f7c452926e41e399bddd77ec4349f01395dc4e3ebe485026867b489b`. This supersedes the running status in the [first-checkpoint snapshot](/model-training-journal/2026/10/30/v6-first-saved-checkpoint/). Completion is verified; **V6 perplexity remains unmeasured**.

The original terminal auditor failed while replaying an older checkpoint-storage schema. Training had already exited successfully; the failed audit did not establish completion. A separate versioned recovery first passed a read-only check of the saved checkpoint, guard and accounting. A distinct completion operation then closed the main ledger at event **1,069,492**. This separates the training outcome, the failed audit, and the later verified completion instead of treating them as one successful operation.

A proposed six-checkpoint CFR scoring allocation bound its inputs to exact hashes, but its **CPU readiness gate produced no positive receipt**. The command returned transport exit code **255** with no output under a configured **180-second** process limit. Postchecks found **zero scoring attempts**, **zero auxiliary evaluation charges**, and no GPU model load. The exact interruption mechanism is unresolved. Expensive repeated ledger replay is a leading explanation; an internal alarm and an unanswered SSH heartbeat remain competing explanations. We have no evidence that a particular scoring stage ran, and no new score to publish.

| Run | Dated evidence boundary | Completed run-local updates | Completed run-local valid labels | Quality status |
|---|---|---|---|---|
| V6 | completed; guard finished 30 Oct 23:23:14 UTC | 1,369 | 44,759,442 | CFR not scored; readiness gate failed before scoring |
| V7 | live ledger observed 31 Oct 00:13:09 UTC | 19 | 621,206 | No new saved checkpoint or score in this snapshot |

V7 continues from V6's exact terminal checkpoint with a separately reviewed, parent-bound permit for the remaining finite text tail, without repeating the earlier source prefix. At **00:13:09 UTC on 31 October**, its ledger confirmed training had begun and completed **19 updates** and **621,206 valid labels**. There was **no new V7 checkpoint** in that observation. The earlier guard launch time includes preflight work; it is not the time of the first training update. These live counts must not be mistaken for saved or evaluated progress.

The installed project cutoff remains **7 November 2026 at 04:12 UTC**. V7 has its own earlier finite guard ending **31 October 2026 at 06:02:12 UTC**. A project extension does not make this run indefinite. The [dashboard](/model-training-journal/dashboard/) collects the dated table above and preserves the older score curves, their populations and run boundaries; unmeasured quality stays missing rather than becoming zero.

**No new reasoning benchmark has run.** V5's terminal CFR development perplexity **34.2885 on 7,057 labels** remains the latest scored terminal result. It must not be attached to V6 or V7. The broader language panel has not been rerun for these stages; BLiMP remains unrun, the format diagnostic has no successful trial, and the sealed final planning holdout remains untouched. The earlier V3 task result remains **0/32 correct and 0/32 protocol-valid**, with its output-interface limitation. This AI-assisted journal publishes reviewed aggregate evidence and failures, not private logs or training text. More completed training is not evidence of transferable reasoning.
