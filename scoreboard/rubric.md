# Scoreboard Rubric

Score every run 1–5 on each dimension. A brief is **passed** at average ≥ 4.0. Score blind where possible (label runs A/B/C/D until Steven scores visual quality and story).

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Visual quality** | Slop: artifacts, broken geometry, text garbage | Clean, professional, minor flaws | Distinctive craft — a style, not a render |
| **Story / coherence** | Incoherent / no arc | Follows the brief, readable | Memorable — reads land, pacing breathes |
| **Audio sync** | VO/music disconnected from visuals | Cuts land near beats/phrases | Word- and beat-locked; direction audible |
| **Style consistency** | Drifts shot to shot | Consistent within acts | One world, one hand, start to finish |
| **Technical cleanliness** | Crashes, black frames, bad encodes | Renders clean, minor QC nits | Deterministic re-render; passes `doctor`/QC gates |

**Judges:** Steven for creative dimensions (visual quality, story); automated/self-review for technical cleanliness; the agent's own watch-skill output as evidence for audio sync and consistency. Record judge identity in every `scores.jsonl` line.

**Convergence rule (from the sprint):** Phase 3 ends when all 5 briefs pass on at least one model AND the last 3 runs on the flagship brief show no score regression. No infinite tinkering.
