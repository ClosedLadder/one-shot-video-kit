# Proof-Frame Checklist

Work every item. Write PASS/FAIL + the frame timestamp as evidence. Any FAIL blocks ship.

## Whole-piece (from the contact sheet)

- [ ] **Event per shot.** First frame vs last frame of every shot: something changed. ("Stands in a meadow being cute" is not a shot.)
- [ ] **One focal point per frame.** Squint test: blur your eyes — is the #1 element obvious, #2 second? If everything is same weight, hierarchy is broken.
- [ ] **No two adjacent beats share a visual formula.** Each beat gets its own world.
- [ ] **One world, one hand.** Palette, medium, and linework consistent start to finish; a deliberate color arc is a plus.
- [ ] **Slop test.** Would a stranger believe "AI made this" immediately? If yes, redesign the offending tiles.
- [ ] **Remove test (spot-check 3 tiles).** Cover each element mentally — does the frame improve? If yes, delete it.

## Transitions (stills at every cut)

- [ ] **Every seam has a transition** — into the first shot, between every pair, out of the last. Never a hard start, never a dead stop.
- [ ] **Transition belongs to the story** (wipe / iris / match cut / cut-on-action / whip pan / camera carry). Not the same default twice.
- [ ] **No black frames, no frozen frames, no flashes** at the seam (check ±2 frames).
- [ ] **Screen direction consistent** across cuts (travels right → keeps traveling right).

## Text (stills at every text element)

- [ ] **Reading-time audit:** visible frames ≥ words × 10 frames/word (@30fps) × 1.5. No text in the last 15 frames before a transition. Typing animations finish before the scene ends.
- [ ] **Size:** ≥ 28px at 1080p; headlines 64–88px; nothing < 24px at 1920×1080.
- [ ] **Clearance:** no overlap with faces/action/focal element; karaoke band (lower third) only, unless the brief demands otherwise.
- [ ] **No text on full-bleed motion** unless the brief's brand language verifiably does it (cite evidence).

## Motion & timing

- [ ] **Nothing ever still.** Idles idle, cameras drift, linework boils. A frozen frame is a bug.
- [ ] **Faces act, never snap.** Emotion changes go through anticipation/take/overshoot, not hard swaps.
- [ ] **Reads land in order.** One read at a time; cause before reaction; fast actions, slow meanings. No piled events.
- [ ] **Beats on beats.** Cuts and hits land on musical/narrative downbeats; no continuous visual pulse synced to BGM.

## Audio sync (spot-check with timestamps)

- [ ] **VO phrase onsets** align with visual cuts/reveals (±3 frames).
- [ ] **Word-level sync** where karaoke or lip emphasis is used (needs word timestamps — no guessing).
- [ ] **No watermarks / voice artifacts** in music or VO beds.

## Technical

- [ ] **Clean encode:** no crashes, no dropped frames, correct fps/duration/aspect, audio present and in sync end-to-end.
- [ ] **Determinism note:** re-render command + seeds recorded in the run log.
- [ ] **Proof frame exported from the FINAL file** into `renders/<brief>/<date>/proof/`.
