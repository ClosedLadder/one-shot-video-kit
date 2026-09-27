# FFmpeg skill — gotchas

Expanded notes for flags referenced from `SKILL.md`. For the full flag list, run
`python3 skills/ffmpeg/scripts/<script>.py --help`.

## audio-only-files

Audio is a first-class input: `probe`, `cut`, `silence`, `loudness`, `audio`, `sync`, `check --platform podcast`, `render --template podcast` accept WAV, FLAC, MP3, M4A/AAC, OGG, Opus. Scripts needing a picture (`fit`, `caption`, `overlay`, `graphics`, `color`, `export`, `scenes`, `look`) refuse audio-only inputs.

## hdr-and-colour

HDR (iPhone, HDR10) re-encoded through an SDR path goes flat. `hdr: true` is a real PQ/HLG/DV signal; `bt2020_or_hdr: true` also covers BT.2020 SDR.

## log-footage

Log footage (S-Log/V-Log/C-Log) tagged SDR looks grey: `probe.py --analyze`, then `color.py --lut` first.

## keyframe-cuts

A `-c copy` cut can start on a wrong or frozen frame; `cut.py` re-encodes past a 0.5 s snap.

## variable-frame-rate

VFR phone/screen recordings: re-encodes conform to CFR; `cut.py` switches to `--accurate`; pick rate with `fit.py --fps` when odd.

## sync-and-drift

Sync `confidence` under 0.3 (or a huge offset) is suspect — check sources; sync aligns audio tracks, never lip sync.

## loudness-and-ambience

"Normalised" audio can still clip (check true peak). Ambience at -40 LUFS or below must never be raised to a speech target.

## captions-fonts-and-text-order

Captions burned before a crop/resize land off-frame; burned small then upscaled by `export.py` come out soft.

## emoji

Emoji need `--emoji-assets DIR` (PNG per glyph) for colour; without it they render monochrome.

## fonts-by-script

Non-Latin text picks a font by script (`graphics.py` shapes via libass). No font = failed job.

## reframing-fps-and-duration

`--fit crop` 16:9→9:16 throws away most of the width. "60 seconds" by speed vs by trim are different answers.

## platform-safe-zones

TikTok/Reels cover bottom fifth and right column — templates keep text out; `look.py --safe tiktok` shows zones.

## highlights

`scenes.py --highlights` ranks by loudness or duration, not meaning — check the sheet before trusting picks.

## chaining-and-speed

Re-encodes use x264 `medium`; chain 3+ steps in one `render.py` project when possible.
