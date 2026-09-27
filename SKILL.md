# One-Shot Video Kit — Master Skill

You are an AI that has been handed a video brief and this kit. Your job: **one invocation → finished video file.** No follow-up questions. No "here's a prompt to paste elsewhere." You build, you watch your own work, you fix it, you ship it.

Read this whole file, then execute Steps 1–6 in order. Every step is mandatory.

---

## Invocation contract (what the brief contains)

A valid brief gives you all of these. If something is missing, fill it from the kit's locked style system — never ask the user:

- `goal`: what the video must make the viewer feel/do
- `duration`: exact seconds
- `aspect`: 16:9 (default) or 9:16
- `tier`: BEST | STUDIO | DRAFT (default: STUDIO)
- `pipeline`: code-film | mixed-flow | ai-footage (default: pick per Step 4)
- `inputs`: assets provided (logo, brand.json, script, images, premise, …)
- `budget_cap`: max API spend for this run (default from tier)

Scoreboard briefs live frozen in `scoreboard/briefs/`. Real briefs look like them.

---

## Step 1 — Read taste + style pack (do this first, every time)

1. Read `references/taste.md` — the anti-slop laws. They override your instincts.
2. Read the character sheet(s) in `characters/` named by the brief. If none is named, read `characters/_template.md` and create one before building.
3. Read `scoreboard/style-memory.md` — the compounding corrections file. Obey every entry.
4. If the brief references a style pack (brand.json, palette, model sheets), read it and treat it as law. **Constraint + creative latitude:** the library is a starting point, not a cage — invent new props/characters with the same tools and rules.

Do not write a line of scene code until you can state the video's one-sentence logline and its three acts.

---

## Step 2 — Intelligence routing: fill, delegate, or bridge

**The invoker fills or delegates — it is never required to be the brain.** Whatever AI invokes this skill (Neo, Grok, Fable, Astra, Opus, Codex, Cursor, a swarm worker…) fills every role below from its own capabilities **or delegates any role to a stronger/specialized AI through the lab's routing paths** (see your lab's routing policy if you delegate across seats or machines). Canonical example: Grok invokes the skill and routes the Director role to Fable 5.1. No external model call is ever the default *for the invoker itself* — but delegation to a better brain is always allowed and often correct.

| Role | Capability class | What it does in this pipeline |
|---|---|---|
| Director | frontier-reasoning | Logline, storyboard, beat map, pacing calls, final ship/no-ship |
| Renderer | strong-code | Writes the deterministic renderer / scene code / ffmpeg assembly |
| Media lead | frontier-reasoning or frontier-multimodal | Archetype dial, style-lock for AI footage, MCSLA prompt writing |
| Watcher | vision-capable | Inspects contact sheets + stills, runs the proof-frame checklist |
| Ear | audio-capable | Word-timestamp alignment, beat maps, TTS direction tags |
| Quartermaster | any | Enforces budget caps, writes scores.jsonl + costs.jsonl |

**Seat bridge (for weak or headless invokers only).** When the invoker can't fill a role — a script, a cron job, a swarm worker, a local model — it calls `scripts/seat_router.py` with the role prompt and a tier. The router probes seats over the lab SSH fabric in tier order, with automatic failover. (`scripts/seat-ask.sh` remains as a thin wrapper: `--frontier` = `--tier frontier`.)

| Tier | Order (pool-aware) | For |
|---|---|---|
| `frontier` | Fable 5.1 → Opus 5.5 → Codex GPT-6 Astra | BEST tier, art direction, final taste calls |
| `standard` | Claude → Codex → Grok seat | General roles |
| `writing` | Grok seat → Claude → Codex | Bulk writing first (scripts, lyrics, VO copy, shot lists) |
| `frontier-async` | **Astra** → Fable 5.1 → Opus 5.5 → Codex | Deep/async judgment via the Air bus |

**Subscription-pool rule (the credit-exhaustion design):** Fable 5.1 has its own *small, precious* pool within Claude that depletes far before the general allocation — so Fable is reserved for highest-intelligence work only (art direction, final taste calls, conducting). Opus 5.5 and general Claude share the big `claude-general` pool, which makes Opus 5.5 the true fallback when Fable's pool runs dry. Beyond that, fallback hops pools (→ Codex Pro → Astra's GPT-6 → Grok), never sideways within a dead pool. Exhaustion signatures (402, balance/usage/quota/rate-limit) cool the whole pool: 240 min for Fable's precious pool, 60 min for Claude-general/Codex, 30 min for Grok/Astra. Three consecutive generic failures cool the individual seat 15 min. Success resets. State lives in `scripts/.seat-state.json`; `seat_router.py --status` shows pool/seat health.

**Astra's placement:** she is GPT-6 on the Air — frontier class, her own subscription pool — and Steven's named co-lead for highest-intelligence work. She is *async-only* (Air bus, ~1 min heartbeat), so she doesn't race synchronous seats; she leads `frontier-async` (curation judging, rubric refreshes, art-direction reviews) where her full lab context beats a cold CLI call, and she is the cross-pool survivor when Claude Max is exhausted.

**Grok 4.7 for writing:** yes — scripts, lyrics, VO copy, shot lists, captions are squarely in its strengths. The `writing` tier leads with the Grok seat (6 leases, his subscription, cheap and fast). Only taste-critical final calls — logline lock, brand voice — stay at frontier.

Usage: `scripts/seat_router.py [--tier T] [--file PROMPT.md] [--timeout SECS] [--max-turns N] [--wait-astra SECS] "prompt"`. Exit 0 with the reply on stdout, 1 if every seat failed. This is the workaround that replaced paid model APIs: the seat CLIs *are* the API, reached over SSH, riding subscriptions already paid for — $0 marginal cost, redundancy across seats instead of a single paid key.

