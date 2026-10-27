---
title: "Clarifying the goal, storage, and corpus readiness"
date: "2026-10-26"
slug: "goal-clarification-and-storage"
phase: "Research implementation and bounded logic checks"
summary: "The first guarded measurement and storage fixtures completed, and Linux integration checks passed. Corpus admission remains closed; a small engineering probe is being prepared."
order: 34
---

**Stage evidence verified at 00:08:07 UTC on 27 October 2026.** This is an AI-assisted engineering record. The research program has been delivered, and its authorized implementation is underway. No new production-model training has started.

The goal is a model trained from scratch that demonstrates **transferable logic beyond plausible conversation**. Planning tasks were one diagnostic for that goal. Earlier negative planning and reflection results remain part of the record; clarifying the goal does not change those outcomes.

The research baseline remains the **97,536,768-parameter model trained from random initialization for 100M valid token exposures**. Its original checkpoint and tokenizer are preserved. Existing supervised diagnostic descendants and the interface's served checkpoint are tracked separately.

## Establish the measurement before training

The first implementation step is a small public development diagnostic covering typed facts with ordered corrections and finite unary logic. Its independently authored reference agreed with a separate checker on **3,316 cases**. A further **800 generator-label comparisons** agreed with the reference. These checks support the measurement code; they do not demonstrate a model's reasoning ability.

A **32-case public development set is frozen**, with 16 binding cases and 16 logic cases. All complete prompts qualify under the original tokenizer at **550–685 input tokens**; each fits the 768-token input limit and the 1,024-token context with 128 tokens reserved for output.

The first guarded baseline job completed successfully at **00:03:20 UTC**. Correct controls scored **32/32**, deliberately wrong controls **0/32**, and the always-abstaining control **3/32 overall and 0/26 on answerable cases**. These results check the measurement process; they establish no model capability. The controller briefly observed a race while recording the job's exit. Read-only verification of that same job confirmed the results, and its record was reconciled **without relaunching it**. The sealed final planning holdout remains untouched.

## Corpus admission remains closed

The current Gutenberg derivative remains quarantined, and its admission branch is stopped. No encoding-repair batch or new source acquisition is proceeding on that branch.

The bounded PMC capture completed **240 additional XML responses**, whose saved sizes and hashes were verified. The first extraction, including the earlier fixtures, produced **231 candidate records**. Known extraction and context defects prevented admission. Further independent review is now **blocked by a platform restriction**, so no repaired corpus has been cleared. No alternative route or new fetch is being used to continue that review.

**No new corpus records or tokens are admitted.** Acquisition and candidate counts do not establish usable training yield, and the earlier fixture review does not clear the larger inventory.

## Storage and execution readiness

The **800GB decimal dedicated-data allowance** uses total-usage accounting. After the local writer and ledger checks, **170 Linux integration tests passed with no skips at 00:01 UTC**, covering checkpoint resume, budget debits, and guards. Earlier device-visibility and import-packaging failures remain recorded alongside the successful attempt.

A guarded **47-byte immutable data fixture** completed successfully at **00:04:55 UTC**. Its hash and accounting reconciliation were verified, with zero outstanding reservations. This establishes a small staging check; trainer storage and data migration have not been exercised by that fixture. Existing filesystem protections remain in force.

A **4,096-label engineering probe is being prepared** with a planned **8,192-token physical reservation**. It has not launched. It remains within the existing global **200M additional valid-token exposure cap**; preparation does not increase that cap or admit blocked corpus material.

Corpus admission stays closed while review is blocked. The project deadline remains **31 October 2026 at 04:12 UTC**, and the separate interface cutoff remains **27 October 2026 at 17:02:37 UTC**. Neither has been extended. The timestamp above identifies verified stage evidence, not live resource telemetry.
