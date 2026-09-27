# SOURCES — pipelines/code-film/

Vendored 2026-09-24 from **ClaudeAnimationBase** (upstream git HEAD `0ac8bf2`, the render/headless-linux merge).

## What's here and where it came from

| kit file | upstream source | notes |
|---|---|---|
| `render.mjs` | `render.mjs` (verbatim) | Headless-Chrome renderer: sheets, strips, crops, stills, PNG loops, `--clip` MP4, `--frames`+`--encode` parallel path, audio mux |
| `studio.html` | `studio.html` (one line changed) | Browser scrubber. Changed: the `src/scenes/demo.js` script tag became a commented placeholder — the demo scene is not vendored |
| `gpu_probe.mjs` | `gpu_probe.mjs` (verbatim) | Answers "which GPU does headless Chrome's WebGL land on?" — run this on any render machine first |
| `package.json` | `package.json` (verbatim) | Deps: `p5`, `p5.brush`, `puppeteer-core`. **Lock file deliberately dropped** (`package-lock.json` left out — install fresh per machine) |
| `src/core.js` | `src/core.js` (verbatim) | Engine: canvas, PAL palette, `paint()`/`inkLine()`, camera, `glow()`, boil seeding, full-frame effects, render hooks |
| `src/timeline.js` | `src/timeline.js` (verbatim) | `shots()`, `LOOPS`, `brushWipe()` transition |
| `src/config.js` | `src/config.js` (verbatim) | `PROJECT = { duration, bpm, offset }` |
| `src/scenes/` | (new, empty) | Convention per SCENE-STRUCTURE.md: one IIFE-wrapped file per scene/chapter |
| `PIPELINE-GUIDE.md` | adapted from `ANIMATION_GUIDE.md` | Rules kept verbatim (handmade / alive / one piece; no-text; transitions-always; pure-function frames; boiling linework). Generalized: "Clawd" → "the character" in prose, character module framed as swappable (`characters/`), demo.js references replaced (not vendored) |
| `SCENE-STRUCTURE.md` | **built** from PDoomVideo's `STORYBOARD.md` + `src/ch/` layout + its `ANIMATION_GUIDE.md` | Multi-scene convention: one file per chapter, IIFE wrap, `fn(t,lt,dur)`, shared-file discipline, karaoke band clearance, ≤2.5 s/frame perf budget |

## Deliberately left out

- `src/scenes/demo.js` ("The fallen star") — the upstream example scene. The guide says don't copy it; it's one idea, not a template.
- `src/sheets.js` — the model-sheet loop renderer; vendored with the character at `characters/clawd/sheets.js` instead (it belongs to the character, not the pipeline).
- `package-lock.json` — lock bloat.
- `docs/` model sheets — vendored with the character at `characters/clawd/`.
- `LICENSE`, `README.md`, `.gitignore` — upstream housekeeping, not needed in the kit.

## Upstream quirks worth knowing

- `render.mjs` expects Chrome/Chromium on PATH or via `--chrome=` / `CHROME_PATH`; on Linux it passes `--no-sandbox`.
- p5.brush logs a few harmless `WebGL: INVALID_OPERATION` warnings once per page load — frames are unaffected; any other page error is real.
- Linux headless on NVIDIA needs `--gpu-angle=vulkan` or `gl-egl`; run `gpu_probe.mjs` to pick.
