# Sources — skills/budget-estimator

Curated 2026-09-24 by Neo for the one-shot video kit. This is the kit's
**cost gate**: no paid generation fires without an estimate on file.

## Origin

- Repo: `danielrosehill/claude-ai-video-producer-plugin`
  (github.com/danielrosehill/claude-ai-video-producer-plugin),
  adapted from the upstream producer plugin (see `docs/SOURCES.md`)
- Original: `skills/budget-estimator/SKILL.md` (MIT)

## What was kept and adapted

- **SKILL.md** — the cost-model discipline kept whole (per-call cost ×
  iteration multiplier; low/typical/high ranges; per-second pricing by
  storyboard duration; price-source dating; USD normalization).
- Adapted to the kit: reads `run.md` (budget cap, target spec) and
  `storyboard/shot-list.md` instead of `brief/tools-and-models.md`;
  writes `budgets/estimate-<YYYY-MM-DD>.md` in the run workspace;
  explicit STOP rule when typical estimate exceeds the cap;
  $0 code-film runs still write a ledger line.

## Deliberately not curated

- The plugin's per-modality generation skills (text-to-image-to-video,
  text-to-video-direct, script-to-tts, voice-to-lip-sync,
  upscale-and-interpolate, model-researcher, recommend-model) — these are
  vendor-specific recipe shells around paid APIs. The kit's own
  `pipelines/ai-footage/` and `pipelines/mixed-flow/` builders will write
  kit-native versions with the cost gates wired in. The storyboard-first
  discipline (iterate on cheap stills before expensive motion) is captured
  in `docs/workspace-conventions.md` instead.
- `runners/` (fal_run.mjs, wavespeed_run.py) — need `FAL_KEY` /
  `WAVESPEED_API_KEY` plus npm/pip installs; violates the kit's $0-build,
  no-secrets rule. Revisit when the kit wires paid footage behind its own
  cost gates.
- `commands/setup-credentials.md` — credential collection; out of scope.
- ComfyUI import/export skills — the kit's lab has its own ComfyUI paths;
  not needed in the run workspace.
