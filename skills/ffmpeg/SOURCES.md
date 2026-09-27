# Sources — skills/ffmpeg

Curated 2026-09-24 by Neo for the one-shot video kit. This is the kit's
**hands**: local assembly, encoding, captioning, audio mixing and QC.

## Origin

- Repo: `kajisho5/ffmpeg-skill` (github.com/kajisho5/ffmpeg-skill),
  vendored under `skills/ffmpeg/` (see `manifest.json`)
- License: check the upstream repo before redistributing outside the lab.

## What was kept

- **SKILL.md** — the router doc (request → script table, workflow, report
  format, gotcha one-liners). Trimmed: 5 request-table rows pointing at
  dropped scripts removed; "42 scripts" → "37 scripts" throughout.
- **scripts/** — 37 public scripts (stdlib-only, Python 3.9+, $0, no cloud):
  probe, cut, fit, crop, cropdetect, deinterlace, denoise, waveform, grid,
  straighten, insert, background, reverse, stabilize, sequence, freeze, pad,
  speedramp, broll, metadata, loop, silence, join, render, scenes, check,
  batch, look, caption, overlay, graphics, sync, audio, loudness, export,
  color, proxy — plus the private helpers they import (`_common/`,
  `_contract.py`, `_platforms.py`, `_ass_overlay.py`).
  `_contract.py` was trimmed so `doctor`/`contract --json` only report the 37
  shipped tools (multicam/redact/sphere/verify/report TOOL_META + MCP
  descriptors removed). Smoke-tested on this VM: probe/join/check/look pass
  against `ffmpeg 8.1.2`.
- **templates/** — all 10 delivery templates (tiktok, reels, shorts,
  youtube-shorts, youtube, x, linkedin, facebook, podcast, audiogram). Tiny
  JSON, load-bearing for `render.py --template` / `export.py`.
- **references/gotchas.md** — the load-bearing trap list SKILL.md links to
  by anchor; reworded the sync/multicam section to sync-only.
- **references/devices.md** — real-device probe notes (iPhone HDR, GoPro,
  DJI, Zoom, OBS). 24 lines, kept whole.
- **references/scripts.md** — every-flag reference for the 37 shipped
  scripts (5 sections for dropped scripts removed, stale cross-mentions
  fixed).

## What was dropped and why

- **scripts/multicam.py, sphere.py, redact.py** — niche tools (multi-camera
  switching, 360° viewport extraction, face/pixelate blur). Not needed for
  one-shot kit outputs; re-add from upstream if a brief needs them.
- **scripts/report.py** — HTML delivery reports; the kit's own scoreboard
  and run logs cover reporting.
- **scripts/verify.py** — upstream's own real-footage self-test harness,
  not a kit tool.
- **demos/, evals/, examples/, docs/** (design-decisions, roadmap,
  ci-platform-pitfalls, process-pitfalls, contract.md, demos.md) — upstream
  development process, CI notes and evals; nothing the kit's agents need at
  run time. (Gotcha detail lives in references/gotchas.md, kept.)
- **mcp/server.py, bin/install.js, package.json** — the kit installs skills
  by vendoring this directory, not via npm/MCP; the MCP wrapper is
  redundant here.
- **assets/** (demo.gif, icons) — marketing images.
- **AGENTS.md, CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md,
  SECURITY.md, README.md** — upstream repo maintenance docs.

## Kit-specific notes

- Run scripts as `python3 <kit>/skills/ffmpeg/scripts/<name>.py`.
- The kit's self-review skill (skills/self-review) calls `look.py` for
  contact sheets/stills and `check.py` for compliance gates.
- The kit's code-film pipeline uses `sequence.py` (frames → video),
  `join.py` (scene concat), `audio.py`/`loudness.py` (mix + LUFS),
  `caption.py`/`graphics.py` (typography overlays), `export.py` (delivery).
