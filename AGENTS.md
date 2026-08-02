# NEET CBT 2027 — AGENTS.md (repo rules for any agent)

## Project
Offline-first PWA: NEET 2027 CBT simulator replicating NTA interface.
FOSS (MIT), free for aspirants, deployed on Vercel.
Owner: Akash (@AkashPriyadarshii).

## Read first
- PRD.md — what is being built, acceptance criteria for v0.1.0.
- CLAUDE.md — build rules, file map, storage keys, verification.

## Ground rules
- No frameworks, no build step, no CDN. Vanilla single-file app.
- No feature beyond PRD v0.1.0. Non-goals are hard walls.
- No AI-generated exam questions. Starter bank = flagged SAMPLE.
- Timer must survive phone sleep (epoch deadline, not interval).
- Exam state persisted to IndexedDB on every action (iOS evicts
  localStorage after 7 days; see CLAUDE.md).
- Import validation atomic: all-or-nothing with error list.
- sw.js never cached (Vercel header + SW version pattern).
- Diff-minimal edits. State file paths. No silent try/catch.
- 3-strike rule: same bug 3x → stop, escalate to human, web-search fix.

## Commands
- serve:  `python -m http.server 8000`
- verify: follow docs/TEST_PLAN.md checklist (headless browser pass
  required before deploy claim)
- deploy: `vercel --prod` (or vercel.new import from GitHub repo)

## Deliverables per change
- File(s) changed with paths.
- Evidence: test output / curl headers / screenshot — no unverified claims.
