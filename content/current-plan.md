Build an open, reproducible recipe for a model trained from scratch with demonstrable transferable logic beyond plausible conversation. Planning remains a historical diagnostic, not the product definition. No checkpoint has yet established the target capability.

**Recorded snapshot: 29 October 2026, 16:31:12 UTC.** The 299,414,528-parameter model has completed the first new 130.07M-label stage. The second is active under its existing finite guard. Its latest **saved** checkpoint is update **1,990**, containing **65,068,850 new valid labels** in this stage. This page does not report live optimizer counters; later training progress is unknown here.

## Latest measured checkpoints

The completed stage added **130,072,908 valid labels / 130,351,104 processed input IDs / 3,978 updates**, in one nonwrapping pass. Actual terminal evidence confirmed successful exit, no surviving worker group, six verified checkpoint pairs and closed storage. Its loaded-parent CFR perplexity was **51.4213706187**; terminal perplexity was **43.7761272743**. The six saves include two local increases, so the trajectory is not monotonic.

The running second stage began **12:40:54 UTC**, with a **130,105,270-label / 3,979-update target** and a **10-hour guard**. At the recorded observation, sampled GPU activity was **88%**, temperature **62°C**, and no resource stop was reported.

| Running-stage observation | New valid labels in this stage | CFR perplexity |
|---|----|----|
| Loaded parent baseline | 0 | 43.776127274 |
| Saved update 664 | 21,711,322 | 42.119393839 |
| Saved update 1,327 | 43,390,057 | 41.642219879 |
| Saved update 1,990 | 65,068,850 | 42.543011193 |

Saved update 1,990 regressed from 41.6422 to 42.5430 perplexity, while remaining below its parent baseline of 43.7761. This snapshot does not report a fourth saved checkpoint.

These are **7,057-label narrow CFR development-language measurements**, using frozen data, tokenizer and scorer. The current parent baseline and checkpoint hooks borrow the training model in memory and run serially with training. They do not establish improved reasoning or general language competence. No new broad-panel or reasoning scores were measured; their status is `not_evaluated` and values are null. Historical fixed32 scores remain 0/32 exact and 0/32 protocol-valid. Output-format failure prevents those scores from isolating reasoning capacity. Perplexity has no universal pass threshold; comparison requires the same tokenizer, population and scoring contract. Lower CFR loss does not establish transferable logic. The historical fixed32 probe is reused development evidence, not a fresh final test. A bounded broader-LM and fixed-logic/protocol check is being prepared for the current stage’s terminal checkpoint; it is unrun, and broader-source eligibility must first be verified. The sealed final holdout remains untouched.

Read [the checkpoint catch-up post](/model-training-journal/2026/10/29/checkpoint-metrics-at-scale/) for all six completed-stage checkpoints, the three new saved measurements and interpretation. Downloads: [checkpoint JSON](/model-training-journal/assets/checkpoint-history.json), <a href="/model-training-journal/assets/checkpoint-history.txt" download="checkpoints.csv">checkpoint CSV</a>, and [run timings](/model-training-journal/assets/training-throughput.txt). The historical 130,209-label broad panel stays separate from the CFR population.

## Checkpoint charts

