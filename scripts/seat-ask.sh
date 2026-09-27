#!/bin/bash
# seat-ask.sh — thin backwards-compatible wrapper over seat_router.py
# (kept because cron scripts and docs reference it).
HERE="$(cd "$(dirname "$0")" && pwd)"
ARGS=()
for a in "$@"; do
  [ "$a" = "--frontier" ] && ARGS+=(--tier frontier) || ARGS+=("$a")
done
exec python3 "$HERE/seat_router.py" "${ARGS[@]}"
