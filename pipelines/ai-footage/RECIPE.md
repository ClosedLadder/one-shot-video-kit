# AI-Footage Pipeline — RECIPE (Religion B, cost-gated)

The model writes prompts; a cloud model paints pixels. Used standalone for cinematic footage / UGC-style ads / photoreal b-roll / human presenters — and as Stage 3 of the mixed-flow pipeline. **Every call in this pipeline sits behind a BUDGET check** (`pipelines/mixed-flow/BUDGET.md`); no budget entry, no call.

## Provider: Higgsfield (stubbed)

- **Endpoint:** `mcp.higgsfield.ai/mcp` (Model Context Protocol — Higgsfield's official MCP server).
- **Capabilities:** Seedance 2.5 video generation, nano banana 2 image generation, seed_audio.
- **Status in this kit: STUB.** The workflow, budget plumbing, prompt discipline, and setup docs are real. No credentials are stored anywhere in the kit, and no live calls are made during the build. Setup (Steven's step, on his machine) is documented in `docs/ai-footage-setup.md`. The day credentials exist, this pipeline activates with no recipe change.

**$0 rule:** paid APIs get stubs + setup docs, NEVER live keys. If you are an agent reading this and you have no credentials configured, you do not have a working ai-footage pipeline — degrade to code-film or mixed-flow STUDIO (code-only) and say so in the disclosure.

## The budget gate (blocking, before every call)

```
1. Read the run's budget.json (tier + cap + spent).
2. Estimate the call's credit cost (validation tier vs ship tier — see below).
3. spent + estimate > cap  →  REFUSE the call. Log the refusal. Continue code-only.
4. Otherwise: make the call, then append to costs.jsonl:
   timestamp, beat, model, prompt-hash, credits, output path.
```

## MCSLA — the prompt formula (mandatory on every call)

Every generative-video prompt is written as five fields, in order:

**M**odel · **C**amera · **S**ubject · **L**ook · **A**ction

```
Model:   Seedance 2.5  (or nano banana 2 for stills)
Camera:  35mm, slow dolly-in, eye-level, shallow depth of field
Subject: [locked description — see soul-id below; never re-described per shot]
Look:    [the style-lock reference plate: lighting, lens, grade, palette]
Action:  [one clear action, one beat long — what happens between first and last frame]
```

Why it wins: it's the best generative-video prompt formula found in the field research — it forces the model to fix camera and look independently of action, which is where drift starts. Reuse the identical Camera + Look lines across every shot of a run; vary only Subject framing and Action.

## soul-id — character consistency (mandatory for recurring humans)

A human who appears in more than one shot is **never re-described per shot**:

1. Collect 5–20 photos of the person (front, 3/4, profile, varied lighting).
2. Register them as a Higgsfield `soul-id` → stable `reference_id`.
3. Every prompt's Subject field references the `reference_id`, not a prose description.

Without soul-id: the same "woman in her 30s, brown hair" prompt produces a different woman every shot. With it: one face, one film. Log the `reference_id` in the run's `style-lock.md`.

## Storyboard-first economics (mandatory)

1. **Validate cheap (~7 credits):** stills instead of video where a still answers the question; shortest durations; lowest acceptable resolution. Validate composition, look-match to the reference plate, and soul-id likeness here.
2. **Ship validated only:** one full-quality generation per beat, only for beats that passed validation.
3. Field benchmark: 10 finished UGC ads < $16 total following this ratio.

## File discipline

```
footage/raw/       # every generation, untouched; filename includes prompt hash + credit cost
footage/selected/  # symlinks/copies of what ships, one per beat
style-lock.md      # reference plate path, soul-id reference_id, MCSLA Camera/Look lines
costs.jsonl        # the ledger — every call and every refusal
```

## What Religion B is for (and not for)

**Wins at:** cinematic footage, UGC-style ads, product lifestyle, photoreal b-roll, human presenters (with soul-id).
**Fails at:** precise typography (never ask it for text — that's the code overlay's job), style consistency without a style lock, cheap iteration (every retry costs credits — that's why validation is stills-first).

## Failure modes this recipe exists to kill

- Style drift shot-to-shot → style lock + identical Camera/Look lines + soul-id.
- Budget blown on "just one more variation" → the per-call budget gate + validation tier.
- Text garbage in frames → the no-text rule (all type is code overlay).
- A presenter who changes faces → soul-id, 5–20 photos, one reference_id.
- Credentials in the repo → there are none, by construction. See `docs/ai-footage-setup.md`.