**Dropped 2026-09-24 (Steven's directive): OpenRouter.** The seat bridge covers every case it did — any invoker, from anywhere, with failover — so no per-call model spend exists in this pipeline. Do not add it back without his explicit approval.

**Selection rule:** invoker first, seat bridge second, local floor last. Never hardcode a vendor. For roles the invoker can't fill and no seat can reach, run the procedure at reduced fidelity and note it in the log.

---

## Step 3 — Tier selection

Default is **STUDIO** unless the brief says BEST or DRAFT. Read `tiers/<TIER>.md` and obey its routing, placement, budget caps, and never-degrade gate. Before any paid API call, validate the shot list against the cap with `skills/budget-estimator/` — STOP if typical cost exceeds the cap.

- **BEST** — best by any means necessary. Best models, paid APIs allowed, no compromises.
- **STUDIO** — Sparks-powered local compute, near-best quality, **$0 marginal cost**.
- **DRAFT** — fast local iteration. Lightweight, single review pass, previews over finals.

**Never-degrade gate (all tiers):** a machine, model, or API is used only where it is neutral-or-better for that tier's quality bar. Cheap that looks cheap is forbidden.

---

## Step 4 — Pipeline selection

Pick one. The brief usually names it; if not:

- **code-film** — motion design, explainers, data-viz, typography, character cartoons, anything needing determinism or precise timing. Renderer: Remotion / p5.js / three.js / manim + ffmpeg. $0 marginal.
- **mixed-flow** — commercial sweet spot: product ads, launch videos, UGC-with-polish. AI footage for hero plates/b-roll (storyboard-first, credit-gated) + code overlays (captions, lower thirds, titles, beat-synced cuts) + ffmpeg assembly.
- **ai-footage** — cinematic footage, photoreal b-roll, human presenters. Cloud video model behind cost gates. Storyboard-first economics: **validate a concept for ~7 credits, ship only validated concepts (~70 credits).**

Pipeline skeletons live in `pipelines/<name>/`. If a pipeline dir is empty, you are the first run: build it from this SKILL.md + the vendored skills in `skills/`, and leave it better than you found it.

---

## Step 5 — Storyboard → build → SELF-REVIEW LOOP (mandatory)

### 5a. Storyboard (before any scene code)

Write `renders/<brief>/<date>/STORYBOARD.md`:

```
Logline: one sentence. [Subject] wants ___, but ___, so ___.
Act 1 (0:00–0:XX): ...
  Shot 1 (0:00–0:XX): event. Reads (in order): 1) ... 2) ...
Act 2 ...
```

Rules: every shot has an **event** (something changes first→last frame); list the **reads** (what the viewer must understand, in order); **model the viewer** — time each read for a first-time watcher, not for you; transitions at every seam (wipe / iris / match cut / cut-on-action / whip pan — never the same default twice, never a hard start or dead stop).

### 5b. Build

- **Code-film:** renderer where **every frame is a pure function of its timestamp** (no carried state, no unseeded randomness) — this is what makes parallel frame rendering flicker-free and re-renders deterministic. Seed everything; record seeds.
- **AI footage:** MCSLA prompts (Model·Camera·Subject·Look·Action); style-lock before spending; generate cheap validation stills first.
- **Audio:** TTS per `audio/tts.md` (audition voices, direction tags like `[comically exasperated]` in the script); word-level timestamps drive animation sync; music from `audio/music/` only (whisper-checked, no watermarks).
- Assemble with ffmpeg. Record exact commands in the run log.

### 5c. Self-review loop (the one-shot unlock — NOT optional)

Use `skills/self-review/` (`SKILL.md` + scripts). The loop:

1. **Preview at 0.3 scale** (or low-res proxy). Never judge quality from a full render you haven't watched.
2. **Contact sheet:** first / middle / last frame of EVERY shot, one image. Look at it as a stranger.
3. **Stills at cue points:** every transition, every text element, every face/hand/detail. Full resolution.
4. **Run the proof-frame checklist** (`skills/self-review/proof-checklist.md`): squint test, slop test, remove test, reading-time audit (words × 10 frames/word at 30fps × 1.5 breathing room), text clearance, audio sync at phrase onsets.
5. **Fix what fails. Re-render. Repeat.** Minimum one full loop; keep going until the checklist passes. Log loop count.
6. **Proof frame from the FINAL file** — not a preview, not an intermediate. A still exported from the shipped MP4, saved to `renders/<brief>/<date>/proof/`.

Ship only when proof frames pass. An agent that can't check its own work is guessing.

### 5d. Swarm option

If the brief is large (90s+ or multi-scene), the director may split scenes into work packets per `swarm/PROTOCOL.md`. Packets are idempotent; frame rendering is map-reduce; a merge + QC gate precedes ship. The self-review loop still applies to the merged cut.

---

## Step 6 — Score + log

1. Score the run against `scoreboard/rubric.md` (5 dimensions, 1–5). Be honest — inflated scores corrupt the kit. Record judge identity.
2. Append one line to `scoreboard/scores.jsonl` (schema documented at the top of that file).
3. Append cost lines to `logs/costs.jsonl`: tokens, API credits, dollars, wall-clock time, self-review loop count.
4. Deposit the best proof frames in `references/gallery/` — the kit's taste compounds from its own output.
5. Absorb corrections: if Steven (or the watcher) flagged anything twice-worthy, append it to `scoreboard/style-memory.md`. Never require the same correction twice.

**Done =** finished video file + proof frames from the final file + scores.jsonl line + costs.jsonl lines. Anything less is not a one-shot.
