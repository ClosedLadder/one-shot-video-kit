# Building a Style — the backlog crank

One page. A future worker takes the next unbuilt entry from `STYLE-BACKLOG.md`
and produces a shippable style pack. No API calls, $0.

## Steps

1. **Claim the entry.** Take the highest-priority unbuilt row. Read its one-line
   art direction until you can picture it. Skim `references/taste.md` (the
   anti-slop laws override your instincts) and the `references/patterns/` recipe
   card closest to the style's motion signature.
2. **Copy the template.** `cp -r styles/_template styles/<slug>/`. Fill `STYLE.md`
   section by section — every section, no deletions. A section that doesn't apply
   gets one honest line (e.g. "Typography: banned in this style — see The look"),
   never silence.
3. **Lock the palette.** 4–6 colours + ground/ink pair, hex codes quoted verbatim
   from the implementation. State the ground rule (what the black/white are) and
   the banned colours. The palette must survive the taste.md blacklist — if it
   drifts toward purple gradients or default dark mode, pick a real palette.
4. **Prove the motion.** Write the Motion language and Shot grammar sections from
   a real mechanism, not adjectives: name the easing curves, the frame-rate or
   redraw signature (boil, step, pop), the transition vocabulary. If you can't
   name the mechanism, you don't understand the style yet — go back to the
   patterns.
5. **Write the pipeline rows.** Fill the feasibility table honestly: `full`,
   `partial`, or `no` per pipeline, with the how. Minimum bar: feasible in two
   pipelines. If ai-footage is feasible, write all three MCSLA example prompts
   (hero still, motion shot, negative prompt) — they must produce on-style
   output from the style-lock alone.
6. **Write SOURCES.md.** Every technique, hex value and timing in the pack gets a
   provenance line: which kit file, reference render, or recipe card it came from.
   No unattributed inventions.
7. **Ship the pack with empty asset slots.** Mark every slot `missing` in the
   Asset inventory table. Slots fill from scored runs of the style (see
   `assets/ASSETS.md`) — never from mockups. A pack with honest empty slots
   ships; a pack with fake slots doesn't.

## Acceptance criteria

- [ ] `styles/<slug>/STYLE.md` exists, all 14 template sections present and filled.
- [ ] One-line art direction matches the backlog row (or the backlog row is updated).
- [ ] Palette table has hex codes; ground rule and banned colours stated.
- [ ] Typography section is explicit — a full spec or a one-line ban.
- [ ] Motion language names mechanisms (curves, frame signatures), not adjectives.
- [ ] Pipeline feasibility table filled; ≥ 2 pipelines feasible; MCSLA prompts
      written for every feasible ai-footage/mixed-flow row.
- [ ] Anti-slop list seeded with ≥ 5 style-specific failures.
- [ ] `SOURCES.md` written; every non-obvious claim has provenance.
- [ ] Asset inventory table present; all slots marked `missing` (or `n/a` for
      model sheets in abstract styles) until real renders exist.
- [ ] `scoreboard/style-memory.md` checked — no entry contradicted.

## Validating a new pack

1. **Template conformance:** diff the pack's section headers against
   `styles/_template/STYLE.md`. Missing section = fail. One-line "n/a" answers
   pass only where the template explicitly allows them (typography ban,
   abstract-style model sheets).
2. **Palette lint:** every hex in the table is a valid 6-digit code; no two
   swatches are visually identical; the palette fails the taste.md blacklist
   check (no purple/blue gradients, no default-dark-with-glow).
3. **Distinctiveness check:** one paragraph — how does this style read differently
   from the three baked styles at a glance? If you can't write it, the style is a
   variant, not a style — demote it to a note inside the nearest pack.
4. **Pipeline smoke test:** for each pipeline marked `full`, name the concrete
   renderer/library/technique that would execute it. "Some AI video model" is not
   a technique — name the style-lock mechanism.
5. **Brief-type fit:** name two scoreboard brief types this style serves and one
   it must never be used for. Update the coverage check in `STYLE-BACKLOG.md`.
6. **Mark it built:** flip the backlog row's status. If the style shipped a scored
   run and all asset slots are filled, mark `BAKED`.
