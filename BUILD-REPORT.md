# BUILD-REPORT — one-shot-video-kit public export

Packaged 2026-09-27 from read-only source `~/github-portfolio-src/one-shot-video-kit/` into `~/github-portfolio/one-shot-video-kit/`.

## File inventory

| Metric | Count |
|---|---|
| Total files | 462 |
| Python (`.py`) | 67 |
| Markdown (`.md`) | ~200 |
| JavaScript (`.js`/`.mjs`) | 6 |
| CI workflow | 1 |

### Top-level layout

```
.github/workflows/ci.yml
LICENSE
README.md
SKILL.md
DECISIONS.md
VERSION
manifest.json
.gitignore
audio/
characters/
docs/
hardware/
logs/
pipelines/
references/
scoreboard/
scripts/
skills/
styles/
swarm/
tiers/
```

Full file list: run `find . -type f | sort` from the repo root.

## Verification results

### `python3 -m py_compile` (all `.py`)

**PASS** — 67 files compiled. Two `SyntaxWarning`s in vendored ffmpeg scripts (`drawtext.py`, `_ass_overlay.py`) about escape sequences; non-blocking.

### `scripts/check_docs_links.py`

**PASS** — `checked=135 skipped=14 broken=0`

- Skipped: `http(s)://`, `mailto:`, and in-page `#` anchors.
- Fixed 9 broken links in `skills/brand-launch/` by adding `references/*.md`, `sound-effects.md` alias, stub `.tsx` assets, and `calculate-metadata.md` link correction.

### Secrets sweep

```bash
grep -rniE 'api_key|apikey|password|passwd|bearer [A-Za-z0-9_-]{8,}|BEGIN.*PRIVATE' ~/github-portfolio/one-shot-video-kit
```

**No literal credentials.** Hits are:

- `REPLACE_ME` placeholders in `docs/SUBSCRIPTIONS.md` (Higgsfield/OpenRouter auth format)
- Environment variable *names* in vendored brand-launch docs (`ELEVENLABS_API_KEY`, `WAVESPEED_API_KEY` as a rejected dependency)
- Product name "1Password" in a narrative template heading

### CI

`.github/workflows/ci.yml` runs the same two commands as local verification. Local run passed before packaging completed.

## Excluded from source (not part of public kit)

| Path | Reason |
|---|---|
| `logs/library-curator-*.log` | Internal session logs |
| `scripts/__pycache__/`, `*.pyc` | Build artifacts |
| `scripts/.seat-state.json` | Runtime seat-router state |
| `scripts/resume-curator-*.sh` | One-off resume scratch script |
| `briefs/` (empty) | Duplicate of `scoreboard/briefs/` |

## Added / repaired for link integrity

| Path | Action |
|---|---|
| `references/taste.md` | **Created** — source export was missing this file; synthesized from rubric + proof-checklist + brief criteria (see `DECISIONS.md` #1, #15) |
| `references/patterns/*.md` | **Created** — index cards pointing at shot-recipes / motion-craft |
| `references/gallery/`, `references/stock/` | **Created** — empty placeholders for run outputs / harvested assets |
| `audio/tts.md`, `audio/{music,sfx,samples}/` | **Created** — audition procedure + empty library dirs |
| `skills/ffmpeg/references/{gotchas,devices,scripts}.md` | **Created** — ffmpeg skill cross-refs |
| `skills/brand-launch/references/*.md` | **Created** — upstream scaffold not shipped; pointers to bundled Remotion rules |
| `docs/SOURCES.md`, `ASSET-SYNC.md`, `SUBSCRIPTIONS.md`, `SKILL.md` | **Edited** — removed machine-specific absolute paths; redacted key format examples |

## Judgment calls

1. **Kept `scripts/seat_router.py` and `seat-ask.sh`** — lab-specific SSH routing; optional for public users who invoke the skill directly from a frontier model. Paths inside remain machine-specific by design.
2. **Kept `characters/clawd/*.jpg`** — character model sheets (not rendered video); part of the character pack.
3. **Kept `logs/costs.jsonl`** — example cost lines with schema; not session logs.
4. **Did not ship rendered MP4s** — per project scope; `.gitignore` blocks media outputs.
5. **Did not invent scoreboard pass results** — `scores.jsonl` in source is schema-only; README states outcomes depend on the invoking model.
6. **brand-launch `scaffold/` omitted** — not present in source export; `references/components.md` documents the gap.
7. **Honest README** — no claims of hosted service, guaranteed one-shot success, or bundled videos.

## Ready for GitHub

Repo is ready to `git init` and push to `ClosedLadder/one-shot-video-kit`. This packaging job did **not** push to GitHub.
