# NEET CBT 2027 — CLAUDE.md (build rules)

Repo: Downloads/neet-cbt. App for NEET aspirants, FOSS MIT, deployed on Vercel.

## File map (v0.1.0 target)

```
index.html              # the whole app: CSS+JS inline, no build step
sw.js                   # service worker: cache-first app shell, version bump on change
manifest.webmanifest    # PWA manifest (standalone, icons 192+512)
icons/icon-192.png      # generated once (pure-Python PNG, no PIL)
icons/icon-512.png
vercel.json             # REQUIRED: sw.js no-cache/no-store headers
robots.txt
sitemap.xml
README.md
docs/BANK_SCHEMA.md
docs/TEST_PLAN.md
```

## Hard rules

1. Vanilla HTML/CSS/JS only. No frameworks, no build tooling, no CDN.
   Single index.html for the app. Lazy is good: shortest diff wins.
2. Timer = epoch deadline (Date.now() diff), NEVER setInterval
   accumulation. Phone sleep must not desync the timer.
3. Persist full exam state to IndexedDB (key `ncbt_test_state`) on
   EVERY action: answer, clear, mark, navigate, subject switch. Refresh
   must resume exactly. IndexedDB REQUIRED over localStorage: iOS
   Safari evicts localStorage after 7 days unused (research T4).
   Vanilla IndexedDB wrapper (~60 lines), no localforage dep.
4. Palette = SHAPES + colors (verified pixel-level vs NTA AboutCBT.pdf):
   Not Visited = grey rounded square; Not Answered = RED left-pointing
   trapezoid; Answered = GREEN right-pointing trapezoid; Marked for
   Review = solid purple circle; Answered & Marked = purple circle with
   small green/yellow badge. Legend box with live counters. 10-column
   grid. Collapsible sidebar (> < tab). Do NOT "simplify" to plain
   colored squares.
5. Marking (NTA official): +4 correct, -1 wrong, 0 unanswered, 0 for
   marked-for-review WITHOUT an option. Answered & marked (via "Save &
   Mark For Review") = scored. Marked-without-answer must NOT be -1.
5b. Buttons (exact labels + order): "Save & Next" (green), "Save & Mark
   For Review" (orange), "Clear Response" (grey), "Mark For Review &
   Next" (blue); secondary "<< Back" / "Next >>" links; green "Submit"
   bottom-right. No invented button names.
6. Import validation is atomic: validate whole bank first, then commit.
   Reject list on any failure. Never half-load.
7. SW: version const; on activate, delete all caches except current.
   fetch handler: cache-first for same-origin GET, network fallback
   + cache put. No caching for /sw.js itself (Vercel header also
   enforces).
8. No features beyond PRD. No percentiles, no accounts, no leaderboard,
   no AI-generated questions. Starter bank flagged SAMPLE.
9. Math in questions: HTML sub/sup. No MathJax (offline, no CDN).
10. Every checkbox/radio: native inputs, big tap targets (min 40px).

## UX (PRD §11 — non-tech first)

11. Exam screen = faithful NTA replica (terms + layout). Home/import/
    result screens = plain language, big type (≥16px), ≥40px targets.
12. Palette status colors always paired with text counts — never color-
    only (color-blind users).
13. Destructive actions (delete bank, clear history, reset) always
    confirm with what will be lost.
14. Errors in human language + next step. No raw JSON dumps, no "undefined".
15. Empty states show the next action. Result screen: score big, subject
    bars, one next-step hint.
16. Every screen has one obvious next action. No dead ends.

## Storage (IndexedDB — iOS evicts localStorage after 7 days)

DB: `ncbt` (version 1), stores:
- `banks` — imported + built-in bank store
- `test_state` — active exam snapshot
- `history` — finished tests
- `meta` — schema version marker
Read-only fallback: migrate any legacy localStorage data on first load.

## Verification (before saying done)

1. `python -m http.server 8000` in repo root.
2. Headless browser: SW registers, manifest parses, palette transitions
   correct, submit flow counts match, timer expires, reload resumes,
   result math spot-check, zero console errors.
3. `curl -I` deployed sw.js shows no-cache.
See docs/TEST_PLAN.md for the full checklist.
