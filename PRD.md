# NEET CBT 2027 Simulator — PRD

Version: v0.1.0
Status: Draft (pending approval)
License: MIT
Target: NEET UG aspirants (free, FOSS)

## 1. Problem

NEET UG 2027 switches to Computer-Based Testing (CBT). Students practicing
on paper OMR get zero exposure to the real NTA interface: question palette
colors, mark-for-review semantics, timer pressure, click-navigation speed.
Paid test series exist; free offline ones don't.

## 2. Product

Offline-first PWA that replicates the NTA CBT interface exactly and runs
any NEET-style question bank. No account, no server data, no paywall.

## 3. Goals (v0.1.0)

- Exact NTA CBT UI replica (palette, buttons, dialogs, flows).
- Full mock: 200 questions presented, 180 attempted, +4/-1/0, 3h20m.
- 2027-mode mock: 180 compulsory questions, 180 min (REPORTED pattern —
  Section B choice discontinued per education news; NOT yet official.
  Both modes selectable; 2027-mode default).
- Custom mode: filter by subject, pick N questions, timer on/off.
- Question bank: 64 built-in sample questions (16/subject, chapter-tagged,
  flagged SAMPLE — verify vs NCERT) + JSON import/export for real PYQs.
- PWA: installable Android (Chrome), iOS (Safari A2HS), laptop (Edge/Chrome).
  Offline after first load.
- Exam state survives phone sleep, refresh, accidental close.
- Score history + full per-question review on result screen.
- FOSS: public GitHub repo, MIT, free for students.

## 4. Non-Goals (v0.1.0)

- Percentile normalization (fake percentiles = slop; raw score only).
- Accounts, login, cloud sync, leaderboards.
- Online answer-key fetching.
- Multi-language UI.
- Question authoring UI.

## 5. UI Spec (NTA replica)

### 5.1 Instruction page
- Rule text blocks, checkbox "I have read and understood the instructions",
  checkbox "I agree to not divulge questions", Proceed button (disabled
  until both checked).
- Wording mirrors NTA style but is NOT a verbatim copy of NTA text
  (we replicate the interface, not their content). NEET-specific rules
  shown: 200 questions, 180 to attempt, +4/-1/0, 3h20m, no calculator,
  rough sheet return.

### 5.2 Exam screen (verified pixel-level vs NTA AboutCBT.pdf screens, Aug 2026)
- Header: NTA-style branding top-left; "[Candidate Name]" in brackets on
  sub-header left; "Question Paper" link top-right (opens full-paper
  overlay); language selector near profile image.
- Timer: label "Remaining Time:" + cyan/light-blue rounded pill badge,
  digital countdown HH:MM:SS, top-right below Question Paper link. Red
  flash last 5 min. Expiry = auto-submit.
- Workspace: left column ~65-70% question panel, right column ~30-35%
  palette. Palette collapsible via > < tab on sidebar's left border
  (expands question panel to 100%).
- Question panel: numbered question, options with circular grey radio
  buttons; clicking selected radio again deselects; in-panel ↑/↓ scroll
  jump buttons for long questions.
- Main button row (exact order + colors, verified):
  1. "Save & Next" — bright green bg, white bold text. Saves + advances.
  2. "Save & Mark For Review" — ORANGE/YELLOW bg, white text. Saves
     answer AND flags for review (evaluated if left as-is).
  3. "Clear Response" — light grey/white bg, dark text. Deselects.
  4. "Mark For Review & Next" — medium blue bg, white text. Flags
     WITHOUT saving, advances.
- Secondary controls: muted grey links "<< Back" and "Next >>" bottom
  left (navigate without saving). Green "Submit" button bottom right.
- Section auto-advance: "Save & Next" on last question of a section
  jumps to Q1 of next section.

### 5.3 Right palette: legend + grid (verified shapes, NOT plain squares)
Legend box (top of sidebar) with live counters and SHAPES:
- Not Visited: grey rounded square box
- Not Answered: RED left-pointing trapezoid/polygon
- Answered: GREEN right-pointing trapezoid/polygon
- Marked for Review: solid purple circle
- Answered & Marked for Review: purple circle with small green/yellow
  badge (legend text: "will be considered for evaluation")
Question grid: 10 columns (01-10, 11-20, ...), numbers in grey rounded
squares by default; answered/marked squares transform into the status
shape. Subject tabs above palette with text counts (not color-only).

### 5.4 Marking scheme (verified: NTA official advisory PDF)
- Correct = +4, Incorrect = -1, Unanswered = 0.
- Marked for Review WITHOUT an option selected = 0 (NOT -1, NOT +4).
- Answered & Marked for Review (via "Save & Mark For Review") = scored
  as answered.

