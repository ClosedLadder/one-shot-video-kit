---
# Adapted from danielrosehill/claude-ai-video-producer-plugin
# `commands/export-final.md` (MIT). Adapted 2026-09-24 for the one-shot
# video kit: run-workspace layout, ffmpeg skill scripts for encode/check,
# sidecar report feeds the kit's scoreboard + cost ledger.
---

# Export final — encode the locked draft to spec

**Usage:** run inside a run workspace (`renders/<brief>/<model>/<date>/`).
The ffmpeg skill lives at the kit's `skills/ffmpeg/`.

1. Identify the locked draft (the latest versioned cut in `drafts/` —
   if it isn't clear which is locked, stop and ask).
2. Read `run.md` for the final delivery spec (codec, bitrate, resolution,
   container, subtitle policy, loudness target).
3. Check `exports/subtitles/` for the `.srt`/`.vtt` to embed (soft or
   burned per the run card). Check `exports/` for a poster frame if the
   run card asks for one.
4. Encode with the ffmpeg skill:
   `python3 skills/ffmpeg/scripts/export.py <draft> --preset <youtube|reels|...>`
   (or a custom `--codec`/`--quality` pass for non-platform specs),
   `--normalize` to hit the loudness target in the same call.
   Write to `final/<project-name>-final.<ext>` — never overwrite an
   existing final; version with `-v2`.
5. Verify: `check.py final/<file> --platform <X>` (all FAIL rows fixed or
   explicitly waived), plus `look.py --tiles 3x2` proof frames into
   `proofs/` — the final isn't done until you've seen it.
6. Write the sidecar `final/<project-name>-final.md`:

   ```md
   # <project> — final
   - Spec: <codec, resolution, fps, container, subtitles policy>
   - Runtime / file size: <from probe>
   - Source draft: <drafts/cut-NN.mp4>
   - Models used: <rolled up from logs/production-log.md>
   - Total estimated cost: $<from budgets/>
   - Check result: <check.py platform rows>
   - Proof frames: <proofs/*.png>
   ```
7. Append a `FINAL EXPORT` entry to `logs/production-log.md` and append
   the cost actuals to the kit's `logs/costs.jsonl`.
8. Absorb corrections into `scoreboard/style-memory.md` and copy the
   best proof frames to `references/gallery/`.

## What NOT to do

- Don't export a draft that failed self-review — fix, re-draft, then export.
- Don't overwrite `final/` — version with `-v2`.
- Don't skip the sidecar — the scoreboard and cost ledger need it.
