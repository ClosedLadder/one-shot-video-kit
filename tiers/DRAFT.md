# Tier DRAFT — fast local iteration

Speed over polish. For exploring ideas, validating storyboards, and killing bad concepts cheaply. Never ships to an audience.

## Model routing (capability classes)

| Role | Class | Selection |
|---|---|---|
| Director | frontier-reasoning | Strongest available, but time-boxed: storyboard in one pass |
| Renderer | strong-code | Fastest capable — lightweight models preferred over frontier |
| Watcher | vision-capable | Single review pass only (see below) |
| Ear | audio-capable | Temp/scratch audio acceptable |

## Render placement

- Local machine running the agent (usually the MBP). No farm scheduling — DRAFT must start in under a minute.
- CPU-ok render paths only: low-res proxies, reduced frame counts, simplified fills (skip watercolor/p5.brush heavy passes; flat fills fine).
- No Spark farm jobs, no paid APIs, no multi-worker swarm (single agent, single pass).

## API budget caps (per run)

| Service | Cap |
|---|---|
| Everything | **$0** |

## Expected cost / time / quality

- **Cost:** $0.
- **Time:** minutes (target: storyboard → watchable proxy in < 30 min).
- **Quality:** rough by design. Composition, timing, and story reads must be judgeable; finish, polish, and final audio are explicitly out of scope.

## Self-review at DRAFT

Exactly ONE loop: 0.3-scale proxy → contact sheet → fix the worst 3 issues → re-render proxy. No proof-frame checklist, no final-file proof frame. DRAFT output is labeled `DRAFT — not for review` and never enters `references/gallery/`.

## Never-degrade gate

DRAFT degrades finish, never judgment. A DRAFT must still answer: does the story read? Does the pacing breathe? Is the composition sound? If a DRAFT can't answer those, it failed as a draft — speed is not an excuse for an unreadable cut. Promote to STUDIO for anything Steven will see.
