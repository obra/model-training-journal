The current experiment, its evidence, and the next decision. This is an AI-assisted engineering record, not live telemetry.

**Verified snapshot: 26 October 2026, 16:36:53 UTC.** The 97,536,768-parameter model started from random weights. No planning checkpoint has been promoted as useful or reliable.

## Current experiment: diversity versus repetition

Both training arms of `binding-diversity-v1` have completed **1,999,822 assistant labels each**, across 13,338 optimizer steps per arm. The evaluation queue completed at **16:36:53 UTC** and results review is underway. No training or evaluation job is active in this notebook snapshot. The original final holdout remains reserved, unevaluated, and excluded from training.

The hypothesis is that **more distinct examples of matching a request to the correct object and action may transfer better than replaying a small set**, when training exposure is held constant. This follows earlier experiments where correct-looking tool calls still changed the wrong item or supported false completion claims.

The two arms start separately from the same preserved 100M-token base checkpoint, with the same tokenizer, optimizer configuration, context length, and token-based learning-rate schedule. Each receives 1,693,854 canonical assistant labels and 305,968 repair labels. The repetition arm uses 100 distinct repair anchors; the fresh arm uses 1,916. The executed label counts and schedule match. Prompt lengths differ slightly, so this is not a claim of identical total input-token exposure.

See the [diversity experiment record](/model-training-journal/2026/10/26/diversity-versus-repetition/) for preparation, controls, and training completion.

## Latest completed evaluation slice

These results concern the **new 96-case development suite**: a 64-case core plus 32 stress cases. They are provisional automated audits of completed evaluations within a larger study whose evaluation queue has completed but interpretation is unfinished. They are not the earlier 64-case binding study, a training-fit sample, or the final holdout.

| New 96-case development check | Repetition arm | Fresh-diversity arm |
|---|---|---|
| Exact requested states | 28/96 | 26/96 |
| Covered false completion claims | 51 | 33 |
| Cases with an applied wrong-object write | 40 | 24 |
| Missing final answers | 17 | 37 |
| Cases with unresolved requested-state / wrong-object scope | 5 | 0 |

The core/stress breakdown is **23/64 plus 5/32** exact states for repetition and **22/64 plus 4/32** for fresh diversity. Neither panel establishes a gain.

Raw and runtime-guarded evaluations produced these same aggregate counts **separately**; the modes are not pooled into 192 cases. Guarding did not turn the result into reliable task completion.

Fewer counted false claims or wrong-object writes do not establish a better model here: exact requested outcomes did not improve, while missing answers rose sharply. Unresolved cases, bounded claim-checking vocabulary, correlated generated examples, and transcript review all limit interpretation. These numbers are not a general safety estimate or a measure of progress toward intelligence.

## How the experiment reached this point

- **Base pretraining completed:** 100M valid token exposures on a 26.91M-token training inventory, roughly 3.7 nominal passes. The [base milestone](/model-training-journal/2026/10/26/first-100m-token-base/) records the completed run. A later [overlap audit](/model-training-journal/2026/10/26/auditing-textbook-overlap/) found contamination risk in language validation; its loss cannot establish independent generalization. [Filtered sensitivity probes](/model-training-journal/2026/10/26/validation-sensitivity-probes/) do not remove that limitation.
- **Planning remains unsuccessful:** the [first matched comparison](/model-training-journal/2026/10/26/first-planning-comparison/) scored 0/80 development successes for both random-plus-supervision and base-plus-supervision. Later serialization repairs and longer training improved some training-fit measurements without establishing useful planning.
- **Year diversity did not solve transfer:** in a separate 48-case fresh transfer probe, year-diverse training produced 8 requested outcomes versus 10 for the canonical comparator, with neither succeeding on the unseen years 2000 and 2044. [The year-diversity result](/model-training-journal/2026/10/26/year-diversity-results/) records regressions and the decision not to promote it.
- **The earlier binding study traded gains for damage:** on its separate 64-case binding development set, exact requested states rose from 3 to 9, but false completion claims rose from 28 to 40 and cases with applied wrong-object writes from 21 to 29. [Those results](/model-training-journal/2026/10/26/counterfactual-binding-results/) motivated the present matched diversity test; they must not be compared directly with the newer 96-case totals.

## Next decision

Review the completed evaluation queue, paired results and retained transcripts before selecting another training change. The comparison must consider exact requested outcomes, wrong-object damage, completion truth, unsupported failure explanations, missing answers, unresolved cases, and retention on older tasks together. Training-fit checks remain separate from development transfer.

No winner is established by the current slice, and no checkpoint is promoted. If broader diversity fails to improve correct actions without shifting failures into silence or regressions, the next hypothesis must change; repeating exposure alone is not evidence of progress. Final-holdout evaluation remains reserved for a defensible milestone rather than routine iteration.

## Fixed time budget

The 120-hour experiment began **26 October 2026 at 04:12 UTC** and ends **31 October 2026 at 04:12 UTC**. At this snapshot, **107 hours 35 minutes** remained. The deadline is fixed and has not been extended.

The header's clock counts down to that deadline using the reader's device time. It does not query the training system or refresh these results. The status becomes visibly stale after one hour; without JavaScript, the header retains the timestamp and time remaining at the snapshot. A newer publication is required to update the experiment state.

Browse the [experiment index](/model-training-journal/experiments/) for the full sequence. Historical entries retain what was known at their own timestamps; this page brings the reviewed plan and status together. Raw logs, source datasets, private machine details, and held-out scenario text remain outside the public journal.
