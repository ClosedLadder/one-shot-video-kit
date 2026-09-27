[![CI](https://github.com/ClosedLadder/one-shot-video-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/ClosedLadder/one-shot-video-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# One-Shot Video Kit

A model-agnostic **SKILL** plus tiered pipelines so a frontier AI can attempt a finished video in one invocation: brief in → storyboard → build → self-review loop → scoreboard log.

## What this is

- A **methodology** (`SKILL.md`) with mandatory steps: taste, tier, pipeline, storyboard, build, self-review, score.
- **Three quality tiers** with explicit budgets and placement rules (`tiers/`).
- **Three pipeline families** with recipes and sources (`pipelines/`): code-film, mixed-flow, ai-footage.
- **Vendored skills**: ffmpeg scripts, shot-recipe cards, motion-craft guides, self-review checklists, budget estimator.
- **Scoreboard**: rubric + `scores.jsonl` schema for repeatable evaluation (`scoreboard/`). The frozen benchmark briefs referenced in `SKILL.md` (`scoreboard/briefs/`) are **not included** in this export.
- **Working Python tooling** for ffmpeg assembly, asset harvesting helpers, and optional lab seat routing (`scripts/`, `skills/ffmpeg/scripts/`).

## What this is not

- Not a hosted service or one-click render farm.
- Not a bundle of finished videos — **no rendered MP4s ship with this repo** (add your own under `renders/` locally).
- Not a turnkey cloud API integration — paid video APIs are documented as optional paths behind tier budgets; you bring credentials on your machine.
- Not a guarantee of one-shot success — the kit defines the **process** and quality gates; outcomes depend on the invoking model and your environment.

## Tier system

| Tier | Intent | API spend | Self-review |
|---|---|---|---|
| **BEST** | Ship-quality when output will be seen or sold | Paid APIs allowed; per-run caps in `tiers/BEST.md` | Full proof-frame loop until checklist passes |
| **STUDIO** | Default — near-best on local hardware | **$0 marginal** (no paid API calls) | Full proof-frame loop |
| **DRAFT** | Fast iteration, not for audience | $0 | Exactly one proxy review loop |

Read `tiers/<TIER>.md` before a run. Default is **STUDIO** when the brief omits a tier.

## Pipelines

| Pipeline | Best for | Notes |
|---|---|---|
| **code-film** | Motion design, explainers, typography, deterministic timing | Remotion/p5/three/manim + ffmpeg; see `pipelines/code-film/` |
| **mixed-flow** | Product ads, launch videos, polished UGC | AI footage plates + code overlays + ffmpeg |
| **ai-footage** | Cinematic b-roll, photoreal plates | Cost-gated; storyboard-first economics in recipes |

## Using with a frontier model

1. Point the model at **`SKILL.md`** (Cursor skill, Claude project file, or system prompt attachment).
2. Supply a brief matching `docs/BRIEF-CONTRACT.md` (goal, duration, aspect, tier, pipeline, inputs).
3. The model reads taste (`references/taste.md`), tier rules, pipeline recipe, then works in a run workspace per `docs/workspace-conventions.md`.
4. Self-review uses `skills/self-review/` (contact sheets, stills, `proof-checklist.md`).
5. Score the run with `scoreboard/rubric.md` and append to `scoreboard/scores.jsonl`.

To benchmark, write your own brief against `docs/BRIEF-CONTRACT.md` and score it with the rubric (the original frozen briefs are not shipped here).

## Requirements

- **ffmpeg** — assembly, proxies, loudness, captions (`skills/ffmpeg/`)
- **python3** (3.11+) — ffmpeg skill scripts and kit utilities
- **Node.js** — only if you use the code-film renderer (`pipelines/code-film/`; run `npm install` there)

## Repo layout

```
SKILL.md              # Master skill — start here
tiers/                # BEST, STUDIO, DRAFT rules
pipelines/            # code-film, mixed-flow, ai-footage recipes
skills/               # ffmpeg, shot-recipes, self-review, motion-craft, …
scoreboard/           # Rubric, briefs, scores.jsonl schema
references/           # taste.md, patterns, gallery (populate on runs)
audio/                # TTS roster, music/sfx/sample libraries (harvest locally)
characters/           # Character sheets and code
styles/               # Style packs and backlog
scripts/              # Harvest helpers, seat router (optional), verify tools
docs/                 # Brief contract, workspace layout, setup notes
swarm/                # Multi-worker protocol for large pieces
hardware/             # Render placement notes (optional lab context)
```

## Verification

```bash
# Compile all Python
find . -name '*.py' -not -path './.git/*' -print0 | xargs -0 python3 -m py_compile

# Check relative links in markdown
python3 scripts/check_docs_links.py
```

CI runs the same checks on push (`.github/workflows/ci.yml`).

## License

MIT — see [LICENSE](LICENSE). Vendored skills under `skills/` may include their own licenses (check each `SOURCES.md`).

## Further reading

- `DECISIONS.md` — design judgment calls from the original build
- `manifest.json` — vendored component inventory
- `BUILD-REPORT.md` — packaging notes for this public export
