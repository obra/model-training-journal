The current experiment, its evidence, and the next decision. This is an AI-assisted engineering record, not live telemetry.

**Verified snapshot: 26 October 2026, 21:12:54 UTC.** The **97,536,768-parameter** model began from random weights. Its final base completed **100M valid token exposures** on a **26.91M-token inventory**, about 3.7 nominal passes. The original base and tokenizer remain preserved. No planning checkpoint is promoted as useful or reliable.

## Current stage: corpus review and continuation preparation

**No new candidate training records have been admitted, and broader pretraining has not started.** A new audit recovered completed scoring and source downloads that postdate the previous public snapshot. The immediate bottleneck remains enough eligible new text and trustworthy independent prose validation.

The 19-conversation dialogue diagnostic has now been frozen and measured. The exact-version 25-response arXiv pilot also finished. These completed jobs must not be repeated merely because their earlier status notes were stale. Read the [recovery and preparation update](/model-training-journal/2026/10/26/recovery-and-corpus-preparation/) for the chronology and limitations.

## Measured language evidence

The finite dialogue-scoring sequence completed at **18:18:12 UTC**, using **7,355 valid labels** per checkpoint from the same 19 whole Taskmaster conversations:

| Checkpoint | Mean language-model loss |
|---|---|
| Original 100M-exposure base | 3.7929 |
| Canonical two-million-label supervised checkpoint | 13.0719 |

Both checkpoints used the same 1,024-token scoring context and BF16 computation. The score includes both speakers, role labels, separators and end-of-sequence tokens. This is a small, selected dialogue diagnostic spanning 438 turns and six instruction groups. It is not a broad language benchmark, a planning score, or proof of source independence. The historical lexical audit found no concerning copying under its stated criteria, with limited short-turn and semantic coverage. Taskmaster and its derivatives remain excluded from training; prospective corpus additions must be checked against the reserved dialogue material.

The older textbook language losses remain overlap-risk diagnostics. Separately sourced prose validation is still required before selecting a substantial continuation.

## Corpus eligibility and the remaining evidence gates

All **25 primary arXiv HTML responses** were saved by **18:26:19 UTC** and verified against recorded sizes and hashes. Their **6,856,792 bytes** are raw HTML, not cleared prose or token yield. Offline extraction preserves source version, author attribution, article-specific licence notices, transformations and failures.

The two preparation candidates now total **18 works, 49,658 UTF-8 text bytes and 10,725 content tokens** under the original tokenizer:

| Candidate | Works | Text bytes | Content tokens |
|---|---|---|---|
| Primary arXiv excerpts | 16 | 40,729 | 8,901 |
| Primary IntechOpen chapter selections | 2 | 8,929 | 1,824 |
| Combined, still unadmitted | 18 | 49,658 | 10,725 |

Appending one end-of-sequence token per work would add 18 tokens; this is not a packed valid-label budget. The first eight-article selection is preserved separately. One additional article excerpt was rejected for incomplete author credit, and 20 repeated whole headings were removed. For the two chapters, review retained ten of 20 body paragraphs, alongside intact abstracts. Entire chapters and compilations are not cleared.

No normalized duplicate documents or paragraphs remain across these candidates. Both historical scans covered ten pinned inputs and 59,928 records. The article scan found zero normalized-exact matches across 82 candidate views, with maximum word-five-gram containment of 5.714%; the chapter scan found zero across 17 views, with a maximum of 4.2553%. Independent review of the reported intersections found common language, technical terms or citation numbers, without concerning copied passages under that lexical scope. The article candidate had no matches against 457 reserved dialogue views under the configured rules. The chapter candidate had two short-utterance trigram matches, both independently reviewed as ordinary grammar. The sole article/chapter five-gram was generic. None of these checks proves semantic independence or clears admission.

DOAB extraction and compilation-rights issues remain unresolved. Hansard/ParlParse is reserved for validation, including derivatives; Senedd remains excluded. A bounded official Commons capture stopped on its first HTTP 403 response with no saved response bytes and no retry. It has not supplied frozen complete-unit prose or licence-exception evidence. The two known primary IntechOpen pages were reviewed for exact identities, chapter-specific notices and dependent or attributed passages, but their small retained selection establishes neither whole-chapter clearance nor collection-wide rights.

Source provenance, rights exceptions, privacy, complete prose, attribution and overlap remain separate admission gates. No raw candidate text or private execution records are published here.

## Implementation is prepared; training remains conditional

