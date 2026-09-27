# DECISIONS.md — judgment calls (draft, 2026-09-24)

One line each: decision, why, alternative considered.

## Judgment calls

1. **taste.md synthesized rather than copied verbatim** — 30x's laws were de-SaaS'd and merged with ClaudeAnimationBase's rules + Boriwatopal gotchas into 37 numbered laws; verbatim port would have carried enterprise-launch-video examples irrelevant to cartoons/film. Alt: verbatim copy of 30x's file.
2. **Default tier = STUDIO** — per Steven's expanded requirements; $0 marginal is the kit's home turf. Alt: default BEST.
3. **Router table uses capability classes, vendors only as parenthetical examples** — "strongest available in each class" is the selection rule; hardcoding vendors would rot. Alt: named model assignments.
4. **Self-review scripts are generic ffmpeg, not render.mjs ports** — the analysis pattern was ClaudeAnimationBase-specific (`--sheet`/`--stills`); mixed-flow and ai-footage pipelines have no render.mjs, so contact-sheet/stills generators work on any MP4. Alt: port render.mjs flags 1:1.
5. **scores.jsonl carries `#`-comment schema + example in-file** — a stranger AI reading one file gets the schema; parsers must skip `#` lines. Alt: separate schema doc.
6. **Briefs live at `scoreboard/briefs/`** — deviation from ANALYSIS §3 layout (`briefs/` top-level); the task spec put them under scoreboard/ and the scoreboard owns frozen briefs. Each file adds a frozen verbatim quote block from §4 so the source text is preserved exactly.
7. **Swarm determinism is a packet acceptance criterion** — map-reduce at frame granularity only works with pure-function frames, so idempotency (identical inputs → identical bytes) is contractual, not advisory. Alt: best-effort determinism.
8. **iPad is review-only, explicitly never a render node** — even for previews; review devices don't touch pixels. Alt: allow light proxy renders on iPad.
9. **TTS winners left TBD** — $0 build constraint means no auditions ran; the roster doc has the audition procedure ready for the first VO run. Alt: pick winners from vibingtalk's reported results (aoede/achird) without auditioning.
10. **Karaoke band = lower-third clearance rule** — interpreted ClaudeAnimationBase's "no text unless karaoke" as a spatial rule (lower third, never over faces/action) rather than a content exception. Alt: ban all text in cartoon styles, no exceptions.
11. **DRAFT tier gets exactly one review loop** — DRAFT degrades finish, never judgment; a draft must still answer "does the story read?" Alt: zero review at DRAFT.
12. **BEST per-run API cap $20, brief-4 footage cap $5** — from the analysis's PromptEngineer48 economics ($16/10 ads) and the brief's own $5 cap; token spend covered by subscriptions. Alt: no caps, "best by any means necessary" literally.
13. **Bonus `skills/budget-estimator/` curated from the producer plugin** (tools worker) — the cost-gate skill the analysis called non-negotiable; wired into SKILL.md Step 3 as a pre-paid-call STOP gate. Alt: leave cost discipline as prose only.
14. **Concurrent worker commits reconciled linearly** — four workers committed to the same repo in parallel; git history is linear, no conflicts, each commit scoped to its component. Coordinator verified JSON validity + ran the ffmpeg skill's check.py smoke test.
15. **Corrected taste.md's "16-law codex" attribution** — 30x-video never enumerates 16 literal laws; its corpus is 5 composition + 3 beat-sync laws + finish-gate + slop blacklist (raw extraction preserved in taste-raw.md). Attribution line fixed to match reality.

## Open for Steven (from ANALYSIS.md §7, unresolved)

**Money**
1. Higgsfield credits: ~$50–100 to start? (Pro plan pricing unverified — confirm on higgsfield.ai; pay-per-credit may be cheaper.)
2. ElevenLabs: start with OpenRouter pay-as-you-go (pennies), upgrade only if voice fails the scoreboard?
3. OpenRouter: ~$20 pay-as-you-go to start (Nano Banana art + Gemini TTS)?
4. Music licensing: subscription (~$10–17/mo) vs per-track?
5. Stock assets: generate everything, buy only what the scoreboard proves we can't generate?

