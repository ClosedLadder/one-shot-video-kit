---
name: budget-estimator
description: Estimate generation costs for a run before any paid API call fires. Reads run.md (budget cap, target spec), the storyboard shot list, and the pipeline recipe, then projects cost per shot and total with a low / typical / high range that accounts for take iteration. Writes budgets/estimate-<YYYY-MM-DD>.md in the run workspace. Use before any generation step that costs money — storyboard-first economics: validate cheap, ship validated only. Adapted from danielrosehill/claude-ai-video-producer-plugin skills/budget-estimator (MIT).
---

# Budget estimator

You produce realistic cost projections for a one-shot video run.

## Inputs

- `run.md` — budget cap, target spec (runtime, aspect, resolution), pipeline choice.
- `storyboard/shot-list.md` — shot count and durations.
- The pipeline recipe in the kit's `pipelines/<name>/` — model/provider per stage.
- Latest pricing — pull from provider pages if the kit's notes are older than ~30 days; AI media pricing changes monthly.

## Cost model

For each shot, for each pipeline stage:

- **Per-call cost** — what one generation costs.
- **Iteration multiplier** — how many takes are typically needed for an acceptable result. Defaults if no project history:
  - Text-to-image: ×3 (cheap, iterate freely)
  - Image-to-video: ×2 (expensive, iterate sparingly)
  - Text-to-video direct: ×3 (drifts; expect retries)
  - Voice: ×1.5
  - Lip-sync: ×1.5
  - Upscale / interpolate: ×1
- **Typical / low / high** = (1 × per-call), (multiplier × per-call), (multiplier × 1.5 × per-call).

If `logs/production-log.md` (or the kit's `logs/costs.jsonl`) has past data on similar shots, use the actual observed iteration count instead of defaults. Code-film runs are $0 — still write the estimate (a one-line $0 record) so the ledger stays complete.

## Output

`budgets/estimate-<YYYY-MM-DD>.md` in the run workspace:

```md
# Cost estimate — <run>
Date: <YYYY-MM-DD>
Kit version: <from run.md>
Pricing source: <date pulled, provider pages>
Budget cap: $<from run.md>

## Per-shot breakdown
| Shot | Pipeline | Stages | Low | Typical | High |
|------|----------|--------|-----|---------|------|

## Totals
- Low (everything first-take): $X.XX
- Typical: $Y.YY
- High (heavy iteration): $Z.ZZ

## Sensitivity
- Single biggest cost driver: <stage / model>
- Cheapest substitute that preserves quality: <if any>

## Assumptions
- <list: aspect, duration per shot, iteration multipliers used, currency>
```

## Discipline

- Always show a range, never a single point estimate.
- Always cite the date the prices came from.
- Convert all prices to a single currency (default USD).
- API spend only — don't include human time or local compute.
- If a stage's pricing is per second of output, multiply by the storyboard duration for that shot, not wall-clock generation time.
- **If the typical figure exceeds the run's budget cap: stop and replan.** Don't generate and hope. Options: shrink shot count, switch expensive stages to code-rendered equivalents, or ask for a cap change.
