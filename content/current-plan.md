The current experiment, its evidence, and the next decision. This is an AI-assisted engineering record, not live telemetry.

**Verified snapshot: 26 October 2026, 17:07:16 UTC.** The 97,536,768-parameter model started from random weights. No planning checkpoint has been promoted as useful or reliable.

## Current stage: corpus rights and provenance review

The bounded reflection checks and small language probe have completed. Acquisition and structural inspection of three candidate source files finished at **17:07:15 UTC**, but **zero candidate records have been admitted**. Broader pretraining has not started, and no training or evaluation job is active in this snapshot.

The immediate task is to establish actual record rights, provenance, source-family separation, privacy and overlap, then freeze independent validation and count eligible new tokens. A successful download or parser run does not establish permission or training suitability. The original final planning holdout remains reserved, unevaluated, and excluded from training.

## Reflection and correction results

The reflection diagnostic used the repetition-arm checkpoint and **three selected known failures**: a wrong-task write, a wrong-duration suggestion after permission withdrawal, and a completion claim without a write. The model received the saved visible history and explicit feedback identifying the error. It returned two irrelevant questions about duration and one calendar-read action despite the offline message-only request. No coherent actionable self-diagnosis was available to turn into a model-derived hint condition.

The follow-up compared the original baseline, a generic rechecking instruction, and an independently written procedural hint on each same case:

| Selected failure | Baseline | Generic recheck | Procedural hint |
|---|---|---|---|
| Update the requested task | Wrong task changed | Wrong task changed | Wrong task changed |
| Suggest the requested 35 minutes after write permission was withdrawn | 20-minute suggestion | 20-minute suggestion | 30-minute suggestion |
| Create the requested task before claiming completion | Read only; false completion | Read only; false completion | Read only; false completion |

The duration hint changed the answer but did not make it correct. All three variants respected the withdrawn permission by making no calendar write; that did not make the suggested interval valid. A successful receipt for the wrong task also did not make its completion claim true.

These observations come from direct inspection of nine saved follow-up traces. Their independent requested-goal review is still marked pending in the source records; this is not a newly audited 0/9 benchmark. The cases were chosen because they already failed, include different source populations, and received supplied assistance. They do not measure generalization or reveal the model's internal cause. No training on the reflections occurred, and the final holdout was not used.

The [reflection experiment plan](/model-training-journal/2026/10/26/reflection-then-broader-pretraining/) records what was proposed before these measurements.

## Open-ended language samples

The completed language probe contains **nine greedy samples from two checkpoints**: three plain continuations from the original base, three plain continuations from the repetition-arm supervised checkpoint, and three chat-format requests to that supervised checkpoint.

- The base continuations became repetitive and did not retain the supplied fact in the short context-fact example.
- The supervised continuations produced repetition or fragments of the learned planning format, rather than useful continuations.
- All three supervised chat samples returned the same stock completion text and cited a receipt that the probe had not supplied. They did not answer the requests.

These are small qualitative observations, not a representative conversation benchmark or human-rated quality score. The base and supervised runs used different context ceilings, 1,024 and 1,536 tokens, and continuation versus chat prompts are different test formats. The evidence does not isolate a model-size ceiling or establish that broader pretraining will fix these failures.

## Candidate acquisition is not corpus admission

The completed inspection records show why the next gate remains substantive:

| Candidate role | What the bounded inspection found | What remains unresolved |
|---|---|---|
| Taskmaster dialogue, proposed for independent language validation only | 5,507 conversations; 1,010 triggered contact-information screening flags | Selected-conversation privacy, rights, provenance, grouped selection and separation from all training; flags are not confirmed personal-data findings |
| DOAB book shard, possible training text | 31,034 records; metadata includes 30,995 CC BY labels and 39 share-alike labels | Actual book/section notices, attribution, exceptions, extraction provenance and overlap; the metadata counts are not counts of eligible records |
| Hansard shard, possible training text | 4,564 records: 542 labeled Senedd and 4,022 labeled written answers | Actual legislature and passage identity, applicable rights and exceptions; a generic Open Parliament Licence label is insufficient |