### 5.5 Submit flow (2-step, NTA style)
1. Submit button → dialog: counts table (Answered / Not Answered /
   Not Visited / Marked for Review) + Yes/No.
2. Yes → second dialog "Do you really want to submit?" → Yes = submit.

### 5.6 Result screen
- Score / 720, per-subject breakdown, correct/wrong/skipped, accuracy %.
- Per-question review: your answer vs correct answer + explanation.
- Export/backup: full test JSON download.

## 6. Timer rule

- Deadline stored as epoch ms. Timer = Date.now() diff, not setInterval
  accumulation. Survives background kill; auto-submit on expiry even if
  reopened late.

## 7. Data

### 7.1 localStorage keys
- `ncbt_banks` — imported banks
- `ncbt_test_state` — active exam (answers, deadline, palette, index)
- `ncbt_history` — finished test summaries
- `ncbt_v` — schema/version marker

### 7.2 Bank JSON schema
See docs/BANK_SCHEMA.md. Validated on import: subject enum, 4 non-empty
options, ans 0-3, unique question text; reject with error list, atomic
load (nothing half-imported).

## 8. Deployment

- Vercel (user requirement). vercel.json REQUIRED: sw.js no-cache/no-store
  headers (Vercel CDN otherwise caches the service worker and users get
  stuck on old versions).
- SEO max: full meta, Open Graph, Twitter card, JSON-LD (WebApplication,
  FAQPage, BreadcrumbList), sitemap.xml, robots.txt.

## 9. Acceptance criteria (v0.1.0)

- [ ] Instructions gate works (Proceed disabled until both checkboxes).
- [ ] Palette colors match spec 5.2; status transitions correct
      (visit/answer/clear/mark/unmark).
- [ ] Marked-for-review + answered counted as answered at submit.
- [ ] Timer counts down, red <5min, auto-submit at 0.
- [ ] Refresh/reload mid-test resumes exact state (answers, timer).
- [ ] Full mock = 200 Q, max 180 attempted, +4/-1, max 720.
- [ ] Custom mode: subject filter + N + timer off works.
- [ ] JSON import validates, rejects bad banks atomically with error list.
- [ ] Result screen math correct (spot-check known answer set).
- [ ] PWA: manifest valid, SW caches app, offline reload works.
- [ ] Vercel prod: sw.js served no-cache (curl header check).
- [ ] No console errors in headless browser run.
- [ ] README documents install (phone+laptop), import format, backup.

## 10. Timeline

- Docs: now (PRD, CLAUDE, AGENTS, README, BANK_SCHEMA, TEST_PLAN).
- Build v0.1.0: after approval.
- Verify: local headless + Vercel deploy + curl checks.

## 11. UX Requirements (non-tech first)

The exam screen is a faithful NTA replica by design — its terms
(Save & Next, Mark for Review) stay. Everything AROUND the exam is
designed for a non-tech user (e.g. a sibling opening it on a phone
with zero setup).

### 11.1 Home screen
- One dominant action: "Start Full Mock" — opens a 2-preset config sheet:
  - "NEET 2027 pattern (reported)": 180 compulsory Q, 180 min.
  - "Classic NEET pattern": 200 Q, 180 attempted, 3h20m.
  Default = 2027 pattern. 2027 = 180-compulsory is REPORTED (Section B
  choice discontinued), not yet NTA-official — label it as such. One tap
  from preset → instructions.
- Secondary: "Practice Mode" (subject chips + question-count slider +
  timer on/off, all sane defaults).
- Plain labels: "Import Questions", "My Banks", "Finished Tests",
  "Backup". No settings labyrinth; every goal ≤ 2 taps.
- No dead ends: every screen has one obvious next action.

### 11.2 Language
- Home / import / result screens: plain words, no exam jargon.
- Errors in human language + what to do next, e.g. "This file isn't a
  question bank. Export one from the app to get a template, or read the
  format guide (docs/BANK_SCHEMA.md)."
- Exam screen keeps NTA vocabulary — that is the point of the replica.

### 11.3 Safety
- Every destructive action (delete bank, clear history, reset) →
  confirm dialog stating exactly what will be lost.
- Import of big files shows progress; success shows bank name + subject
  split.
- Reload mid-exam → "Resume your test?" prompt; never silent state loss.

### 11.4 Clarity & accessibility
- Body type ≥ 16px, high contrast, tap targets ≥ 40px.
- Palette status colors never the only signal: text counts beside each
  subject tab (e.g. "Answered 42 · Marked 3").
- Result: score large, green above target / red below, per-subject bars,
  one next-step hint ("Review mistakes").
- Visible focus/active states for keyboard and touch.

### 11.5 Guidance
- First run: dismissible 3-line "how to start" hint card.
- Empty states explain next action ("No tests yet — start a Full Mock.").
- After result: "Review mistakes" is the obvious next step; export backup
  offered.
