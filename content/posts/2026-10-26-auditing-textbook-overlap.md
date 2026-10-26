---
title: "Auditing overlap across the textbook split"
date: "2026-10-26"
slug: "auditing-textbook-overlap"
phase: "Validation"
summary: "A bounded lexical audit finds strong overlap candidates involving 42 validation documents. Exact hashes and separate book URLs had not established independent content."
order: 12
---

After the first 100-million-token base run, a lexical audit found adapted chapters and repeated boilerplate across the textbook training and validation splits. Earlier checks had established distinct book URLs and no exact normalized-text overlap. They had not established independent content.

The original validation results remain unchanged: loss **4.02058 on the fixed 65,536-label prefix**, and **3.86067 on a separate 900,000-label probe**. Neither is now presented as a demonstrably independent-work evaluation.

## Shortlist with fingerprints, then compare actual strings

The auditor normalizes Unicode words and uses deterministic five-word fingerprints to shortlist document pairs. It then verifies overlap using actual shared five-word strings, recording containment in both directions. These lexical measures flag candidates for interpretation; they do not establish semantic equivalence or automatically select documents for deletion.

The completed configured scan covered **15,714 training documents and 592 validation documents**. It verified **5,537 shortlisted pairs in 27.80 seconds**:

| Lexical category | Pairs |
|---|---|
| Near-whole-document candidates | 58 |
| Asymmetric-containment candidates | 14 |
| Limited shared passages | 178 |
| Small overlaps | 5,287 |

The **72 strongly flagged pairs involve 42 distinct validation documents**. High containment in one direction alone does not mean most of the validation document was seen during training: the shared training passage can be much shorter. Metadata review also distinguished repeated access-request boilerplate from related textbook chapters.

## Keep the partial attempt and its limits

The initial audit stopped at its 2,000-pair limit while the training scan was incomplete. That partial result was preserved. A second run increased the explicit bounds to 15,000 pairs overall and 600 per training document, while retaining a 300-second runtime limit and 32 MB report cap.

The expanded run verified input hashes and ordinary file stability. The reviewed implementation had 19 focused test passes. It still uses a heuristic shortlist, omits overly common fingerprints, and can miss a short passage embedded in a long document. Completing its configured scan is not proof that all overlap has been found.

## Measure sensitivity without rewriting history

The follow-up plan was to freeze two new validation views: one excluding all 42 flagged documents, and a stricter view excluding their existing book groups. Both would retain the original tokenizer and record coverage before measuring losses.

These are changed diagnostic samples, not replacements for the original learning curve and not a claim of complete decontamination. Training inputs, model weights, and the final behavioral holdout were not changed by the audit. The [validation sensitivity probes](/model-training-journal/2026/10/26/validation-sensitivity-probes/) report the resulting measurements.
