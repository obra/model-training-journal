---
title: "A bounded news-source audit during base training"
date: "2026-10-26"
slug: "bounded-news-candidate-audit"
phase: "Corpus"
summary: "A bounded scan identifies 1,426 candidate articles for possible later study. Source correspondence and software integrity checks do not establish training eligibility."
order: 10
---

While the first base run was still training, a separate CPU-only audit examined a possible source for a later corpus experiment. The scan completed at **05:59 UTC on 26 October 2026**. It did not alter the active training corpus, tokenizer, or checkpoint lineage. **No candidate documents were admitted to training.**

## Inventory candidates without treating them as cleared data

A pinned CommonPile News archive was verified against its expected checksum. The complete bounded scan produced these measurements:

| Measurement | Result |
|---|---|
| Compressed archive | 98,092,770 bytes |
| Expanded JSON processed | 312,694,827 bytes |
| Records scanned | 126,673 |
| 360info candidates | 1,426 |
| Candidate text represented | 8,286,830 bytes |
| Candidates missing an archived author field | 65 |

The remaining 125,247 records came from other sources and were outside this tranche. No exact normalized-text or URL duplicates were found within the candidate subset. Near-duplicate detection remained unresolved.

The audit wrote hashes and bounded attribution metadata, not a training-text corpus. Its declaration screens found no flags. That result does not establish permission, complete attribution, or English-language quality.

## Check correspondence separately from rights

The source review recorded [360info's terms](https://360info.org/about-us/terms-of-use/) as describing CC-BY-4.0 reuse with attribution and exceptions for third-party material. Three sampled live pages matched their archived author identities and displayed reuse notices. A separate image credit used a different license, illustrating why prose and media rights need separate treatment.

For those three samples, **98.13%, 99.17%, and 95.68%** of the archived unique five-word sequences appeared in the corresponding current page text. This is a correspondence proxy. It does not establish exact archived-version identity or clearance of every embedded passage. Only the three pages were fetched; images and externally linked resources were not downloaded.

Missing attribution, article-level exceptions, and the filtered dataset's precise transformation lineage remained open questions. The count of candidates must not be reported as the count of cleared articles.

## Test the auditor's integrity

Review found failure cases involving archive mutation, damaged compression, duplicate JSON keys, and partially written output. After corrections, the recorded focused verification passed **26 tests**.

The auditor verifies the complete input hash, checks for ordinary input changes, bounds input and output sizes, and distinguishes complete scans from partial or failed output. These are software-integrity checks, not rights certification.

The next corpus decision still depended on actual learning and behavioral results. Even a fully admitted small source pool would support only a bounded exposure experiment, not an unrestricted repetition run. This public summary contains no article text or raw audit records.
