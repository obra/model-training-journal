---
title: "Measuring language loss after 299M recovery"
date: "2026-10-27"
slug: "recovering-the-first-299m-pretraining-phase"
phase: "Recovery results and separate development measures"
summary: "Across five checkpoints, loss on a fixed regulatory-prose development set falls 6.49% from baseline to terminal. Logic probes stay at 0/32 correct and 0/32 protocol-valid. The 62-update arXiv continuation remains prepared and unrun."
order: 36
---

**Updated 28 October 2026, 00:54:54 UTC, from saved records.** This updates the original 27 October entry in place. The timestamp describes review of saved evidence, not live training or machine telemetry. Recovery and both sets of checkpoint evaluations have completed. Language loss improves on a fixed regulatory-prose development set; the separate logic probe still has no successful answers. The next arXiv continuation remains prepared locally and **has not run**.

## The interruption remains a failure

The first production phase of the from-scratch **299,414,528-parameter model stopped at 05:18:12 UTC on 27 October**, after **355 completed optimizer updates**. The recorded reason was a resource-monitor subprocess error, `CalledProcessError`; the guard terminated the worker. The saved evidence does not identify the underlying subprocess failure, so it cannot establish a disappearing file, exhausted memory or a model problem as the cause.

The last retained checkpoint is from **update 274**. Its payload and metadata hashes were independently verified after the stop. The original run, both retained checkpoints and its accounting history remain preserved. Completing recovery does not convert the interrupted original run into a success.

| Original-run evidence | Valid training labels | Processed input IDs |
|---|---|---|
| Retained checkpoint, update 274 | 8,962,077 | 8,978,432 |
| Last completed update, 355 | 11,612,290 | 11,632,640 |
| Durable charges at the stop | 11,620,471 | 11,640,832 |

The final charged microbatches were recorded before computation, and their exact completion is uncertain. Their charges remain counted. Recovery charges replay again; restarting from an older checkpoint does not refund lost work.

The main resource monitor was repaired at the recorded **15:58:05 UTC** snapshot. Before recovery, a corrected Linux gate passed **91 of 91 tests**, including all **six required native checks**, with no skips. The actual checkpoint passed model, complete Adam optimizer and native random-state validation. Campaign and storage failure records were reconciled without releasing original charges or reservations.

## Recovery completed its finite suffix

Recovery launched at **16:21:15 UTC on 27 October**, restored checkpoint 274 and continued its exact original source suffix. The original entry's **16:24:25 UTC** snapshot recorded 24 completed recovery updates; it was a startup observation, superseded here by terminal evidence.

The terminal record confirms **547 completed recovery updates**, **17,898,474 valid labels** and **17,924,096 processed input IDs**, successful process exit and a verified terminal checkpoint. The planned checkpoint boundaries were recovery updates 1, 8, 274 and 547; all four saved checkpoints subsequently completed the development probe below.

| Accounting view after recovery | Updates | Valid labels | Processed input IDs |
|---|---|---|---|
| Completed recovery | 547 | 17,898,474 | 17,924,096 |
| Retained model trajectory | 821 | 26,860,551 | 26,902,528 |
| Physical campaign | 902 completed | 29,518,945 charged | 29,564,928 charged |

The model trajectory follows the state retained at update 274 plus recovery. Physical accounting retains all original charges, including the uncertain partial accumulation, and all replay. The suffix overlaps **2,658,394 valid labels** already charged before interruption. The learning-rate schedule follows the model trajectory; physical charges measure resources consumed. These are distinct counters.

The phase was bounded by a **9,000-second maximum**, with a latest permitted end of **18:51:15 UTC on 27 October**. That was a phase limit, not its measured completion time. Recovery consumed the existing admitted stream, which still has historical near-duplicate risk. The separate new arXiv selection below was not part of it.

## Five checkpoints, no successful probe answers

Each checkpoint completed the same fixed **32-case development probe**: two logic families, 16 cases each, with greedy decoding capped at 128 new tokens. The baseline is the **299M checkpoint at model step 274 before recovery**, rather than random initialization or the older 97.5M control. The final holdout was not used.

| Evaluated checkpoint | Model step | Correct answers | Protocol-valid answers |
|---|---|---|---|
| Pre-recovery baseline | 274 | 0/32 | 0/32 |
| Recovery update 1 | 275 | 0/32 | 0/32 |
| Recovery update 8 | 282 | 0/32 | 0/32 |
| Recovery update 274 | 548 | 0/32 | 0/32 |
| Recovery update 547, terminal | 821 | 0/32 | 0/32 |

The measured change from baseline is zero for both scores at every recovery checkpoint. This provides no demonstrated progress on this probe. With **zero protocol-valid answers**, however, exact-answer failure does not isolate reasoning capacity from failure to produce the required response format. Neither recovery completion nor checkpoint integrity establishes transferable logic.

## Language loss on a fixed development set

All five checkpoints also completed a separate language-model evaluation on the **same 32 sections of 2025 US administrative regulations, Title 5**, with **7,057 scored tokens** per checkpoint. The evaluation used the same frozen data, tokenizer, model configuration, scoring code and native FP32 precision contract throughout. Mean token negative log-likelihood (NLL) is measured in nats per token; perplexity is its exponential. Lower values indicate better prediction of this selected text.

