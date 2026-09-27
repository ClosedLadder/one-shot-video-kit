#!/usr/bin/env python3
"""harvest_samples.py — free sample-pack harvester ($0).

Source: Openverse API (https://api.openverse.org/v1/audio/), aggregating
CC-licensed audio (freesound.org provider). "Samples" = longer usable
textures: field recordings, ambience loops, drones, nature, city beds.
Per-asset license is returned by the API (license + license_url, verified
per record). Default pulls a mix via license_type=all so the library holds
both publish-safe and personal-only material.

Pipeline: query -> download -> normalize to 44.1kHz WAV -> verify
(ffprobe duration > 0) -> provenance in audio/samples/MANIFEST.jsonl
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from harvest_common import (  # noqa: E402
    download, openverse_search, openverse_audio_file_url, slugify,
    sha1_of, media_duration, today, manifest_append, existing_filenames,
    allowed_intents_for, LICENSE_LABELS, ov_license_ok,
)

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(KIT, "audio", "samples")
MANIFEST = os.path.join(OUT, "MANIFEST.jsonl")


def _lic_label(lic, lic_ver):
    base = LICENSE_LABELS.get(lic, f"Unknown ({lic})")
    if lic_ver and lic_ver not in base:
        base += f" {lic_ver}"
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="ambient field recording",
                    help="sample theme, e.g. 'rain ambience', 'city night', 'forest'")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--license-type", default="all",
                    help="all = mixed personal/publish; commercial = publish-safe only")
    ap.add_argument("--min-dur", type=float, default=10.0,
                    help="samples are longer textures; default skips short hits")
    ap.add_argument("--max-dur", type=float, default=900.0)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    seen = existing_filenames(MANIFEST)
    got = 0
    page = 1
    tried_urls = set()
    while got < args.count and page <= 10:
        data, _ = openverse_search("audio", args.query,
                                   page_size=20, page=page)
        results = data.get("results", [])
        if not results:
            break
        publish_only = args.license_type == "commercial"
        for r in results:
            if got >= args.count:
                break
            if not ov_license_ok(r, publish_only):
                continue
            dur = float(r.get("duration") or 0) / 1000.0  # Openverse reports ms
            if not (args.min_dur <= dur <= args.max_dur):
                continue
            furl = openverse_audio_file_url(r)
            if not furl or furl in tried_urls:
                continue
            tried_urls.add(furl)
            lic = (r.get("license") or "unknown").lower()
            lic_ver = r.get("license_version") or ""
            stem = slugify(r.get("title") or "sample")
            fname = f"sample-{stem}.wav"
            dest = os.path.join(OUT, fname)
            if fname in seen or os.path.exists(dest):
                continue
            print(f"[samples] {r.get('title')} ({dur:.1f}s, {lic}) <- {furl}", flush=True)
            try:
                download(furl, dest + ".src")
                rc = subprocess.run(
                    ["ffmpeg", "-v", "error", "-y", "-i", dest + ".src",
                     "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", dest],
                    timeout=600,
                ).returncode
                if rc != 0:
                    raise RuntimeError("ffmpeg normalize failed")
                ndur = media_duration(dest)
                if ndur <= 0:
                    raise RuntimeError("zero duration")
                intents = allowed_intents_for(lic)
                manifest_append(MANIFEST, {
                    "filename": fname,
                    "source": f"Openverse audio API (provider: {r.get('provider')})",
                    "source_url": furl,
                    "source_page": r.get("foreign_landing_url"),
                    "title": r.get("title"),
                    "creator": r.get("creator"),
                    "license": _lic_label(lic, lic_ver),
                    "license_url": r.get("license_url"),
                    "harvested": today(),
                    "allowed_intents": intents,
                    "duration_s": round(ndur, 2),
                    "sha1": sha1_of(dest),
                    "notes": "Normalized to 44.1kHz/16-bit stereo WAV. "
                    + ("Credit required if published." if "publish" in intents else
                       "PERSONAL CONSUMPTION ONLY — license forbids publish/commercial use."),
                })
                got += 1
                print(f"[samples] OK {fname} ({ndur:.1f}s)", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[samples] FAIL {r.get('title')}: {e}", flush=True)
                if os.path.exists(dest):
                    os.remove(dest)
            finally:
                if os.path.exists(dest + ".src"):
                    os.remove(dest + ".src")
        page += 1
    print(f"[samples] harvested {got} new samples")


if __name__ == "__main__":
    main()
