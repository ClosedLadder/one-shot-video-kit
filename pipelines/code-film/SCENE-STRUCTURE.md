# Scene Structure — the multi-scene convention

How to organize a longer code-film video (multiple scenes, chapters, or acts) so several files — and potentially several agents — compose one coherent film. Adapted from the 2:36 PDoomVideo production, which built 9 chapters this way and shipped in 2 generations.

## One file per scene

```
src/scenes/
  c01_lab.js        # chapter 1
  c02_chorus1.js    # chapter 2
  ...
  c09_finale.js     # final chapter
```

- **One file = one chapter/scene.** Numbered prefixes (`c01_`, `c02_`…) keep time order obvious in the directory listing.
- Each file is wrapped in an **IIFE**: `(() => { … })();` — nothing leaks into global scope except through the registered API.
- The scene defines shot functions and ends with `shots([[t0, fn], [t1, fn], …])` to register them on the shared timeline.
- In `studio.html`, add one `<script>` tag **per scene file, in order**.

## The shot signature: `fn(t, lt, dur)`

Every shot is a **pure function of time**:

| param | meaning |
|---|---|
| `t` | video time (global seconds) |
| `lt` | time since *this shot* started (local seconds) |
| `dur` | this shot's length in seconds |

Rules that follow from purity:
- Frames render **in parallel and out of order**. No state carried between frames: no counters, no `Math.random()`, no physics that integrates frame by frame. Compute everything from `t` in closed form.
- Stable per-object values come from `hash(i)`; boil comes from `jit()`/`random()` (reseeded 12×/s); each separate element gets its own `boilSeed(key)`.
- **Each shot paints the whole frame**, background included.

## Shared-file discipline

- **Edit only your own scene file.** If a shared helper is missing, write it *privately inside your IIFE* — do not add it to the shared engine.
- If you find a real bug in a shared file, **report it; don't edit it**. Shared files: `core.js`, the character module, `timeline.js`, `studio.html`, `render.mjs`, and any `lyrics.js`-style global data.
- This is what makes parallel scene authorship safe: N scene files, zero merge conflicts.

## Private helpers inside the IIFE

Each chapter file defines its own local vocabulary at the top — set pieces (`wall()`, `floorBand()`, `desk()`), props (`monitor()`, `lamp()`), and cheap background variants — then the shots that use them. A recurring pattern worth copying: a **cheap background extra** (e.g. PDoomVideo's `miniClawd`: same silhouette and face as the hero, flat washes instead of watercolour fills) for crowds and dancers that must be cheap to render.

## Beat-locked timing

If the video has music, set `bpm` (and `offset` = first downbeat) in `src/config.js`, then define a beat helper at the top of each chapter file:

```js
const B = n => OFF + n * BEAT;   // time of beat n — land hits, cuts and takes on beats
```

Cut on bar lines for big changes; give each musical phrase its own visual. Every idle, bounce and dance locks to the same pulse so the whole film shares one beat.

## Karaoke / caption band clearance

If the video carries a lyric or caption band (a timeline-level overlay, not drawn by the shot):

- **The band covers the bottom of the frame (about y 975–1070 on 1920×1080) whenever text is showing. Keep faces and key action above about y 960.**
- Check the "nothing important sits under the band" rule in the review loop with a `--crop` of the band region.
- The timeline adds these automatically: the karaoke/caption band, and chapter-break transitions. A shot can opt a prop out of the automatic overlay by drawing its own (e.g. a hand-drawn meter prop that suppresses the corner meter).

## Transitions at chapter breaks

- **Brush wipes mark chapter breaks.** Inside a chapter, the action carries you across the cut: chomps to black, falls, zooms through an eye, flashes, door slams, whip pans.
- Rule stands at every altitude: a transition at every seam, into the first shot and out of the last one.
- Endings rhyme with openings: the same place, pose or motif, changed.

## One world per chapter, one film overall

- **Sets, not cards.** Each chapter happens in one place; the camera moves through it.
- Pick a palette and setting that carries the whole video, with a **colour arc** across it (e.g. cold night → warm dawn as the mood lifts).
- Recurring set pieces escalate on return (the same stage, bigger each time).
- Screen direction stays consistent across cuts (travel right → keep travelling right); props and characters carry over.

## Perf budget: ≤ 2.5 s per frame

The render log prints ms/frame — watch it.

- Watercolour `fill` cost grows with **vertex count**: big or many-vertex shapes should use flat `wash`; keep fills low-poly.
- Background crowds get the cheap variant (flat washes, no fills).
- Hundreds of shapes/strokes per frame are fine; thousands are not.
- If a chapter is heavy, the `render.mjs --frames --workers=N` path parallelizes across CPU cores and is resumable — budget the heavy chapters accordingly.

## Scale reference

PDoomVideo's chapter files ran **400–900 lines each** for a 2:36 video across 9 chapters — that's the shape of a production that works: meaty per-chapter files, private helpers, no shared-file edits. A 30–60 s video typically needs 3–6 chapter files.