No independent validation reserve or expanded training corpus is ready in this snapshot. There is no claim that all these collections are permissively licensed or that enough new text will qualify. No candidate text or raw probe transcripts are published here.

## Latest completed evaluation slice

The preceding diversity-versus-repetition study remains negative evidence. Both arms completed **1,999,822 assistant labels each**, across 13,338 optimizer steps per arm. Its **new 96-case development suite** contained a 64-case core plus 32 stress cases:

| New 96-case development check | Repetition arm | Fresh-diversity arm |
|---|---|---|
| Exact requested states | 28/96 | 26/96 |
| Covered false completion claims | 51 | 33 |
| Cases with an applied wrong-object write | 40 | 24 |
| Missing final answers | 17 | 37 |
| Cases with unresolved requested-state / wrong-object scope | 5 | 0 |

Fewer counted false claims or wrong-object writes did not establish a better model: exact outcomes did not improve and missing answers increased. Raw and guarded histories were identical within each arm; these are correlated views, not 192 independent cases. The older 64-case binding development set, training-fit checks, retained calendar cases and final holdout are separate populations. See the [completed diversity results](/model-training-journal/2026/10/26/diversity-results-and-language-limits/) for their distinct results and limitations.

## Next decision

The current hypothesis is that a broader language base may help more than another narrow supervised variant. The reflection and language samples motivate investigating that hypothesis; they do not establish it. Curriculum gaps, optimization, source diversity and capacity remain unresolved explanations.

1. **Audit before admission.** Verify actual record rights and provenance, preserve attribution and source identity, screen selected material for private information, and check exact and bounded near-duplicate overlap against existing training, validation and supervised inputs. Keep rejected and unresolved records out.
2. **Freeze independent validation before measuring loss.** Reserve a source-disjoint dialogue family, with whole-conversation and related-instruction grouping, and exclude that entire family from training. Existing textbook validation has documented overlap risk; filtering a few documents does not make it independent.
3. **Continue only if enough new text clears the gates.** Preserve the original 100M-token base as control and retain the same 97.5M-parameter architecture and tokenizer. The ceiling is **200M additional valid tokens**, conditional on at least 100M new unique eligible tokens with both proposed training families represented and at most two exposures per document. A 50–100M-token yield reduces the target; less than 50M is a data bottleneck rather than a reason to replay the old pool and call it diversity.
4. **Compare both bases with identical supervision and evaluations.** Apply the same pinned supervised recipe, decoding and task evaluations to the original-base control and continued base. Report independent language loss, frozen generation probes, requested outcomes, wrong-object writes, false completion, missing answers and retention separately. The final planning holdout remains reserved.

The original base completed 100M exposures on a 26.91M-token inventory, about 3.7 nominal passes. The proposed continuation adds both data and optimization exposure and would use a fresh optimizer; it tests that whole intervention, not a pure causal effect of diversity. A matched old-corpus continuation has not been run.

No checkpoint is promoted, and **there is no commitment to a 1B-parameter model**. Scaling the earlier measured training-invocation rate to 200M additional tokens gives an arithmetic estimate of about 3.72 hours. That earlier rate already included its own initialization, validation and checkpoint overhead; new packing, acquisition, checkpointing and evaluation can change actual elapsed time. This remains an estimate, not an active or completed run.

## Fixed time budget

The 120-hour experiment began **26 October 2026 at 04:12 UTC** and ends **31 October 2026 at 04:12 UTC**. At this snapshot, **107 hours 4 minutes** remained. The deadline and resource limits have not been extended.

The header counts down using the reader's device time. It does not query the training system or refresh these facts. Status becomes visibly stale after one hour; without JavaScript, the timestamp and time remaining at the snapshot remain visible. A newer publication is required to update the experiment state.

Browse the [experiment index](/model-training-journal/experiments/) for the full sequence. Historical posts retain what was known at their own snapshots. Raw logs, source datasets, private machine details and held-out scenario contents remain outside the public journal.
