---
# Adapted from danielrosehill/claude-ai-video-producer-plugin `commands/storyboard.md`
# (MIT). Adapted 2026-09-24 for the one-shot video kit: run-workspace layout,
# run.md instead of brief/, no interactive-approval wording (the agent runs
# unattended), budget-estimate step added.
---

# Storyboard — break the locked script into a shot list

**Usage:** run inside a run workspace (`renders/<brief>/<model>/<date>/`).

1. Read `run.md` for the target spec (runtime, aspect, resolution, fps,
   format, audio plan, pipeline, budget cap) and the locked script
   (code-film: the renderer's scene plan; mixed/ai-footage: the VO script).
   If `run.md` is missing, stop — no storyboarding without a run card.
2. Produce a shot list. For each shot:

   | # | Duration | Visual | Audio | Generation approach | Pipeline |
   |---|----------|--------|-------|---------------------|----------|

   - **#** — `01`, `02`, ... matches the `NN` in artefact filenames.
   - **Visual** — one sentence of what's on screen.
   - **Audio** — VO line, dialogue, SFX, music cue.
   - **Generation approach** — modality (code-rendered, text-to-image→video,
     text-to-video direct, stock+edit) and which model/style from `run.md`.
   - **Pipeline** — the file in the kit's `pipelines/` to invoke (or "custom").
3. Write the table to `storyboard/shot-list.md`.
4. For each shot, write a per-shot brief at
   `storyboard/NN-shortname.md` with: visual prompt seed, audio script,
   character refs (paths into the kit's `characters/`), duration, notes.
   These become the input to generation for that shot.
5. Confirm shot count and total runtime against `run.md`. Flag mismatches.
6. If the pipeline uses any paid API: run the budget estimator
   (`skills/budget-estimator/`) against this shot list before any
   generation. Typical estimate must be ≤ the run's budget cap.

## What NOT to do

- Don't storyboard from a draft script that isn't locked — lock it first.
- Don't generate cover art, clips, or VO before the shot list exists.
- Don't let per-shot durations drift the total runtime past the brief —
  re-time the shots instead.
