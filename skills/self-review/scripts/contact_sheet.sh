#!/usr/bin/env bash
# contact_sheet.sh — tile first/middle/last frame of every shot into one image.
# Usage: contact_sheet.sh <video> <out.jpg> [shot_timestamps...]
#   If shot_timestamps given (comma-separated seconds), sheets are built per shot.
#   Otherwise shot boundaries are auto-detected via ffmpeg scene detection.
# Requires: ffmpeg, ffprobe.
set -euo pipefail

VIDEO="$1"; OUT="$2"; SHIFTS="${3:-}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")"

if [ -n "$SHIFTS" ]; then
  IFS=',' read -ra BOUNDS <<< "$SHIFTS"
else
  # Auto-detect scene cuts; build boundary list 0, cut1, cut2, ..., dur
  mapfile -t CUTS < <(ffprobe -v error -skip_frame nokey -select_streams v:0 \
    -show_entries frame=pkt_pts_time -of csv=p=0 \
    -vf "select='gt(scene,0.35)',showinfo" "$VIDEO" 2>/dev/null | grep -oP 'pts_time:\K[0-9.]+' || true)
  BOUNDS=(0 "${CUTS[@]}" "$DUR")
fi

i=0
for ((s=0; s<${#BOUNDS[@]}-1; s++)); do
  a="${BOUNDS[$s]}"; b="${BOUNDS[$((s+1))]}"
  mid=$(awk "BEGIN{printf \"%.3f\", ($a+$b)/2}")
  for t in "$a" "$mid" "$b"; do
    ffmpeg -v error -y -ss "$t" -i "$VIDEO" -frames:v 1 -q:v 3 "$TMP/f$(printf %03d $i).jpg"
    i=$((i+1))
  done
done

# Tile: 3 columns (first/mid/last per shot), rows = shots. Cap width for readability.
ffmpeg -v error -y -pattern_type glob -i "$TMP/f*.jpg" \
  -filter_complex "scale=426:-1,tile=3x$(awk "BEGIN{printf \"%d\", ($i+2)/3}")" \
  -q:v 4 "$OUT"
echo "contact sheet: $OUT ($i frames, $(( (${#BOUNDS[@]}-1) )) shots)"
