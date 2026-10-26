---
title: "Document review narrows the validation candidates"
date: "2026-10-26"
slug: "document-rights-and-validation-candidates"
phase: "Data audit"
summary: "Nineteen dialogue candidates remain after record review, but none are admitted. Book extraction and arXiv version checks show why archive metadata cannot establish usable training yield."
order: 32
---

**Snapshot through 17:52:33 UTC on 26 October 2026:** no new corpus records were admitted, and no new training had started. Document review narrowed the possible language-validation set and exposed reconstruction problems in the candidate book corpus. A completed lexical overlap audit supplied limited evidence, without establishing independence.

This continues the [first corpus audit](/model-training-journal/2026/10/26/reflection-and-corpus-audit/). The question remains whether broader, auditable base training can improve the same small model before matched conversational supervision. Downloaded bytes and metadata labels do not answer that question.

## Thirty-six conversations become nineteen candidates

The Taskmaster survey selected 36 whole conversations in deterministic hash order, four from each of nine instruction groups. All 36 were then read, with candidate hashes, structure, and annotation spans checked. Choices were frozen before consulting model outputs or losses.

| Record-review outcome | Conversations |
|---|---|
| Retained for overlap checks | 19 |
| Excluded: unresolved participant identity or contact details | 5 |
| Excluded: unresolved outside prose | 7 |
| Excluded: incomplete or deleted source material | 4 |
| Excluded: collection failure without a substantive task | 1 |

These are exclusive primary reasons; some records had additional issues. Automatic screening had missed short or attached contact-number forms. Entire conversations were excluded rather than silently editing their turns or replacing them after scoring.

The remaining **19 conversations contain 438 turns across six groups**: four coffee, four pizza, four ride, six movie-ticket conversations across two groups, and one restaurant-table conversation. Both auto-repair groups and the second restaurant-table group disappeared. This is a small, selection-biased dialogue-language diagnostic, no longer a balanced nine-group sample.

The source's CC BY 4.0 attribution must be preserved, but its notice does not resolve outside prose or participant details automatically. Simulated success statements lack verified tool-state receipts. These records are not truthful-action supervision. The entire Taskmaster family and its derivatives remain excluded from training. **Nineteen candidates still means zero admitted validation records.**

## A completed overlap check with limited coverage

The historical audit finished at **17:46:53 UTC**. It compared the 19 candidates with ten listed inputs: Pressbooks training and previous validation, plus eight distinct conversational-supervision corpora. All input hashes matched and the files remained unchanged through scanning.

The scan covered 59,928 source records and 360,599 source units, including separate conversation and message views. These counts do not represent unique works or novel training tokens. All **29,366 source–validation pairs with any match** were classified as limited shared language; none met the stronger overlap criteria.

That does not prove independent origin. The detector checks normalized words and short word sequences, not semantic paraphrase, translation, or unlisted sources. **Turns shorter than eight words receive whole-unit exact checks only, without substring search.** Common phrasing can match innocently, and embedded material can escape detection.

Any eventual broader training text must be added and rescanned before validation is frozen. Verified source provenance remains necessary. This audit also does not repair the earlier overlap-affected language-validation split.

## Books need individual-work reconstruction

The DOAB shard contained 31,034 records associated with 1,499 parent-book keys. IntechOpen and MDPI accounted for 98.13% of records, a record fraction rather than a token fraction or count of independent works.

The deliberately selected review sample covered 24 records from 13 books. Twelve short records were read completely; twelve longer records were inspected only at documented boundaries and notice passages. Their unread interiors remain unreviewed, and the sample is not representative.

Reviewed MDPI notices distinguish CC BY individual articles from CC BY-NC-ND compilations. Reviewed IntechOpen notices license individual chapters under CC BY 3.0 while reserving compilation rights and some credited material. The [publisher copyright policy](https://www.intechopen.com/page/copyright-policy) separately describes individual works, compilations, historical license differences, and reproduced figures or tables. Neither distinction supports treating every extracted row as a separately cleared chapter.

| Triage decision | Records |
|---|---|
| Priority for document-level review | 2 |
| Reconstruct before further review | 11 |
| Exclude non-substantive attribution block | 1 |
| Exclude compilation front matter | 4 |
| Retain copyright pages as rights evidence only | 6 |

All 24 remain unadmitted. Some rows join several works, repeat or scramble material, or combine a correction with its original article. Careless splitting could discard a correction to a scientific claim. No eligible unique-token yield has been established.

Hansard is deferred from the first continuation unless a useful cleared subset can be established. The acquired written answers differ from the proposed debates; their complete-unit reconstruction and licence exceptions require separate review. Senedd remains excluded.

## arXiv supplies identifiers, not admitted prose

One acquired archive was inspected successfully, yielding 10,096 records. The records lack an explicit source-version field. Differences between pinned collector code and the released dataset description leave the extraction lineage unresolved; a submission date cannot identify the revision of a multi-version paper.

Two early candidates matched official v1 identities and CC BY 4.0 notices, but their complete contents were not cleared. They do not establish archive-wide permission or likely yield.

The resulting bounded pilot uses the archive **only as an identifier catalog**. It selects 25 candidate IDs and would derive text afresh from exact official versioned HTML, preserving response hashes, version, licence, attribution, and transformations. Two responses had been saved at this snapshot; document parsing, full review, and admission had not run. Saving a response does not establish complete, clean, or wholly covered prose.

The continuation remains conditional, capped at **200M additional valid tokens**, with the original base preserved as control. The final planning holdout remains excluded from training and unevaluated. The deadline stays **31 October 2026 at 04:12 UTC**; the [current plan](/model-training-journal/current-plan/) records later decisions.

This AI-assisted account was checked against the notebook, record-review ledgers, acquisition records, and historical-audit summary. No candidate text, conversations, raw logs, or private execution details are published here.
