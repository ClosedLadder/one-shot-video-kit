#!/usr/bin/env python3
"""check-publish-assets.py — publish-intent clean-sourcing gate.

Reads the brief's `intent:` field (docs/BRIEF-CONTRACT.md). For
intent=personal: informational only, always passes. For intent=publish:
every asset referenced by the run (or, with --assets, every asset in the
given library dirs) must have publish-safe provenance in its category
MANIFEST.jsonl — i.e. allowed_intents contains "publish". Fails (exit 1)
on any violation.

Usage:
  check-publish-assets.py --brief scoreboard/briefs/brief-1-logo-sting.md \
      --assets audio/music audio/sfx references/stock/images
  check-publish-assets.py --brief briefs/my-brief.md --run-dir renders/x/y/z \
      --assets-from-run   # read asset filenames from the run dir
"""
import argparse
import json
import os
import re
import sys

KIT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LIB_DIRS = [
    os.path.join(KIT, "audio", "music"),
    os.path.join(KIT, "audio", "sfx"),
    os.path.join(KIT, "audio", "samples"),
    os.path.join(KIT, "references", "stock", "images"),
    os.path.join(KIT, "references", "stock", "video"),
]


def read_intent(brief_path):
    with open(brief_path, encoding="utf-8") as f:
        text = f.read()
    # YAML frontmatter style:  intent: publish
    m = re.search(r"^intent:\s*(personal|publish)\s*$", text, re.M | re.I)
    if not m:
        # Inline brief header style:  **Intent:** personal
        m = re.search(r"\*\*Intent:\*\*\s*(personal|publish)", text, re.I)
    return (m.group(1).lower() if m else "personal")


def load_manifests(lib_dirs):
    """filename -> record across all category MANIFEST.jsonl files."""
    index = {}
    for d in lib_dirs:
        mp = os.path.join(d, "MANIFEST.jsonl")
        if not os.path.exists(mp):
            continue
        with open(mp, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                index[rec.get("filename", "")] = rec
    return index


def find_referenced_assets(run_dir, index):
    """Scan run-dir text files for filenames that match library assets."""
    refs = set()
    if not run_dir or not os.path.isdir(run_dir):
        return refs
    names = set(index.keys())
    for root, _, files in os.walk(run_dir):
        for fn in files:
            if not fn.endswith((".md", ".json", ".jsonl", ".txt", ".edl")):
                continue
            p = os.path.join(root, fn)
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            for name in names:
                if name in text:
                    refs.add(name)
    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True, help="brief markdown file")
    ap.add_argument("--assets", nargs="*", default=[],
                    help="library dirs to check wholesale (relative to kit root or absolute)")
    ap.add_argument("--run-dir", default=None,
                    help="run workspace; referenced asset filenames are scanned from it")
    ap.add_argument("--assets-from-run", action="store_true",
                    help="check only assets referenced by --run-dir")
    ap.add_argument("--provenance-log", default=None,
                    help="write per-asset provenance log here (md)")
    args = ap.parse_args()

    intent = read_intent(args.brief)
    print(f"brief: {args.brief}\nintent: {intent}")

    lib_dirs = [os.path.join(KIT, a) if not os.path.isabs(a) else a for a in args.assets]
    if not lib_dirs:
        lib_dirs = LIB_DIRS
    index = load_manifests(lib_dirs)
    print(f"library assets indexed: {len(index)}")

    if args.assets_from_run:
        if not args.run_dir:
            print("ERROR: --assets-from-run needs --run-dir", file=sys.stderr)
            sys.exit(2)
        targets = find_referenced_assets(args.run_dir, index)
        print(f"assets referenced by run: {len(targets)}")
    else:
        targets = set(index.keys())

    violations = []
    rows = []
    for name in sorted(targets):
        rec = index[name]
        ok_publish = "publish" in (rec.get("allowed_intents") or [])
        rows.append((name, ok_publish, rec))
        if intent == "publish" and not ok_publish:
            violations.append((name, rec))

    if args.provenance_log:
        with open(args.provenance_log, "w", encoding="utf-8") as f:
            f.write(f"# Provenance — {os.path.basename(args.brief)} (intent: {intent})\n\n")
            f.write("| asset | publish-safe | license (as stated by source) | source |\n")
            f.write("|---|---|---|---|\n")
            for name, ok, rec in rows:
                f.write(f"| {name} | {'yes' if ok else 'NO'} | "
                        f"{rec.get('license','?')} | {rec.get('source_url','?')} |\n")
        print(f"provenance log: {args.provenance_log}")

    if intent == "personal":
        print("intent=personal: no gate enforced (informational only). PASS")
        sys.exit(0)

    # intent == publish
    if violations:
        print(f"\nFAIL: {len(violations)} asset(s) lack publish-safe provenance:")
        for name, rec in violations:
            print(f"  - {name}: license={rec.get('license')} "
                  f"intents={rec.get('allowed_intents')} src={rec.get('source_url')}")
        print("\nReplace with publish-safe assets (allowed_intents includes 'publish') "
              "or re-scope the brief to intent: personal.")
        sys.exit(1)
    print(f"\nPASS: all {len(targets)} checked asset(s) are publish-safe.")


if __name__ == "__main__":
    main()
