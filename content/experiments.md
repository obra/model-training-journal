The experiment record, in the order the work happened. Status describes the cited entry, not a live view of the training machine.

## Training a small model from scratch

The initial objective is a language model with roughly 100 million parameters. The entries follow a randomly initialized **97,536,768-parameter** causal model from environment checks to a completed real-text pilot. They do not establish a capable assistant.

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
<dt>Corpus and tokenizer</dt>
<dd>A bounded textbook subset and fresh 16,384-token BPE vocabulary prepared: 26.91M training tokens, with archived license evidence and limited live checks.<br><a href="/model-training-journal/2026/10/26/real-corpus-and-fresh-tokenizer/">Corpus preparation and its limits</a> · 26 Oct 2026</dd>
<dt>Real-text GPU pilot</dt>
<dd>2M valid tokens completed in 137.238 seconds; fixed-sample validation loss fell from 9.831619 to 6.235447. The 100M total-token continuation was still in progress.<br><a href="/model-training-journal/2026/10/26/first-real-text-gpu-run/">Pilot measurements and continuation</a> · 26 Oct 2026</dd>
<dt>Behavioral evaluation preparation</dt>
<dd>Revised frozen suite and 946 context-checked training conversations prepared; 22 world and 19 supervised-interface tests passed. The scripted development baseline scored 0/80 and remains under methodological review; no learned conversational behavior had been evaluated.<br><a href="/model-training-journal/2026/10/26/frozen-planning-world-and-review-corrections/">Planning world and review corrections</a> · 26 Oct 2026</dd>
</dl>

## What those results establish

The initial byte-token diagnostic established mechanical execution on a tiny repeated corpus. The later [real-text pilot](/model-training-journal/2026/10/26/first-real-text-gpu-run/) completed 2M valid training tokens and reduced loss on a fixed 16,384-token textbook validation sample. This is narrow language-model evidence, not a conversational capability evaluation.

The [corpus record](/model-training-journal/2026/10/26/real-corpus-and-fresh-tokenizer/) documents a 26.91M-token training pool. The 100M-token continuation target represents roughly 3.7 passes over that pool, not 100M distinct tokens; completion is not claimed here. Book-level license assertions and bounded live checks have explicit limits, and no source text is published.

The [revised planning-world entry](/model-training-journal/2026/10/26/frozen-planning-world-and-review-corrections/) records implementation tests and evaluation preparation. The scripted baseline's zero score is under methodological review and supports no claim of model superiority. Matched supervised-training comparisons and learned-policy evaluation remain future work in this snapshot.
