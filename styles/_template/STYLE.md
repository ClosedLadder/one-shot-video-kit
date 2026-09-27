# Style: <slug>

**Name:** <Human-readable name, e.g. "Flat Vector Motion">
**One-line art direction:** <one sentence — the elevator pitch. A renderer who has never seen this style must picture it from this line alone>
**Status:** `draft` | `baked` — baked means all asset slots filled and it has shipped at least one scored run.
**Version:** 0.1.0 (bump minor on palette/motion changes, patch on copy fixes)
**Origin pipeline:** <code-film | mixed-flow | ai-footage — where the style was born; others must still be feasible>

---

## The look

Describe the medium and rendering technique as law, not vibe:

- **Medium:** <what everything is made of — e.g. painted with p5.brush through `paint()`/`inkLine()`; flat vector shapes; AI-generated plates; folded paper>
- **Dimensionality:** <flat 2D always / 2.5D parallax / true 3D — and what is FORBIDDEN, e.g. no 3D projection in a flat style>
- **Linework/texture:** <boiling ink at 12 redraws/s; clean vector strokes; film grain; thumbprint clay texture — with the technical mechanism that produces it>
- **Lighting:** <how light works here — additive glow, flat cel shadows, volumetric haze, none — and how it's faked>
- **Depth:** <how depth is achieved — overlap/scale/colour, parallax layers, camera moves — never projection in flat styles>
- **Text in frame:** <state the rule up front even if the Typography section owns the details>

## Palette

Base palette (hex codes are law — quote verbatim from the implementation):

| swatch | hex | role |
|---|---|---|
| <name> | `#RRGGBB` | <role — ground, linework, accent, etc.> |

Rules:

- **Ground rule:** <e.g. "No pure black or pure white, ever. PAL.ink is the black; PAL.paper is the white." Or: "true black ground, paper-white type">
- **Palette size per video:** <e.g. 4–6 colours + the ground/ink pair>
- **Colour arc:** <does the palette shift across the film? e.g. cold indigo → warm ochre as mood lifts>
- **Readability:** <character readable against background — separate by value, not just hue; text contrast minimums>
- **Banned colours:** <e.g. taste.md bans purple/blue gradients — restate what this style must never drift into>
- Any hex works in implementation (`mixCol(a, b, k)` blends), but the result must feel like one hand/eye made it.

## Typography rules

<If this style bans text, say so in one line and point at The look. If it allows text, this section is a full spec:>

- **Allowed / banned:** <what text may appear — titles, captions, karaoke lyrics, UI — and what may not>
- **Typefaces:** <named fonts, fallbacks, why — no vague "clean sans">
- **Sizes:** <minimums — headlines 64–88px @1080p, body ≥ 28px; reading-time audit: visible frames ≥ words × 10 × 1.5>
- **Placement:** <karaoke band / lower-third clearance — never over faces or the focal action; no text in the last 15 frames before a transition>
- **Animation:** <how type enters — mask-line rise, scramble, stomp; ref `references/patterns/text-reveals.md`>

## Character & prop conventions

<One-liners are fine if the style has no characters ("no characters — abstract only"). Otherwise:>

