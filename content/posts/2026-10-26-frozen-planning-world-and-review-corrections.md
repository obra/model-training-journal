---
title: "Freezing the planning world and correcting the evaluation"
date: "2026-10-26"
slug: "frozen-planning-world-and-review-corrections"
phase: "Evaluation"
summary: "Review exposed weaknesses in completion checking and the original language split. A revised frozen suite and supervised-training checks improve the machinery, while a failed scripted baseline remains under methodological review."
order: 7
---

Before behavior tuning, the fictional calendar, task, and note simulator received implementation review. The aim was to make future results interpretable: the system needed to check what an agent actually changed, distinguish its raw output from guarded execution, and preserve a held-out evaluation.

This entry records the revised evaluation freeze at **04:48 UTC** and runtime checks completed around **04:55 UTC on 26 October 2026**. The simulator makes only in-memory fictional changes. No learned conversational model had been evaluated, and the 100-million-token base continuation was still in progress.

## A valid receipt must not justify an unrelated claim

Review found that a genuine tool receipt could accompany an unrelated fabricated completion statement and evade the original checker. The revised checker separates affirmative clauses and relates them to receipt domains, quoted identities, and explicit times within its defined vocabulary.

That correction closes a demonstrated failure in the tested grammar. It does not solve general semantic entailment. A zero count of covered unsupported-completion flags cannot establish that arbitrary prose contains no fabricated claims. Broader claims require a recorded audit of the retained transcripts.

Raw model output and guarded behavior remain separate measurements. A guard can block an attempted mock action without making the original model output appropriate. Likewise, strict parsing does not repair malformed model output before scoring it.

## Replace wrapper variation with a more demanding split

The original final suite mostly varied language wrappers around common templates. Distinct family labels therefore did not establish structurally different requests.

The revised `final-v2` suite changes request grammars, constraint orderings, and referential follow-ups across splits. Its freeze manifest is timestamped **04:48:27 UTC**, before the revised supervision export. The original suite remains preserved.

| Revised split | Recorded cases |
|---|---|
| Training, before deduplication | 1,200 |
| Development | 80 |
| Frozen final evaluation | 160 |

These are still narrow, programmatically generated scenarios from the same authoring system. Both logic and language change across splits, so a failure does not isolate which changed factor caused it. The split does not establish broad linguistic generalization, and no final evaluation had run.

## Preserve the scripted result without settling its explanation

A recorded development rollout of the public-input-only scripted baseline produced **0 successes in 80 scenarios**, with 80 syntactically valid clarification messages and **zero tool attempts**. With no tool attempts, tool-call syntax validity has a denominator of zero and is undefined.

The baseline's adequacy and interpretation are **under methodological review**. The observation does not establish a settled parsing-limit explanation, learned-model superiority, or safety through successful tool use. The original result remains part of the record; any revised baseline needs its own result and explanation.

## Check complete conversations before supervised training

The programmatic training conversations are recorded as original CC0 material. After removing 254 duplicates, the export retained **946 complete conversations**. Exact counting with the actual BPE tokenizer rejected none for context length; the longest retained conversation was **700 tokens**, below the 1,024-token context limit.

No conversation was shortened by truncating a user constraint or permission. The retained material includes six silence situations and six grounded-acknowledgment situations. That is limited training coverage, not evidence of broad initiative or humane conversation. No human dialogue ratings were collected or invented.

The export uses training records, not held-out final answers. This journal publishes neither the conversation data nor held-out scenarios and oracle text.

## Verify the machinery, then test the model separately

The Linux runtime log records **22 world-test passes** and **19 supervised-interface-test passes**, with no skips in those runs. The checks cover strict parsing, permission and stale-state behavior, context refusal, assistant-only shifted-label loss, provenance boundaries, and exact interrupted CPU supervised-training resume.

Resume validation binds the shared trainer implementation to the checkpoint. Base initialization requires a recognized base-training origin with matching source, tokenizer, and stream evidence; supervised or unknown origins cannot simply be relabeled as the base control.

These are software and resume checks. They do not establish that supervised training has produced useful conversational behavior. A fair future comparison must match the two branches' **actual trained assistant-token counts**, not merely their configured budgets, while preserving raw outputs and separate guarded results.

This AI-assisted summary was checked against the freeze and export manifests, implementation reviews, and runtime test log. The unresolved baseline methodology, limited completion grammar, and narrow generated distribution remain part of the experiment's limits.
