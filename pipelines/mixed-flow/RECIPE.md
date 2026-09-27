# Mixed-Flow Pipeline — RECIPE

**Religion C, the kit's flagship.** AI footage for hero plates and b-roll (cost-gated) + code overlay for everything code does better (graphics, captions, lower thirds, beat-synced cuts, titles) + ffmpeg assembly. Photorealism where it counts, pixel-perfect branding where code wins, deterministic assembly throughout.

This is the pleometric/donaldjewkes one-prompt workflow shape (AI footage + reference libraries + code polish) and where Brad's pipeline and 30x-video converge. The code-film pipeline (`pipelines/code-film/`) and the brand-launch skill (`skills/brand-launch/`) are this recipe's two hands — read both before running it.

## Stage 0 — Budget check (blocking)

Read `BUDGET.md` first. Every footage call spends from the run's footage budget; when the budget is $0 the pipeline **degrades to code-only** (footage stages become style-locked code plates) and still ships. No budget, no footage, no exceptions, no "just one more generation."

## Stage 1 — Beat sheet

Write the beat sheet before anything is generated. One line per beat: timecode, what's on screen, what it must accomplish, which plate type (AI footage / code graphic / hybrid).

```
00:00–00:03  HOOK       — product in hero lighting, macro push-in          [AI footage]
00:03–00:08  PROBLEM    — pain, desaturated, handheld feel                  [AI footage]
00:08–00:12  TURN       — code title card: the claim, editorial type       [code]
00:12–00:24  PROOF      — 3 vignettes: UI mockup + footage b-roll           [hybrid]
00:24–00:30  CLOSE      — logo lockup + CTA                                [code]
```

Rules: one argument per beat (taste-raw §5); hits land on musical beats; the hook must work with the sound off (captions carry it).

## Stage 2 — Style lock

Lock these **before** any footage is generated — style drift across AI shots is Religion B's #1 failure, and the lock is the fix:

- **Reference plate:** one generated-or-found image that IS the look (lighting, lens, grade, palette). Every footage prompt references it.
- **Character consistency:** if a human appears in more than one shot, use `soul-id` (5–20 photos → stable `reference_id`) — never re-describe the face per shot. See `pipelines/ai-footage/RECIPE.md`.
- **Prompt formula:** MCSLA — Model · Camera · Subject · Look · Action — on every footage call, verbatim.
- **Palette + type lock:** hex palette and the single typeface (weight 300–600) for all code overlays, from the brand (or invented once, then frozen).
- **No-text rule for footage:** AI footage never carries typography — text is drawn by the code overlay, always. (Religion B can't do precise text; don't ask it to.)

Style lock is a written artifact (`style-lock.md` in the run dir): reference plate path, soul-id id, palette hexes, typeface, prompt formula template. Footage that doesn't match the lock gets regenerated — against the budget.

## Stage 3 — AI footage (COST-GATED, stubbed)

All generation goes through the `pipelines/ai-footage/` workflow — Higgsfield MCP endpoint `mcp.higgsfield.ai/mcp` (Seedance 2.5 video, nano banana 2 images). **$0 build cost: this stage is a stub** — no live API calls during the build; the workflow, budget plumbing, and setup docs are real, the credentials are Steven's to add (see `docs/`).

**Storyboard-first economics (mandatory):**
- **Validate cheap (~7 credits):** generate the cheapest possible validation of each beat first — stills instead of video where a still answers the question, shortest durations, lowest acceptable resolution.
- **Ship validated only:** full-quality generations happen once per beat, only for beats that passed validation. PromptEngineer48's benchmark: 10 finished UGC ads < $16 total — that ratio (validate ~7, ship ~70) is the discipline.
- Every call logs to the run's cost ledger (`logs/costs.jsonl`): timestamp, beat, prompt hash, credits, result path. Budget exhausted = stage ends, pipeline continues code-only.

Order: hero plates first (they set the look), then b-roll, then alternates. Keep every generation: `footage/raw/` (everything) vs `footage/selected/` (what ships) — the selects are the proof trail.

## Stage 4 — Code overlay

This is where the video becomes *finished* rather than *generated*. Built in Remotion (or the code-film engine for hand-drawn styles):

- **Graphics:** lower thirds, title cards, end cards, logo animations — code-drawn, brand-exact.
- **Captions:** word-timestamp captions (karaoke/scalePop/kinetic styles from the brand-launch skill's `Captions.tsx`); the hook works muted.
- **Beat-synced cuts:** footage cut points snap to the audiomap grid (`analyze-audiomap.py` → `rules/beat-sync.md` Law 1–3) — cuts on downbeats, transitions on energy-phase boundaries.
- **Grade match:** footage plates get a unifying grade (grain + vignette + color) so AI shots and code graphics read as one film, not a collage.
- **QC gates apply:** the brand-launch skill's four evidence gates run here — per-act frame evidence on every overlay pass, honest disclosure at delivery.

The overlay never *covers* footage with decoration — full-bleed footage moments stay textless (taste-raw §1); type lives in its own beats or in lower-third safe zones.

## Stage 5 — ffmpeg assembly

Deterministic assembly, same as the other pipelines:

```bash
ffmpeg -y -framerate 30 -i overlay_frames/f%05d.png -i final_mix.wav \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart out/video.mp4
```

Then `render-qa` machine QC (blackdetect / freezedetect / silencedetect / volumedetect) before any human sees it.

## Run directory layout

```
renders/<brief>/<model>/<date>/
  beat-sheet.md      # Stage 1
  style-lock.md      # Stage 2 (reference plate, soul-id, palette, type, MCSLA template)
  footage/raw/       # every generation, with prompt + credit log
  footage/selected/ # what ships
  overlay/          # Remotion / code-film project
  out/video.mp4     # assembled final
  costs.jsonl       # per-call credit ledger for this run
```

## Failure modes this recipe exists to kill

- Style drift across AI shots → the style lock (Stage 2) + soul-id.
- Typography rendered by the video model → the no-text rule; code draws all type.
- Budget blown on iteration → storyboard-first economics; validation is cheap by design.
- A "generated" feeling → the code overlay + unifying grade; the footage is the plate, not the film.
- Unverifiable quality claims → the four evidence gates + render-qa + honest disclosure.
