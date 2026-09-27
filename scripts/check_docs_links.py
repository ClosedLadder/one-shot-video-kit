#!/usr/bin/env python3
"""Extract relative markdown links from *.md and verify targets exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:")


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.md"))


def normalize_target(raw: str) -> tuple[str, str | None]:
    target = raw.strip()
    if " " in target and not target.startswith("<"):
        target = target.split(" ", 1)[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].split(" ", 1)[0]
    path_part, anchor = (target.split("#", 1) + [None])[:2]
    return path_part, anchor


def check_link(md_file: Path, raw: str, root: Path) -> tuple[bool, str]:
    path_part, _anchor = normalize_target(raw)
    if not path_part or any(path_part.startswith(p) for p in SKIP_PREFIXES):
        return True, "skipped"
    if path_part.startswith("/"):
        return False, "absolute path not checked"
    resolved = (md_file.parent / path_part).resolve()
    if resolved.exists():
        return True, "ok"
    return False, f"missing: {resolved.relative_to(root)}"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    checked = 0
    skipped = 0
    broken: list[str] = []

    for md_file in iter_markdown_files(root):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            raw = match.group(1)
            path_part, _ = normalize_target(raw)
            if not path_part or any(path_part.startswith(p) for p in SKIP_PREFIXES):
                skipped += 1
                continue
            checked += 1
            ok, detail = check_link(md_file, raw, root)
            if not ok:
                rel_md = md_file.relative_to(root)
                broken.append(f"{rel_md}: ]({raw}) -> {detail}")

    print(f"checked={checked} skipped={skipped} broken={len(broken)}")
    for line in broken:
        print(line)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