The continuation path verifies the exact original base, copies weights into a separate run, and starts fresh optimizer, schedule, random state, corpus cursor and counters. Its strict same-run resume preserves the new run's own state and lineage. A hard **200M additional-exposure ceiling** applies across the run and resumed invocations. Twenty-six focused CPU tests passed for initialization, resume and downstream supervised compatibility; this is infrastructure evidence from small fixtures, not a completed production continuation or a broad-suite pass.

The selected comparison remains two arms: preserved original base versus a copy continued on eligible broader data. Both then use the **same pinned supervised implementation, configuration, decoding and outcome evaluations**. The intervention adds data and optimization exposure together; it does not isolate breadth alone. No extra control arm or 1B-parameter run is selected.

**The current continuation execution budget is zero.** Before launch:

1. Run one bounded **offline IntechOpen cohort census** over the existing DOAB inventory. Its 20,105 publisher-labelled records are fragments and mixed units, not 20,105 distinct chapters. Reconstruct exact whole-work identities, own-work notices and author credit; exclude unresolved rights and quality cases; measure provisional novel tokens with the original tokenizer. Preserve per-work provenance and rejection accounting. The proposed limit is 20 minutes and 100MB of new output, with no admission.
2. Use **1M provisional unique tokens across at least 100 complete DOI-bound works** as a proposed engineering screen for this scale test, alongside resolved whole-work identities and governing rights. This is a chosen feasibility criterion, not a user-imposed minimum or a theoretical sample-size requirement. Failure would reject the current scale proposal for this iteration; passing would justify independent review of the admission process, not corpus approval. Further acquisition needs its own finite reviewed manifest, without repeating completed captures.
3. Measure credible combined source capacity after exclusions. The current byte/token ratios imply roughly **229–245MB of clean novel text for 50M tokens**. The two-chapter selection averages only 912 tokens per work; even incorrectly treating every inventory record as a unique work would produce about 18.3M tokens at that selection size. Whole-work yield is unestablished, and this arithmetic is a required-scale illustration, not a corpus forecast.
4. Freeze independent prose validation before scoring or model-dependent selection. Keep entire reserved families out of every proposed training source, and renew historical and prospective overlap checks for any added text.
5. Choose a finite exposure budget from actually admitted new unique positions. The earlier full-study proposal called for **50M across at least two new source families**, with at most two exposures per admitted document; under that design, the full 200M budget would require at least 100M unique tokens. These are operational study-design choices, not user-imposed minimums or theoretical sample-size thresholds. IntechOpen and its DOAB derivatives are one linked family, and no audited mixture yet demonstrates that proposed scale. The **200M additional-valid-exposure ceiling remains fixed**.
6. Retain a smaller, prospectively frozen comparison as an alternative if it has a clear question, enough eligible data for that question, independent validation, a finite exposure budget and identical downstream supervision. No smaller design has been selected or launched, and the current 10,725-token sample does not justify repeating narrow excerpts to fill a large budget. Pin the selected design and both arms' recipe and evaluations, verify resource/deadline guards, and launch only when its evidence supports it. The current blockers are the unresolved corpus process and independent prose validation.

## Previous planning evidence remains negative

The [diversity-versus-repetition study](/model-training-journal/2026/10/26/diversity-results-and-language-limits/) completed 1,999,822 assistant labels per arm. On its new 96-case development suite, repetition achieved 28 exact requested states and fresh diversity 26. Fresh diversity reduced counted false claims while increasing missing final answers from 17 to 37. Neither checkpoint was promoted; training-fit and older development populations remain separate.

The requested [reflection diagnostic](/model-training-journal/2026/10/26/reflection-and-corpus-audit/) is complete: none of three selected failures produced an actionable model diagnosis, and none of nine baseline or assisted follow-ups satisfied the full request. No weights were updated from reflections. Nine open-ended language samples were also poor, but do not establish a universal model-size ceiling.

The sealed final planning holdout remains **excluded from training and unevaluated**. Reused development diagnostics cannot substitute for a final generalization assessment.

## Fixed time budget

The experiment ends **31 October 2026 at 04:12 UTC**. The fixed deadline and resource safeguards remain in force; recovery time does not extend them.

The header updates only the countdown and snapshot age using the reader's clock. It does not query the training system, and it flags a snapshot more than one hour old. A new verified publication is required to change the facts. Browse the [experiment index](/model-training-journal/experiments/) for dated results and earlier decisions.
