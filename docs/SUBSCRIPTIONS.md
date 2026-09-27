# SUBSCRIPTIONS — what to buy for frequent video creation

Kit v0.1.0. Authorized API budget: **$100** (one-shot AI video sprint).
Status conventions: **VERIFIED** = read on the provider's own docs page today (2026-09-24).
**UNVERIFIED-AT-RUNTIME** = from reputable third-party sources, not re-confirmed on the provider page today — verify in the dashboard before committing.

Standing rule (from `docs/api-setup.md`): a new paid endpoint is added only when
(a) a tier's budget allows it, (b) a scored run proves the free path can't clear the bar,
and (c) Steven approves. No keys in this repo — see `docs/ai-footage-setup.md`.

---

## 1. Higgsfield — AI footage (the expensive line)

**What it unlocks:** Seedance-class text/video-to-video generation, Nano-Banana-class
image generation (`pipelines/ai-footage/`, `pipelines/mixed-flow/`).

**Two access surfaces — do not confuse them:**

| Surface | Credential | How it bills |
|---|---|---|
| Hosted MCP `https://mcp.higgsfield.ai/mcp` (kit's current recipe) | **No key.** OAuth sign-in with Steven's personal Higgsfield account inside the MCP client | Personal account credits/subscription |
| REST API `https://api.higgsfield.ai` (server-side/unattended) | API key **ID + secret** pair, created in Higgsfield Console (console.higgsfield.ai) → API Keys | Pay-as-you-go in USD |

**Auth (VERIFIED, docs.higgsfield.ai, read 2026-09-24):**
`Authorization: Key REPLACE_ME:REPLACE_ME` against `https://api.higgsfield.ai` (create keys in the provider console; never commit them).
Async lifecycle: submit → `request_id` + `status_url`/`cancel_url` → poll
`GET /requests/{request_id}/status` or register a webhook. Outputs kept ≥7 days.
Key creation location: Higgsfield Console → API Keys (VERIFIED on official docs).

**Model routes the kit needs (UNVERIFIED-AT-RUNTIME, third-party, Sept 2026):**
image→video `/higgsfield-ai/dop/standard|turbo|lite` (each with `/first-last-frame`
variant) and `/v1/image2video/seedance`; text→image `/higgsfield-ai/soul/v2/standard`;
soul-id character creation. Routes are account-specific — enable the modern models
(nano_banana_pro, seedance_2_5) on the key in the Console if the API answers
`model_disabled` for them.

**Pricing (UNVERIFIED-AT-RUNTIME — could not read the provider pricing page today;
no login available; field data + third-party, Feb–Sept 2026):**
- Rate: **$1 = 16 credits**. DoP Standard 5s = 9 credits (**~$0.56**); DoP Turbo 5s = 6.5 (~$0.41);
  DoP Lite 5s = 2 (~$0.13); Soul 720p = 1.5 (~$0.09); Soul 1080p = 3 (~$0.19).
- API is pay-per-generation in USD — no monthly subscription required.
- Reported first-week offers (from Sept 2026 API tutorials — verify in Console):
  15% off on signup; up to 50% off selected model prices in week 1; $15 free credits
  with business-email verification; 12-month price lock available via sales contact.
- Field benchmark from the Phase-1 research (PromptEngineer48): **10 finished UGC ads < $16**
  → storyboard-first economics: ~7 credits to validate a concept, ~70 to ship
  (~$0.44 validation, ~$4.4 ship at current rates).
- **Break-even:** there is no mandatory plan on the API surface — PAYG is the default
  and is the right choice under ~10–15 shipped videos/month. If Higgsfield's consumer
  web plans (higgsfield.ai) carry a credit-included subscription, verify its per-credit
  rate in-account; the API PAYG only loses when a plan's effective rate beats ~$0.40/credit.

**Recommendation:** $65 of the $100 goes here. That buys ~150 storyboard-validation
passes or ~13–18 shipped videos at current API rates.

---

## 2. OpenRouter — DROPPED 2026-09-24 (Steven's directive)

**Verdict: $0. Do not provision.** Steven holds Claude Max 20x, 2× ChatGPT/Codex Pro
20x, Grok top, Gemini Pro, and Muse Pro — when a frontier AI invokes the skill, the
invoker *is* the Director/Judge/Writer, so renting another flagship per call was
pure waste. For weak/headless invokers, `scripts/seat-ask.sh` (the seat bridge)
routes over the lab SSH fabric to the seat CLIs on the MBP (`claude -p`, `codex exec`,
`grok-seat run`) with automatic failover — the same coverage OpenRouter offered, at
$0 marginal cost, on subscriptions already paid for. The prior $20 allocation is
released back to the reserve. Do not re-add without his explicit approval.

(The notes below are kept for the record only.)
**What it would have unlocked:** Nano-Banana-class image generation + Gemini-class
TTS + cheap LLM calls via `https://openrouter.ai/api/v1` (`POST /chat/completions`,
`Authorization: Bearer REPLACE_ME`, credit packs $5–$100 with ~5.5% fee.)

---

## 3. ElevenLabs — premium VO (audition-gated upgrade only)

**What it unlocks:** higher-fidelity VO *only if* the `audio/tts.md` audition proves
the cheap tier can't clear the scoreboard's audio bar.

**Provisioning (all UNVERIFIED-AT-RUNTIME — consistent across current third-party
docs; official API-reference page unreachable during recon):**
- Host: `https://api.elevenlabs.io/v1`; kit endpoint: `POST /v1/text-to-speech/{voice_id}`.
- Credential: API key created at elevenlabs.io → app/profile **Settings → API keys**.
- Auth: `xi-api-key: <key>` header. No documented scopes — treat the key as
  full-access to the account; keychain-only storage.
- Free plan (10k credits/mo) works for testing; note free-tier audio is
  **non-commercial** (attribution required).

**Pricing (UNVERIFIED-AT-RUNTIME — cross-checked Aug–Sept 2026 against the official
pricing page; sources agree on tiers, small variance on Creator credit count):**
- Free $0 — 10k credits/mo, ~10 min, non-commercial.
- **Starter $6/mo** ($60/yr) — 30k credits/mo, ~30 min, commercial license.
- Creator $22/mo ($11 first month, $220/yr) — 121k credits/mo, ~121 min.
- Pro $99/mo — 600k; Scale $299/mo — 1.8M; Business $990/mo — 6M.
- 1 credit ≈ 1 character (Multilingual v2); Flash/Turbo ≈ 0.5 credit/char.
  Paid tiers roll over unused credits up to ~2 months.

**Break-even vs OpenRouter TTS:**
- A 60s VO ≈ 900–1000 chars ≈ 450–900 credits. Starter ($6) covers 33–66 such VOs/mo.
- OpenRouter PAYG VO runs ~$0.02–0.10 per VO. $6 of PAYG buys ≥60 VOs — so Starter
  **never beats PAYG on cost** at sprint volume; it buys quality, voice cloning,
  and commercial rights. Per the kit's cost-gate rules: **stay on PAYG until the
  scored audition proves the need.**

**Recommendation:** $0 of the $100 now. Subscribe to Starter ($6/mo) only after the
audition gate passes — and cancel the month the audit trail stops needing it.

---

## 4. Music licensing — subscription vs per-track

**What it unlocks:** cleared music beds for shipped videos (no copyright strikes).

**Options (UNVERIFIED-AT-RUNTIME — third-party, mid-2026; verify on provider pages):**

| Option | Price | Terms |
|---|---|---|
| Epidemic Sound — Creator | ~$10–17/mo (monthly vs annual varies) | Unlimited downloads; licensing for social/pods/YouTube; single-track licenses also offered |
| Artlist — personal | ~$15/mo or ~$120/yr | Royalty-free; commercial plans $199–299/yr |
| Uppbeat — Premium | ~$5.59/mo | Unlimited downloads; 3 YouTube channels safelisted; free tier: 1 download/mo |
| Per-track AI generation (e.g. Muzaic-style services) | ~$0.10–2/track | Full ownership per track |
| YouTube Audio Library / Uppbeat free | $0 | Free tier limits |

**Break-even math:** at ~$2/track AI-generated, a $10/mo subscription breaks even at
**~5 tracks/month**. At $5.59/mo (Uppbeat Premium), break-even is ~3 tracks/month.
The sprint is low-volume and the kit can audition with free libraries first.

**Recommendation:** $0 of the $100 now. Subscribe (Uppbeat Premium or Epidemic
Creator, whichever wins the taste audition) only when shipping **≥4 monetized
videos/month** — at that point the subscription beats per-track pricing and removes
per-video license admin.

---

## 5. Recommended first-$100 allocation

| Allocation | Amount | Why |
|---|---|---|
| Higgsfield API credits | **$65** | The only expensive line; footage unlocks BEST-tier runs (~13–18 shipped videos) |
| OpenRouter credits | **$0 — DROPPED 2026-09-24** | Seat bridge (`scripts/seat-ask.sh`) replaces it at $0 marginal; see §2 |
| Reserve | **$15** | Overages / price-check experiments / first-week Higgsfield discount plays |
| ElevenLabs | $0 | Audition-gated; free plan covers tests |
| Music licensing | $0 | Free libraries for the sprint; subscribe at ≥4 videos/mo |

Check the Higgsfield first-week offers (15% signup / up to 50% model discounts /
$15 business-email credits) in the Console before buying — they may stretch the
$65 materially. Revisit allocations after the first scored run lands in `costs.jsonl`.

---

## 6. Credential status (2026-09-24 ~19:22 ET)

- **OpenRouter**: DROPPED 2026-09-24 by Steven — credential remains in vault but
  MUST NOT be used by any kit workflow; the seat bridge replaces it (see §2).
  Old status for the record: connected-but-UNVERIFIED, keyinfo.py egress timeouts.
- **Higgsfield**: NO credentials in vault yet — provisioning pending (see recon in
  §1 of this doc: MCP path needs no key; REST path needs Console API key ID+secret).
- **ElevenLabs**: NO credentials in vault — fallback only, audition-gated.
