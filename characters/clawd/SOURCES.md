# SOURCES — characters/clawd/

Vendored 2026-09-24 from **ClaudeAnimationBase** (upstream git HEAD `0ac8bf2`).

## What's here and where it came from

| kit file | upstream source | notes |
|---|---|---|
| `clawd.js` | `src/clawd.js` (verbatim) | The character module: drawn key views (`front q side qback back`), 31-emotion system (`feel()`/`emotions()`), eyes, mouths, hats, emotes, dances (`move()`/`dancer()`), turn/spin helpers |
| `sheets.js` | `src/sheets.js` (verbatim) | Model sheets as renderable loops (`?loop=emotions`, `?loop=views`) |
| `emotions.jpg` | `docs/emotions.jpg` | All 31 emotions on one sheet — **read before drawing** |
| `views.jpg` | `docs/views.jpg` | The five key views + motion helpers + hats — **read before drawing** |

## Deliberately left out

- `docs/emotions.webp` — 6.6 MB duplicate of `emotions.jpg`; the JPG carries the same information.
- The character's role as pipeline default: `PIPELINE-GUIDE.md` documents the character module as **swappable** — Clawd is the bundled example, not a requirement. New characters go in `characters/<name>/` following `characters/_template.md`.

## License

Upstream is MIT (see upstream `LICENSE`). Sheets and code inherit that.
