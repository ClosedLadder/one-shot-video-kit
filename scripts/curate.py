#!/usr/bin/env python3
"""curate.py — deterministic curation engine for the asset library.

The "toss crap as the library grows" function. Runs every harvest cycle:

  1. Load every category MANIFEST.jsonl; verify files exist + tech gates
     (ffprobe: audio/video duration > 0; images: readable dimensions;
     fonts: font magic bytes).
  2. Dedupe by sha1 (belt-and-braces; harvesters dedupe at intake).
  3. Apply Grok judgments (optional --grok FILE): {file: {score 1-10}}.
  4. Rising bar: per-category bar in assets/curation/bars.json. A scored
     asset keeps iff score >= bar. After each cycle the bar ratchets to
     max(bar, p75 of scored library) — the library only gets pickier.
     Unjudged assets (Grok unavailable) keep on tech-gates alone but never
     ratchet the bar.
  5. Caps: over-cap categories cull lowest-scored first.

Output: JSON {keep: [...], toss: [{file, reason}], bars: {...}} on stdout.
With --commit, writes bars.json and a toss log.

Usage:
  curate.py [--grok judgments.json] [--commit]
"""
import argparse
import json
import os
import subprocess
import sys

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CUR_DIR = os.path.join(KIT, "assets", "curation")
BARS = os.path.join(CUR_DIR, "bars.json")

CATEGORIES = {
    "music":       {"manifest": "audio/music/MANIFEST.jsonl",        "cap": 400, "bar0": 6.0},
    "sfx":         {"manifest": "audio/sfx/MANIFEST.jsonl",          "cap": 600, "bar0": 6.0},
    "samples":     {"manifest": "audio/samples/MANIFEST.jsonl",      "cap": 400, "bar0": 6.0},
    "images":      {"manifest": "references/stock/images/MANIFEST.jsonl", "cap": 600, "bar0": 6.0},
    "stock-video": {"manifest": "references/stock/video/MANIFEST.jsonl",  "cap": 300, "bar0": 6.0},
    "fonts":       {"manifest": "assets/fonts/MANIFEST.jsonl",       "cap": 300, "bar0": 5.0},
}

FONT_MAGICS = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1")


def ffprobe_ok(path, kind):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration:stream=width,height",
             "-of", "json", path],
            capture_output=True, timeout=30, text=True)
        d = json.loads(out.stdout or "{}")
        dur = float((d.get("format") or {}).get("duration") or 0)
        if kind in ("music", "sfx", "samples", "stock-video") and dur <= 0:
            return False, "zero duration"
        if kind == "images":
            streams = d.get("streams") or [{}]
            if not streams[0].get("width"):
                return False, "unreadable image"
        return True, ""
    except Exception as e:
        return False, f"ffprobe: {e}"


def tech_gate(cat, path):
    if not os.path.exists(path):
        return False, "missing file"
    if os.path.getsize(path) == 0:
        return False, "empty file"
    if cat == "fonts":
        with open(path, "rb") as f:
            if f.read(4) not in FONT_MAGICS:
                return False, "bad font magic"
        return True, ""
    if cat in ("music", "sfx", "samples", "stock-video", "images"):
        return ffprobe_ok(path, cat)
    return True, ""


def load_bars():
    if os.path.exists(BARS):
        with open(BARS) as f:
            return json.load(f)
    return {c: {"bar": v["bar0"], "n_scored": 0} for c, v in CATEGORIES.items()}


def p75(xs):
    if not xs:
        return 0
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(0.75 * len(xs)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grok", default="")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    judgments = {}
    if args.grok and os.path.exists(args.grok):
        with open(args.grok) as f:
            judgments = json.load(f).get("judgments", {})
    bars = load_bars()
    keep, toss = [], []
    seen = set()

    for cat, cfg in CATEGORIES.items():
        mp = os.path.join(KIT, cfg["manifest"])
        if not os.path.exists(mp):
            continue
        entries = []
        with open(mp) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
        scored = []
        catdir = os.path.dirname(cfg["manifest"])
        for e in entries:
            rel = os.path.join(catdir, e.get("filename", ""))
            sha = e.get("sha1", "")
            if sha in seen:
                toss.append({"file": rel, "reason": "duplicate sha1"})
                continue
            seen.add(sha)
            ok, why = tech_gate(cat, os.path.join(KIT, rel))
            if not ok:
                toss.append({"file": rel, "reason": why})
                continue
            j = judgments.get(rel) or judgments.get(e.get("filename", ""))
            score = (j or {}).get("score") if isinstance(j, dict) else j
            bar = bars.get(cat, {}).get("bar", cfg["bar0"])
            if score is None:
                e["_unjudged"] = True
                e["_rel"] = rel
                keep.append(e)
            elif score >= bar:
                e["_score"] = score
                e["_rel"] = rel
                scored.append(score)
                keep.append(e)
            else:
                toss.append({"file": rel, "reason": f"score {score} < bar {bar}"})
        # cap enforcement: cull lowest-scored first (unjudged survive)
        cat_keep = [e for e in keep if e.get("_rel", "").startswith(catdir)]
        if len(cat_keep) > cfg["cap"]:
            scored_only = sorted([e for e in cat_keep if "_score" in e],
                                 key=lambda e: e["_score"])
            n_cull = len(cat_keep) - cfg["cap"]
            for e in scored_only[:n_cull]:
                toss.append({"file": e["_rel"],
                             "reason": f"over cap {cfg['cap']}: culled score {e['_score']}"})
                keep.remove(e)
        # ratchet the bar
        if scored:
            new_bar = max(bars.get(cat, {}).get("bar", cfg["bar0"]), p75(scored))
            bars[cat] = {"bar": round(new_bar, 2), "n_scored":
                         bars.get(cat, {}).get("n_scored", 0) + len(scored)}

    result = {"keep": [e.get("_rel") for e in keep], "toss": toss, "bars": bars,
              "n_keep": len(keep), "n_toss": len(toss)}
    if args.commit:
        os.makedirs(CUR_DIR, exist_ok=True)
        with open(BARS, "w") as f:
            json.dump(bars, f, indent=2)
        with open(os.path.join(CUR_DIR, "toss.log"), "a") as f:
            for t in toss:
                f.write(json.dumps(t) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main() or 0)
