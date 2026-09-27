#!/bin/bash
# library-curator-cron.sh — twice-daily asset library harvest + curation.
#
# Flow: probe Grok seat -> harvest (music/sfx/samples/images/video/fonts,
#   rotating queries) -> local tech-gate curation -> Grok judging when the
#   seat has balance (auto-skips on 402) -> rising-bar keep/toss ->
#   rsync keepers to the NAS HDD -> commit.
#
# Design: Grok is the taste brain (rubric author + batch judge). Local
# deterministic stages do the cheap filtering so Grok time is spent only
# on judgment. When the seat is depleted the job still runs fully on
# local gates and marks assets unjudged for a later Grok pass.
set -u
KIT=/home/hatch/workspace/one-shot-video-kit
SCRIPTS=$KIT/scripts
LOGDIR=$KIT/logs
CUR=$KIT/assets/curation
LOCK=$CUR/curator.lock
SSH="ssh -F /home/hatch/.ssh/lab_config -o ConnectTimeout=20 -o BatchMode=yes"
MBP=/home/hatch/workspace/goals/ark-runner-v2-build-blitz/hidden_files/mbp.sh
NAS_DIR="/mnt/nas/archive/Media/AI-Video-Assets"
RUN_ID=$(date +%F-%H%M)

exec 9>"$LOCK"
flock -n 9 || { echo "$RUN_ID: another curator holds the lock, exiting"; exit 0; }

LOG=$LOGDIR/library-curator-$RUN_ID.log
mkdir -p "$LOGDIR" "$CUR"
exec >>"$LOG" 2>&1
echo "=== library curator $RUN_ID ==="

# ---- run counter -> rotating queries (cream-of-the-crop first) ----
COUNTER_FILE=$CUR/run-counter
N=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
echo $((N+1)) > "$COUNTER_FILE"

MUSIC_Q=("cinematic" "dark tension" "upbeat corporate" "ambient calm" "epic orchestral" "wonder")
SFX_Q=("whoosh" "impact" "riser" "pop click" "transition swoosh" "deep boom")
SAMPLE_Q=("rain ambience" "forest night" "city rain" "ocean waves" "cafe ambience" "thunderstorm")
IMG_Q=("aerial landscape" "city night" "forest fog" "desert" "ocean" "architecture")
VID_Q=("aerial" "nature" "city" "ocean" "forest" "desert")
pick() { local -n arr=$1; echo "${arr[$((N % ${#arr[@]}))]}"; }

# ---- 1. probe the seat bridge (claude -> codex -> grok, auto-failover) ----
SEAT_OK=0
SEAT_ASK=$SCRIPTS/seat-ask.sh
PROBE_OUT=$($SEAT_ASK --timeout 120 --max-turns 1 "Reply with exactly one word: READY" 2>&1 | tail -3)
if echo "$PROBE_OUT" | grep -q "READY"; then
  SEAT_OK=1; echo "seat bridge: OK"
else
  echo "seat bridge: UNAVAILABLE ($(echo "$PROBE_OUT" | head -1 | cut -c1-120))"
fi

# ---- 2. harvest ----
cd "$SCRIPTS"
STAGE=$KIT/assets/staging/$RUN_ID
mkdir -p "$STAGE"
python3 harvest_music.py --query "$(pick MUSIC_Q)" --count 8 --max-minutes 6 || true
python3 harvest_sfx.py --query "$(pick SFX_Q)" --count 10 || true
python3 harvest_samples.py --query "$(pick SAMPLE_Q)" --count 8 || true
python3 harvest_stock_images.py --query "$(pick IMG_Q)" --count 12 || true
python3 harvest_stock_video.py --query "$(pick VID_Q)" --count 6 --max-minutes 10 || true
python3 harvest_fonts.py --count 8 --offset $((N*8)) || true
python3 verify_library.py 2>&1 | tail -3 || true