**Creative direction**
6. Which 3 visual styles get baked in first? (Recommendation: hand-painted watercolor cartoon, Vox explainer, cinematic mixed-flow.)
7. Aspect ratio priority: 16:9 first, 9:16 second, or both day one?
8. Voice of the kit: lock 2 English voices after auditions, or keep open? (Recommendation: lock 2 EN first.)
9. Human-in-the-loop: pure one-shot vs storyboard-gate? (Recommendation: storyboard-gate for brief 4 — money at stake; pure one-shot for the rest.)

**Hardware**
10. Render placement: MBP vs Sparks — run `gpu_probe.mjs` to confirm which Spark has a real GPU path for headless Chrome.
11. Build resourcing: authorize parallel Cursor/Grok Seat sessions for the remaining build list, or keep builds Neo-driven?

## Resolved by Steven 2026-09-24 ~19:19 ET (Phase 3 kickoff)
16. **API spend authorized: up to $100.** Provisioning via secure API-access cards (parent agent); no keys in repo, agents never ask Steven for keys. OpenRouter credits may already exist — verify before buying.
17. **Phase 3 loop default = PURE one-shot.** Scoreboard runs: agent ships, Steven judges after — that is the true measurement of the end goal. Storyboard-gate stays as a flag for real projects, not the scoreboard protocol.
18. **Asset libraries**: harvest FREE music/samples/SFX/stock images/stock video, amass on local hardware (NAS sync later; NAS workspace not provisioned yet). Licensing lens: **personal consumption**. Brief contract gains `intent: personal | publish` — personal = relaxed; publish = kit enforces clean-sourcing checks + per-asset provenance log.
19. **Own-music path**: procedural/synth generation first (royalty-free by construction), structured for later melody models.
20. **Style system for 20-30**: 3 approved styles stay baked in; build styles/_template/ + prioritized STYLE-BACKLOG.md; future workers crank through the backlog.
21. **Formats**: both 16:9 and 9:16 from day one; 16:9 is the primary look. Every pipeline and scoreboard run produces both.
22. **Subscription tracking**: docs/SUBSCRIPTIONS.md maintained — log candidate subscriptions/plans for frequent video creation with break-even math vs pay-as-you-go as spend happens or is planned.
23. **OpenRouter — dropped, conditional return only (Steven, 2026-09-24)**: no per-call model spend in this pipeline. Intelligence routing is invoker-first, then the seat bridge (`scripts/seat-ask.sh`: MBP seat CLIs over SSH with failover), then local models. OpenRouter may ONLY be reconsidered if a necessary capability has no MCP and no other tool/plug-in path — never as a general brain rental, given the existing subscriptions (Claude Max 20x, 2× Codex Pro 20x, Grok top, Gemini Pro, Muse Pro).
24. **Seat router machinery (Steven, 2026-09-24; pool model corrected 2026-09-25)**:
`scripts/seat_router.py` — subscription-pool-aware routing with circuit breakers.
Pools: fable-pool (SMALL/PRECIOUS — Fable 5.1 depletes far before the general
allocation; reserved for highest-intelligence work + conducting; 240m cooldown),
claude-general (opus-5-5, claude), codex-pro (codex, codex-astra), grok-sub, astra.
Fable exhaustion → Opus 5.5 is a TRUE pool hop (Steven's original ordering was
right; the "same pool" correction was wrong and is retracted). Then cross-pool:
Codex Pro → Astra → Grok. 3 generic fails cool a seat 15m. Tiers: frontier
(fable→opus-5-5→codex-astra), standard, writing (grok first), frontier-async
(Astra leads). Astra = async frontier (Air bus, GPT-6, own pool). Grok 4.7
approved for bulk writing; taste-critical finals stay frontier. Opus 5.5 went
live on the MBP via `claude update` 2.1.270→2.1.282 (2026-09-25, verified).