- **Anatomy:** <proportions, head:body ratio, what makes this style's faces read — big eyes, dot eyes, no mouth>
- **Hands:** <how hands are drawn/rendered — mittens, three fingers, hidden, photoreal — and the failure mode to avoid>
- **Model-sheet rule:** <every recurring character needs front/3/4/side/back views; turns go through key views, never projection>
- **Props:** <prop style — same medium as characters; props must touch hands, never float near them>
- **Crowds/background actors:** <cheap variant rules — when to simplify>
- **Faces act through the emotion system** (`emotions()` or the style's equivalent), never by snapping eyes/mouths.

## Motion language

- **Easing:** <every move eased slow-in/slow-out — never raw lerp; named curves from `references/patterns/easing-and-rhythm.md`>
- **Cartoon physics:** <anticipation before big moves; squash-and-stretch preserving volume; follow-through and overshoot; overlapping action — eyes lead, body follows, props settle last>
- **Idles:** <nothing is ever still — idles, camera drift, swaying, twinkling, boiling linework; a frozen frame reads as a bug>
- **Timing signature:** <what makes this style's motion recognizable — e.g. 12 redraws/s boil; 12fps step motion; snappy 6-frame pops>
- **Determinism:** <every frame a pure function of timestamp; seeded randomness (`boilSeed(key)`); record seeds — parallel rendering flicker-free>

## Shot grammar

- **Framing:** <default shot sizes, headroom rules, the style's compositional skeleton — one focal point per frame>
- **Camera:** <allowed moves — drift, push-in, whip pan, parallax — and banned moves for this style>
- **Transitions:** <the style's transition vocabulary — wipe / iris / match cut / cut-on-action — never the same default twice, transition at EVERY seam>
- **Act variation:** <if two acts share a compositional skeleton, one is lazy — each beat gets its own world>
- **Peak–end:** <invest disproportionate polish in the climax and the final shot>

## When to use it

**Use for:** <brief types and jobs — e.g. character loops, lyric videos, logo stings with personality. Reference scoreboard brief numbers where they fit.>

**Don't use for:** <what this style cannot do — e.g. photoreal realism, precise UI mockups, on-screen typography. Name the style/pipeline that should be used instead.>

## Pipeline feasibility

One row per pipeline — `full` / `partial` / `no`, with the how:

| pipeline | fit | how |
|---|---|---|
| code-film | <full/partial/no> | <how the style is built here — renderer, libraries, techniques> |
| mixed-flow | <full/partial/no> | <what's AI footage vs code overlay — style-lock notes for footage> |
| ai-footage | <full/partial/no> | <style-lock approach — what goes in the lock prompt, what drifts> |

A style earns a backlog slot by being feasible in at least two pipelines; a baked style must be producible in all three (even if one is a degraded-but-honest variant — say which).

## Example prompts for AI-footage tiers

<MCSLA format — Model·Camera·Subject·Look·Action. Write one of each; they must produce on-style output from the style-lock alone.>

**Hero still (validation):**
```
<MCSLA prompt — the single still that proves the style locks. Include: art-direction line, palette hexes, lighting, texture, camera, what to exclude>
```

**Motion shot (validated concept):**
```
<MCSLA prompt — the same world in motion. Include: shot size, camera move, action, duration feel>
```

**Negative prompt (always append):**
```
<the style's slop list as negatives — e.g. no purple gradients, no 3D render look, no photorealism>
```

## Cost & hardware

- **Marginal cost:** <$0 local compute / credit-gated — with per-shot credit estimates for ai-footage>
- **GPU needs:** <what the technique demands — e.g. p5.brush watercolour wants a real GPU; run `gpu_probe.mjs` on any render machine first>
- **Perf budget:** <e.g. ≤ 2.5 s/frame; big shapes go flat; crowds get the cheap variant>
- **Graceful degradation:** <how the look degrades on weak hardware — e.g. drop watercolour fills, keep flat wash>
- **Parallel + resumable:** <how long renders are split — e.g. `render.mjs --frames --workers=N` then `--encode`>

## Anti-slop for this style (from the field)

<The style-specific failure list — things that have actually gone wrong in this style's renders. Append after every scored run. Seed with the obvious ones:>

- <e.g. jittery stills (missing `boilSeed`) · muddy green-grey glows (yellow painted over blue) · props floating near hands instead of touching>

## Asset inventory

| slot | file | status |
|---|---|---|
| palette swatch | `assets/palette.png` | <filled / missing> |
| model sheet A | `assets/model-sheet-<name>.png` | <filled / missing / n/a — abstract style> |
| model sheet B | `assets/model-sheet-<name>.png` | <filled / missing / n/a> |
| example frame 1 | `assets/example-frame-1.png` | <filled / missing> |
| example frame 2 | `assets/example-frame-2.png` | <filled / missing> |
| example frame 3 | `assets/example-frame-3.png` | <filled / missing> |

Frames must be exported from real renders of this style — never mockups. Slot spec: see `assets/ASSETS.md`.

## Changelog

- 0.1.0 — <date> — initial pack
