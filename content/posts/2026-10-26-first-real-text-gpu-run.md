---
title: "The first real-text GPU run"
date: "2026-10-26"
slug: "first-real-text-gpu-run"
phase: "Pilot"
summary: "A two-million-token pilot finishes in 137.238 seconds with lower held-out loss and a verified checkpoint. The larger 100-million-token continuation remains in progress."
order: 6
---

The first real-text pilot completed **2,000,000 valid training tokens** at **04:51 UTC on 26 October 2026**. It used the [fresh BPE tokenizer and bounded textbook corpus](/model-training-journal/2026/10/26/real-corpus-and-fresh-tokenizer/), rather than the temporary byte mapping from the diagnostic.

The pilot's purpose was to establish finite loss, real-token throughput, observed memory use, and a recoverable checkpoint. A lower loss on a small held-out textbook sample would support continuing the experiment. It would not establish instruction following or conversational usefulness.

## Use the schedule intended for continuation

The model had **97,536,768 trainable parameters**: 12 layers, hidden width 768, 12 attention and key/value heads, a SwiGLU intermediate width of 2,048, tied embeddings, and context length 1,024. Batch size was 1 with gradient accumulation over eight microbatches.

The run used BF16 computation on an AMD Radeon 8060S with PyTorch `2.14.0+rocm10.1.0`. Its AdamW optimizer used a peak learning rate of `3e-4`, with two million tokens of warmup and a cosine schedule defined for **100 million total tokens**. The pilot stopped at the end of warmup while preserving the schedule intended for the longer continuation.

This was a randomly initialized model, not a pretrained model adapted to the corpus.

## Measured outcome

| Measurement | Pilot result |
|---|---|
| Completed valid training tokens | 2,000,000 |
| Optimizer steps | 245 |
| Elapsed time, including validation and checkpoint overhead | 137.238 seconds |
| Valid training tokens per second | 14,573.2 |
| Fixed validation sample | 16,384 tokens |
| Initial validation loss | 9.831619 |
| Final validation loss | 6.235447 |
| Final observed allocated GPU memory | 1.639 GiB |
| Final observed reserved GPU memory | 2.594 GiB |

The lower validation loss is evidence of improved prediction on this particular held-out sample. The sample is small and belongs to the same textbook source family as training. It is not a general capability evaluation.

The memory figures are **end-of-run observations, not measured peaks**. The final reported GPU temperature was 42°C; the sampled training log also contained higher readings, reaching 55°C. Neither is a comprehensive peak-temperature measurement. No nonfinite-loss or hardware error was reported in the completed pilot record. Its short duration does not establish sustained thermal behavior.

## Checkpoint integrity and the limit of the check

The committed atomic checkpoint and its checksum sidecar reloaded successfully on CPU. The recorded reload verified FP32 persistent model tensors and FP32 optimizer tensor states. It also preserved the two-million-token scheduler position and the exact training-stream position.

The checkpoint format carries optimizer, scheduler, random-number-generator, and stream state. Earlier trainer checks included exact interrupted CPU resume. A successful CPU reload of this pilot checkpoint should not be presented as proof that a later GPU continuation restored every state correctly; that continuation requires its own runtime evidence.

## Continue toward a total of 100 million tokens

The next run continues the same model toward **100 million valid tokens in total**, including the pilot's two million. It does not add another 100 million. At the **05:04:35 UTC** status snapshot used for this publication, the continuation was **still in progress**, so this entry makes no claim that the base run finished.

The continuation is configured to preserve the learning-rate schedule and optimizer. Its planned checkpoint interval is five million tokens or 900 seconds. Validation expands from 16,384 to 65,536 tokens, every five million training tokens and at completion. Later losses therefore use a different validation denominator and should not be compared as if the measurement were unchanged.

The corpus contains 26.91 million stored training tokens. A 100-million-token exposure budget is roughly 3.7 passes over that inventory, not 100 million distinct tokens. Dividing the total target by the pilot rate gives about **1.91 hours**, an arithmetic estimate that can change with sustained clocks, validation, checkpointing, and other overhead. The continuation has a four-hour job bound and remains subject to the experiment's absolute deadline.

No learned conversational behavior had been evaluated. The planned next comparison remains random-initialized-plus-supervised-training versus base-trained-plus-supervised-training, using matched fictional planning data and evaluation conditions.

This AI-assisted account was checked against the pilot event log, result and checkpoint-reload record, and the pilot and continuation configurations. It does not publish the checkpoint, training data, raw logs, or private runtime details.
