---
title: "Paired probes isolate date and identifier failures"
date: "2026-10-26"
slug: "paired-transfer-probe-results"
phase: "Diagnosis"
summary: "Changing a year or target identifier breaks otherwise successful requests. Longer training improves some ordering cases while false completion claims increase."
order: 22
---

The paired diagnostic completed at **10:57 UTC on 26 October 2026**. It compared the saved canonical-supervision checkpoints trained for roughly 500,000 and two million assistant labels. No training occurred during this diagnostic.

The question was narrower than whether the model could plan: when it solves a request, does it still solve that request after one controlled change?

## Forty pairs, five changed factors

Each checkpoint received **80 episodes arranged in 40 pairs**. A pair changed the year, wording, target identifier, returned-item order, or a calendar blocker's endpoint. Sixteen underlying anchors were reused across factors, making these correlated, development-informed probes rather than a blind generalization test.

Both checkpoints used the same unconstrained greedy BF16 decoder, context of 1,536 tokens, six assistant turns, and 96-token reply limit.

Exact final states increased from **40/80 to 43/80**. A stricter measure requiring a successful read followed by exactly one write attempt increased from **40/80 to 42/80**. The difference was a real recovery: the longer-trained model submitted an invalid interval, received a rejection, reread the calendar, and then made the correct booking. Its final state and completion statement were correct; its history failed the one-attempt rule.

## Measure transfer only when the control works

The following fractions use that stricter definition. Each numerator counts successful changed requests among controls the same checkpoint solved.

| Changed factor | 500K checkpoint | 2M checkpoint |
|---|---|---|
| Year | 0/5 | 0/5 |
| Target identifier | 0/8 | 0/8 |
| Returned-item order | 5/8 | 7/8 |
| Wording | 5/5 | 4/5 |
| Calendar geometry | 0/2 | 0/2 |

The successful controls are not always the same across checkpoints. Only four task controls are shared for year and wording: all four retain wording success and lose year transfer. The identifier and order comparisons share the same eight successful controls. Geometry has no shared successful control under the strict rule, so its fractions do not show matched improvement or deterioration.

The failures also differ. The longer-trained checkpoint continued using a familiar year after the request's year changed. Renamed targets elicited updates to an absent, familiar identifier. Ordering failures were not explained by always choosing the first listed item: some earlier successes correctly chose the second item. Interval errors remained even when year and identifier were unchanged.

## More correct states, more false claims

False completion claims increased from **23 to 28**. The latter included 25 statements following wrong applied writes and three following rejected writes. Fewer missing final answers therefore did not establish better completion reporting.

One worker's complete artifacts were recovered and validated after a registration failure, but its process exit remained unknown. The result record preserves that distinction; valid output is not proof of a successful process exit.

The next selected experiment was [varied training years](/model-training-journal/2026/10/26/year-diversity-experiment/). Identifier binding and interval arithmetic remained separate problems. The final behavioral holdout stayed reserved, and no checkpoint was promoted on these results.

This AI-assisted account was checked against the frozen probe metadata and independent paired comparison. Raw transcripts and evaluation content are not published here.
