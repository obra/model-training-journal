---
title: "Broader supervision, with failures kept in the record"
date: "2026-10-26"
slug: "broader-supervision-preflight"
phase: "Preparation"
summary: "A larger owned supervision set passes bounded data and context checks. The next comparison tests broader coverage without treating training fit as planning ability."
order: 15
---

This entry records preparation at **08:14 UTC on 26 October 2026**, before the second comparison had a model result. The [first planning comparison](/model-training-journal/2026/10/26/first-planning-comparison/) had produced 0/80 structural-development successes for both models. Base-plus-supervision reproduced 64/64 training-calibration cases, while random initialization reproduced 14/64. The next question was whether broader supervision could improve transfer.

## Broaden the examples while controlling exposure

The new programmatic corpus, recorded as owned CC0 material, contains **3,000 complete training conversations** and **80 development cases**. A unique training pass has **444,537 assistant labels**. Twelve components cover scheduling, missing constraints, corrections, unavailable tools, revoked permission, stale state, notes and grounded responses.

The accepted build retained all 3,080 candidates. Exact cross-split initial-user-prompt overlap was zero, but the examples share component operations and JSON structure. They are generated conversations, not human dialogue. The authoring program is development-informed; its success does not establish independent generalization. The new development suite froze before model training, while the old suite became an unchanged known diagnostic. Final holdouts remained reserved.

The planned pilot compares the old 946-conversation supervision with this broader corpus. Both arms start afresh from the preserved 100M-token base and reset the optimizer. Model, tokenizer, seed, precision and nominal **500,000-assistant-label** cap remain matched. Equal exposure means roughly 3.35 old-data passes versus 1.12 broader-data passes, not equal epochs. Whole-conversation stopping can leave a small unused budget.

## Keep the failed preflight visible

The first build failed at context 1,024: twenty full development conversations required 1,044–1,049 tokens, and another twenty exceeded the prefix-plus-response allowance. Both arms moved to **context 1,536**, preserving the difficult examples and complete histories. The accepted build's longest conversation is 1,055 tokens, longest generation prefix 1,002, and longest assistant payload 89 against a 96-token reply reservation.

The explicit context migration preserves every other architecture field and fixed rotary-position frequencies. The recorded CPU and GPU checks verified shared-prefix agreement and finite longer-sequence execution. A command-local device-visibility setting initially caused runtime aborts; correcting it allowed all 27 context/conversation checks to pass. These are mechanical compatibility checks, not evidence of long-context reasoning.

## Audit the requested outcome, not only the receipt

A supplemental checker replays completed fictional transcripts and compares completion statements with the currently delivered request and actual state. A valid write receipt can accompany the wrong item, date or correction.

Its recorded 37 focused tests passed. In the earlier random training calibration, it found **41 state contradictions and three skipped required clarifications**: 44 unsupported covered completions, including 38 missed by the receipt check. Unknown prose remains manual review. These finite checks do not certify broad truthfulness.

The next step was an isolated smoke test followed by the paired pilots and both development suites. [The completed pilot entry](/model-training-journal/2026/10/26/broader-supervision-pilot/) records what followed. This AI-assisted account was checked against the accepted freeze, budget records and implementation reviews; no conversation data or raw logs are published.
