# motion-craft — curated iart-ai motion skill packs

6 packs, 25 skills. Each skill is a `SKILL.md` (with a "use when" activation
description, so agents auto-discover it) plus a `references/` folder of recipes,
playbooks, and timing tables. Every pack also ships the shared verify toolkit
in `scripts/` (contact-sheet.sh, probe-mp4.sh, seek-shot.sh) — the render →
screenshot → check loop that underpins one-shot reliability.

Provenance and keep/drop rationale per pack: see each pack's `SOURCES.md`.

## Pack index

### motion-design/ (9 skills) — craft foundation
| skill | job |
|---|---|
| animation-principles | The 12 principles + easing curves; "make this feel natural" |
| remotion-video | Programmatic Remotion video API + patterns |
| shot-composition | Camera, grids, frame composition |
| motion-art-direction | Creative/art direction playbook for a motion piece |
| beat-sync-editing | Cutting and pacing to music |
| color-motion | Palette building for motion; color management + interpolation |
| motion-background | Animated backgrounds: mesh/gradient recipes |
| logo-animation | Logo intro/stinger patterns |
| after-effects | AE expressions + JSX batch scripts (expression-library.md is portable timing math even without AE) |

### explainer/ (5 skills) — educational video
| skill | job |
|---|---|
| explainer-video | Script-to-screen workflow: brief → storyboard → finished explainer |
| diagram-animation | Animate diagrams/flowcharts revealing |
| whiteboard-animation | Draw-on hand-drawn explainers (draw-on recipes + pipeline) |
| isometric-animation | 2.5D isometric scene recipes |
| wrapped-video | Spotify-Wrapped-style yearly-recap videos; scene-grammar sequencing vocabulary |

### ad/ (3 skills) — commercial video
| skill | job |
|---|---|
| launch-video | Product hype/sizzle launch structure |
| ad-creative-video | Animated ads; batch-ad-pipeline for volume; platform specs (formats, safe areas) |
| testimonial-video | Animated testimonials; quote cards + typography pipeline |

### kinetic-typography/ (1 skill) — text animation
| skill | job |
|---|---|
| kinetic-typography | Headline/kinetic-type animation; reveal-recipes.md: copy-paste timings for CSS/GSAP/Remotion — ease-out `cubic-bezier(0.16, 1, 0.3, 1)`, stagger lines 60–100ms / words 40–70ms / chars 20–40ms |

### data-animation/ (3 skills) — data-driven video
| skill | job |
|---|---|
| chart-animation | Bar chart races; CSV → animated charts data pipeline |
| animated-infographic | Sequenced infographic recipes |
| presentation-video | Animated presentations; pitch-deck sequencing + slide components |

### tiktok/ (4 skills) — 9:16 short-form
| skill | job |
|---|---|
| short-form-video | Reels/TikTok/Shorts pacing (retention-pacing rules) |
| caption-animation | Word-timed karaoke captions (pairs with whisper word timestamps) |
| lower-thirds | Animated lower-third components |
| countdown-video | Countdown timers; digit-flip recipes |

## How to use
Skills activate by their "use when" descriptions — any of the kit's agents (Neo,
Grok/Grok Seat, Fable 5.1, Astra, Opus 5.5, Codex, Cursor) reads the SKILL.md
whose job matches the brief. For a full video job, pair with
`../shot-recipes/` (pick named shots) and `../self-review/` (inspect frames).
