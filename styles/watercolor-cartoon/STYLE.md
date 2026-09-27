# Style: watercolor-cartoon

The kit's **Style A** — the look produced by the code-film pipeline. Hand-painted 2D cartoon: watercolour washes, boiling ink linework, flat colour. The PDoomVideo (2:36, 2 generations) and ClaudeAnimationBase demo ("The fallen star") are the reference renders.

## The look

- **Medium:** everything painted with p5.brush through `paint()` and `inkLine()`. Characters: flat `wash` colour + ink outline. Backgrounds: soft watercolour `fill` shapes (bleeding edges, pigment texture), usually no outline or a thin one.
- **Linework boils:** every drawing wobbles slightly, 12 redraws/second, like hand-drawn animation on twos. Still things must hold their boil (per-element `boilSeed()`), or they jitter.
- **Flat 2D, always.** No 3D projection, no `rotateY`/WEBGL, no perspective boxes. Turns happen through drawn key views (front → 3/4 → side → back), like a cartoon model sheet. Depth comes from overlap, scale and colour (farther = smaller, bluer, paler).
- **No text in frame.** Reactions are painted marks (`!` `?` zzz sweat hearts bulbs rain clouds), never letters. (If a word is truly the joke, one or two painted words, once.)
- **Light is additive:** `glow()` for anything that shines — p5.brush mixes colour like pigment, so painted yellow-over-blue turns green.

## Palette rules

Base palette (`PAL` in `src/core.js`):

| swatch | hex | role |
|---|---|---|
| paper | `#F3EBDC` | ground — warm cream, never pure white |
| ink | `#2B2233` | linework — soft near-black, never pure black |
| clay / clayDk / clayLt | `#D97757` `#A84D33` `#F2A283` | terracotta family (the bundled character's body) |
| night / indigo | `#1F2550` `#2F3C7A` | dark grounds |
| rose / ochre | `#E27A92` `#E8AA38` | warm accents |
| sap / teal | `#6E9F58` `#3A9C98` | greens |
| violet / sky | `#7B5CA8` `#8EC3E6` | cool accents |
| cream | `#FFF5E2` | highlights |

Rules:
- **No pure black or pure white, ever.** `PAL.ink` is the black; `PAL.cream`/`PAL.paper` is the white.
- **Small palette per video.** Pick 4–6 colours + the paper/ink pair, and run a **colour arc** across the film (e.g. cold night indigo → warm dawn ochre as the mood lifts).
- Characters stay clearly readable against the background — separate by value, not just hue.
- Any hex works (`mixCol(a, b, k)` blends), but the palette must feel like one hand painted it.

## Motion grammar

- Every move is eased (slow in / slow out) — never a linear `lerp`.
- Anticipation before big moves; squash-and-stretch on impacts; follow-through and overshoot after.
- Overlapping action: eyes lead, body follows, arms/hats/props drag behind and settle last.
- Nothing is ever still: idles, camera drift, swaying grass, twinkling stars — a frozen frame reads as a bug.
- Faces act through the emotion system (`emotions()`), never by snapping eyes/mouths.

## When to use it

**Use for:** character loops, short narrative films, lyric/music videos, logo stings with personality, anything where a handmade, warm, distinctive look is the point. Briefs 1, 2 and 5 on the scoreboard.

**Don't use for:** photoreal or cinematic realism (that's mixed-flow/ai-footage), precise UI mockups or data-viz (code-crisp vector styles read better), anything needing on-screen typography (this style bans text).

## Cost and hardware

- **$0 marginal.** Render cost is local compute only.
- p5.brush watercolour wants a **real GPU**: the MBP's M4 GPU is fine, the Sparks are better. Run `gpu_probe.mjs` on any render machine first.
- On integrated-only paths, drop the watercolour `fill`s (use flat `wash`) — the look degrades gracefully.
- Perf budget: **≤ 2.5 s/frame** (watch the render log's ms/frame). Big watercolour shapes go flat; crowds get the cheap variant. See SCENE-STRUCTURE.md.
- Parallel + resumable: `render.mjs --frames --workers=N` then `--encode` — a heavy film renders overnight on a Spark.

## Anti-slop for this style (from the field)

Signs/captions/labels · characters standing still and smiling · one constant speed with piled events · moments over before the viewer gets them · tiny character in a huge empty landscape · snapping faces · mirrored/twinning motion · timid unreadable poses · jittery stills (missing `boilSeed`) · hard cuts everywhere · 3D rotation · plain p5 shapes or digital glows mixed into the paint · muddy green-grey glows (yellow painted over blue) · props floating near hands instead of touching · every shot a different world.
