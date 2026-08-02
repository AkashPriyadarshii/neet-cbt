# NEET CBT 2027 — README

Free, offline-first PWA that replicates the NTA computer-based test
interface for NEET UG 2027. Practice the real exam interface on your
phone or laptop — question palette, mark-for-review, timer, auto-submit —
with your own question banks.

MIT licensed. Free for all NEET aspirants. No accounts, no tracking, no
server data. Everything stays on your device.

## Features

- Exact NTA CBT replica: 5-color question palette, subject tabs,
  Save & Next / Clear Response / Mark for Review, 2-step submit dialogs.
- Full mock: 200 questions, 180 attempted, +4/-1, 720 max, 3h20m timer.
- Custom mode: pick subject + question count, timer on/off.
- Timer survives phone sleep; refresh resumes exam exactly where you left.
- Result screen: score, per-subject breakdown, per-question review.
- Import your own PYQ banks as JSON (schema: docs/BANK_SCHEMA.md).
- Works fully offline after first visit. Installable as an app.

## Install

Laptop (Chrome/Edge):
1. Open the site.
2. Address bar → "Install" / "Add to desktop" icon.

Android (Chrome):
1. Open the site.
2. Menu → "Add to Home screen" → Install.

iPhone/iPad (Safari):
1. Open the site.
2. Share button → "Add to Home Screen".

## Question banks

Built-in: 64 sample questions (16 per subject), chapter-tagged, flagged
SAMPLE — verify against NCERT before trusting.

Bring your own: export PYQs to the JSON format documented in
docs/BANK_SCHEMA.md, import in-app, then run unlimited custom tests.

Generate with AI: copy the master prompt in docs/AI_BANK_PROMPT.md (also
built into the app: Home → Get Banks via AI) into Claude / Gemini /
ChatGPT, save the JSON reply as `bank.json`, import. Always verify
generated answers against NCERT.

## Backup

Result screen exports each finished test as JSON. `Export backup` on the
home screen downloads banks + history. Store it; re-import on any device.

## Development

See PRD.md, CLAUDE.md, AGENTS.md, docs/TEST_PLAN.md.

- Serve locally: `python -m http.server 8000`
- Deploy: Vercel (vercel.json sets sw.js no-cache so updates reach users)

## License

MIT — use, fork, improve. Built for NEET aspirants.
