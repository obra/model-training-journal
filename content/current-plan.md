The current experiment, its evidence, and the next decision. This is an AI-assisted engineering record, not live telemetry.

**Verified snapshot: 26 October 2026, 18:11:04 UTC.** The 97,536,768-parameter model started from random weights. No planning checkpoint has been promoted as useful or reliable.

## Current stage: document rights and validation review

**No new candidate records have been admitted to training or validation, and broader pretraining has not started.** Training and evaluation remain idle in the 18:11:04 UTC status snapshot. The immediate task is to establish usable document-level text, rights, provenance and validation evidence before selecting a continuation corpus.

The original final planning holdout remains reserved, unevaluated, and excluded from training. A completed download, document review or lexical audit is a measurement milestone, not a model-capability result or permission to use an entire collection.

## Nineteen validation candidates, with a limited overlap result

A deterministic survey selected 36 complete Taskmaster conversations for record review before consulting model losses. Seventeen were excluded for unresolved identity/contact information, outside prose, incomplete source material, or a failed collection. **Nineteen conversations remain candidates**, totaling 438 turns across six instruction groups. They are a small, selection-biased diagnostic, not the originally balanced nine-group set or an admitted validation benchmark. The entire Taskmaster family and its derivatives remain excluded from training.

The completed historical overlap audit checked those candidates against **10 listed inputs**: prior base training, the previous language-validation text, and eight distinct supervised-training corpora. It scanned 59,928 source records and 360,599 document/message units. Those are coverage counts, not unique works or new training tokens. Complete input hashes matched, and the inputs stayed unchanged during scanning.

All **29,366 source–validation unit pairs with a detected match** received the limited-shared-language classification. There were **zero normalized-exact or stronger-threshold lexical matches**. This is a bounded lexical result, not proof of independence: paraphrases, translation, unlisted origins and short embedded passages can escape it. Turns shorter than eight words receive whole-unit exact checks only, without substring search.

Any eventually admitted broader text must be added and rescanned before the validation set is frozen. Source-family exclusion still depends on provenance beyond the detector. The audit does not repair the old textbook validation split's known overlap risk, and none of the 19 candidates has been admitted by this check.

Read the [document-rights and validation milestone](/model-training-journal/2026/10/26/document-rights-and-validation-candidates/) for the review scope, exclusions and detection limits.

## Training-corpus eligibility remains unresolved

The document review establishes limitations rather than an eligible-token yield:

- **DOAB:** 24 sampled records span 13 parent books. Twelve short records were read fully; twelve longer records received only boundary and notice/provenance inspection, leaving their interiors unreviewed. Individual article or chapter notices must be distinguished from compilation rights and credited outside material. Extraction can join multiple works, scramble text, or combine a correction with its original article. Two priority candidates are not two admitted documents, and no eligible unique-token yield is established.
- **Hansard:** the acquired written-answer material differs from the originally proposed debates subset. It is deferred from the first continuation unless a useful, cleared subset can be established; Senedd remains excluded. A generic archive license label is not passage-level clearance.
- **arXiv:** a further bounded archive inspection found 10,096 candidate records, but the released extraction's exact source-version lineage remains unresolved. The archive serves only as an ID catalog for a proposed exact-version official-HTML pilot. The 17:52:33 UTC milestone records a frozen 25-ID selection and two saved official responses; parsing/review and admission had not run at that milestone. Saving an official response does not establish complete extraction or clear every included passage.

Source attribution, rights exceptions, personal information, extraction integrity and overlap remain gates before admission. No raw candidate conversations, book text or HTML responses are published here. There is no claim that a collection is uniformly permissive or that enough new text will qualify.

## Reflection and correction results

The reflection diagnostic used the repetition-arm checkpoint and **three selected known failures**: a wrong-task write, a wrong-duration suggestion after permission withdrawal, and a completion claim without a write. The model received the saved visible history and explicit feedback identifying the error. It returned two irrelevant questions about duration and one calendar-read action despite the offline message-only request. No coherent actionable self-diagnosis was available to turn into a model-derived hint condition.

The follow-up compared the original baseline, a generic rechecking instruction, and an independently written procedural hint on each same case:

