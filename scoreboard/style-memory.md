# Style Memory — persistent corrections

Append-only. Every human note absorbed here so the same correction is never given twice. Each entry references the run that produced it. The agent reads this file in SKILL.md Step 1, every run.

Format per entry: `## <date> — <run/brief> — <judge>` then the correction as an imperative rule.

---

## 2026-09-24 — kit seed — neo

**Pure-function frames law.** Every frame must be a pure function of its timestamp: no carried state, no unseeded randomness. Seed everything (`hash(i)`, per-element boil seeds) and record seeds in the run log. Violation symptom: parallel frame rendering flickers; re-renders drift. (Source: OrcaRouter's law via sprint analysis.)

## 2026-09-24 — kit seed — neo

**Karaoke band clearance.** On-screen words are allowed ONLY for sung/karaoke-synced lyrics or brief-demanded titles, confined to the lower-third band, never overlapping faces or the focal action. Everything else: show it, don't write it. (Source: ClaudeAnimationBase's "no text unless karaoke" + taste law 31.)

## 2026-09-24 — kit seed — neo

**Storyboard before code.** Write `STORYBOARD.md` (logline + acts + shots + ordered reads) before any scene code, and list the reads the viewer must understand per shot. Timing failures come from skipping this, not from bad easing curves. (Source: ClaudeAnimationBase workflow + taste law 28.)

## 2026-09-24 — scoreboard baseline (5 briefs, STUDIO/code-film) — neo

**Two-point strokes are invisible.** p5.brush `spline()` silently drops 2-point `inkLine` paths — no error, just missing rain, stems, legs, axes, knurling, antennae. Rule: every `inkLine` gets ≥3 points; insert a textual midpoint for straight segments. (Cost us two full review cycles on the b5 storm before we caught it.)

**Verify absence, don't assume presence.** The missing rain survived two "looks fine" reviews because dark-on-dark thin strokes are easy to miss at contact-sheet scale. When a shot's key effect is subtle, render one full-res still and measure pixel stats (mean/std of a sky crop), not eyeballs.

**Reading audits need frame math, not vibes.** The b1 wordmark hold (48f vs 60f guide) and b4 logo hold (70f vs 90f minimum) were only caught by counting frames against the guide. Build the audit into the storyboard timing pass: logo ≥90f, headline ≥60f, 15 text-free frames before any transition.

**9:16 by pan-and-scan, not by re-layout.** The engine is 1920×1080-native; rebuilding five scenes for vertical wasn't in budget. Per-brief ffmpeg `crop=608:1080:x='<expr>'` with shot-aware x(t) (jumps hidden under transitions, smooth pans where the eye follows action) plus lanczos upscale is honest, reproducible, and scored fairly: center-weighted compositions (b1, b4) lose nothing; wide diagrams (b3) suffer most.

**Two-pass audio is non-negotiable.** Finalize the WAV, audition/measure it (−16.8 dB mean VO), THEN mux with `-c:v copy`. Never encode AAC straight from a filtergraph in the same pass as video.

**Fallback fonts beat blocked fonts.** The Google Fonts `<link>` caused `networkidle0` timeouts in headless Chrome; removing it and using local fallbacks unblocked the whole farm. For painted work the fallback handwriting-style stack is visually fine.

**Invented stand-ins must be labeled.** Missing Given assets (logos, scripts, data, premise) were authored locally (EMBER & OAK, illustrative BLEU numbers). Every substitution is logged in the run log AND the score notes — never let an invented number read as measured.
