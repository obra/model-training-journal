---
title: "V8 completes, but the development score moves backward"
date: "2026-10-31"
slug: "v8-completes-with-a-development-panel-regression"
phase: "Completed pretraining and fixed-panel evaluation"
summary: "The software-run V8 slice completed 10.20 million usable training targets and both planned evaluations. Its terminal CFR perplexity is 35.1517, about 3.75% higher than V7's 33.8823 on the same development panel."
order: 50
---

The V8 residual slice completed **312 updates**, **10,201,586 usable training targets** and **10,223,616 processed input positions** without repeating its admitted source span. Its guarded training job exited successfully; both saved checkpoints, the terminal accounting audit, and the two planned postrun evaluations completed through the deterministic controller. This is an execution result, not a proposed run.

On the same frozen **7,057-target CFR development panel**, V7's terminal perplexity was **33.88233562**. V8 scored **34.83798355** at update 156 and **35.15167043** at its terminal checkpoint. Lower is better on this panel, so the V8 terminal result is about **3.75% higher** than V7's and about **0.90% higher** than V8's midpoint. The panel manifest and scorer fingerprints match the V7 evaluation. This is a measured regression on a repeatedly used development check; it is not evidence that every language ability worsened.

| Saved model | New V8 usable targets | CFR perplexity | Mean loss, nats per target |
|---|---|---|---|
| V7 terminal parent, repeated baseline | 0 | 33.88233562 | 3.52289381 |
| V8 update 156 | 5,100,685 | 34.83798355 | 3.55070827 |
| V8 terminal, update 312 | 10,201,586 | 35.15167043 | 3.55967214 |

The [dashboard](/model-training-journal/dashboard/#cfr-v8) charts all three points with the parent marked as a repeated baseline. Its [public data](/model-training-journal/assets/v8-cfr-checkpoints.json) retain full score precision, checkpoint fingerprints and separate stage-local counts. The V8 checkpoint files, model weights, corpus and private operational records are not published.

Checkpoint and writer work took **405.53 seconds** of a **3,728.24-second training loop**, or **10.88%**. That exceeds the 10% target. The guarded run lasted 71 minutes 56 seconds, about **2,364 usable targets per wall-clock second** including startup and closure. The measured loop rate was about **2,736 per second**. These are different denominators, and the remaining setup and closure time has not been isolated into causes.

There is **no new reasoning, BLiMP, broader-language-panel or sealed-final-holdout result**. The earlier task test remains 0/32 correct and 0/32 format-valid at an older checkpoint, so it does not isolate reasoning. The CFR panel has been used repeatedly during development. The next decision should consider complementary standard tests and a bounded speed comparison before allocating more training; neither is reported as run here. This AI-assisted journal records a real software execution and an unfavorable narrow result without treating either as a final capability verdict.
