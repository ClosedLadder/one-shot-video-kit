# Asset Sync — NAS staging plan

> **Status (2026-09-24): NAS workspace NOT provisioned.** Everything stages
> locally in the kit repo (`audio/`, `references/stock/`). This document
> describes the intended sync layout so the move is mechanical once the NAS
> workspace exists. Nothing in the harvesters depends on the NAS.

## Intended layout

Once Steven provisions the NAS video-kit workspace (coordinate path/ownership
with the existing NAS hardening owner before creating anything — see kit
`DECISIONS.md` / memory on the NAS gate), the kit's asset libraries sync to:

```
<nas-video-kit>/assets/
├── music/        <- kit audio/music/        (WAV + MANIFEST.jsonl)
├── sfx/          <- kit audio/sfx/
├── samples/      <- kit audio/samples/
├── stock-images/ <- kit references/stock/images/
└── stock-video/  <- kit references/stock/video/
```

One directory per category keeps rsync simple and lets renders pull only
the categories they need.

## Sync command (when NAS is ready)

Run from the kit root, after confirming the NAS mount/path with Steven:

```bash
NAS=<provisioned-nas-video-kit-path>   # e.g. /mnt/nas/archive/video-kit
rsync -av --delete \
  --include='*/' --include='*.wav' --include='*.mp4' --include='*.jpg' \
  --include='*.jsonl' --include='*.md' --exclude='*' \
  audio/music/     "$NAS/assets/music/" \
  audio/sfx/       "$NAS/assets/sfx/" \
  audio/samples/   "$NAS/assets/samples/" \
  references/stock/images/ "$NAS/assets/stock-images/" \
  references/stock/video/  "$NAS/assets/stock-video/"
```

Notes:

- `.src*` / `*.part` files are never synced (partial downloads).
- `MANIFEST.jsonl` files MUST sync — they are the provenance record the
  publish gate (`scripts/check-publish-assets.py`) reads.
- Never `rsync --delete` in the reverse direction; the NAS is a mirror,
  the kit repo is the source of truth.
- Expected volume at current harvest depth (10–15 assets/category):
  ~150–250 MB audio, ~50–100 MB images, ~0.5–2 GB video. Fine for a first
  sync; re-evaluate before scaling to hundreds of assets.

## What does NOT sync

- Run workspaces (`renders/`) — runs sync per their own retention rule.
- `scripts/` harvesters need no sync; they run on any machine with the kit.
- Anything under private lab bus inboxes on your machines — never touch from a run workspace.
