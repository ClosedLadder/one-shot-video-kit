# Sources — docs/workspace-conventions.md + docs/commands/

Curated 2026-09-24 by Neo for the one-shot video kit. These are the kit's
**working conventions**: how a run workspace is laid out, named, budgeted,
and shipped.

## Origin

- Repo: `danielrosehill/claude-ai-video-producer-plugin`
  (github.com/danielrosehill/claude-ai-video-producer-plugin),
  snapshotted from the upstream plugin repo (see `manifest.json` for vendored paths)
- Conventions doc: adapted from `skills/video-workspace-conventions/SKILL.md` (MIT)
- Commands: adapted from `commands/storyboard.md`, `commands/assemble.md`,
  `commands/export-final.md` (MIT)

## What was kept and adapted (not copied blindly)

- **Lifecycle phases** (brief → characters → script → storyboard → generation
  → clips → timeline → exports → output → logs) kept as the spine, remapped
  to the kit's two-level layout: the kit repo is the **library** (skills,
  characters, references, pipelines), each attempt is a **run workspace**
  under `renders/<brief>/<model>/<date>/`.
- **Naming discipline** (`NN-shortname-vN`, prompt+model+seed paired with
  every artefact), **raw vs selected** (never delete raw; promote with
  rationale), **pipelines are recipes**, **log every model call** — kept
  verbatim in spirit.
- Commands rewritten for the kit: run-workspace paths instead of a flat
  project root; `run.md` run card instead of `brief/`; the ffmpeg skill's
  scripts (`join.py`, `audio.py`, `caption.py`, `loudness.py`, `export.py`,
  `check.py`, `look.py`) instead of hand-written ffmpeg; dry-run-first
  discipline; `render.py` project.json for 3+ step chains.
- Kit-native additions with no upstream equivalent: budget-cap gate before
  any paid call (ANALYSIS §1.4), OrcaRouter's determinism law for code-film
  (every frame a pure function of timestamp), self-review proof frames in
  `proofs/`, post-run compounding into `scoreboard/style-memory.md`,
  `references/gallery/`, and `logs/costs.jsonl`.

## Deliberately not curated

- `install-video-workspace` — the kit repo ships its own layout; a
  per-project scaffolder isn't needed (run workspaces follow
  workspace-conventions.md directly).
- `onboard`, `draft-script`, `define-character` — conversational capture
  procedures; the kit's `briefs/`, `characters/_template.md`, and router
  SKILL.md cover this ground (other kit builders own them).
- `log-take`, `promote-take` — their discipline (prompt pairing, raw vs
  selected, SELECTIONS.md rationale) is folded into
  workspace-conventions.md; separate commands add surface without value.
- `setup-credentials`, `runners/` — API keys + npm/pip; violates the kit's
  $0-build, no-secrets rule.
- The plugin's per-modality generation skills — vendor-specific shells
  around paid APIs; the kit's pipeline builders will write kit-native
  versions behind cost gates (see skills/budget-estimator/SOURCES.md).
