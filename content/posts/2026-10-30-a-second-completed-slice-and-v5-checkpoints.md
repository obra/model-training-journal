---
title: "A second completed slice and five V5 checkpoints"
date: "2026-10-30"
slug: "a-second-completed-slice-and-v5-checkpoints"
phase: "Finite continuation: measured language loss"
summary: "The second V4 slice completed 111.43M valid labels; V5 is running. Same-panel CFR perplexity fell across both slices, with one retained checkpoint regression. Reasoning improvement remains unproven."
order: 46
---

The second V4 corpus slice completed **111,430,307 valid next-token labels** in **3,408 updates**, consuming its admitted data once. Its terminal checkpoint scored **35.9212 perplexity** on the same frozen **7,057-label CFR development panel**, versus **37.7860** for the repeated parent. That is a **4.94% lower** perplexity on this narrow panel. The history includes a small regression at checkpoint 2,841; we did not discard it.

The next finite slice, V5, was **still running at the 17:14 UTC observation**. Its ledger had completed **3,600 of 3,833 updates** and **117,702,026 of 125,320,085 planned valid labels**. Its fifth saved checkpoint, update 3,195 at **104,460,450 stage-local valid labels**, scored **34.5556 perplexity**, versus **35.9212** for its repeated parent: **3.80% lower** on the same development panel. Later token progress is not a later quality measurement. V5's terminal checkpoint had not been evaluated in this snapshot.

| Slice | Checkpoint update | Stage-local valid labels | CFR perplexity |
|---|---|---|---|
| V4 second | repeated parent | 0 | 37.7860 |
| V4 second | 569 | 18,604,411 | 36.9802 |
| V4 second | 1,137 | 37,176,043 | 36.5873 |
| V4 second | 1,705 | 55,747,706 | 36.1164 |
| V4 second | 2,273 | 74,319,327 | 36.0421 |
| V4 second | 2,841 | 92,891,175 | 36.1805 |
| V4 second | terminal 3,408 | 111,430,307 | 35.9212 |
| V5 | repeated parent | 0 | 35.9212 |
| V5 | 639 | 20,891,966 | 35.4747 |
| V5 | 1,278 | 41,783,903 | 35.3711 |
| V5 | 1,917 | 62,676,097 | 34.9232 |
| V5 | 2,556 | 83,568,380 | 34.8974 |
| V5 | 3,195 | 104,460,450 | 34.5556 |

<figure class="metric-chart">
<img src="/model-training-journal/assets/charts/v4-v5-cfr-perplexity.svg" alt="Two stage-local CFR perplexity curves: blue completed second V4 slice falls from 37.7860 to 35.9212 with a regression at checkpoint 2841; green running V5 falls from repeated parent 35.9212 to checkpoint 3195 at 34.5556.">
<figcaption>Blue is the completed second V4 slice; green is V5 through checkpoint 3,195. Hollow starting points repeat a parent checkpoint and consume no new labels in that slice. Horizontal positions are <em>stage-local</em> valid labels, not a single cumulative token clock. The vertical range is restricted to 34.0–38.2 and lower is better. All points use the same frozen 7,057-label CFR development panel; this is repeatedly viewed development data, not a sealed test or a universal perplexity target. <a href="/model-training-journal/assets/charts/v4-v5-cfr-perplexity.svg">Open the chart</a>.</figcaption>
</figure>

This is evidence of improved likelihood on one narrow text distribution, **not yet evidence of transferable reasoning or chatbot competence**. The older 130,209-label broader language panel remains a separate historical result; it was not rerun for these checkpoints. The last completed 32-case task diagnostic remains **0/32 correct and 0/32 protocol-valid**. Its output-interface failure prevents interpreting that score as an isolated capacity test. A proposed before-and-after format diagnostic stopped at CPU readiness and has no successful trial result. A standard zero-shot [BLiMP](https://github.com/alexwarstadt/blimp) minimal-pair evaluation is being assessed as a complementary grammar measure; **it has not run**. Neither BLiMP nor this CFR panel alone would prove the project's transferable-logic goal.

The frozen tokenizer, model configuration and evaluation population are shared across the charted checkpoints. Exact saved-checkpoint metrics and stage-local label counts are in the [sanitized chart data](/model-training-journal/assets/v4-v5-cfr-checkpoints.json); the passive SVG is reproducible with `python3 scripts/build_v4_v5_cfr_chart.py`. This AI-assisted journal publishes aggregate results and documented failures. It does not publish raw training text, private records, credentials, or a claim that model weights have been released.
