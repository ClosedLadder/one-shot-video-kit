# Tier STUDIO — Sparks-powered, $0 marginal (DEFAULT)

The default tier. Near-best quality on lab hardware with zero marginal spend. If the brief doesn't name a tier, you are in STUDIO.

## Model routing (capability classes)

| Role | Class | Selection |
|---|---|---|
| Director | frontier-reasoning | Strongest available in-lab |
| Renderer | strong-code | Strongest available in-lab |
| Media lead | frontier-reasoning or frontier-multimodal | Strongest available in-lab |
| Watcher | vision-capable | Any vision-capable lab AI; agent self-review is mandatory regardless |
| Ear | audio-capable | Any |

Same "strongest available in each class" rule as BEST — the tier changes the budget and placement, not the ambition.

## Render placement

- Frame renders: **Sparks render farm first** (GPU-verified via `hardware/MACHINE-ROLES.md`). Code-film pipelines (Remotion/p5.js/three.js/manim + ffmpeg) run here at $0 marginal.
- Authoring/storyboard/assembly/QC: MBP.
- iPad: review only — never a render node (see `hardware/MACHINE-ROLES.md`).

## API budget caps (per run)

| Service | Cap | Notes |
|---|---|---|
| AI footage | **$0** — not available in STUDIO | Mixed-flow/ai-footage briefs at STUDIO use code-rendered plates or already-licensed assets only |
| TTS | $0 marginal | Local/free voices only, or subscription-included endpoints; auditions still run, winners recorded in `audio/tts.md` |
| Art/stills | $0 | Generate with code or reuse kit gallery |
| **Total API per run** | **$0** | Any paid call = tier violation; escalate to BEST or get Steven's sign-off |

## Expected cost / time / quality

- **Cost:** $0 marginal (electricity + hardware Steven already owns).
- **Time:** hours (Sparks are slower than cloud GPUs per frame but free; parallelize scenes).
- **Quality:** near-best for code-film; deliberately capped for footage-heavy briefs (that's what BEST is for).

## Never-degrade gate

Hardware is used only where neutral-or-better. Concretely: a Spark joins the farm only after `gpu_probe.mjs` returns a real GPU renderer string for headless Chrome — an unverified GPU path that falls back to software rendering (slow, or watercolor fills that need a real GPU) is worse than the MBP's M4 GPU and is NOT used. p5.brush watercolor on integrated-only paths: drop the watercolor fills, keep the design. Cheap that looks cheap is forbidden — if STUDIO can't clear the bar for a brief, say so and recommend BEST.
