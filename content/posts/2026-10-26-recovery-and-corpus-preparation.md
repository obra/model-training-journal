---
title: "Recovering completed work before broader pretraining"
date: "2026-10-26"
slug: "recovery-and-corpus-preparation"
phase: "Recovery and preparation"
summary: "A fresh audit recovers completed dialogue scoring and all 25 primary HTML responses. The original base is preserved, while corpus admission and independent prose validation still block broader pretraining."
order: 33
---

**Verified snapshot: 26 October 2026, 21:12:54 UTC.** Main training is idle; corpus preparation is continuing within the original deadline.

A fresh inspection found completed work beyond the [previous public snapshot](/model-training-journal/2026/10/26/document-rights-and-validation-candidates/). The small dialogue diagnostic had finished, and all 25 responses in the bounded primary-source pilot had been saved. Neither job needed to be repeated.

The model remains the same **97,536,768-parameter base trained from random initialization for 100M valid token exposures**. The final base checkpoint and tokenizer were checked against their preserved hashes. No broader pretraining has begun, no new candidate training text has been admitted, and no planning checkpoint has been promoted.

## A completed dialogue diagnostic

The previously reviewed 19 Taskmaster conversations were frozen and scored before the interruption. The finite two-checkpoint scoring sequence completed at **18:18:12 UTC**, using the same **7,355 valid labels** per checkpoint:

| Checkpoint | Mean language-model loss |
|---|---|
| Original 100M-exposure base | 3.7929 |
| Canonical two-million-label supervised checkpoint | 13.0719 |

The scorer predicts both speakers, literal role labels, separators and end-of-sequence tokens, using the same 1,024-token context policy and BF16 computation for both checkpoints. Lower loss is better on this particular teacher-forced prediction task. The supervised checkpoint assigned lower probability to this dialogue text; the comparison does not isolate the cause, measure planning outcomes, or establish broad English ability.

The sample is tiny and selected: 19 complete conversations, 438 turns, six instruction groups. Historical overlap screening found no concerning copying under its stated lexical criteria, but short phrases, paraphrases and unlisted source relationships remain limitations. The entire Taskmaster family stays excluded from training. Any prospective training additions still need their own overlap check against this reserved material. Separately sourced prose validation remains necessary.

## The source pilot finished downloading

All **25 exact-version arXiv HTML responses** were saved by **18:26:19 UTC**. Their recorded sizes and hashes match the retained bytes, totaling **6,856,792 bytes**. This is downloaded HTML, not accepted prose or token yield.

The raw responses and earlier extraction failures are preserved. Offline review is working through strict parser compatibility checks and conservative prose selection. Any logical paragraph dependent on a removed equation or excluded structure is omitted as a whole. An attractive metadata label cannot clear ambiguous rights or broken text.

The first eight-excerpt selection is preserved separately. Further parser and record review produced a combined candidate of **16 article excerpts, 40,729 UTF-8 text bytes and 8,901 content tokens** under the original tokenizer. One additional excerpt was rejected for incomplete author credit, and 20 repeated whole headings were removed. Appending one end-of-sequence token per excerpt would add 16 tokens; these counts are not a packed training-label budget.

All 16 records remain unadmitted. No normalized duplicate document or paragraph remains within this candidate. The historical lexical scan completed over ten pinned inputs, covering 59,928 records and 82 candidate document/paragraph views. It found zero normalized-exact matches; the maximum containment of candidate word-five-grams in one historical view was 5.714%. Independent review of all 43 views with a nearest match found common phrasing, technical terms or citation numbers, with no concerning copied passage under that bounded lexical scope. These lexical measurements do not prove independent origin or exclude paraphrases.

The first scan attempt stopped before processing because its 250MB aggregate input bound was below the exact 285,319,045-byte historical catalog. A reviewed 300MB bound allowed the same ten files, retaining the 200MB per-file and 1,200-second limits. The failed attempt is preserved. A separate check of the 16 excerpts against 457 views of the reserved dialogue set detected no lexical matches under its configured rules. Input hashes stayed unchanged in both completed checks. Even a clean result for this small, concentrated scientific sample would not justify repeating it until a 200M-token target was reached.

A separate bounded attempt to retain official Commons source material stopped on the first HTTP 403 response, saving no response bytes. No retry or substitute route followed. That Commons capture has not supplied the missing independent prose-validation evidence.

