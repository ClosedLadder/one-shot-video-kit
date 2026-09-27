#!/usr/bin/env python3
"""harvest_sfx.py — free sound-effects harvester ($0).

Source: Openverse API (https://api.openverse.org/v1/audio/), aggregating
CC-licensed audio (freesound.org provider). Per-asset license is returned by
the API as license + license_url (verified per record; e.g.
https://creativecommons.org/licenses/by/4.0/). license_type=commercial keeps
results publish-safe; --license-type all also pulls personal-only (NC) assets.

Pipeline: query -> download -> normalize to 44.1kHz WAV -> verify
(ffprobe duration > 0) -> provenance in audio/sfx/MANIFEST.jsonl
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
OUT = os.path.join(KIT, "audio", "sfx")
MANIFEST = os.path.join(OUT, "MANIFEST.jsonl")


def _lic_label(lic, lic_ver):
    base = LICENSE_LABELS.get(lic, f"Unknown ({lic})")
    if lic_ver and lic_ver not in base:
        base += f" {lic_ver}"
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="whoosh", help="SFX query, e.g. whoosh, impact, pop, riser")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--license-type", default="commercial",
                    help="commercial = publish-safe only (client-side filter); "
                         "all = include personal-only licenses")
    ap.add_argument("--min-dur", type=float, default=0.3)
    ap.add_argument("--max-dur", type=float, default=60.0)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    seen = existing_filenames(MANIFEST)
    got = 0
    page = 1
    tried_urls = set()
    while got < args.count and page <= 8:
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
            stem = slugify(r.get("title") or "sfx")
            fname = f"sfx-{stem}.wav"
            dest = os.path.join(OUT, fname)
            if fname in seen or os.path.exists(dest):
                continue
            print(f"[sfx] {r.get('title')} ({dur:.1f}s, {lic}) <- {furl}", flush=True)
            try:
                download(furl, dest + ".src")
                rc = subprocess.run(
                    ["ffmpeg", "-v", "error", "-y", "-i", dest + ".src",
                     "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", dest],
                    timeout=300,
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
                print(f"[sfx] OK {fname} ({ndur:.1f}s)", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[sfx] FAIL {r.get('title')}: {e}", flush=True)
                if os.path.exists(dest):
                    os.remove(dest)
            finally:
                if os.path.exists(dest + ".src"):
                    os.remove(dest + ".src")
        page += 1
    print(f"[sfx] harvested {got} new SFX")


if __name__ == "__main__":
    main()
