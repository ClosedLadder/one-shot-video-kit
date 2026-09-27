# SOURCES.md — data-animation

## Origin
- Repo: `iart-ai/data-animation-skills` (https://github.com/iart-ai/data-animation-skills),
  MIT licensed (see LICENSE). Cloned 2026-09-24; curated into this pack.
- 3 skills for analysts and PMs making data-driven video.

## Kept
- All 3 skills: animated-infographic, chart-animation, presentation-video.
  Each keeps `SKILL.md` + `references/`.
- Key references: `bar-chart-race.md` + `data-pipeline.md` (CSV → animated
  charts), `sequenced-infographic.md`, `sequencing.md` + `slide-components.md`.
- Shared verify toolkit `scripts/`: contact-sheet.sh, probe-mp4.sh, seek-shot.sh.

## Dropped
- `showcase.gif` / `showcase.html`, `.claude-plugin/`, skill-level `README.md`
  files, pack `README.md` — demos and install marketing, no skill content.

## Why this cut
Data-viz is a first-class one-shot job (scoreboard brief 3 includes animated
charts). The data-pipeline recipe (CSV → frame-accurate charts) is exactly the
deterministic pattern the kit's code-film pipeline wants.
