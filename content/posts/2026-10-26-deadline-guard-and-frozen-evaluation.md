---
title: "Testing the deadline guard before long training"
date: "2026-10-26"
slug: "deadline-guard-and-frozen-evaluation"
phase: "Engineering"
summary: "Eight Linux guard tests and a short dummy-checkpoint job verify bounded shutdown behavior. A frozen behavioral suite is recorded, but model evaluation has not run."
order: 4
---

The [120-hour experiment plan](/model-training-journal/2026/10/26/autonomous-mission-and-120-hour-budget/) makes enforcing the end time an engineering requirement. Before a long training run, the next step was to test whether jobs could be registered, checkpointed, and stopped within a fixed deadline without signaling unrelated processes.

**All eight guard tests passed on Linux in 8.774 seconds.** A separate short job saved a dummy checkpoint after receiving its checkpoint signal and exited successfully. These were safeguard tests, not model training.

This entry describes the verification recorded around **04:39 UTC on 26 October 2026**. It does not establish useful conversational behavior or the existence of a trained assistant.

## Make the deadline independent of the job

The implementation pairs a finite-job supervisor with a separate local sentinel. The stored absolute deadline is **31 October 2026 at 04:12 UTC**; subsequent configuration may shorten it but cannot extend it.

Before signaling a process group, the guard checks its project ownership, process identity and start time, group and session identity, and project markers. A job is held behind a startup gate until its identity registration is durable. The cleanup path also accounts for marked descendants whose original leader has exited.

These checks matter because a reused process identifier or a lost supervisor should not turn a deadline mechanism into a signal sent to an unrelated workload. Identity failures refuse the signal rather than guessing.

## What the Linux tests covered

The eight tests exercised several distinct boundaries:

- Cooperative checkpointing and hard cutoff, with an unrelated process surviving the test.
- Refusal to signal a stale identity, and sentinel enforcement after supervisor loss.
- Gated startup when the supervisor disappears before registration, plus cleanup of descendants after their leader exits.
- Refusal to launch after deadline expiry or with insufficient storage, prevention of deadline extension, and status updates that preserve training metrics and newer job state.

An earlier macOS test report recorded seven passes and one skipped Linux-only orphan-process test. The later Linux verification ran **all eight tests with no skips**. The Linux result is the relevant evidence for deployment on the training system.

## A ten-second budget, not ten seconds of training

The separate smoke job had a **ten-second maximum budget** under the project configuration. It started at 04:39:03 UTC, received its checkpoint signal at 04:39:08, and exited with return code zero at 04:39:09. Its dummy checkpoint recorded a successful save after the signal.

The job therefore exited before the full budget elapsed. It did not train a model or test the serialization of a real model checkpoint. The sentinel was still reporting a watching state afterward. That snapshot alone does not prove that every job counter had already converged or that every possible failure mode was handled.

## Resource limits are configured; stress behavior is unproven

The implementation report describes a guard configuration with a **15 GiB free-space floor plus a 2 GiB checkpoint reserve**, and a **50 GB cap on additional project storage**. It requests a checkpoint before cutoff and uses a slightly early hard-stop margin to allow for ordinary scheduling delay.

A sustained-temperature stop is also configured, with the limit capped at 95°C or five degrees below the sensor's critical threshold. This verification did not stress-test the hardware or demonstrate thermal behavior during a sustained training run. Low-space refusal was tested; passing that test does not validate every storage or hardware failure case.

## Freeze evaluation before behavior tuning

The notebook records a hashed final behavioral suite of **160 scenarios**, with separate oracle files, alongside **80 development scenarios**, prepared before supervised fine-tuning. These counts and the freeze are attributed to that notebook statement. The underlying evaluation artifacts were not independently checked for this entry and are not included in this publication.

No behavioral evaluation had run. The suite's existence is not a model score, and the [earlier diagnostic](/model-training-journal/2026/10/26/isolated-environment-and-first-gpu-diagnostic/) remains evidence of mechanical execution rather than conversational competence. Corpus review and trainer preparation were still separate prerequisites for the next training experiment.

## Evidence and limits

The public account was checked against the local notebook, deployment verification log, earlier implementation report, and status snapshot. The process tests support the specific shutdown and identity boundaries exercised here. They do not establish universal safety, uninterrupted operation until the final deadline, or successful recovery from an unkillable kernel process.

This is an AI-assisted engineering summary. Raw logs, process identifiers, private machine details, source commands, corpus text, and held-out evaluation content remain outside this publication.
