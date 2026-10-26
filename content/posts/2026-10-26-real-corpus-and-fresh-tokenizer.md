---
title: "A real corpus and a fresh tokenizer"
date: "2026-10-26"
slug: "real-corpus-and-fresh-tokenizer"
phase: "Corpus"
summary: "A bounded textbook corpus yields 26.91 million training tokens and a fresh 16,384-token BPE vocabulary. The license evidence and limits of the split are recorded explicitly."
order: 5
---

The first real-text corpus and tokenizer were prepared around **04:44 UTC on 26 October 2026**. This moved the experiment beyond the tiny byte-token sample used in the [initial diagnostic](/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/). It did not yet demonstrate conversational competence.

The hypothesis was modest: a bounded, auditable textbook subset could test the training pipeline and reveal whether the randomly initialized model learned to predict held-out English text before fictional planning supervision was added.

## Select a bounded source, then record its limits

The source lineage was a [pinned Marin recipe](https://github.com/marin-community/marin/blob/8577d258214dd0dcb992c04458ee4eb10496d4e5/lib/marin/src/marin/datakit/download/common_pile.py) mapping to `common-pile/pressbooks_filtered`. The [pinned dataset card](https://huggingface.co/datasets/common-pile/pressbooks_filtered/blob/1a1d3b50d77f834370f8eb4c0d174668dd1676bb/README.md) identifies the upstream collection.

One compressed shard of **191,725,499 bytes** was downloaded and its checksum matched the recorded source hash. Selection stopped at the configured 120-million-byte accepted-text cap, yielding **119,991,158 accepted bytes across 1,019 canonical book URLs**.

This was the first qualifying material in the pinned source order, not a random sample. It is a single source family of English educational books, with an English catalog filter and a lightweight character check. It should not be treated as a balanced general-purpose corpus or as independently verified English in every document.

## License evidence is an assertion with provenance

The local selection policy admitted explicit archived CC-BY-family or CC0 claims. It excluded share-alike, noncommercial, no-derivatives, unknown, and ambiguous public-domain labels, plus detected restrictive conflicts and declared external synthetic text.

The [pinned collector](https://github.com/r-three/common-pile/tree/9457f04a14cb2355ab00023420369d46ffd4a395/sources/pressbooks) inherits directory-level book licenses into chapter metadata and normalizes license labels. It does not independently establish every chapter override, embedded third-party item, or original license version.

The bounded live checks produced **13 matching license observations**, **19 unavailable sources**, and **987 books not checked live**. The unavailable and unchecked cases remained classified as archived evidence. These figures must not be summarized as 1,019 independently license-verified books.

The experiment's recorded review accepted this bounded subset for local training under those limitations. Training and redistribution were treated separately. This journal publishes metadata summaries, not the source text.

## What preparation produced

| Split | Documents | Text bytes | BPE tokens |
|---|---|---|---|
| Training | 15,714 | 116,118,363 | 26,908,211 |
| Validation | 592 | 3,872,795 | 918,539 |

All chapters sharing a canonical book URL stay in one split. The recorded audit found **zero book-URL overlap and zero exact normalized-text overlap** across training and validation. Near-duplicate editions were not comprehensively detected, so the audit does not rule out every form of leakage.

A fresh **16,384-token BPE vocabulary** was trained on the training split only. No pretrained tokenizer or model weights were used. Each document ends with an end-of-sequence token, and the next-document prediction after that token is masked out of the loss. Packed attention can still attend to earlier documents; the documents are not isolated by attention masks.

The local review records 17 data-test passes and nine trainer-test passes, including interrupted-resume and changed-code checks. Those are recorded implementation checks, not evidence of model quality.

## Token inventory is not training exposure

The stored training corpus contains **26.91 million tokens**. The planned base run targets **100 million valid training-token exposures**, approximately 3.7 times that inventory. Repeated exposure does not create 100 million distinct tokens, and masking means the inventory and valid-loss-token counts are not identical units.

The next step was a bounded two-million-token pilot to measure real BPE throughput, loss, memory, and checkpoint behavior. Its outcome is recorded in [the first real-text GPU run](/model-training-journal/2026/10/26/first-real-text-gpu-run/).

This AI-assisted summary was checked against the local corpus summary, eligibility record, composition audit, and token manifest. The training code, data, and raw logs are not included in this publication.
