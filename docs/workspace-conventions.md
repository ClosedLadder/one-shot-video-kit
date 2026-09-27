# One-Shot Video Kit — Workspace Conventions

How a single video run is laid out, named, and tracked. Adapted from
danielrosehill's `claude-ai-video-producer-plugin`
(`skills/video-workspace-conventions`) to the kit's shared-library layout —
not copied blindly. The kit repo itself is the **library** (skills,
characters, references, pipelines); each **run** gets its own workspace
under `renders/`, following the conventions below.

## The two levels

| Level | Lives at | Contents |
|-------|----------|----------|
| **Library** (shared, versioned) | kit root | `skills/`, `characters/`, `references/`, `audio/`, `pipelines/`, `briefs/`, `styles/`, `tiers/` |
| **Run** (one attempt) | `renders/<brief>/<model>/<date>/` | everything produced for that run |

Pipeline files stay in the library at `pipelines/<pipeline>/` — a run gets
a *copy* only if the recipe is edited for that run. Never edit the library
recipe from inside a run workspace.

## Run workspace layout

```
renders/<brief>/<model>/<date>/
├── run.md              # run card: kit version, model, seed, budget cap, pipeline, target spec
├── storyboard/         # shot-list.md + NN-shortname.md per-shot briefs
├── generation/         # raw model output by modality + prompts/
│   ├── text-to-image/  # stills (cheap; iterate here first)
│   ├── image-to-video/ # animated takes
│   ├── text-to-video/  # direct video takes
│   ├── voice/          # TTS takes
│   ├── lip-sync/       # lip-synced takes
│   ├── upscale/        # upscaled/interpolated takes
│   └── prompts/        # prompt + model + seed + params for EVERY artefact,
│                       # same filename stem (reproducibility)
├── clips/              # raw/ selected/ edited/ b-roll/
├── timeline/           # edit decision list, sequencing notes
├── exports/            # thumbnails, captions (.srt/.vtt), subtitle files
├── proofs/             # self-review contact sheets + proof frames from finals
├── final/              # locked deliverable + sidecar .md (spec, cost, models)
├── budgets/            # estimate-<date>.md + actuals
└── logs/               # production-log.md (one line per model call)
```

The kit's code-film pipeline adds `frames/` (rendered PNG sequences,
joined with `skills/ffmpeg/scripts/sequence.py`) and `src/` (the renderer
code — Remotion/p5/manim project) inside the run workspace.

## Lifecycle (in order)

1. **Run card first.** No generation until `run.md` exists: frozen brief
   reference, target runtime, aspect, resolution, fps, format, audio plan,
   pipeline choice, budget cap, seed. No brief → no generation.
2. **Storyboard.** Locked script → shot list (`storyboard/shot-list.md`:
   number, duration, visual, audio, generation approach, pipeline per shot)
   → per-shot briefs (`storyboard/NN-shortname.md`: visual prompt seed,
   audio script, character refs, duration, notes). Confirm total runtime
   against the brief; flag mismatches. (See `docs/commands/storyboard.md`.)
3. **Budget estimate.** Before any paid API call: run the budget estimator
   (`skills/budget-estimator/`). Typical estimate must be under the run's
   budget cap, or the run stops here — storyboard-first economics: validate
   cheap, ship validated only. Code-film runs are $0; the estimator still
   writes a (trivial) estimate for the record.
4. **Generate.** Cheapest modality first: stills before motion, TTS before
   lip-sync. Every artefact lands in `generation/<modality>/` with its
   prompt file in `generation/prompts/`. Everything raw stays raw.
5. **Select, don't delete.** Only explicitly approved takes get copied into
   `clips/selected/` (with rationale in `clips/selected/SELECTIONS.md`).
   Never delete raw output — iteration loops back to it. `clips/edited/`
   holds graded/trimmed versions; `clips/b-roll/` holds supporting footage.
