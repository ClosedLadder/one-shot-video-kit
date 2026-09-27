# SOURCES.md — shot-recipes

## Origin
- Repo: `video-shotcraft` (cards vendored under `skills/shot-recipes/`),
  SKILL.md by vincentwei1021. Cards live at `references/shots/<category>/<name>.md`
  (byte-identical copies of `gallery/source/<name>.md`).
- The cards are written in Chinese. Kept verbatim — translations would drift from the
  proven timing values; the English `cards-index.md` in this directory provides
  the one-liner, duration, and energy for every card so agents can pick without
  reading all 50.

## Kept
- **50 of 157 recipe cards**, grouped by video job into `cards/{intros,text-reveals,
  transitions,product,data-viz,outros,emphasis-camera}/`:
  - intros/ (6): brand-ink-open, spotlight-hero-card, crane-rise-reveal, fracture,
    dataviz-landscape-open, lead-word-zoom-assemble
  - text-reveals/ (10): typewriter-moves, document-typewriter-reveal, scramble,
    text-as-mask, letterspace-materialize, neon-triple-marquee, paper-title-card,
    type-entrance-moves, assemble-then-type-flyin, stroke-segment-build
  - transitions/ (10): shot-transitions ★, wipe-transitions, bottom-push-stack-wipe,
    color-block-step-wipe, circle-match-iris, blur-slide, gradient-transition,
    white-flash-logo-simplify-cut, transition-hidden-cut ★, beat-cut-moves
  - product/ (7): deck-deal-flyin, crash-zoom-punch, product-card-progressive-assemble,
    card-stack, list-stack-press, page-waterfall-wall, morph-from-primitive
  - data-viz/ (7): chart-live-moves, counter-confetti, gauge-readout-moves,
    odometer-digit-roll, timeline-travel, ring-diagram-annotation-reveal,
    cycle-glass-node-morph
  - outros/ (5): outro-group-photo-launch, logo-shrink-wordmark-lockup,
    grain-dissolve, ui-strip-away-outro, ui-to-brand-morph
  - emphasis-camera/ (5): impact-feedback ★, particle-celebrate-hits,
    overhead-camera-moves, depth-layer-moves, cel-flash-stomp
  (★ = technique pick-list card, not an energy-slot shot.)
- `sequences/promo-energy-arc.md` — the default 4-segment energy skeleton; the
  "fill slots before picking cards" pattern is the key one-shot reliability trick.
- `references/aesthetic-rules.md` — timing/taste rules with case law (R1–R4, Q1–Q11,
  S1–S5, C1–C3, P1–P4). Directly usable as a QC checklist.
- `references/music-beat-sync.md` — beat-grid methodology with hard tolerances
  (≤3f cut error, 1.28f AAC priming offset, ≤3 full-frame slams per film).
- New docs written here: `SKILL.md` (router: pick-a-named-shot pattern),
  `cards-index.md` (English one-liner index for all 50 cards).

## Dropped
- **107 other cards**: UI-interaction-heavy cards (chat bubbles, command palettes,
  dictation pills, theme switches) — product-demo specific, not general video jobs.
  Duplicative entries (draw-svg-trace vs stroke-segment-build, scramble vs
  scramble-decode-in-type-entrance-moves, several neon/flash variants).
- `gallery/` (161–214 browsable motion previews, ~GBs of MP4s) — too heavy for the
  kit; card parameter tables carry the value.
- `demos/` and `workbench/` — full Remotion projects (~MBs of node_modules-scale
  scaffolding); the kit's pipelines directory owns the render engine.
- `template/` (Ink Press template project) — a specific product-promo template;
  not general-purpose one-shot knowledge.
- `jianying-export/` — Jianying-specific export tooling; not portable.
- `assets/` (audio library) — audio belongs to the kit's `audio/` lane, not skills.
- `references/pipeline.md`, `guided-free-creation.md`, `final-review.md`,
  `sound-design.md`, `workbench.md`, `jianying-export.md`, `sequences/` (other),
  `ATTRIBUTION.md` — workflow docs tied to the video-shotcraft pipeline itself;
  the essential timing content is captured in `aesthetic-rules.md` and
  `music-beat-sync.md`.

## Why this cut
The one-shot trick is "pick a named shot, don't invent motion." 50 cards cover
every standard video job (intro → reveals → transitions → product → data → outro)
with the most versatile, least product-demo-specific entries. The remaining 107
cards are mostly narrow UI-demo shots whose value is in their reference demos
(which live upstream), not in prose rules.
