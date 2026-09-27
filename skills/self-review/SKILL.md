# Self-Review Skill ("the watch skill")

You are the agent's eyes. Your job: inspect renders as a hostile stranger would, catch everything, and refuse to ship until the proof-frame checklist passes.

You operate in a loop with the builder: **render → inspect → fix → re-render**. Minimum one full loop per run. Preview cheap, ship once.

## The loop

### 1. Preview at 0.3 scale
Render a low-res proxy first (`-vf scale=iw*0.3:ih*0.3` or the pipeline's low-res flag). Judge pacing, composition, and timing here — never burn a full render on a pacing mistake. Watch it at 1x as a VIEWER, not as its author.

### 2. Contact sheet: the shape of the whole piece
Run `scripts/contact_sheet.sh <video> <out.jpg>` — it extracts first/middle/last frame of every shot (shot boundaries detected via ffmpeg scene detection, or passed explicitly as timestamps) and tiles them into one image.

Read the sheet left-to-right, top-to-bottom and ask:
- Does every shot have an **event** (first frame ≠ last frame in story terms)?
- One focal point per tile? Hierarchy by size/contrast/position/weight?
- Does any tile look frozen, empty, or template-generated?
- Do adjacent tiles share a visual formula? (Two "map + arcs" beats in a row = one is lazy.)
- Color arc across the piece? One world, one hand?

### 3. Stills at cue points
Run `scripts/stills_extract.sh <video> <timestamps...> --out=dir/` for:
- **Every transition** (2 frames before / on / 2 frames after the cut)
- **Every text element** (check clearance, size ≥ 28px at 1080p, no overlap with faces/action, on screen long enough: words × 10 frames/word @30fps × 1.5 breathing room)
- **Faces, hands, contacts, glows** — full-res crops; look for broken geometry, melted features, artifact smears
- **First and last frames of the whole video** — never a hard start, never a dead stop

### 4. Proof-frame checklist
Work through `proof-checklist.md` item by item. Write PASS/FAIL per item with the frame timestamp as evidence. Any FAIL = fix + re-render + re-inspect.

### 5. Proof frame from the FINAL file
After the final encode, extract one representative still **from the shipped MP4 itself** (never from a preview or intermediate) into `renders/<brief>/<date>/proof/`. This is the frame that represents the run in the gallery and the scoreboard.

## Rules of the watch

- **You are not the builder.** Read the frames as a first-time viewer. The builder knows what was intended; you only know what is on screen.
- **A frozen frame is a bug.** Something must always be moving; linework must boil; idles must idle.
- **Text is guilty until proven innocent.** Every word must pass the reading-time audit and the karaoke-band rule (references/taste.md).
- **Transitions are graded.** Every seam gets a transition that belongs to the story. A plain cut is allowed only on action or as a deliberate smash cut.
- **Log everything.** Loop count, timestamps inspected, FAILs found, fixes applied → the run log and scores.jsonl notes field.
