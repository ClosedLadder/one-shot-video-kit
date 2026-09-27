# SOURCES.md — motion-design

## Origin
- Repo: `iart-ai/motion-design-skills` (https://github.com/iart-ai/motion-design-skills),
  MIT licensed (see LICENSE). Cloned 2026-09-24; curated into this pack.
- 9 skills for professional motion designers working in code.

## Kept
- All 9 skills: after-effects, animation-principles, beat-sync-editing,
  color-motion, logo-animation, motion-art-direction, motion-background,
  remotion-video, shot-composition. Each keeps `SKILL.md` + `references/`.
- `after-effects/scripts/*.jsx` (apply-effect-to-layers, batch-rename,
  sequential-offset) and `references/expression-library.md` / `expressions.md` —
  the expressions are portable timing math even without After Effects.
- Shared verify toolkit `scripts/`: contact-sheet.sh, probe-mp4.sh, seek-shot.sh
  (frame-freeze / contact-sheet / MP4 probe — the deliver-and-verify loop),
  plus the scripts README.

## Dropped
- `showcase.gif` / `showcase.html` — multi-MB marketing demos, no skill content.
- `.claude-plugin/` — marketplace install metadata, not needed in the kit.
- Skill-level `README.md` files — one-paragraph blurbs duplicating SKILL.md
  frontmatter; pack `README.md` — install/marketing copy for `npx skills add`.

## Why this cut
This pack is the craft foundation: easing curves and the 12 principles
(animation-principles), Remotion API patterns (remotion-video), camera/grids
(shot-composition), logo patterns, beat-sync editing, art-direction playbook.
Nothing here exceeds 72KB; everything is decision knowledge, not assets.
