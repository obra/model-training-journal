---
title: "Qualifying a 299M model and counting the next training phase"
date: "2026-10-27"
slug: "larger-model-qualification-and-phase1"
phase: "Larger-model qualification and data preparation"
summary: "A fresh 299M model completes qualification and begins a finite pretraining phase. The first update is recorded and its checkpoint independently verified; broader corpus candidates remain unadmitted."
order: 35
---

The next stage moves to a **299,414,528-parameter model trained from scratch**, with substantially more pretraining as the research direction. The original 97.5M model and its controls remain preserved. The goal is an open, reproducible training recipe that produces transferable logic beyond plausible conversation. Planning remains one diagnostic among several.

The first production phase launched at **04:42:54 UTC on 27 October 2026** and remained running at the **04:47:51 UTC verification snapshot**. Its first optimizer update completed with **32,704 valid labels** from **32,768 processed input IDs**. The first external checkpoint and its sidecar were independently rehashed and matched their recorded hashes. Those counts describe the verified first checkpoint, not the later live total. These startup results do not establish completion of the full phase or model capability.

## What the qualification measured

The new model completed eight optimizer updates using **65,386 valid next-token labels** from 65,536 processed input token IDs. Training took 14.40 seconds, or **4,542 valid labels per second** across those updates. Peak reserved accelerator memory was **7.01 GiB**. Initial and terminal checkpoint files were written and verified.

The model uses 22 transformer layers, width 1,024, a 2,816-wide gated feed-forward layer, 16 attention heads, the existing 16,384-token vocabulary and a 1,024-token context. It began from random weights; it does not incorporate pretrained weights.

These are measurements of a short training execution. They do not establish sustained throughput, conversational quality or transferable reasoning. A small loss check used additional blocks from the training source, so it is not an independent generalization result.

A separate Linux preparation gate passed **97 of 97 named tests**, with no skips, covering checkpoint handling, storage accounting and candidate-scan behavior. The subsequent production integration gate passed **81 of 81 named tests**, also with no skips, including a native CPU tensor checkpoint round trip. These tests support proceeding to a finite run; they do not establish that a broader corpus is eligible or that a long run will remain stable.

## The first production phase is finite

The running phase makes a bounded, nonwrapping pass through the existing training stream. Historical near-duplicate text remains, so this is not a claim of 26.86M unique labels. The measured inventory contains **26,908,211 stored token IDs**, including end-of-document markers. The phase processes **26,902,528 input IDs** in complete blocks and leaves a **5,683-ID tail unused**. Label masking produces **26,860,551 valid training labels** across 821 updates. Stored IDs, processed inputs and valid prediction targets are different counts; each will remain visible in the run record.

The phase has a **9,000-second maximum** and four planned retained checkpoint pairs, including the first pair now independently verified. The broader campaign has a ceiling of one billion valid labels, with a separate processed-input ceiling. That ceiling is not an assertion that one billion suitable new tokens are available, nor a commitment to fill the budget by repeating a small source. Later phases depend on admitted data, verified recovery and a fresh runtime forecast.

The old language-validation population has documented overlap with training. It remains a diagnostic with that limitation. New validation must separate related works and duplicated passages before any broader-data result can support a generalization claim.

## A zero-yield scan exposed an interface error

A bounded scan of the pinned textbook archive examined all **54,455 records** and produced zero candidates because every license field failed the parser. A metadata-only check then identified the mistake: the archive stores specific collector labels followed by license URLs, while the parser expected bare URLs.

The failed scan is preserved. A new parser version recognizes only the two exact observed eligible collector formats for CC BY 4.0 and CC0 1.0. Negated, restrictive, conflicting and extra-text claims still fail. Independent review passed 40 named tests and additional rejected-format checks before another bounded scan.

The corrected scan completed in **184.57 seconds**. It staged 35,414 documents after record-level filters, then excluded 13,129 staged documents through whole-book quarantine. The resulting **22,285 candidate documents** contain **237,077,890 bytes of text** across 971 recorded book groups. In total, 909 book groups were quarantined. All six output files were rehashed, and the original archive hash remained unchanged.

These are candidate counts and text bytes, **not admitted unique tokens**. Automated rights and privacy filters can miss problems or reject harmless text. Related-work grouping, passage deduplication, independent review and tokenizer measurement remain necessary. The scan's sampled passage fingerprints do not establish exhaustive deduplication.

Two further pinned archives from government and parliamentary source collections were acquired and verified: **789,507,600 compressed bytes** in total. They remain in private quarantine and have not been decompressed or admitted to training. The completed acquisition released its storage reservation. Document-level rights, privacy, quality and family-separation review are still required; downloaded bytes and upstream catalog sizes will not be reported as usable model-token yield.

## What determines the next decision

The immediate decisions are whether the finite production phase completes within its limits with verified checkpoints, and how much genuinely distinct eligible text the candidate work yields with this tokenizer. Exact duplicates, related works, passage overlap and previously used validation families must be resolved before a new split is frozen. Format validity, answer correctness, familiar-example fit and structural transfer will remain separate measurements.

The project storage allowance is **800 GB on the dedicated data volume**. Existing free-space, memory, thermal and checkpoint safeguards remain in force. The installed training cutoff is **31 October 2026 at 04:12 UTC**; the separate UI session expiry remains **27 October at 17:02:37 UTC**. These are execution limits, not a claim that the research program is complete at that time. This update does not extend either limit.

Earlier posts describe the budgets and plans in effect at their own stages. The former 200M-additional-token comparison has been superseded by the larger-model direction and finite phase budgets above. Its failed results remain in the record. The original controls and sealed final holdout remain preserved, and this stage uses no proprietary services or private trace inputs.

This is an AI-assisted engineering record. See the [current plan](/model-training-journal/current-plan/) for the latest reviewed snapshot.
