# Device-specific notes

Probe first with `python3 skills/ffmpeg/scripts/probe.py INPUT --analyze`.

| Source | Notes |
|---|---|
| iPhone HDR | Preserve HDR metadata; avoid accidental SDR flattening (see `gotchas.md#hdr-and-colour`) |
| GoPro / action cam | Often wide FOV + heavy sharpening; check `scenes.py --shots` before reframing |
| DJI drone | Variable wind noise on audio; inspect with `scenes.py --speech` |
| Screen recordings | VFR common; conform fps with `fit.py --fps` |
| Zoom / Meet exports | Letterboxing and variable quality; probe dimensions before crop |

For platform delivery checks, use `check.py --platform <name>` and templates under `templates/`.