# ---- 3. AI judging via the seat bridge (subscription seats, $0 marginal) ----
JUDGMENTS=""
if [ "$SEAT_OK" = 1 ]; then
  BRIEF=$STAGE/curation-brief.md
  {
    echo "# filled $RUN_ID"
    echo "## candidate manifests (new this run)"
    for m in audio/music audio/sfx audio/samples references/stock/images references/stock/video assets/fonts; do
      echo "### $m"; tail -20 "$KIT/$m/MANIFEST.jsonl" 2>/dev/null
    done
    echo "## library stats"; cat "$CUR/bars.json" 2>/dev/null || echo "{}"
    echo "## hunt targets"; grep -A8 "Hunt targets" "$CUR/CURATION-RUBRIC.md" | head -12
  } > "$STAGE/context.md"
  # fill template vars with python (safe substitution)
  python3 - "$SCRIPTS/seat-curation-brief.md" "$STAGE/context.md" "$BRIEF" <<'EOF' || true
import sys
tpl = open(sys.argv[1]).read()
ctx = open(sys.argv[2]).read()
out = tpl.replace("{{CANDIDATE_MANIFESTS}}", ctx[:6000])
out = out.replace("{{LIBRARY_STATS}}", "see context")
out = out.replace("{{HUNT_TARGETS}}", "see context")
open(sys.argv[3], "w").write(out)
EOF
  echo "dispatching curation judging via seat router (curator tier: opus-5-5 -> codex-astra -> grok-seat, up to 25m)..."
  SEAT_OUT=$(python3 $SCRIPTS/seat_router.py --tier curator --file "$BRIEF" --timeout 1500 --max-turns 60 2>>"$LOG" | tail -80)
  echo "$SEAT_OUT" > "$STAGE/seat-output.txt"
  python3 - "$STAGE/seat-output.txt" "$STAGE/judgments.json" <<'EOF' || true
import sys, json, re
txt = open(sys.argv[1]).read()
m = re.search(r"\{[\s\S]*\"judgments\"[\s\S]*\}", txt)
if m:
    try:
        d = json.loads(m.group(0))
        json.dump(d, open(sys.argv[2], "w"), indent=2)
        print(f"grok judgments: {len(d.get('judgments', {}))} scored")
    except Exception as e:
        print(f"judgment parse failed: {e}")
else:
    print("no judgment JSON found in seat output")
EOF
  [ -f "$STAGE/judgments.json" ] && JUDGMENTS="--grok $STAGE/judgments.json"
  # apply any rubric updates grok proposed (logged for review, applied on next funded run)
  echo "--- grok run notes ---"; grep -A3 rubric_updates "$STAGE/seat-output.txt" | head -8 || true
else
  echo "grok unavailable: local-gates-only mode, assets marked unjudged"
fi

# ---- 4. curate: tech gates + rising bar + caps ----
python3 "$SCRIPTS/curate.py" $JUDGMENTS --commit > "$STAGE/curation.json" 2>&1 || true
python3 - "$STAGE/curation.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
print(f"curation: {d['n_keep']} keep, {d['n_toss']} toss")
print("bars:", json.dumps(d["bars"]))
EOF

# ---- 5. sync keepers to NAS HDD ----
$SSH spark1 "mkdir -p $NAS_DIR/{music,sfx,samples,images,stock-video,fonts}" 2>&1 | tail -1 || true
for spec in "audio/music:music" "audio/sfx:sfx" "audio/samples:samples" \
            "references/stock/images:images" "references/stock/video:stock-video" \
            "assets/fonts:fonts"; do
  src="${spec%%:*}"; dst="${spec##*:}"
  rsync -a --ignore-existing -e "$SSH" "$KIT/$src/" "spark1:$NAS_DIR/$dst/" 2>&1 | tail -2 || true
done
# manifests ride along so the NAS copy is self-describing
rsync -a -e "$SSH" "$KIT/assets/curation/" "spark1:$NAS_DIR/_curation/" 2>&1 | tail -1 || true

# ---- 6. commit kit state ----
cd "$KIT"
git add -A >/dev/null 2>&1
git commit -qm "library curator $RUN_ID (seat=$SEAT_OK)" 2>&1 | tail -1 || true

echo "=== done $RUN_ID seat=$SEAT_OK ==="
