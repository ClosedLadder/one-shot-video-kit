# API Setup — media generation endpoints

**No keys, ever.** Keys live in the provider's own auth (keychain, subscription login, env on the machine that needs them) — never in this repo, never in chat, never in a brief. Setup is done by Steven on his machines; agents only ever reference endpoint *names*.

## Higgsfield (AI footage)

- **Unlocks:** Seedance-class video generation, Nano-Banana-class image generation, seed audio — the Religion B/C footage path (`pipelines/ai-footage/`, `pipelines/mixed-flow/`).
- **Access:** Higgsfield MCP at `mcp.higgsfield.ai/mcp` + official skills. Steven sets up the account/credits on the MBP.
- **Cost-gate rules (non-negotiable):** storyboard-first — validate concepts with cheap stills/previews (~7 credits) before shipping footage (~70 credits); per-run caps in `tiers/BEST.md`; brief-4 hard cap $5. The Quartermaster role enforces; over-cap = stop and report.
- **Link:** https://higgsfield.ai (verify current pricing before committing — pay-per-credit may beat a plan at our volume).

## OpenRouter (art + TTS)

- **Unlocks:** Nano Banana-class image generation (style-lock stills, reference art) + Gemini-class TTS (VO for briefs 3–4 at pennies per explainer).
- **Access:** OpenRouter pay-as-you-go. Steven funds ~$20 to start, on his account.
- **Cost-gate rules:** TTS pennies-first — always try the cheap voice before ElevenLabs; art calls capped per run in the tier file.
- **Link:** https://openrouter.ai

## ElevenLabs (premium VO — upgrade path only)

- **Unlocks:** higher-fidelity VO if OpenRouter voices fail the scoreboard's audio-sync/quality bar.
- **Access:** only if the audition procedure in `audio/tts.md` demonstrates the cheap tier can't clear it. Starter ~$5/mo.
- **Cost-gate rules:** audition-gated — no subscription until a scored run proves the need.
- **Link:** https://elevenlabs.io

## Standing rule

A new paid endpoint is added only when (a) a tier's budget allows it, (b) a scored run proves the free path can't clear the bar, and (c) Steven approves. Agents never sign up, never enter payment details, never handle keys.
