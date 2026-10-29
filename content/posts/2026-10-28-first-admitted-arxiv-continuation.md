---
title: "Completing the first admitted arXiv continuation pilot"
date: "2026-10-28"
slug: "first-admitted-arxiv-continuation"
phase: "Infrastructure pilot and corpus continuation"
summary: "A bounded infrastructure pilot completes one pass over 99 admitted arXiv papers: 62 updates and 2,029,534 valid labels. All three logic probes return 0/32 correct and 0/32 protocol-valid answers. New-phase language loss is unmeasured; broader corpus admission continues."
order: 37
---

**Saved-record review: 28 October 2026, 02:39:23 UTC.** This timestamp describes review of saved evidence, not live training or machine telemetry. The pilot completed **62 updates**, with all three checkpoint pairs verified, all three logic probes completed and successful process exit. It is a bounded infrastructure test on a small admitted cohort, not the main pretraining program. Broader corpus admission continues separately.

## A bounded pilot after recovery

The **299,414,528-parameter model** began from random weights. Its first production run failed after 355 completed updates, leaving checkpoint 274 retained. Recovery restored that checkpoint and completed 547 updates. Its terminal model reached **step 821**, with **26,860,551 valid labels** and **26,902,528 processed input IDs** on the retained trajectory.

Physical accounting at recovery completion retained **902 completed updates**, **29,518,945 charged valid labels** and **29,564,928 charged input IDs**. Those charges include interrupted partial accumulation and replay; the original failure and accounting are preserved. The arXiv phase begins after those historical totals and does not relabel replay as new material.

The preceding [recovery and language-measurement entry](/model-training-journal/2026/10/27/recovering-the-first-299m-pretraining-phase/) preserves the original failure history and five-checkpoint results. The pilot tests the training, accounting, checkpoint and serial-evaluation path on additional admitted scientific prose, with the same architecture and tokenizer.

## Admitted papers and reserved development material

The pilot used **99 whole training papers**, containing **2,032,000 content token IDs**, admitted from a bounded **128-paper review cohort** within a pinned Common Pile arXiv archive. Another **10 papers with 224,896 content IDs** remained reserved as development material and excluded from training. The 99-paper result reflects that limited cohort, not an exhaustive archive admission or extraction failure. The broader corpus-admission pipeline is active; this infrastructure pilot does not define the size of the main pretraining program.

The admission evidence binds the archive revision and exact compressed bytes to selected rows, original text hashes and tokenization. Archived per-paper CC BY 4.0, CC BY 3.0 or CC0 labels and original notices are preserved. Observed work families and normalized author connections define the frozen separation. Historical overlap exclusions, negative controls and source-quality holds remain excluded.

This scoped decision covers known pinned bytes and observed source families. The exact upstream converter build, original arXiv versions and unobserved author or publication aliases remain unknown. It is not universal rights, privacy, factual or semantic-novelty certification. The earlier unresolved Pressbooks follow-on remains unadmitted; this distinct admission does not clear its extraction, rights or source-family failures. No corpus passages are published here.

## One completed nonwrapping pass

The pilot restored the recovery terminal model, complete optimizer and random state. It launched at **02:17:09 UTC on 28 October** and its guard recorded successful exit at **02:32:18 UTC**, about **909 seconds** later. The worker reported **884.43 seconds**, on its own elapsed timer. Its **30-minute maximum** would have ended at **02:47:09 UTC**.

It completed **62 optimizer updates**, **2,029,534 valid labels** and **2,031,616 processed input IDs** across **1,984 microbatches**. The source contains 2,032,000 content IDs plus separate end-of-document markers; **483 trailing stored IDs** were unused by the full-update schedule. Source inventory, valid labels and processed IDs therefore have different denominators. This was one pass without wrapping, synthetic repair examples or a repeat pass.

Terminal review verified all **three checkpoint payload/metadata pairs**, their accounting and evaluation bindings, successful process exit and absence of surviving workers. Checkpoint storage was closed after verification. The completed checkpoints and serial fixed-32 probe scores were:

| Pilot checkpoint | Model step | Physical campaign step | Correct answers | Protocol-valid answers |
|---|---|---|---|---|
| Update 16 | 837 | 918 | 0/32 | 0/32 |
| Update 31 | 852 | 933 | 0/32 | 0/32 |
| Update 62, terminal | 883 | 964 | 0/32 | 0/32 |

The first checkpoint contains **523,750 new valid labels** from **524,288 processed input IDs**. The terminal retained model trajectory reaches **883 steps**, **28,890,085 valid labels** and **28,934,144 processed input IDs**. Physical campaign totals reach **964 completed steps**, **31,548,479 charged valid labels** and **31,596,544 charged input IDs**.

Model steps count the retained trajectory; physical steps and checkpoint metadata also count original interrupted work and replay. The physical token totals preserve historical partial accumulation. These counters describe different histories and do not establish unique corpus size.

## What the boundary probe measures

The fixed development suite has **32 cases**, split equally across two logic families. At all three boundaries, it returned **0/32 task-correct answers** and **0/32 protocol-valid answers**. Zero valid answers prevents isolation of reasoning capacity from failure to produce the required answer format. No capability improvement is established.

All three boundary probes used the same frozen protocol and **BF16 computation using the existing training model in memory**, with greedy decoding, a 128-token output cap and no output repair. They ran serially with training, taking **150.56, 150.88 and 150.95 seconds**, respectively. The earlier fixed-32 probes used standalone checkpoint execution. The execution contexts differ, so raw scores can be compared descriptively but are not strict automatic deltas under a matched contract. No synthetic repair training was added to fit this probe. The sealed final holdout remains untouched.

Companion language-model scoring remained **disabled** at all three boundaries, with no metric values. New-checkpoint language loss and perplexity are **not measured**. The earlier standalone regulatory-prose evaluation remains a historical result: across model steps 274 to 821, NLL changed from **6.304254 to 5.895244 nats per token** and perplexity from **546.8935 to 363.3055**, using the same **32 sections and 7,057 scored tokens**. That is a **6.49% loss reduction** and **33.57% perplexity reduction** on that narrow development measure, not a reasoning result or a score for this continuation.

The earlier lexical audit covered the pinned Pressbooks training corpus and old validation only. It did not certify globally unseen families, semantic or paraphrase exclusion, earlier or later regulatory editions, unknown model histories, or coverage of the new arXiv phase. That earlier result cannot be silently extended to the new checkpoints.

## Scope and continuing work

The data-volume allowance remains **800 GB** and the broader campaign ceiling remains **one billion valid labels**, with processed input IDs counted separately. The last recorded installed training cutoff remains **31 October 2026 at 04:12 UTC**. This saved-record review does not extend that deadline or establish a new live machine-state claim. Resource, memory, thermal, free-space and checkpoint safeguards remain execution requirements.

Completion establishes the bounded infrastructure path on this cohort. It does not establish transferable logic or replace the broader admission and pretraining program. The research goal remains an open-source, reproducible recipe for transferable logic beyond plausible conversation. This stage uses no paid compute, proprietary model APIs or private trace inputs for model training and corpus preparation. This is an AI-assisted engineering record of aggregate methods and results. See the [current plan](/model-training-journal/current-plan/) for the reviewed snapshot.