| Selected failure | Baseline | Generic recheck | Procedural hint |
|---|---|---|---|
| Update the requested task | Wrong task changed | Wrong task changed | Wrong task changed |
| Suggest the requested 35 minutes after write permission was withdrawn | 20-minute suggestion | 20-minute suggestion | 30-minute suggestion |
| Create the requested task before claiming completion | Read only; false completion | Read only; false completion | Read only; false completion |

The duration hint changed the answer but did not make it correct. All three variants respected the withdrawn permission by making no calendar write; that did not make the suggested interval valid. A successful receipt for the wrong task also did not make its completion claim true.

A separate independent requested-outcome review is now complete: **0 of the nine selected follow-ups satisfied the full request**, with six false completion replies and three incorrect time suggestions. All 24 generated action envelopes parsed; syntax validity did not establish correct action. The cases were chosen because they already failed, include different source populations, and received supplied assistance. This is an assisted diagnostic on three known cases, not a generalization benchmark or evidence of the model's internal cause. No training on the reflections occurred, and the final holdout was not used.

The [completed reflection and first corpus audit](/model-training-journal/2026/10/26/reflection-and-corpus-audit/) records these measurements; the earlier [experiment plan](/model-training-journal/2026/10/26/reflection-then-broader-pretraining/) preserves what was proposed beforehand.

## Open-ended language samples

The completed language probe contains **nine greedy samples from two checkpoints**: three plain continuations from the original base, three plain continuations from the repetition-arm supervised checkpoint, and three chat-format requests to that supervised checkpoint.

- The base continuations became repetitive and did not retain the supplied fact in the short context-fact example.
- The supervised continuations produced repetition or fragments of the learned planning format, rather than useful continuations.
- All three supervised chat samples returned the same stock completion text and cited a receipt that the probe had not supplied. They did not answer the requests.

These are small qualitative observations, not a representative conversation benchmark or human-rated quality score. The base and supervised runs used different context ceilings, 1,024 and 1,536 tokens, and continuation versus chat prompts are different test formats. The evidence does not isolate a model-size ceiling or establish that broader pretraining will fix these failures.

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
3. **Continue only if enough new text clears the gates.** Preserve the original 100M-token base as control and retain the same 97.5M-parameter architecture and tokenizer. The ceiling remains **200M additional valid tokens**. The earlier full-run proposal required at least 100M new unique eligible tokens, both selected training families represented, and at most two exposures per document. A 50–100M-token yield would reduce the target; less than 50M would be a data bottleneck. The usable source mix and yield are still unsettled, so no launch gate has been cleared. Replaying the old pool would not establish broader data coverage.
4. **Compare both bases with identical supervision and evaluations.** Apply the same pinned supervised recipe, decoding and task evaluations to the original-base control and continued base. Report independent language loss, frozen generation probes, requested outcomes, wrong-object writes, false completion, missing answers and retention separately. The final planning holdout remains reserved.

The original base completed 100M exposures on a 26.91M-token inventory, about 3.7 nominal passes. The proposed continuation adds both data and optimization exposure and would use a fresh optimizer; it tests that whole intervention, not a pure causal effect of diversity. A matched old-corpus continuation has not been run.

No checkpoint is promoted, and **there is no commitment to a 1B-parameter model**. Scaling the earlier measured training-invocation rate to 200M additional tokens gives an arithmetic estimate of about 3.72 hours. That earlier rate already included its own initialization, validation and checkpoint overhead; new packing, acquisition, checkpointing and evaluation can change actual elapsed time. This remains an estimate, not an active or completed run.

## Fixed time budget

The 120-hour experiment began **26 October 2026 at 04:12 UTC** and ends **31 October 2026 at 04:12 UTC**. At this snapshot, **106 hours 0 minutes** remained. The deadline and resource limits have not been extended.

The header counts down using the reader's device time. It does not query the training system or refresh these facts. Status becomes visibly stale after one hour; without JavaScript, the timestamp and time remaining at the snapshot remain visible. A newer publication is required to update the experiment state.

Browse the [experiment index](/model-training-journal/experiments/) for the full sequence. Historical posts retain what was known at their own snapshots. Raw logs, source datasets, private machine details and held-out scenario contents remain outside the public journal.
