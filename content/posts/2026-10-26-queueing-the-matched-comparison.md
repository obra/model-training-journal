---
title: "Queueing the matched comparison"
date: "2026-10-26"
slug: "queueing-the-matched-comparison"
phase: "Engineering"
summary: "A reviewed sequential pipeline waits for the base checkpoint, then plans a bounded language probe, isolated supervised smoke test, matched training branches, and development evaluations."
order: 9
---

This entry records the comparison being queued on **26 October 2026**, while the original base run was still active. The CPU coordinator waited for that run; it did not restart it or launch a competing GPU workload. **The stages described here were queued work, not completed model results.**

The aim was to carry the [matched comparison design](/model-training-journal/2026/10/26/making-the-planning-comparison-fair/) through execution without losing its measurement boundaries.

## Fix launch and recovery defects first

Independent review found two defects beyond the initial passing tests. The shortened supervised smoke configuration inherited a warmup longer than its whole run. A recovery edge case could also leave status pointing at a finished job.

The smoke-only schedule was corrected to a 1,000-label warmup within a 10,000-label requested budget. Recovery could clear stale status only for the exact completed job after a fresh check established that its process group was absent. A different, live, or uncertain job blocked progression.

The notebook records **38 comparison-test passes on Linux** and a CPU preflight that constructed both schedulers with the actual tokenizer and data budgets. Independent review also records 38 passing tests. These are orchestration and preparation checks, not evidence of conversational ability.

| Planned supervised stage | Complete-conversation labels | Steps |
|---|---|---|
| Isolated smoke test | 9,976 | 66 |
| Each matched branch | 1,999,931 | 12,672 |

The unused labels preserve complete conversations rather than truncating constraints or permissions.

## A fixed sequence with separate evidence

1. Require clean base completion at **100 million valid tokens**. Reload and verify its checkpoint, recoverable state, hashes, finite weights, and FP32 persistent tensors; preserve a separate base snapshot.
2. Run a **900,000-valid-label language probe** under a ten-minute bound. CPU counting showed it would consume 902,144 of the 918,539 available raw validation tokens without cycling. This is a partial single pass, not evaluation of every raw token.
3. Run the isolated supervised smoke test under a six-minute external bound and three-minute trainer limit. Its trained state must not initialize either matched branch.
4. Train random-plus-supervised and base-plus-supervised branches sequentially, each bounded by four hours. Verify equal actual labels, optimizer steps, and stream positions.
5. Evaluate both branches on all **80 development cases**, separately in raw and guarded modes, each bounded by one hour. Both use the same 96-token greedy decoding policy, preserve raw output, and receive no oracle state. Report read-before-write policy separately from original scores.

The final holdout was excluded from this sequence. All GPU stages remained subject to the independent deadline guard and absolute stop of **31 October 2026 at 04:12 UTC**.

## Stop visibly when execution is uncertain

Changed pinned inputs, uncertain launches, failed checkpoint checks, incomplete evaluations, or an unhealthy sentinel would halt progression for inspection. Partial transcripts would remain labeled partial. The pipeline would not blindly retry or launch a duplicate job.

This AI-assisted record describes the intended sequence at queue time. The experiment still needed actual development outcomes and failure analysis before any model could be considered useful or promoted.
