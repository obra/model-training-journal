---
title: "An isolated environment and the first bounded GPU diagnostic"
date: "2026-10-26"
slug: "isolated-environment-and-first-gpu-diagnostic"
phase: "Diagnostic"
summary: "A 97.5M-parameter model passes six correctness checks and a short Radeon 8060S benchmark, with explicit limits on what those results demonstrate."
---

The first diagnostic answered a concrete question: could this system run a randomly initialized, roughly 100-million-parameter causal model with BF16 computation, FP32 persistent state, and working loss and checkpoint behavior?

**Yes, for the bounded tests recorded here.** A model with **97,536,768 trainable parameters** passed six correctness checks and completed a short GPU benchmark at **11,697.79 valid training tokens per second**. This establishes local execution and test behavior. It does not establish useful language ability or a trained assistant.

This entry summarizes the diagnostic completed on 26 October 2026 and recorded at 04:05 UTC. It follows the [initial inventory](/model-training-journal/2026/10/26/setup-access-and-inventory/). Statements about what had not yet run refer to that historical stage.

## Preparing an isolated environment

The occupied GPU allocation was released before the experiment. Reported GPU memory use fell from approximately 31.44 GiB to 171 MiB. The experiment then used a project-local Python environment and runtime libraries; it did not require a system-wide framework installation or a driver or firmware change.

| Software or device | Recorded version or identification |
|---|---|
| Python | 3.14.4 |
| PyTorch | `2.14.0+rocm10.1.0` |
| ROCm package | 10.1.0 |
| HIP build string | `7.16.26385` |
| GPU | AMD Radeon 8060S Graphics |
| Architecture | `gfx1151` |
| Reported device memory | 32 GiB |

The notebook records selecting official AMD packages using the [ROCm compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html), [ROCm pip guidance](https://rocm.docs.amd.com/en/latest/install/rocm.html), and [AMD's PyTorch installation guidance](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html). These links are living documentation; the versions above are the versions recorded for this experiment.

The first import failed because `libgomp.so.1` was missing. The resolution was to extract Ubuntu's `libgomp1` package, version `16-20260322-1ubuntu1`, into the project runtime and expose it through a process-local library search path. The package was not installed system-wide. Dependency checking then passed.

NumPy remained absent, causing an optional PyTorch bridge warning. The diagnostic needed only PyTorch and the Python standard library. A tensor-to-scalar warning in a loss assertion was also nonfatal; no GPU or nonfinite-loss errors were observed in the completed tests.

## Model and optimizer

The model started from random weights. It used 12 layers, hidden width 768, 12 attention heads and 12 key/value heads, a SwiGLU intermediate width of 2,048, RMSNorm, RoPE, tied embeddings, and no linear biases. Context length was 1,024 and vocabulary size was 16,384.

The temporary tokenizer simply mapped bytes to IDs 0–255. Most of the model's vocabulary was therefore unused. This was a diagnostic tokenizer, not a trained tokenizer suitable for judging production language-model performance.

AdamW used a learning rate of 0.001, betas of `(0.9, 0.95)`, epsilon `1e-8`, no weight decay, and gradient clipping at 1.0, with a LambdaLR schedule. The seed was `20261026`, and the process used eight CPU threads. The benchmark used PyTorch's automatic scaled dot-product attention backend policy; no particular fused attention kernel is claimed.

## Small data, limited purpose

The benchmark repeatedly consumed a small, 18,959-byte CPython tutorial sample. The source notebook pins it to revision `0cc81280367df838c4b199f8f0378837165071c2` and records its license as PSF License Version 2 for prose, with an additional 0BSD option for examples. The overfit test used separate original diagnostic text, 13,652 bytes, recorded as CC0.

No dataset or third-party text excerpt is redistributed with this journal entry. No pretrained weights or external synthetic teacher were used. These tiny samples tested execution and learning mechanics; they did not constitute a representative training corpus or a quality evaluation.

## Six correctness checks

All six recorded checks passed:

1. **Parameter count:** the instantiated model had 97,536,768 trainable parameters.
2. **Shifted labels and padding:** the loss used the intended next-token targets and mask.
3. **Causal masking:** future tokens did not influence the tested earlier predictions.
4. **Tiny-batch overfit:** loss decreased from 9.860314 to a final-three-step mean of 0.216215 over 44 steps at sequence length 64.
5. **Persistent precision:** parameters, gradients, and Adam moments remained FP32; attention projection computation was observed in BF16 during overfitting.
6. **Checkpoint continuation:** model and optimizer continuation matched bitwise after restoration, along with scheduler state, data position, and subsequent Python, CPU, and GPU random-number draws.

The exact-resume subtest used **FP32 computation and math attention**. Its bitwise result should not be generalized into a claim of exact BF16 resume under every attention backend. The saved checkpoint was 1,170,579,467 bytes. The throughput benchmark initialized a separate model and did not load that checkpoint.

## The bounded benchmark

Each measured step performed a full forward pass, backward pass, and optimizer update with batch size 1 and sequence length 1,024. Each full sequence contributed 1,023 valid shifted training labels.

| Measurement | Result |
|---|---|
| Measured steps | 1,024 |
| Measured valid training tokens | 1,047,552 |
| Measured time | 89.551 seconds |
| Valid training tokens per second | 11,697.79 |
| Excluded warmup | 5 steps; 5,115 tokens |
| Total tokens including warmup | 1,052,667 |
| First / last measured loss | 3.995616 / 0.372822 |
| Mean measured loss | 1.709772 |
| Peak PyTorch allocated memory | 2.164 GiB |
| Peak PyTorch reserved memory | 2.219 GiB |
| Stop reason | Step bound reached |

The benchmark observed BF16 attention projection computation with FP32 parameters, gradients, and Adam moments. The memory figures describe the PyTorch allocator and exclude other driver allocations.

The run stopped at its 1,024-step bound. Other limits were 120 seconds of measured work, 1,048,576 measured valid tokens, and 160 seconds of internal total runtime, with an external timeout as a backstop. Warmup was excluded from the measured throughput. The run was not extended to pursue a better number.

The falling loss is expected on a repeated tiny sample. It is not evidence of generalization, instruction following, or assistant quality.

## What the measurement can support

Dividing 100 million tokens by the measured rate gives approximately **2.37 hours** of comparable training steps. This is arithmetic, not a production duration promise. A production tokenizer changes what a token means; data loading, checkpointing, evaluation, sustained thermals, and a more representative workload can all change the rate.

At the time of this diagnostic, no long production run or 100-million-token run had been performed. Production tokenizer training, corpus selection, and validation/test design remained future work. Physical installed RAM also remained unverified by firmware inspection.

The useful outcome was a tested starting point: GPU execution worked, the bounded correctness checks passed, and a short-run throughput measurement existed. The next experiment needed a representative, licensed data and tokenizer plan with an evaluation design capable of detecting something more meaningful than memorization of a tiny sample.

## Evidence and publication boundaries

The public figures were checked against the local correctness and benchmark result files. The diagnostic source revision is identified by SHA-256 `d5140c2d6a34a8d48ae1b9bb971d4b91361fdc9106eb99c5eba6d4dfdb69d91e`; no source repository commit was recorded for that diagnostic.

This is an AI-assisted editorial summary of the engineering record, not a personal account attributed to the repository owner. The original result files, raw logs, source scripts, data, and checkpoint remain outside this publication. Those omissions protect private details and keep this journal distinct from a complete reproduction package.
