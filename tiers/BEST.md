# Tier BEST — best by any means necessary

No compromises. Best models, paid APIs allowed, fastest hardware. Use when the output will be seen, sold, or shipped.

## Model routing (capability classes)

| Role | Class | Selection |
|---|---|---|
| Director | frontier-reasoning | Strongest available (e.g. Opus-class, Fable-class) |
| Renderer | strong-code | Strongest available (e.g. Opus-class, Astra-class) |
| Media lead | frontier-multimodal | Strongest available for style-lock + MCSLA prompting |
| Watcher | vision-capable | Strongest vision available; human (Steven) grades the final creative dims |
| Ear | audio-capable | Best TTS direction available |

Single-agent runs: the agent wears all hats and notes reduced fidelity where a class is uncovered.

## Render placement

- Heavy frame renders: Sparks render farm (GPU-verified via `hardware/MACHINE-ROLES.md` procedure).
- Authoring, storyboard, assembly, QC: MBP (director station).
- Parallelize: scene-per-worker packets via `swarm/PROTOCOL.md` for 90s+ pieces.

## API budget caps (per run)

| Service | Cap | Notes |
|---|---|---|
| AI footage (Higgsfield/Seedance-class) | ≤ $5 footage for brief-4 style; ≤ $15 otherwise | Storyboard-first: validate concepts cheap (~7 credits), ship validated only |
| TTS (ElevenLabs-class) | ≤ $2 | Prefer OpenRouter Gemini TTS pennies-first; upgrade only if voice fails the scoreboard |
| Art/stills (Nano Banana-class) | ≤ $3 | Reference stills and style-lock frames only |
| **Total API per run** | **≤ $20** | Quartermaster enforces; over-cap = STOP, report, await Steven |

Token/model spend: covered by Steven's subscriptions — optimize for quality, not tokens.

## Expected cost / time / quality

- **Cost:** $5–20 API per run (footage + voice), $0 marginal compute.
- **Time:** hours to a day (multi-loop self-review is the point).
- **Quality:** the ceiling. Target: brief pass (avg ≥ 4.0) on first scored run.

## Never-degrade gate

Paid APIs and bigger models are used ONLY where they are neutral-or-better for the quality bar. A paid voice that scores worse than the free auditioned voice is cut. A GPU render path that introduces artifacts vs CPU is cut. "Best by any means necessary" means best *results* — never spend as a substitute for craft.
