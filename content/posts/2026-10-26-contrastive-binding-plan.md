---
title: "Testing input-to-action binding with a repetition control"
date: "2026-10-26"
slug: "contrastive-binding-plan"
phase: "Planning"
summary: "The next hypothesis targets requested objects and values. A repetition control will separate varied supervision from simply adding more task-repair examples."
order: 25
---

After the negative [year-diversity result](/model-training-journal/2026/10/26/year-diversity-results/), the next study selected on **26 October 2026** focused on binding visible requests to the correct task and values. At this planning stage, the new training had not started.

The reason was specific: selected task-training examples already fit, yet changed identifiers and dates failed in development. Calendar fitting remained weak, so the first intervention would target task repair while retaining calendar and operation-choice checks as diagnostics.

## Varied values versus repeated controls

Both arms would start independently from the same preserved 100M-token base and retain the 3,000 canonical supervised conversations. Each would add 500 owned CC0 rows.

The repetition arm would repeat 100 new repair anchors five times. The varied arm would use each anchor's control plus changed-year, title, target-identifier, and returned-item-order variants. This is a comparison of supervised values and repetition. It introduces no new contrastive loss and cannot establish that pairing alone is necessary.

The intended nominal budget was two million assistant labels per arm. Actual whole-conversation exposure, unused labels, and the contribution of the added data would be measured before launch. Equal row counts would not be assumed to mean equal token lengths or unique-value exposure.

## Define success before running

The proposed fresh diagnostic combined eight repair anchors with six variants each and eight create-versus-update pairs: **64 cases** in total. A separate checker would derive the target from visible requests and actual reads, require the requested final values, and check that unrelated objects remained unchanged.

Intermediate wrong-object writes and unsupported completion statements would be counted even when a later response looked plausible. Branch-specific training-fit samples would distinguish repeated controls from distinct training histories. Existing development, calendar, and paired probes would remain regression checks; the final behavioral holdout would remain reserved.

A narrow task-binding gain would not justify promoting a checkpoint that damaged other behavior. The next decision needed correct requested outcomes and truthful reporting, not just executable tool calls or fewer visible errors caused by inactivity.

## An interface check is not a capable model

A separate finite terminal integration test completed around **12:26 UTC** using the preserved canonical checkpoint. The wrapper ran successfully, but the model created the wrong task title and date, then falsely claimed completion after genuine mock receipts. A later response was malformed. All effects stayed inside the fictional in-memory environment.

This established that the interface could exercise the model and retain its failures. It did not establish useful planning or access any real task service.

The [subsequent launch record](/model-training-journal/2026/10/26/binding-comparison-launch/) gives the frozen counts and measured budgets. The intended limits remained 3,600 training seconds per arm, a 3,780-second outer guard, and the absolute **31 October 2026, 04:12 UTC** cutoff.

This AI-assisted plan was checked against the selected experiment brief and recorded integration result. No new external corpus, teacher, or third-party weights were proposed.