Two previously identified primary chapter pages from IntechOpen were retained, totaling 1,906,717 raw HTML bytes. Their identities and chapter-specific notices were reviewed. Review of 20 body paragraphs retained ten and rejected ten; the two candidates, including intact abstracts, contain **8,929 text bytes and 1,824 content tokens**. Whole chapters and compilation material are not cleared. Figure dependencies, attributed outside passages and rights exceptions require exclusions; no collection-wide rights claim follows from this small probe.

The combined preparation candidate is now **18 works, 49,658 text bytes and 10,725 content tokens**, with zero admitted records. One optional end-of-sequence token per work would add 18 tokens; these are not packed valid labels. There are no normalized duplicate documents or paragraphs across the two candidates. The chapter historical scan covered the same ten inputs and 59,928 records, with zero normalized-exact matches across 17 candidate views and maximum five-gram containment of 4.2553%. Independent inspection found ordinary shared wording in every reported chapter historical match and both short-utterance matches against reserved dialogue. The sole cross-candidate five-gram was also generic. These bounded lexical checks found no substantive copying evidence in the inspected intersections; they do not establish semantic independence or admission.

## Preparing a controlled continuation

The continuation implementation now separates initialization from same-run resume. It verifies the exact original base and imports model weights into a new run with a fresh optimizer, schedule, random state, stream position and counters. Strict resume retains the new run's own state and provenance.

The code enforces **at most 200M additional valid token exposures across a continuation run**, including resumed invocations. It preserves the original parent identity through downstream supervised training and rejects unknown or inconsistent ancestry. Both eventual comparison arms must use the same pinned supervised implementation, configuration and evaluations.

**Twenty-six focused CPU tests passed** for continuation, resume and supervised-training compatibility. These are small implementation fixtures; they do not constitute a production continuation, corpus admission, or evidence that the model improved. No broad-suite pass is claimed.

## What must happen before training

The next step is a **source-level feasibility census of the existing IntechOpen-labelled DOAB inventory**, not a succession of tiny paper-by-paper selections. Its 20,105 records include fragments and front matter, so they cannot be counted as distinct chapters. A bounded offline pass would reconstruct exact whole-work identities, preserve each work's own notice and author credit, exclude unresolved rights or text-quality cases, and measure novel token yield with the original tokenizer. It would stop after 20 minutes or 100MB of new output and would produce no training admission.

The proposed engineering screen is **1M measured provisional unique tokens from at least 100 complete DOI-bound works**, with full provenance and rejection accounting. This is a chosen feasibility test for the current route, not a user-imposed minimum or a theoretical sample-size requirement. Failure to recover unambiguous works, resolve governing rights, or reach that screen would reject this particular scale proposal for the present iteration. Passing would justify independent review of the cohort process, not training. Any further acquisition requires a separate finite manifest; completed captures remain cached.

The scale gap is substantial. At the measured byte-to-token ratios, 50M tokens would need roughly **229–245MB of clean novel text**. The current two-chapter selection averages 912 tokens per work. Even the invalid optimistic assumption that all 20,105 inventory records were distinct works would yield only about 18.3M tokens at that selection size. This is a reason to test whole-work yield, not a forecast that the inventory contains that many eligible tokens.

No audited combination has demonstrated the earlier full-study proposal of **50M eligible new unique tokens across at least two new source families**. That was an operational design choice, not a user-imposed minimum or a theoretical requirement; IntechOpen and its DOAB derivatives count as one linked family. A smaller comparison could be considered if its question, adequate eligible corpus, independent validation, exposure budget and common downstream recipe were frozen prospectively. None has been selected or launched. The present 10,725-token preparation sample does not justify filling a large budget through repetition. The current continuation execution budget remains zero, and independently sourced prose validation is still missing.

If enough eligible new material clears those gates, continue a separate copy of the original base within the approved cap and compare it with the preserved original base using identical downstream supervision and outcome checks. Additional data, tokens and optimization form the intervention together; this is not an isolated test of breadth alone. No extra control arm or larger-model run has been selected.

The sealed final planning holdout remains excluded from training and unevaluated. The hard deadline remains **31 October 2026 at 04:12 UTC**. The [current plan](/model-training-journal/current-plan/) records the current evidence and launch gates; historical posts preserve what was known at their snapshots.
