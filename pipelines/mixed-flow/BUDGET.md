# Mixed-Flow Budget — per-run caps

Money is a pipeline input, not an afterthought. The tier is chosen before the beat sheet is written; the budget is enforced by the ledger, not by willpower.

## Per-run footage caps

| Tier | Footage budget | Meaning |
|---|---|---|
| **BEST** | up to **$5** in footage credits | Best by any means necessary — full storyboard-first economics: validate cheap (~7 credits), ship validated only |
| **STUDIO** | **$0** — code-only | Sparks-powered, $0 marginal. Footage stages degrade to style-locked code plates; the pipeline still ships |
| **DRAFT** | **$0** — code-only | Fast local iteration. Same as STUDIO, lower render settings, watermark-free drafts |

BEST is the only tier that may call paid generation. STUDIO and DRAFT **never** call paid APIs — their footage stages are replaced by code-rendered plates (code-film engine or Remotion) under the same style lock.

## Enforcement

1. The tier + cap are written into the run dir (`budget.json`) before Stage 1.
2. Every generation call checks the ledger first: `spent + estimate > cap` → call refused, pipeline continues code-only.
3. Every call appends to the run's `costs.jsonl`: timestamp, beat, model, prompt hash, credits spent, output path.
4. Budget exhaustion is a normal outcome, not a failure — the disclosure section says what was code-substituted.

## Reference economics (from the field)

- PromptEngineer48: 10 finished UGC ads < **$16** total — storyboard-first (validate ~7 credits, ship ~70).
- vibingtalk recipe: full explainer VO for **<$0.10** via Gemini TTS on OpenRouter — voice is never the expensive part.
- Scoreboard brief 4 (mixed-flow product ad) must come in under a **$5** footage budget — that's the BEST-tier cap, by design.

## What the $0 build covers

Paid APIs get **stubs + setup docs, never live keys** (see `pipelines/ai-footage/RECIPE.md` and `docs/`). The budget machinery — caps, ledger, degrade-to-code-only paths — is fully built and works with $0. The day Steven adds credentials, BEST tier activates without any pipeline change.
