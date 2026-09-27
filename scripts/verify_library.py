#!/usr/bin/env python3
"""verify_library.py — verify every harvested asset + manifest consistency.

Checks per category dir:
  - each MANIFEST.jsonl record -> file exists, media verifies
    (audio: ffprobe duration > 0; image: valid dimensions;
     video: has video stream + duration > 0)
  - each asset file -> has a manifest record
  - no leftover .part/.src files
Reports failures; exit 1 if any asset is broken (caller should delete/retry).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from harvest_common import media_duration, image_dims, has_video_stream  # noqa: E402

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# (kind, dir) pairs
JOBS = [
    ("audio", os.path.join(KIT, "audio", "music")),
    ("audio", os.path.join(KIT, "audio", "sfx")),
    ("audio", os.path.join(KIT, "audio", "samples")),
    ("image", os.path.join(KIT, "references", "stock", "images")),
    ("video", os.path.join(KIT, "references", "stock", "video")),
]

failures = []
counts = {}


def check_media(kind, path):
    if kind == "audio":
        d = media_duration(path)
        return (d > 0, f"duration={d:.2f}s")
    if kind == "image":
        w, h = image_dims(path)
        return (w > 0 and h > 0, f"{w}x{h}")
    d = media_duration(path)
    ok = d > 0 and has_video_stream(path)
    return (ok, f"duration={d:.2f}s video_stream={has_video_stream(path)}")


for kind, d in JOBS:
    mp = os.path.join(d, "MANIFEST.jsonl")
    recs = {}
    if os.path.exists(mp):
        with open(mp, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    recs[r["filename"]] = r
    files = [x for x in os.listdir(d)
             if os.path.isfile(os.path.join(d, x))
             and not x.endswith((".md", ".jsonl", ".part", ".src"))]
    counts[d] = len(files)
    leftovers = [x for x in os.listdir(d)
                 if x.endswith((".part", ".src"))]
    for x in leftovers:
        failures.append(f"{d}: leftover temp file {x}")
    for fn, r in recs.items():
        p = os.path.join(d, fn)
        if not os.path.exists(p):
            failures.append(f"{d}: manifest record without file: {fn}")
            continue
        ok, info = check_media(kind, p)
        if not ok:
            failures.append(f"{d}: BROKEN {fn} ({info})")
        for field in ("source_url", "license", "harvested", "allowed_intents"):
            if not r.get(field):
                failures.append(f"{d}: {fn} missing provenance field '{field}'")
    for fn in files:
        if fn not in recs:
            failures.append(f"{d}: file without manifest record: {fn}")

print("asset counts:", {os.path.relpath(d, KIT): n for d, n in counts.items()})
if failures:
    print(f"\n{len(failures)} PROBLEM(S):")
    for f_ in failures:
        print("  -", f_)
    sys.exit(1)
print("\nALL OK: every file verifies and has full provenance.")
