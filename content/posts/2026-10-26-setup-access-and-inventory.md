---
title: "Access, resource inventory, and setup status"
date: "2026-10-26"
slug: "setup-access-and-inventory"
phase: "Setup"
summary: "A read-only inventory establishes the starting point for a small model experiment: capable hardware, occupied GPU memory, and an unverified training environment."
---

This is the opening record of an AI-assisted engineering experiment: investigate training a model of roughly 100 million parameters from scratch on an AMD Strix Halo system. The immediate task was narrower than training. Establish access, identify available resources, and find the constraints that would need resolving before any computation began.

**This post describes the setup snapshot recorded at 03:43 UTC on 26 October 2026.** No training, benchmark, GPU stress test, package installation, or model or dataset download occurred in this phase. The [next entry](/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/) records the subsequent environment setup and completed diagnostic.

## The question

Was there a usable starting point for a small training experiment, and which assumptions still needed evidence?

A hardware specification alone would not answer that question. GPU memory could already be allocated, the active Python interpreter might lack a compatible framework, and nominal storage capacity might not provide a writable workspace. The method was a bounded, read-only inventory of the operating system, device driver, memory accounting, storage, and selected software availability.

## What the inventory established

| Component | Observed at setup |
|---|---|
| CPU | AMD Ryzen AI Max+ 395; 16 cores, 32 threads |
| GPU | AMD Strix Halo Radeon; Radeon 8060S identified by CPU information |
| Driver | `amdgpu` |
| Operating system | Ubuntu 26.04.1 LTS, x86_64 |
| Kernel | `7.0.0-38-generic` |
| Checked Python interpreter | Python 3.14.4 |
| PyTorch import | Failed with `ModuleNotFoundError` |
| ROCm installation | No version found at the checked standard location or through the checked command search path |

The software checks had a deliberately limited conclusion: the checked host interpreter did not have PyTorch. They did not establish that every possible virtual environment or container lacked it. Likewise, a GPU visible to the operating system was not yet evidence that PyTorch could execute on it.

## Memory accounting mattered

Linux reported **30.48 GiB of system memory**, with approximately 27 GiB available. The GPU driver reported a **32 GiB VRAM budget**, of which roughly **31.44 GiB was allocated**. Only about 575 MiB remained in that GPU allocation pool.

Reported GPU activity was 0% at the snapshot. That did not make the allocated memory available for training: idle computation and free memory are different conditions.

The driver also reported a 15.24 GiB GTT budget. This overlaps system RAM and must not be added to the other figures as extra physical memory. The Linux and VRAM split was consistent with a 64 GB configuration, but the physical capacity was not independently verified. Reading firmware memory information was denied by the operating system's permissions, and the inventory did not use elevated privileges.

Storage had sufficient apparent headroom for a small diagnostic, but a writable training-data location was still undecided. Capacity and permission were treated as separate checks.

## Failures and unresolved observations

The failed PyTorch import was a useful result: a functioning GPU driver was insufficient on its own, and a compatible software environment would have to be established before testing the model.

An initial notebook-generation wrapper also failed with a Python syntax error before reaching the remote system. It made no remote changes and was corrected before the notebook was created.

At this stage, the source of the large GPU memory allocation had not yet been established conclusively. The setup work did not attempt to free that memory. The later diagnostic entry records the memory release and the environment that actually passed the tests.

## What remained to decide

The proposed model still lacked a settled architecture, tokenizer, licensed training corpus, training budget, and evaluation design. The next engineering steps were to make GPU capacity available, choose an isolated software environment, and test a tightly bounded workload before projecting a longer run.

This inventory established a starting point and its uncertainties. It produced no trained model and no evidence of language-model quality.

## About this record

This public entry is an AI-assisted editorial summary of a local engineering notebook. It preserves relevant observations and their limits while omitting private machine identifiers, access details, unrelated service inventory, and raw logs. Times identify the historical record; they are not a live report of the machine's current state.
