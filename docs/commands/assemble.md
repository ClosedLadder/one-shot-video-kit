---
# Adapted from danielrosehill/claude-ai-video-producer-plugin `commands/assemble.md`
# (MIT). Adapted 2026-09-24 for the one-shot video kit: run-workspace layout,
# ffmpeg skill scripts instead of hand-written ffmpeg, dry-run-first
# discipline, look/check verification before reporting.
---

# Assemble — build a rough cut from selected clips

**Usage:** run inside a run workspace (`renders/<brief>/<model>/<date>/`).
The ffmpeg skill lives at the kit's `skills/ffmpeg/` — use its scripts,
never hand-written ffmpeg.

1. Read `storyboard/shot-list.md` for shot order, durations, and audio cues.
2. List what's present in `clips/edited/` (fall back to `clips/selected/` if
   no edited versions exist).
3. Cross-reference: any shots in the shot list missing from `clips/`? Flag
   them — don't silently ship a gap.
4. Read `run.md` for the target spec (resolution, fps, aspect, format).
5. Plan the assembly with the ffmpeg skill, dry-run first:
   - **Join** scenes in shot order:
     `python3 skills/ffmpeg/scripts/join.py <clips...> --transition <t> --dry-run --json`
   - **VO**: align narration from `generation/voice/` to shot timing —
     `sync.py` to measure offset, `audio.py --replace/--music` to lay it in.
   - **Music + SFX**: `audio.py --music <bed> --duck` (mix under VO),
     keep ambience out of the loudness target's way.
   - **Captions**: `caption.py --srt exports/subtitles/...` (burn or mux
     per the run card).
   - **Loudness**: `loudness.py` to the platform target last.
   - 3+ steps: write a `render.py` project.json instead of chaining by hand.
6. Execute (never point `-o` at a file you didn't create; `--overwrite`
   only to replace a previous draft) and write to a versioned draft path
   (e.g. `drafts/cut-01.mp4`, incrementing — never overwrite a draft).
7. Verify the draft: `check.py` for spec compliance and `look.py` for a
   contact sheet — a probe cannot see a caption on a face. Record the
   sheet path and check result.
8. Append the assembly recipe (script invocations, dry-run plan, check +
   look results) to `logs/production-log.md`.

Don't touch `final/` from this command — that's `export-final.md`.

## What NOT to do

- Don't assemble from `clips/raw/` — only `selected/` or `edited/`.
- Don't re-encode more than necessary: chain in one `render.py` project,
  intermediates at CRF 18, delivery encode last.
- Don't report a draft as done without a `look.py` sheet you actually
  inspected (or the explicit "pixels not inspected" note).
