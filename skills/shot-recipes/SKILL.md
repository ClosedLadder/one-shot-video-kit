---
name: shot-recipes
description: Pick named shot recipe cards to build reliable video shots — intros, text reveals, transitions, product shots, data-viz, outros. Use when the user asks to make a video or a single shot, wants a "named shot" like crash-zoom-punch or deck-deal-flyin, or needs proven timing parameters for motion design. The pick-a-named-shot pattern: select cards from the index, read the chosen cards fully, adapt their motion core and parameter tables to the brief — never invent motion from scratch.
---

# shot-recipes — pick a named shot

One-shot video works when the agent **selects motion instead of inventing it**.
This skill holds 50 curated recipe cards (from video-shotcraft's 157), each with
proven intent, motion core, parameter tables, and known pitfalls.

## How to use this skill

1. **Read `cards-index.md` first.** It's the English summary of all 50 cards:
   one-liner, typical duration at 30fps, energy level. Pick by job, not by style.
2. **Read the chosen cards in full** (`cards/<category>/<name>.md`). Each card has
   frontmatter (duration, energy, intended use), 意图 (intent), 动效核心 (motion
   core — the frame-exact recipe), 参数表 (parameter table with typical values
   and "adjustment feel"), 已知坑 (known pitfalls), 参考实现 (reference demo).
   The body is in Chinese; the timings are numbers and transfer directly.
3. **Pick technique cards separately.** Cards tagged ★ in the index
   (`shot-transitions`, `transition-hidden-cut`, `impact-feedback`) are technique
   pick-lists for seams/emphasis — they don't occupy an energy slot.
4. **Start from the energy skeleton.** Read `sequences/promo-energy-arc.md`
   before picking cards for a full film: fill the four segments first, then slot
   cards in. Budget hold/breathe frames before placing motion.
5. **Apply the taste & timing rules.** `references/aesthetic-rules.md` holds the
   proven rules (hold key info ≥1s · never uniform-linear motion · hero arc ≥3s ·
   ≤3 full-frame hits per film · subtitles ≥5.2% of frame height). Run every
   shortlisted card against them at acceptance time.
6. **Beat-sync with discipline.** If the film has a driving BGM, follow
   `references/music-beat-sync.md`: fit the grid with least squares, cut on
   whole beats, keep cut error ≤3f, and treat the hit list as a candidate pool —
   not every kick gets a screen impact.

## One-shot selection rules (apply without asking)

- **A technique stars once.** If you used deck-deal-flyin as the lead of shot 2,
  don't deal again in shot 5 — pick a different entrance.
- **One hero per opening.** Open with a single subject and a complete action arc.
- **Hold before you cut.** Key information lands, then holds (≥1s for brand
  marks, ≥0.5s for boards/grids), then the cut happens.
- **Energy alternates.** Don't stack high-energy shots; separate them with
  breath cards (`paper-title-card`) or low-energy reveals.
- **Ending peaks.** The outro is the energy maximum of the film, not an afterthought.
