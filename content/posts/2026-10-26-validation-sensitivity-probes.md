---
title: "Validation sensitivity after the overlap audit"
date: "2026-10-26"
slug: "validation-sensitivity-probes"
phase: "Validation"
summary: "Two frozen filters raise loss on changed validation populations. They measure sensitivity to detected overlap, not an independently sourced test of generalization."
order: 14
---

Two filtered views of the textbook validation were measured on the preserved 100-million-token base, completing at **07:36 UTC on 26 October 2026**. They quantify sensitivity to the [detected lexical overlap](/model-training-journal/2026/10/26/auditing-textbook-overlap/). They are **not independently sourced validation**, and neither result alone supports further pretraining.

| Sample | Retained documents | Scored labels | Loss |
|---|---|---|---|
| Original broader partial probe | Original 592-document stream | 900,000 | 3.8606707 |
| Exclude strongly flagged documents | 550 | 808,644 | 3.9216265 |
| Exclude flagged existing book groups | 433 | 595,978 | 4.0027060 |

The original fixed 65,536-label prefix remains separately recorded at **4.0205829**. These samples differ in difficulty, source composition, packing, and adjacent context. Their losses cannot be joined into a learning curve or used to isolate the causal effect of overlap.

## Freeze the filters before measuring loss

The document filter removes **42 validation documents**, excluding **107,895 tokens including end-of-sequence markers**. It conservatively includes both strong-containment categories, even where the high containment concerns only the shorter training passage.

The stricter filter removes **159 documents across ten existing book keys**, excluding **320,612 tokens including end-of-sequence markers**. Those keys are existing resolver groups, not certified independent works. The method does not connect unrelated books through shared access-request boilerplate.

Both views retain document order and the original tokenizer, append one end-of-sequence token per document, and record retained and excluded identities, hashes, coverage, and offsets. The root manifest was frozen before the new loss measurements. Original source manifests and scores were preserved.

## Count only the nonwrapping capacity

The ordinary evaluator permits cycling, so these probes explicitly requested the verified capacity of a single nonwrapping pass at context 1,024 and batch size 1. End-of-sequence transitions and each context block's final source position are masked; incomplete final blocks are discarded.

The document-filtered view consumed **791 complete blocks**, leaving 660 raw tail tokens unscored. It evaluated 808,644 valid labels in **13.81 seconds**. The book-filtered view consumed **583 complete blocks**, leaving 935 tail tokens unscored, and evaluated 595,978 labels in **9.97 seconds**.

Both used BF16 computation and the same preserved checkpoint. No optimizer update occurred. The builder's recorded verification included 12 focused tests, including a real-tokenizer fixture; an independent review also checked 98,280 small capacity cases.

## Keep the conclusion narrow

Loss increased on the filtered populations, but removing content changes more than contamination alone. The results remain diagnostics with residual overlap risk. Further pretraining decisions still require independently sourced or source-family-disjoint validation, alongside actual behavioral results.

The next training experiment instead focused on broader original planning supervision. Candidate news records remained outside training, and no checkpoint was promoted on the basis of these language-model losses.
