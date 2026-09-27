# Machine Roles — MBP / Sparks / iPad

## MBP — director / authoring station

- Storyboard, beat maps, style-lock, code authoring, ffmpeg assembly, QC, scoring.
- Light renders and previews fine (M4 GPU handles p5.js/Canvas comfortably).
- The human (Steven) scores creative dimensions here; runs are labeled for blind scoring here.
- **Degrade gate:** heavy frame renders move to the Sparks when a timeline exceeds ~30 min on the MBP — but only to a GPU-verified Spark (below). An unverified remote path is slower than local and is not used.

## Sparks — render farm (code-rendered pipelines only)

Sparks take frame-render jobs for code-film pipelines: Remotion / p5.js / three.js / manim frame painting + ffmpeg assembly. Deterministic, parallelizable, $0 marginal.

### GPU verification procedure (mandatory before a Spark joins the farm)

Ported from ClaudeAnimationBase's `gpu_probe.mjs` pattern (kept in `pipelines/code-film/`):

1. Copy the probe to the Spark; run: `node gpu_probe.mjs <chrome-path>` (headless Chrome/Chromium on that box).
2. The probe tries flag sets (angle-vulkan, gl-egl, angle-gl-egl, kit-default) and prints the unmasked WebGL renderer per set.
3. **Pass criteria:** at least one flag set returns a REAL GPU renderer string (e.g. NVIDIA / Apple / AMD GPU — not "SwiftShader", not "llvmpipe", not "no WebGL context").
4. Record the winning flag set per Spark in the run log and in `hardware/` notes. Frame workers launch headless Chrome with those flags.
5. **Fail = CPU-only box:** still usable for ffmpeg assembly and non-GL pipelines (manim, pure-canvas 2D), but p5.brush watercolor and WebGL-heavy scenes stay on the MBP or a passing Spark.

### Farm rules

- Frames are pure functions of timestamps → partition by frame ranges across workers; merge by filename order; idempotent (re-run = identical bytes).
- Never run renders on a Spark Steven is using interactively; the farm is background priority.
- **Degrade gate:** a Spark renders only what it renders neutral-or-better. Software-fallback GL that is slower than the MBP, or watercolor fills on integrated-only paths, stay off that box.

## iPad — REVIEW / APPROVE station (NOT a render node)

What Steven does on the iPad:

- **Storyboard approval:** read `STORYBOARD.md` + beat map, approve or red-line before render (the storyboard-gate for footage-spend briefs).
- **Watch renders:** play proxies and finals, scrub, timestamp notes.
- **Greenlight:** approve ship / request changes while traveling.

What the iPad NEVER does: render frames, run the farm, execute pipeline code, hold API keys. It is a screen and a judgment device. No kit software is installed on it; it consumes `renders/` outputs and proof frames via whatever file sharing Steven uses.

**Degrade gate:** review devices don't touch the pixels. If a render needs re-encoding "for the iPad," that transcode is a delivery copy — the shipped master is untouched.

## Per-machine degrade summary

| Machine | Role | Joins when | Never |
|---|---|---|---|
| MBP | Director/authoring/QC | Always | Heavy renders past ~30 min (farm it) |
| Spark | Frame farm | `gpu_probe.mjs` returns a real GPU string (for GL work); CPU-ok for ffmpeg/manim | Unverified GL paths; interactive-use boxes |
| iPad | Review/approve | Always (as a screen) | Render, code, keys, farm work |

**The gate, one line:** a machine touches a job only where the result is neutral-or-better than the alternative. When in doubt, verify (probe it) or keep it on the MBP.
