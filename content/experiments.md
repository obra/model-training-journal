The experiment record, in the order the work happened. Status describes the cited entry, not a live view of the training machine.

## Training a small model from scratch

The initial objective is a language model with roughly 100 million parameters. These first entries establish the environment and test a randomly initialized **97,536,768-parameter** causal model. They do not establish a capable assistant.

<dl class="experiment-list">
<dt>Access and inventory</dt>
<dd>Hardware and resource snapshot recorded; GPU computation not yet tested.<br><a href="/model-training-journal/2026/10/26/setup-access-and-inventory/">Setup and inventory</a> · 26 Oct 2026</dd>
<dt>Isolated environment</dt>
<dd>GPU visible in the isolated PyTorch environment; missing runtime library resolved locally.<br><a href="/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/">Environment and first diagnostic</a> · 26 Oct 2026</dd>
<dt>Correctness</dt>
<dd>Six checks passed, including label masking, causal masking, tiny-batch overfit, persistent-state dtypes, and exact checkpoint continuation.<br><a href="/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/#six-correctness-checks">Correctness results</a></dd>
<dt>Bounded throughput</dt>
<dd>11,697.79 valid diagnostic tokens/s over 1,024 measured steps.<br><a href="/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/#the-bounded-benchmark">Benchmark results</a></dd>
<dt>120-hour program</dt>
<dd>A bounded planning experiment defined, with proposed evaluation targets, baseline comparisons and deadline safeguards. These are plans, not measured outcomes.<br><a href="/model-training-journal/2026/10/26/autonomous-mission-and-120-hour-budget/">The 120-hour plan</a> · 26 Oct 2026</dd>
<dt>Deadline guard</dt>
<dd>Eight Linux guard tests passed. A separate bounded job saved a dummy checkpoint and exited after a checkpoint request; behavioral evaluation remained unrun.<br><a href="/model-training-journal/2026/10/26/deadline-guard-and-frozen-evaluation/">Guard verification and evaluation preparation</a> · 26 Oct 2026</dd>
</dl>

## What those results establish

A short GPU diagnostic can run and its basic correctness checks pass in the recorded environment. The benchmark uses a temporary byte tokenizer and a repeated tiny corpus. Its falling loss and arithmetic runtime estimate are not a quality evaluation or a production training forecast.

The [120-hour plan](/model-training-journal/2026/10/26/autonomous-mission-and-120-hour-budget/) defines the next program of work. Longer training, a production tokenizer, data selection and licensing, and held-out evaluation still need their own evidence. Later entries will record those outcomes when reviewed; this index does not infer them from the diagnostic or the plan.
