#!/usr/bin/env bash
# stills_extract.sh — pull full-resolution stills at exact cue points.
# Usage: stills_extract.sh <video> --out=<dir> <t1> [t2 ...]
#   Timestamps in seconds. Each still is named still_<t>.png (full res, PNG).
# Requires: ffmpeg.
set -euo pipefail

VIDEO="$1"; shift
OUT="stills"
TS=()
for a in "$@"; do
  case "$a" in
    --out=*) OUT="${a#--out=}" ;;
    *) TS+=("$a") ;;
  esac
done
mkdir -p "$OUT"
[ ${#TS[@]} -gt 0 ] || { echo "usage: stills_extract.sh <video> --out=<dir> <t1> [t2 ...]" >&2; exit 1; }

for t in "${TS[@]}"; do
  safe="$(printf '%s' "$t" | tr '.' '_')"
  # -ss after -i = accurate seek for inspection frames
  ffmpeg -v error -y -i "$VIDEO" -ss "$t" -frames:v 1 "$OUT/still_${safe}.png"
  echo "$OUT/still_${safe}.png  (t=${t}s)"
done
