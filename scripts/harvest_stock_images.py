#!/usr/bin/env python3
"""harvest_stock_images.py — free stock-photo harvester ($0).

Source: Openverse API (https://api.openverse.org/v1/images/), aggregating
CC-licensed photography (Flickr, StockSnap, etc.). Per-asset license is
returned by the API (license + license_url, verified per record).
license_type=commercial keeps results publish-safe; --license-type all
also pulls personal-only (NC/ND) assets.

Pipeline: query -> download -> normalize (max 1920px long edge, JPEG) ->
verify (valid dimensions) -> provenance in
references/stock/images/MANIFEST.jsonl
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from harvest_common import (  # noqa: E402
    download, openverse_search, openverse_image_file_url, slugify,
    sha1_of, image_dims, today, manifest_append, existing_filenames,
    allowed_intents_for, LICENSE_LABELS, ov_license_ok,
)

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(KIT, "references", "stock", "images")
MANIFEST = os.path.join(OUT, "MANIFEST.jsonl")
MAX_EDGE = 1920


def _lic_label(lic, lic_ver):
    base = LICENSE_LABELS.get(lic, f"Unknown ({lic})")
    if lic_ver and lic_ver not in base:
        base += f" {lic_ver}"
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="mountain landscape", help="image search theme")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--license-type", default="commercial",
                    help="commercial = publish-safe only (client-side filter); "
                         "all = include personal-only licenses")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    seen = existing_filenames(MANIFEST)
    got = 0
    page = 1
    tried_urls = set()
    while got < args.count and page <= 8:
        data, _ = openverse_search("images", args.query,
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
            furl = openverse_image_file_url(r)
            if not furl or furl in tried_urls:
                continue
            tried_urls.add(furl)
            lic = (r.get("license") or "unknown").lower()
            lic_ver = r.get("license_version") or ""
            stem = slugify(r.get("title") or "stock")
            fname = f"img-{stem}.jpg"
            dest = os.path.join(OUT, fname)
            if fname in seen or os.path.exists(dest):
                continue
            print(f"[images] {r.get('title')} ({lic}) <- {furl[:90]}", flush=True)
            try:
                download(furl, dest + ".src")
                w0, h0 = image_dims(dest + ".src")
                if w0 <= 0 or h0 <= 0:
                    raise RuntimeError("unreadable image")
                if w0 < 640 or h0 < 640 and max(w0, h0) < 640:
                    raise RuntimeError(f"too small ({w0}x{h0})")
                rc = subprocess.run(
                    ["ffmpeg", "-v", "error", "-y", "-i", dest + ".src",
                     "-vf", f"scale='min(iw,{MAX_EDGE})':'min(ih,{MAX_EDGE})':eval=frame",
                     "-q:v", "3", dest],
                    timeout=300,
                ).returncode
                if rc != 0:
                    raise RuntimeError("ffmpeg normalize failed")
                w, h = image_dims(dest)
                if w <= 0 or h <= 0:
                    raise RuntimeError("broken output image")
                intents = allowed_intents_for(lic)
                manifest_append(MANIFEST, {
                    "filename": fname,
                    "source": f"Openverse image API (provider: {r.get('provider')})",
                    "source_url": furl,
                    "source_page": r.get("foreign_landing_url"),
                    "title": r.get("title"),
                    "creator": r.get("creator"),
                    "license": _lic_label(lic, lic_ver),
                    "license_url": r.get("license_url"),
                    "harvested": today(),
                    "allowed_intents": intents,
                    "dimensions": f"{w}x{h}",
                    "sha1": sha1_of(dest),
                    "notes": f"Normalized: longest edge capped at {MAX_EDGE}px, JPEG q3. "
                    + ("Credit required if published." if "publish" in intents else
                       "PERSONAL CONSUMPTION ONLY — license forbids publish/commercial use."),
                })
                got += 1
                print(f"[images] OK {fname} ({w}x{h})", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[images] FAIL {r.get('title')}: {e}", flush=True)
                if os.path.exists(dest):
                    os.remove(dest)
            finally:
                if os.path.exists(dest + ".src"):
                    os.remove(dest + ".src")
        page += 1
    print(f"[images] harvested {got} new images")


if __name__ == "__main__":
    main()
