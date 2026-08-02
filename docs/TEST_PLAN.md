# Test Plan (v0.1.0)

Run against local `python -m http.server 8000` in a headless browser
(scrapling/playwright), then against the deployed Vercel URL.

## A. Instructions gate

- [ ] Proceed button disabled until BOTH checkboxes checked.
- [ ] Unchecking one re-disables Proceed.
- [ ] Proceed enters exam with configured test (full mock / custom).

## B. Palette & status transitions

- [ ] All squares grey initially (Not Visited).
- [ ] Opening a question → square shows red (Not Answered).
- [ ] Save & Next → green (Answered), moves to next question.
- [ ] Clear Response → red again, option deselected.
- [ ] Mark for Review & Next → purple (marked, unanswered).
- [ ] Answer then Mark → purple with green dot; counts as answered at submit.
- [ ] Subject tabs filter palette; per-subject counts correct.
- [ ] Clicking a palette square jumps to that question.

## C. Timer

- [ ] Counts down HH:MM:SS, no drift after 30s idle.
- [ ] Red flash style applied under 5 min (custom mode: timer on, short N).
- [ ] Expiry → auto-submit fires, result screen shown.

## D. Persistence

- [ ] Answer 3 questions, reload page → "Resume exam" prompt, exact state
      (answers, current index, deadline) restored.
- [ ] Phone-sleep simulation (raise deadline by 60s in devtools, reload)
      → timer reflects wall clock, not uptime.

## E. Scoring

- [ ] Full mock config: 200 questions presented, max 180 attempted.
- [ ] 2027 preset: exactly 180 compulsory questions, 180-min timer.
- [ ] Marked+answered counted as answered; answered+marked never counted
      twice; unvisited = skipped (0).
- [ ] Spot-check: known answer set → expected score/720, accuracy %
      correct.
- [ ] Subject breakdown sums to total.

## F. Banks

- [ ] Built-in: 64 questions, 16 per subject, all SAMPLE-flagged.
- [ ] Import valid bank (docs/BANK_SCHEMA.md example) → appears in list.
- [ ] Import corrupt bank (bad subject, 3 opts, dup q, ans=5) → rejected
      atomically, error list names each failing question, existing banks
      untouched.
- [ ] Export bank → JSON round-trips back into the app.

## G. PWA & deploy

- [ ] manifest.webmanifest valid JSON, icons exist at declared paths.
- [ ] SW registers on first load; second load works offline (devtools
      network offline → reload OK).
- [ ] SW version bump → activate deletes old caches (no stale app).
- [ ] Deployed: GET / 200; GET /sw.js response header
      `Cache-Control: no-cache, no-store, must-revalidate`.
- [ ] robots.txt + sitemap.xml served; sitemap URLs return 200.
- [ ] Zero console errors across the full run.

## H. Mobile sanity (manual, user side)

- [ ] Android Chrome: Add to Home screen installs standalone app.
- [ ] iOS Safari: Share → Add to Home Screen; app runs offline.
- [ ] Touch targets usable (min 40px).
