#!/usr/bin/env python3
"""harvest_fonts.py — free font harvester ($0).

Source: github.com/google/fonts (SIL Open Font License 1.1 — publish-safe).
Pipeline:
  GitHub contents API -> rotate through family dirs -> download OFL.txt +
  TTFs -> magic-byte verify -> provenance in assets/fonts/MANIFEST.jsonl

Usage:
  harvest_fonts.py [--count N] [--offset N] [--query SUBSTRING]
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_DIR = os.path.join(KIT, "assets", "fonts")
MANIFEST = os.path.join(FONT_DIR, "MANIFEST.jsonl")
API = "https://api.github.com/repos/google/fonts/contents/ofl"
RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl"


def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "one-shot-video-kit/1.0",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def seen_shas():
    shas = set()
    if os.path.exists(MANIFEST):
        with open(MANIFEST) as f:
            for line in f:
                try:
                    shas.add(json.loads(line).get("sha1", ""))
                except Exception:
                    pass
    return shas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--query", default="")
    args = ap.parse_args()

    os.makedirs(FONT_DIR, exist_ok=True)
    try:
        entries = api_get(API)
    except Exception as e:
        print(f"github api failed: {e}", file=sys.stderr)
        return 1
    families = sorted(e["name"] for e in entries if e.get("type") == "dir")
    if args.query:
        q = args.query.lower()
        families = [f for f in families if q in f.lower()]
    if not families:
        print("no families matched", file=sys.stderr)
        return 1
    # rotate through the catalog across runs
    rot = families[args.offset % len(families):] + families[:args.offset % len(families)]
    picked = rot[:args.count]

    known = seen_shas()
    added = 0
    with open(MANIFEST, "a") as mf:
        for fam in picked:
            try:
                files = api_get(f"{API}/{urllib.request.quote(fam)}")
            except Exception as e:
                print(f"  {fam}: list failed: {e}", file=sys.stderr)
                continue
            famdir = os.path.join(FONT_DIR, fam)
            os.makedirs(famdir, exist_ok=True)
            for fe in files:
                name = fe.get("name", "")
                if not (name.lower().endswith(".ttf") or name.lower().endswith(".otf")
                        or name == "OFL.txt"):
                    continue
                url = f"{RAW}/{urllib.request.quote(fam)}/{urllib.request.quote(name)}"
                dest = os.path.join(famdir, name)
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "one-shot-video-kit/1.0"})
                    with urllib.request.urlopen(req, timeout=60) as r:
                        data = r.read()
                except Exception as e:
                    print(f"  {fam}/{name}: download failed: {e}", file=sys.stderr)
                    continue
                if name != "OFL.txt" and len(data) > 4 and data[:4] not in (
                        b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"):
                    print(f"  {fam}/{name}: bad font magic, skipped", file=sys.stderr)
                    continue
                sha1 = hashlib.sha1(data).hexdigest()
                if sha1 in known:
                    continue
                with open(dest, "wb") as f:
                    f.write(data)
                known.add(sha1)
                mf.write(json.dumps({
                    "filename": os.path.relpath(dest, FONT_DIR),
                    "family": fam,
                    "source": "github.com/google/fonts",
                    "source_url": url,
                    "license": "OFL-1.1",
                    "sha1": sha1,
                    "bytes": len(data),
                    "allowed_intents": ["personal", "publish"],
                }) + "\n")
                added += 1
            print(f"  {fam}: done")
    print(f"fonts: {added} new files across {len(picked)} families")
    return 0


if __name__ == "__main__":
    sys.exit(main())
