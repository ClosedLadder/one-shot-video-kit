#!/usr/bin/env python3
"""Shared helpers for the one-shot-video-kit asset harvesters ($0 workstream).

Each harvester: takes a query/theme, fetches from a genuinely free source,
downloads, normalizes, verifies, and appends a provenance record to the
category MANIFEST.jsonl.
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

UA = "one-shot-video-kit/0.1.0 (asset-harvester; +personal-consumption research)"

# Licenses that the kit treats as safe for PUBLISH intent (commercial use
# allowed). Everything else is personal-consumption only.
PUBLISH_SAFE_LICENSES = {"cc0", "pdm", "by", "by-sa", "sampling-plus"}

# Human-readable license labels for the Openverse short codes.
LICENSE_LABELS = {
    "cc0": "CC0 1.0 Universal (public domain dedication)",
    "pdm": "Public Domain Mark 1.0",
    "by": "Creative Commons Attribution",
    "by-sa": "Creative Commons Attribution-ShareAlike",
    "by-nc": "Creative Commons Attribution-NonCommercial",
    "by-nc-sa": "Creative Commons Attribution-NonCommercial-ShareAlike",
    "by-nd": "Creative Commons Attribution-NoDerivatives",
    "by-nc-nd": "Creative Commons Attribution-NonCommercial-NoDerivatives",
    "sampling+": "Creative Commons Sampling Plus 1.0",
    "nc-sampling+": "Creative Commons NonCommercial Sampling Plus 1.0",
}


def allowed_intents_for(license_code, source_license_note=""):
    """Return ['personal'] or ['personal', 'publish'] for a license code."""
    code = (license_code or "").strip().lower()
    if code in PUBLISH_SAFE_LICENSES:
        return ["personal", "publish"]
    return ["personal"]


def _curl(args, timeout):
    """Run curl, return stdout bytes. Some hosts (api.openverse.org)
    fingerprint-block python's urllib TLS stack; curl works reliably."""
    cmd = ["curl", "-sS", "-L", "--fail", "--max-time", str(timeout),
           "-A", UA] + args
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout + 15)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"curl timeout: {e}")
    if out.returncode != 0:
        raise RuntimeError(f"curl failed rc={out.returncode}: "
                           f"{out.stderr.decode()[:200]}")
    return out.stdout


def http_get(url, timeout=60, retries=6):
    import random
    last = None
    for attempt in range(retries):
        try:
            return _curl([url], timeout)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(min(60, 2 ** attempt) + random.uniform(0, 2))
    raise RuntimeError(f"GET failed after {retries} tries: {url}: {last}")


def http_json(url, timeout=60):
    return json.loads(http_get(url, timeout=timeout).decode("utf-8", "replace"))


def download(url, dest, timeout=120, retries=3):
    """Download a URL to dest (temp file, then rename). Returns size bytes."""
    import random
    tmp = dest + ".part"
    last = None
    for attempt in range(retries):
        try:
            _curl(["-o", tmp, url], timeout)
            os.replace(tmp, dest)
            return os.path.getsize(dest)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(min(60, 2 ** attempt) + random.uniform(0, 2))
            if os.path.exists(tmp):
                os.remove(tmp)
    raise RuntimeError(f"download failed after {retries} tries: {url}: {last}")


def slugify(s, maxlen=48):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen] or "asset"


def sha1_of(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path):
    """ffprobe JSON for a file, or None."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", path],
            capture_output=True, text=True, timeout=60,
        )
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except Exception:  # noqa: BLE001
        return None


def media_duration(path):
    p = probe(path)
    if not p:
        return 0.0
    try:
        return float(p["format"].get("duration", 0) or 0)
    except (ValueError, TypeError):
        return 0.0


def image_dims(path):
    """(width, height) via ffprobe, or (0, 0) if unreadable."""
    p = probe(path)
    if not p or not p.get("streams"):
        return (0, 0)
    s = p["streams"][0]
    return (int(s.get("width", 0) or 0), int(s.get("height", 0) or 0))


def has_audio_stream(path):
    p = probe(path)
    return bool(p and any(s.get("codec_type") == "audio" for s in p.get("streams", [])))


def has_video_stream(path):
    p = probe(path)
    return bool(p and any(s.get("codec_type") == "video" for s in p.get("streams", [])))


def today():
    return datetime.date.today().isoformat()


def manifest_append(manifest_path, record):
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    with open(manifest_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def openverse_search(media, query, license_type=None, page_size=20, page=1,
                   extra_params=None):
    """Search the Openverse API (images or audio). Anonymous, no key.
    license_type is deliberately NOT sent: api.openverse.org intermittently
    401s filtered queries; filter licenses client-side instead."""
    import urllib.parse as up
    params = {"q": query, "page_size": page_size, "page": page}
    if license_type:
        params["license_type"] = license_type
    if extra_params:
        params.update(extra_params)
    url = f"https://api.openverse.org/v1/{media}/?" + up.urlencode(params)
    return http_json(url), url


# Client-side license filtering (server-side license_type 401s intermittently).
PUBLISH_SAFE = {"cc0", "pdm", "by", "by-sa", "sampling+"}


def ov_license_ok(record, publish_only):
    lic = (record.get("license") or "").lower()
    if not lic or lic == "unknown":
        return False
    if publish_only:
        return lic in PUBLISH_SAFE
    return True


def openverse_image_file_url(record):
    # Openverse gives the direct foreign image URL in 'url'.
    return record.get("url")


def openverse_audio_file_url(record):
    # For audio (freesound provider) 'url' is the direct preview/file URL.
    return record.get("url")


def existing_filenames(manifest_path):
    if not os.path.exists(manifest_path):
        return set()
    names = set()
    with open(manifest_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                names.add(json.loads(line).get("filename", ""))
            except json.JSONDecodeError:
                continue
    return names
