# SOURCES.md — tiktok

## Origin
- Repo: `iart-ai/tiktok-video-skills` (https://github.com/iart-ai/tiktok-video-skills),
  MIT licensed (see LICENSE). Cloned 2026-09-24; curated into this pack.
- 4 skills for TikTok / Reels / Shorts creators (9:16 short-form).

## Kept
- All 4 skills: caption-animation, countdown-video, lower-thirds, short-form-video.
  Each keeps `SKILL.md` + `references/`.
- Key references: `word-timed-captions.md` (karaoke-style word timing —
  pairs with whisper word timestamps), `retention-pacing.md` (short-form
  pacing rules), `lower-third-component.md`, `countdown-cookbook.md` +
  `digit-flip.md`.
- Shared verify toolkit `scripts/`: contact-sheet.sh, probe-mp4.sh, seek-shot.sh.

## Dropped
- `showcase.gif` / `showcase.html`, `.claude-plugin/`, skill-level `README.md`
  files, pack `README.md` — demos and install marketing, no skill content.

## Why this cut
9:16 is the second aspect-ratio priority in the analysis. Word-timed captions
and retention pacing are the two most one-shot-relevant short-form skills;
the rest of the pack's value is platform-specific and stays upstream.
