#!/usr/bin/env python3
"""harvest_music.py — free music harvester ($0).

Source: incompetech.com (Kevin MacLeod catalog). License verified 2026-09-24
from https://incompetech.com/music/royalty-free/licenses/:
"Creative Commons - Free. No charge. Requires that you credit the music."
=> publish-safe with attribution.

Pipeline:
  pieces.json catalog -> download MP3 -> normalize to 44.1kHz WAV ->
  verify (ffprobe duration > 0) -> provenance in audio/music/MANIFEST.jsonl
"""
import argparse
import os
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from harvest_common import (  # noqa: E402
    download, http_json, slugify, sha1_of, media_duration, today,
    manifest_append, existing_filenames, LICENSE_LABELS, UA,
)

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(KIT, "audio", "music")
MANIFEST = os.path.join(OUT, "MANIFEST.jsonl")
PIECES_URL = "https://incompetech.com/music/royalty-free/pieces.json"
MP3_BASE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"
LICENSE_URL = "https://incompetech.com/music/royalty-free/licenses/"
SOURCE_URL = "https://incompetech.com/music/royalty-free/"


def parse_len(s):
    # "mm:ss" or "hh:mm:ss"
    parts = [int(x) for x in str(s).split(":")]
    secs = 0
    for p in parts:
        secs = secs * 60 + p
    return secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="", help="theme/feel keyword, e.g. cinematic, dark, upbeat")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--max-minutes", type=float, default=6.0,
                    help="skip tracks longer than this (WAV size sanity)")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    seen = existing_filenames(MANIFEST)
    catalog = http_json(PIECES_URL)
    q = args.query.lower()
    cands = []
    for p in catalog:
        blob = " ".join(str(p.get(k, "")) for k in ("title", "description", "feel")).lower()
        if q and q not in blob:
            continue
        fn = p.get("filename")
        if not fn or not fn.lower().endswith(".mp3"):
            continue
        plen = parse_len(p.get("length", "0:00"))
        if plen < 20 or plen > args.max_minutes * 60:
            continue
        cands.append(p)
    # prefer longer, well-described tracks; deterministic order
    cands.sort(key=lambda p: (-parse_len(p.get("length", "0:00")), p.get("title", "")))

    got = 0
    for p in cands:
        if got >= args.count:
            break
        stem = slugify(p["title"])
        fname = f"incompetech-{stem}.wav"
        dest = os.path.join(OUT, fname)
        if fname in seen or os.path.exists(dest):
            continue
        url = MP3_BASE + urllib.parse.quote(p["filename"])
        tmp_mp3 = dest + ".src.mp3"
        print(f"[music] {p['title']} ({p.get('length')}) <- {url}", flush=True)
        try:
            download(url, tmp_mp3)
            # normalize: 44.1kHz stereo WAV
            r = subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", tmp_mp3,
                 "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", dest],
                timeout=300,
            )
            if r.returncode != 0:
                raise RuntimeError("ffmpeg normalize failed")
            dur = media_duration(dest)
            if dur <= 0:
                raise RuntimeError("zero duration after normalize")
            manifest_append(MANIFEST, {
                "filename": fname,
                "source": "incompetech.com",
                "source_url": url,
                "source_page": SOURCE_URL,
                "title": p.get("title"),
                "creator": "Kevin MacLeod",
                "attribution": "Music: Kevin MacLeod (incompetech.com), CC-BY",
                "license": "Creative Commons (per incompetech.com license page: "
                           "free, no charge, credit required; page states no version number)",
                "license_url": LICENSE_URL,
                "harvested": today(),
                "allowed_intents": ["personal", "publish"],
                "duration_s": round(dur, 2),
                "sha1": sha1_of(dest),
                "notes": "Normalized to 44.1kHz/16-bit stereo WAV. Publish use requires crediting Kevin MacLeod.",
            })
            got += 1
            print(f"[music] OK {fname} ({dur:.1f}s)", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[music] FAIL {p['title']}: {e}", flush=True)
            if os.path.exists(dest):
                os.remove(dest)
        finally:
            if os.path.exists(tmp_mp3):
                os.remove(tmp_mp3)
    print(f"[music] harvested {got} new tracks")


if __name__ == "__main__":
    main()
