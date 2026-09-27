# AI footage setup — Higgsfield (human step, no keys in the kit)

This pipeline (`pipelines/ai-footage/`) is **stubbed by design**: the workflow, budget gates, and prompt discipline are fully built, but the kit ships with **no credentials and makes no live calls**. Activating it is a human step, done once on Steven's machine. No agent should ever ask Steven for API keys — this page is the standing answer to "how do I turn footage on."

## What to set up

1. **Higgsfield account + credits.** Sign up at higgsfield.ai. For the scoreboard + experimentation, budget **~$50–100 in credits** to start (field benchmark: 10 finished UGC ads < $16; confirm current per-credit pricing before committing — pay-per-credit may beat a plan at our volume).
2. **MCP access.** Higgsfield's official MCP server lives at `mcp.higgsfield.ai/mcp`. Connect it from the agent host (Claude Code / Codex) per Higgsfield's MCP docs — the kit's recipes assume an MCP client that can call Seedance 2.5 (video), nano banana 2 (images), and seed_audio.
3. **soul-id registration.** In Higgsfield, register each recurring human (5–20 photos → stable `reference_id`) and record the id in the run's `style-lock.md`. Without this, multi-shot humans drift.
4. **Budget activation.** Nothing in the pipeline changes — the per-call budget gate reads the run's `budget.json`. BEST tier (up to $5/run footage) becomes available the moment credentials exist; STUDIO/DRAFT stay $0 code-only regardless.

## Rules (standing)

- **No keys in the repo. Ever.** Not in `.env`, not in chat logs, not in `budget.json`, not in `costs.jsonl`. Credentials live in the MCP client's own credential store / OS keychain on the machine that runs the calls.
- **Agents never ask Steven for keys.** If footage is requested and no credentials are configured, degrade to code-only (mixed-flow STUDIO) and disclose it.
- **Voice/music are separate decisions** (ElevenLabs vs OpenRouter TTS, music licensing) — tracked in the ANALYSIS.md §7 decisions list, not here.

## Verify it works

1. Run `pipelines/code-film/gpu_probe.mjs`-style thinking for the wallet: make one nano banana 2 still (~validation tier, a few credits) and confirm the charge + output land where expected.
2. Confirm `costs.jsonl` logging works — one ledger line per call.
3. Confirm the budget gate refuses: set a $0 test cap and watch a call get refused (not attempted).