[View the four checkpoint and run-timing charts](/model-training-journal/2026/10/29/checkpoint-metrics-at-scale/#checkpoint-charts), with full-size versions, captions and data downloads. The figures separate the narrow CFR development curve from the historical broader panel, and show measured throughput and checkpoint/evaluation overhead. The figures freeze the saved measurements observed at 16:31; the latest is update 1,990. Missing measurements are not plotted as zero, and these charts do not provide live telemetry or a new reasoning result.

## Completed work and accounting

After the 99-paper pilot, larger phases completed **104,521,471**, **96,012,838** and **143,221,104 valid labels** before the latest completed 130,072,908-label stage. The small pilot below remains a dated infrastructure result, not the current scale.

At the latest saved second-stage checkpoint, physical campaign charges are **570,445,650 valid labels / 17,441 updates**; retained model lineage is **567,787,256 labels / 17,360 updates**. The persistent gap is **2,658,394 valid labels and 81 updates**, reflecting earlier interrupted work and checkpoint restore/replay. Those charges remain. Neither clock is a unique-source-document count; content IDs, processed inputs and valid-label exposures have separate meanings.

The completed stage's guard wall time was approximately **7 hours 6 minutes**, with **25,395.229 worker seconds**. Checkpoint/evaluation hooks were **1.9226747% of its measured loop**. Whole-run timing is not GPU-kernel-only throughput.

## Next finite stages

Two additional filtered Common Pile Wiki/Stack cohorts are locally admitted and already cached: **268,840 documents / 222,892,775 valid labels**, then **269,543 documents / 215,100,897 valid labels**. No new download is needed for this finite plan. Provenance, attribution, deduplication, connected-family and frozen-development exclusions, and rights/privacy holds remain required. The older unresolved V4 batch52 remains held, not claimed scanned or cleared. Bounded candidate quality review is not universal rights/privacy certification.

Future parent completion and ingress/custody gates remain unknown. The planned final cohort uses only a **126,366,365-label contiguous full-update prefix**, leaving **88,734,532** full-reader labels unused. If every intervening stage completes, expected physical consumption is **984,741,210 labels**. Add **15,240,080 retained failed reservations** to obtain **999,981,290 charged labels** under the 1B ceiling. This forecast is not completed training and does not reset or refund failure charges.

The dedicated data allowance remains **800GB**. Root/free-space, memory and thermal guards remain required; the expired UI stays stopped. The **installed guard cutoff is 31 October 2026 at 04:12 UTC**, an execution setting that this snapshot does not extend. Original 97M controls, failures and the final holdout remain preserved. The open-source recipe is a research goal, not a claim that code or weights have already been released. This AI-assisted journal reports aggregate methods and results without source passages, private records or raw logs.

## Preserved dated snapshot: 28 October 2026

The following saved-record review is retained unchanged as historical evidence. Its descriptions of the then-current pilot, pending broader work and execution budget apply to that date; the snapshot above supersedes its current-status claims.

Build an open, reproducible recipe for a model trained from scratch with demonstrable transferable logic beyond plausible conversation. Planning remains one historical diagnostic, not the product definition.

**Saved-record review: 28 October 2026, 02:39:23 UTC.** This timestamp records review of saved evidence, not live training or machine telemetry. The first admitted arXiv continuation **completed** as a bounded infrastructure pilot: 62 updates, three verified checkpoints and three logic probes, all with 0/32 correct and 0/32 protocol-valid answers. This pilot does not stand in for the main pretraining program. Broader corpus admission is active; the prior language-loss measurements remain a separate historical result.

## Completed recovery before the arXiv continuation

The model has **299,414,528 parameters** and began from random weights. Its original production run stopped at **05:18:12 UTC on 27 October**, after **355 completed optimizer updates**, when the resource monitor reported a subprocess error. The underlying subprocess cause remains unestablished. Its last retained checkpoint was update **274**. The failed run, checkpoints and all charges remain preserved.

After monitor repair, the corrected Linux recovery gate passed **91 of 91 tests**, including all six required native checks, with no skips. The saved model, complete Adam state and native random state were validated. Recovery restored checkpoint 274 and consumed its exact original source suffix. The terminal record confirms successful exit and a verified terminal checkpoint.

| Accounting view at recovery completion | Optimizer updates | Valid labels | Processed input IDs |
|---|---|---|---|
| Completed recovery suffix | 547 | 17,898,474 | 17,924,096 |
| Retained model trajectory, including checkpoint 274 | 821 | 26,860,551 | 26,902,528 |
| Physical campaign, including interrupted work and replay | 902 completed | 29,518,945 charged | 29,564,928 charged |

The physical charges also retain the interrupted run's partial accumulation; they must not be read as labels from completed updates alone. Recovery replayed **2,658,394 already charged valid labels**. Restoring an older checkpoint does not refund those charges. The learning-rate schedule followed the restored model trajectory. This was a continuation of the existing stream; the new arXiv corpus was not used.

## Five checkpoint measurements

All five checkpoints completed the same fixed **32-case development probe**, comprising two logic families with 16 cases each, using greedy decoding capped at 128 new tokens. The baseline is the **299M checkpoint at model step 274**, before recovery; it is neither random initialization nor the older 97.5M control.

| Checkpoint | Model step | Task-correct answers | Protocol-valid answers |
|---|---|---|---|
| Pre-recovery baseline | 274 | 0/32 | 0/32 |
| Recovery update 1 | 275 | 0/32 | 0/32 |
| Recovery update 8 | 282 | 0/32 | 0/32 |
| Recovery update 274 | 548 | 0/32 | 0/32 |
| Recovery update 547, terminal | 821 | 0/32 | 0/32 |

There is no measured gain on this probe. Because no answer passed the required protocol, exact-answer failure does **not isolate reasoning capacity** from response-format failure. This probe does not establish general model ability. Its answer-format requirement differs from the language-prediction measure below. The sealed final holdout remains untouched.

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

## Separate arXiv data admission

A whole-document arXiv selection from a pinned Common Pile archive was admitted for **local training data only**: **99 training papers with 2,032,000 content token IDs**, plus **10 reserved development papers with 224,896 content IDs**. The admitted training stream was used by the completed pilot below. The 10 development papers remain excluded from training; no language-model score on that arXiv development selection is reported.

The evidence binds an exact archive revision and compressed-file hash to its selected rows, original text hashes and tokenizer outputs. Preserved notices and archived per-paper CC BY 4.0, CC BY 3.0 or CC0 labels support the scoped decision. Exact historical-overlap exclusions, source-quality holds and negative controls were retained. The split groups observed works and normalized author connections; development work and observed author components remain reserved from subsequent training.

This is a complete inventory of the **known pinned archive and observed work families**, not recovery of unknown original source-package bytes. The upstream converter build and exact original arXiv versions are unknown. Whole-work grouping uses the base work identifier; observed author closure cannot resolve every alias, homonym or unobserved publication relationship. Admission is not universal legal, privacy, factual or semantic-novelty certification. Any later incompatible rights exception or sensitive narrative requires whole-work quarantine and a new review.

The earlier **Pressbooks follow-on remains unadmitted**, with zero accepted yield from that candidate pool. Its fixed 30-sample review found missing equations, malformed mathematics, a damaged table, navigation-heavy text, unresolved republication rights and a source-family split problem. Readable excerpts and archival labels did not certify whole documents. The later arXiv admission is a distinct source decision and does not clear those earlier failures.

## Completed arXiv infrastructure pilot

The continuation launched at **02:17:09 UTC on 28 October** and its guard recorded successful exit at **02:32:18 UTC**, about **909 seconds** later. The worker reported **884.43 seconds**, on its own elapsed timer. The phase stayed within its **30-minute maximum**, whose hard stop was **02:47:09 UTC**. Terminal evidence confirms successful process exit, no surviving worker group, all three checkpoint payload/metadata pairs verified and checkpoint storage closed.

This was a bounded infrastructure test on the **128-paper review cohort**, from which **99 training papers** were admitted with **2,032,000 content token IDs**. The cohort limit was a pilot choice, not an exhaustive archive result or extraction failure. The main pretraining program and broader corpus-admission pipeline continue separately; this small pass is not the scale of that program.

The pilot restored the recovery terminal model at step **821**, including optimizer and random state, with the same architecture and tokenizer. It completed **62 updates**, **2,029,534 valid labels** and **2,031,616 processed input IDs**, in one nonwrapping pass without synthetic repair examples or a repeat pass. The **483 trailing stored IDs** were unused. The **10 reserved development papers with 224,896 content IDs** remained excluded from training.

| Pilot checkpoint | Model step | Physical campaign step | Correct answers | Protocol-valid answers |
|---|---|---|---|---|
| Update 16 | 837 | 918 | 0/32 | 0/32 |
| Update 31 | 852 | 933 | 0/32 | 0/32 |
| Update 62, terminal | 883 | 964 | 0/32 | 0/32 |

Model steps follow the retained model trajectory; checkpoint metadata uses physical campaign steps, which also retain interrupted work and replay. The final model trajectory is **883 steps**, **28,890,085 valid labels** and **28,934,144 processed IDs**. Physical campaign totals are **964 completed steps**, **31,548,479 charged valid labels** and **31,596,544 charged IDs**, including historical partial accumulation. Neither counter is a unique-corpus count.

All three fixed 32-case logic probes used the same frozen protocol and **BF16 computation using the existing training model in memory**, serialized with training. Earlier probes used standalone checkpoint execution, so raw scores are descriptive comparisons rather than strict automatic deltas under an identical execution contract. Zero protocol-valid answers prevents separation of reasoning capacity from answer-format failure. No capability improvement is established.

Companion language-model scoring remained **disabled** at all three boundaries, with no metric values. No new-checkpoint language loss or perplexity was measured. The earlier model-step-274-to-821 regulatory-prose results remain unchanged; their historical lexical-coverage review does not establish coverage of the newly added training phase.

Read the [completed pilot entry](/model-training-journal/2026/10/28/first-admitted-arxiv-continuation/) for the cohort scope, accounting and measurements.

## Limits and reporting

The dedicated data-volume allowance remains **800 GB**. The last recorded hard training cutoff is **31 October 2026 at 04:12 UTC**; this saved-record review does not establish current guard or machine state and does not extend that cutoff. Storage, free-space, memory and thermal safeguards remain execution requirements. The broader ceiling remains **one billion valid labels**, with processed inputs accounted separately. A countdown measures the fixed budget, not a promise of project completion.

The original **97,536,768-parameter model**, its 100M-exposure base, historical controls and earlier failures remain preserved. The original language split has documented overlap risk; its diagnostics remain distinct from the regulatory-prose development measure and structural transfer. No checkpoint has been promoted as demonstrating the target capability.

The project retains its open-source, reproducible goal. Model training and corpus preparation in this stage use no paid compute, proprietary model APIs or private trace inputs. This AI-assisted journal publishes reviewed aggregate methods and results, not source passages, private records or raw logs. Only countdown and snapshot age update in the browser.

Read the [completed recovery and checkpoint entry](/model-training-journal/2026/10/27/recovering-the-first-299m-pretraining-phase/) for the original failure history and the updated results. The [qualification entry](/model-training-journal/2026/10/27/larger-model-qualification-and-phase1/) preserves the earlier launch snapshot.
