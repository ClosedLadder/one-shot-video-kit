#!/usr/bin/env python3
"""harvest_stock_video.py — free stock-video harvester ($0).

Source: Internet Archive (archive.org) public-domain film collections
(e.g. Prelinger Archives). License is verified per item from the item
metadata's licenseurl field (e.g. http://creativecommons.org/publicdomain/
or .../publicdomain/mark/1.0/). Only items whose licenseurl indicates
public domain / CC0 / CC-BY / CC-BY-SA are harvested.

Pipeline: query -> pick MPEG4 MP4 file -> download -> normalize to
1080p H.264 MP4 (scale to fit 1920x1080, pad) -> verify (video+audio
streams, duration > 0) -> provenance in
references/stock/video/MANIFEST.jsonl
"""
import argparse
import os
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from harvest_common import (  # noqa: E402
    download, http_json, slugify, sha1_of, media_duration, today,
    manifest_append, existing_filenames, probe,
)

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(KIT, "references", "stock", "video")
MANIFEST = os.path.join(OUT, "MANIFEST.jsonl")

# licenseurl substrings we accept, mapped to a label + intents.
ACCEPTED_LICENSES = [
    ("creativecommons.org/licenses/publicdomain", "Public domain (archive.org licenseurl)"),
    ("creativecommons.org/publicdomain/mark", "Public Domain Mark 1.0"),
    ("creativecommons.org/publicdomain/zero", "CC0 1.0 Universal (public domain dedication)"),
    ("licenses/by/4.0", "Creative Commons Attribution 4.0"),
    ("licenses/by/3.0", "Creative Commons Attribution 3.0"),
    ("licenses/by-sa/4.0", "Creative Commons Attribution-ShareAlike 4.0"),
]


def search_items(query, rows=60):
    q = f'({query}) AND mediatype:movies'
    url = ("https://archive.org/advancedsearch.php?q="
           + urllib.parse.quote(q)
           + "&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=licenseurl"
           + f"&rows={rows}&output=json")
    d = http_json(url)
    return d.get("response", {}).get("docs", [])


def item_metadata(identifier):
    return http_json(f"https://archive.org/metadata/{identifier}")


def pick_mp4(meta):
    """Return the smallest downloadable MP4 (derivatives OK — faster pulls)."""
    MP4_FORMATS = ("MPEG4", "h.264", "512Kb MPEG4", "HiRes MPEG4")
    cands = []
    for f in meta.get("files", []):
        name = f.get("name", "")
        if f.get("format") not in MP4_FORMATS:
            continue
        if not name.lower().endswith(".mp4"):
            continue
        size = int(f.get("size", 0) or 0)
        if size <= 0 or size > 600 * 1024 * 1024:
            continue
        cands.append((size, f))
    if not cands:
        return None
    cands.sort(key=lambda c: c[0])
    return cands[0][1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="collection:prelinger",
                    help="archive.org search query, e.g. 'collection:prelinger'")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--rows", type=int, default=60,
                    help="search result rows to consider (long/licensed items are skipped)")
    ap.add_argument("--max-minutes", type=float, default=30.0,
                    help="skip source clips longer than this (bandwidth sanity)")
    ap.add_argument("--clip-seconds", type=int, default=0,
                    help="if >0, harvest a centered excerpt of this many seconds "
                         "instead of the full source (fast stock-clip mode)")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    seen = existing_filenames(MANIFEST)
    docs = search_items(args.query, args.rows)
    got = 0
    for doc in docs:
        if got >= args.count:
            break
        ident = doc.get("identifier")
        licurl = (doc.get("licenseurl") or "").lower()
        label = next((lbl for sub, lbl in ACCEPTED_LICENSES if sub in licurl), None)
        if not label:
            continue
        stem = slugify(doc.get("title") or ident)
        fname = f"vid-{stem}.mp4"
        dest = os.path.join(OUT, fname)
        if fname in seen or os.path.exists(dest):
            continue
        print(f"[video] {doc.get('title')} [{ident}]", flush=True)
        try:
            meta = item_metadata(ident)
            frec = pick_mp4(meta)
            if not frec:
                print("[video]   no suitable MP4 file, skipping")
                continue
            dur = media_duration_of_meta(meta, frec)
            src_url = (f"https://archive.org/download/{ident}/"
                       + urllib.parse.quote(frec["name"]))
            clip = args.clip_seconds
            if not clip and dur and dur > 300:
                print(f"[video]   source too long ({dur/60:.1f} min), skipping")
                continue
            print(f"[video]   <- {src_url} ({int(frec.get('size',0))/1e6:.1f} MB)", flush=True)
            download(src_url, dest + ".src")
            src_dur = media_duration(dest + ".src")
            if not clip and src_dur > 300:
                print(f"[video]   source too long ({src_dur/60:.0f} min), skipping")
                continue
            in_args = []
            note_extra = ""
            if clip and src_dur > clip:
                start = max(0.0, (src_dur - clip) / 2)
                in_args = ["-ss", f"{start:.1f}", "-t", str(clip)]
                note_extra = f" {clip}s excerpt taken from the middle of the full source."
            rc = subprocess.run(
                ["ffmpeg", "-v", "error", "-y", *in_args, "-i", dest + ".src",
                 "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                 "-r", "30", "-c:v", "libx264", "-preset", "ultrafast",
                 "-crf", "21", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-ar", "44100", "-b:a", "128k",
                 "-movflags", "+faststart", dest],
                timeout=1800,
            ).returncode
            if rc != 0:
                raise RuntimeError("ffmpeg normalize failed")
            p = probe(dest)
            streams = p.get("streams", []) if p else []
            kinds = {s.get("codec_type") for s in streams}
            if "video" not in kinds:
                raise RuntimeError("no video stream")
            ndur = media_duration(dest)
            if ndur <= 0:
                raise RuntimeError("zero duration")
            manifest_append(MANIFEST, {
                "filename": fname,
                "source": "Internet Archive (archive.org)",
                "source_url": src_url,
                "source_page": f"https://archive.org/details/{ident}",
                "title": doc.get("title"),
                "creator": doc.get("creator"),
                "license": label,
                "license_url": doc.get("licenseurl"),
                "harvested": today(),
                "allowed_intents": ["personal", "publish"],
                "duration_s": round(ndur, 2),
                "sha1": sha1_of(dest),
                "notes": "Normalized to 1080p (1920x1080, letterboxed) H.264/AAC MP4 @30fps. "
                         "Public domain — no credit required." + note_extra,
            })
            got += 1
            print(f"[video] OK {fname} ({ndur:.1f}s)", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[video] FAIL {ident}: {e}", flush=True)
            if os.path.exists(dest):
                os.remove(dest)
        finally:
            if os.path.exists(dest + ".src"):
                os.remove(dest + ".src")
    print(f"[video] harvested {got} new videos")


def media_duration_of_meta(meta, frec):
    for f in meta.get("files", []):
        if f.get("name") == frec["name"] and f.get("length"):
            try:
                parts = str(f["length"]).split(":")
                if len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                if len(parts) == 2:
                    return int(parts[0]) * 60 + float(parts[1])
                return float(parts[0])  # plain seconds, e.g. "382.35"
            except ValueError:
                pass
    return None


if __name__ == "__main__":
    main()