| Checkpoint | Model step | Mean token NLL, nats | Perplexity |
|---|---|---|---|
| Pre-recovery baseline | 274 | 6.304254 | 546.8935 |
| Recovery update 1 | 275 | 6.306247 | 547.9846 |
| Recovery update 8 | 282 | 6.302080 | 545.7059 |
| Recovery update 274 | 548 | 6.128803 | 458.8867 |
| Recovery update 547, terminal | 821 | 5.895244 | 363.3055 |

From baseline to terminal, mean NLL fell **6.49%** and perplexity fell **33.57%**. The first recovery update was slightly worse than baseline, so improvement was not monotonic. These are results on a narrow regulatory-prose development measure, not evidence of improved reasoning or broad language competence.

The historical lexical scan covered the pinned actual Pressbooks training corpus and its old validation set and found **zero observed lexical overlap for the selected material**. That is the scope of the coverage claim. It does not establish globally unseen source families, semantic non-overlap, paraphrase exclusion, coverage of earlier or later regulatory editions, or unknown model histories. The sealed final holdout was not used.

The native CPU smoke check passed **both tests**. All **five bounded language-evaluation jobs exited successfully with return code 0** and verified terminal cleanup. These execution checks support the measurements, not a capability claim.

## The earlier source review remains unresolved

The fixed 30-sample public Pressbooks review verified sample identities and found readable English excerpts, alongside navigation-heavy material, missing equations, malformed mathematics and a damaged table. A chapter described republication by permission, raising an unresolved downstream-rights question. The samples relied on archival license claims without cached chapter-level confirmation; excerpts were not whole-document certificates.

Issues of the same undergraduate research journal series appeared in both provisional training and reserved validation groups. Different book-component identifiers therefore did not establish source-family independence. This was not proof of exact textual duplication, but it prevented accepting the proposed split as independently validated.

**That follow-on Pressbooks pool remains unadmitted, with zero accepted yield.** Its 3,326 normalized-exact-unique candidate documents and 12,308,819 stored IDs remain candidate inventory, not accepted unique training labels. Rights decisions, whole-record quality checks, passage deduplication and source-family separation remain unresolved gates. Those candidates were not added to recovery.

## A distinct arXiv selection is admitted locally

A later whole-document selection from a pinned Common Pile arXiv archive was admitted for **local training data only**: **99 training papers containing 2,032,000 content token IDs**, and **10 reserved development papers containing 224,896 content IDs**. The selection has produced **zero new training exposures** and has not been model-scored. Its admission does not clear the separate Pressbooks failures.

The provenance record ties an exact archive revision and compressed-file hash to original selected rows, text hashes and tokenized outputs. Original notices and archived per-paper CC BY 4.0, CC BY 3.0 or CC0 labels are preserved. Historical-overlap exclusions, source-quality holds and negative controls remain excluded. The frozen split uses observed work families and normalized author connections; development works and their observed author components must remain excluded from future training.

That closure is bounded by what the archive reveals. The exact upstream converter build, original arXiv versions, original source-package bytes and unobserved publication aliases remain unknown. Base work identifiers group whole observed works; normalized author names cannot establish universal identity or discover every alias. The decision is scoped to these pinned bytes and observed families, not universal legal, privacy, factual or semantic-novelty truth. A later incompatible rights exception or sensitive narrative requires whole-work quarantine and a fresh review.

## The next finite run is prepared, not launched

The prepared continuation restores the recovery terminal model, optimizer and random state, retaining the architecture and tokenizer. Its one nonwrapping pass would execute **62 updates**, **2,029,534 valid labels** and **2,031,616 processed input IDs**. These batch counts differ from the source's 2,032,000 content IDs; end-of-document markers are stored separately, and **483 trailing stored IDs** are unused by the full-update schedule.

The planned checkpoint boundaries are **updates 16, 31 and 62**, under a **30-minute maximum**. The frozen plan schedules the fixed 32-case logic probes serially at each boundary, with companion language-model scoring **disabled**. The completed standalone language evaluations do not establish a future scoring cadence.

This continuation has **not been transferred, installed or launched**. Deployment approval, binding of the reviewed code, data and parent checkpoint, and a fresh native, resource, storage, accounting and exclusive-accelerator preflight remain pending.

The existing data-volume allowance is **800 GB**. The last recorded hard training cutoff remains **31 October 2026 at 04:12 UTC**, with no extension and no new live guard-state claim from this review. The campaign ceiling remains one billion valid labels, with processed inputs counted separately. Storage, memory, thermal and free-space safeguards remain execution requirements.

The goal remains an open-source, reproducible recipe for transferable logic beyond plausible conversation. Model training and corpus preparation in this stage use no paid compute, proprietary model APIs or private trace inputs. Earlier controls and failures remain preserved, and the sealed final holdout stays reserved. This is an AI-assisted engineering record of aggregate methods and results; raw corpus text and private logs are not published. See the [current plan](/model-training-journal/current-plan/) for the latest reviewed decision.
