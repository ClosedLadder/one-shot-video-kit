# One-Shot Video Kit — Brief Contract

This is the machine- and human-readable contract every brief in `briefs/`
(and `scoreboard/briefs/`) must satisfy before a run is planned. The kit
version in `VERSION` is the contract version's home; bump the contract's
`contract_version` below when the schema changes.

## Required fields

| Field | Type | Meaning |
|---|---|---|
| `title` | string | Brief name, e.g. "Brief 1 — Logo Sting" |
| `duration` | string | Target runtime, e.g. "5 seconds" |
| `aspect` | string | "16:9" \| "9:16" \| "1:1" |
| `pipeline` | string | `code-film` \| `mixed-flow` \| `ai-footage` |
| `tier` | string | `STUDIO` \| `PRO` \| `INDIE` (see `tiers/`) |
| `intent` | **string** | **`personal`** \| **`publish`** — see below |
| `goal` | string | What the video is for, in one paragraph |
| `given` | list | Frozen inputs (brand.json, logo SVG, references…) |
| `tests` | list | What the brief evaluates |
| `ship_criteria` | list | Concrete pass conditions |

## The `intent:` field

`intent` declares the licensing posture of the run. The kit's asset
libraries (`audio/`, `references/stock/`) are harvested under **personal
consumption** assumptions: free sources, many publish-safe, some strictly
personal-only. `intent` decides how the kit treats provenance.

- **`personal`** — Relaxed harvesting allowed. Any asset in the library may
  be used. Provenance is still recorded in the run log for hygiene, but no
  license gate fires. This is the default for practice, tests, and drafts.
- **`publish`** — The run is destined for posting/shipping. The kit enforces
  **clean-sourcing checks**:
  1. Every asset referenced by the run must exist in the category
     `MANIFEST.jsonl` with `allowed_intents` containing `"publish"`.
  2. The run log (`renders/<brief>/<model>/<date>/logs/provenance.md`)
     records, per asset: filename, source URL, license as stated by the
     source, and attribution text if the license requires credit.
  3. `scripts/check-publish-assets.py` is the enforcer — run it with
     `--brief <brief-file>` before locking the final. It exits non-zero
     (failing the run) if any asset lacks publish-safe provenance.

### Writing a brief

Put the fields as a YAML-ish header at the top of the brief Markdown file:

```md
---
title: Brief 1 — Logo Sting
duration: 5 seconds
aspect: 16:9
pipeline: code-film
tier: STUDIO
intent: personal
contract_version: 1
---

**Goal:** ...
```

`intent: personal` is the default when omitted, but writing it explicitly
is preferred. Flip to `publish` only when the video will actually ship;
the enforcer will then demand clean provenance for every referenced asset.

Existing scoreboard briefs use the inline header style instead of YAML
frontmatter — the enforcer reads both:

```md
**Duration:** 5 seconds · **Aspect:** 16:9 · **Pipeline:** code-film · **Tier:** STUDIO · **Intent:** personal
```

## Enforcement points

1. **Planning:** the planner must read the brief's `intent` and select
   assets accordingly (for `publish`, filter library manifests to
   `allowed_intents ⊇ publish`).
2. **Pre-lock gate:** `scripts/check-publish-assets.py --brief <brief>
   --run-dir renders/<brief>/<model>/<date>` — fails the run on any
   violation; writes `logs/provenance.md`.
3. **Self-review:** the self-review skill's proof checklist includes an
   intent/provenance line item for `publish` runs.

## Contract version

`contract_version: 1` — adds `intent` (2026-09-24, Phase 3 workstream B).