6. **Assemble.** EDL in `timeline/`, then join + VO alignment + music mix +
   captions via the ffmpeg skill (`skills/ffmpeg/`) into rough cuts.
   (See `docs/commands/assemble.md`.)
7. **Self-review.** Contact sheets and proof frames from every draft go in
   `proofs/`. The agent inspects its own output and fixes before calling it
   done — "an agent that can't check its own work is just guessing."
   Drafts are never shipped; only `final/` is.
8. **Export final.** Locked draft → encode to spec, embed subtitles, write
   `final/<project>-final.<ext>` + sidecar `<project>-final.md` (spec,
   runtime, size, source draft, models used, total cost). Never overwrite a
   final — version with `-v2`. (See `docs/commands/export-final.md`.)
9. **Compound.** Absorb corrections into the kit's `scoreboard/style-memory.md`;
   add the run's best proof frames to `references/gallery/`;
   append cost actuals to `logs/costs.jsonl` and the run line to
   `scoreboard/scores.jsonl`.

## Working principles

- **Run card before generation.** Don't fire model calls until `run.md`
  exists with target runtime, format, aspect ratio, and pipeline choice.
- **Pair every artefact with its prompt.** Prompt + model + seed + params
  in `generation/prompts/` with a matching filename stem, so any take can
  be reproduced or iterated.
- **Raw vs selected.** Everything the model produces lands in
  `generation/<modality>/` and `clips/raw/`. Only approved takes get
  copied into `clips/selected/`. Never delete raw output without asking.
- **Pipelines are recipes, not magic.** A pipeline file describes a chain
  (e.g. storyboard → still → animate → TTS → assemble). Walk it
  step-by-step, surfacing intermediate outputs. Code-film pipelines add:
  **every frame is a pure function of its timestamp** (no carried state,
  no unseeded randomness) or parallel rendering flickers.
- **Log model calls.** One line per non-trivial generation in
  `logs/production-log.md`:
  `YYYY-MM-DD HH:MM | <model> | <platform> | $<cost> | <artefact-path>`.
  Cost actuals also go to the kit's `logs/costs.jsonl`.
- **Cost discipline.** Paid calls (AI footage, voice, upscale) happen only
  with a budget estimate on file and typical-estimate ≤ cap. Show a range
  (low/typical/high), never a single point estimate. If the typical figure
  exceeds the cap, stop and replan — don't generate and hope.

## Naming conventions

- Generated artefacts: `NN-shortname-vN.ext` — e.g.
  `03-rooftop-establish-v2.mp4`. `NN` orders shots, `vN` tracks iterations.
- Prompts: matching stem in `generation/prompts/` — e.g.
  `03-rooftop-establish-v2.md` (prompt + model + seed + parameters).
- Characters: `characters/<name>.md` (kit library; see
  `characters/_template.md`).
- Per-run pipeline copies: `pipelines/<descriptive-name>.md` inside the
  run workspace only when edited for the run.
- Budget estimates: `budgets/estimate-<YYYY-MM-DD>.md`.

## Command procedures

`docs/commands/` holds the step-by-step procedures, adapted from the
upstream plugin to this layout and to the kit's ffmpeg skill:

1. `storyboard.md` — locked script → shot list + per-shot briefs.
2. `assemble.md` — EDL → rough cut via the ffmpeg skill (join, VO, music,
   captions), drafts versioned.
3. `export-final.md` — locked draft → spec encode + sidecar report in
   `final/`.

## What NOT to do

- Don't generate anything before the run card exists.
- Don't overwrite files in `clips/selected/` or `final/` — version with
  `-v2` instead.
- Don't invoke a paid model without a budget estimate on file.
- Don't delete from `generation/` or `clips/raw/` — discarded takes often
  get revisited.
- Don't edit library files (`skills/`, `pipelines/`, `characters/`,
  `references/`) from inside a run workspace.
- Don't call a render "done" without proof frames in `proofs/`.
