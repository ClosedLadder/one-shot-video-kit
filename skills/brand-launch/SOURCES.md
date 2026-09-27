# SOURCES — skills/brand-launch/

Vendored 2026-09-24 from **30x-video** (upstream git HEAD `51a6063`), path `skills/30x-web-to-video/`.

## What's here and where it came from

| kit path | upstream source | notes |
|---|---|---|
| `SKILL.md` | `SKILL.md` (+ 3-line kit header) | The URL→launch-video workflow: 8 steps + 4 evidence QC gates, output contract, blocking gates |
| `rules/` | `rules/` (all 24 files, verbatim) | The judgment corpus: taste, composition (5 laws), qc-gates, finish-gate, beat-sync, narration-sync, typography, color, layout, motion, transitions, cinematic, narrative, workflow, media-resolve, archetypes, ui-mockups, cards, data-viz, artifact-catalog, creative-moves |
| `references/` | `references/` (verbatim) | Copy-paste Remotion patterns: animations, audio (ElevenLabs TTS `with-timestamps`), components, lottie, visual-effects |
| `remotion-best-practices/` | `remotion-best-practices/` (verbatim) | Bundled Remotion 4.x API reference (videos, audio, timing, transitions, compositions, sequencing, fonts, images, charts, light-leaks, lottie, text-animations, voiceover, ffmpeg) |
| `scripts/` | `scripts/` (verbatim) | The load-bearing pipeline scripts: `url-to-video.ts` (intake orchestrator + preflight), `project-blueprint.ts`, `evidence-model.ts`, `scene-constitution.ts`, `analyze-audiomap.py` (the ONE trusted beat analyzer), `beat-sync.ts`, `timing-audit.ts`, `visual-audit.ts`, `iterate.ts` + `critique-scenes.ts` + `regenerate-scene.ts` (critic loop), `render-qa.ts` (blocking machine QC on the MP4), `generate-bgm.py` (local BGM generation) |
| `scaffold/` | `scaffold/` (verbatim) | Ready-to-run Remotion 4.x project template (Atmosphere, transitions, captions, shader FX) that the orchestrator fills |
| `AGENTS.md`, `README.md` | verbatim | Skill map + install/usage notes |
| `LICENSE` | repo-root `LICENSE` | Upstream license |

## Deliberately left out

- `cli/` (repo root) — the v1 standalone CLI; the V2 orchestrator in `scripts/` supersedes it for kit use.
- `examples/` (20 example productions, `.tsx` scenes) — reference output, not needed to run the skill; upstream repo remains the reference gallery.
- `benchmarks/` — the V2 regression benchmark suite + canonical URL manifest; harness tooling, not the workflow.
- `docs/` — marketing site assets, 20 finished `.mp4` films, posters; heavy media, left out for leanness.
- `FUSION-REPORT.md` — internal ADOPT/ADAPT/REJECT fusion notes; provenance record, not workflow.
- `.gitignore` — housekeeping.

## The four evidence/proof-frame gates (from `rules/qc-gates.md`)

These are the skill's blocking quality machinery — the "watch skill" pattern in concrete form. Every gate verifies by **rendering pixels and Reading them**, never by grepping source.

1. **Gate 1 — Asset Audit (Step 2.5):** every visual asset must be *looked at* (contact sheet or individual Reads; 3 extracted frames for any `.mp4`) and logged in `asset-audit.md` with a USE (naming the act) or SKIP (with a real reason) verdict. An unaudited asset may not appear in any scene.
2. **Gate 2 — Per-Act Frame Evidence (Step 4):** after building EACH act, render 1–3 representative stills, Read each PNG, and append a structured evidence block (`On screen / Brand assets / Matches plan? / Legibility / Motion state / Composition / FLAG / VERDICT`). VERDICT must be PASS before the next act starts.
3. **Gate 3 — Critic Loop (Step 7.5):** `iterate.ts` — a vision critic scores every act and rewrites the single weakest scene, repeating until `overallScore ≥ threshold` or rounds are exhausted. Skips must be disclosed.
4. **Gate 4 — Honest Disclosure (Step 8):** the delivery message ends with "**What I verified**" (one bullet per gate, evidence cited) and "**What I did NOT verify**" (spot-check list; the header must appear even if the list is "None").

Machine QC behind Gate 4's render step: `render-qa.ts` — ffprobe stream/dimension/duration checks + `blackdetect`/`freezedetect`/`silencedetect`/`volumedetect`; WARN windows get frame-extracted and Read by a human/vision pass.
