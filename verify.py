import json, sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/"
fails = []
console_errors = []

def check(name, cond, extra=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f" — {extra}" if extra else ""))
    if not cond:
        fails.append(name)

def pass_gate(page):
    page.check("#chk-read")
    page.check("#chk-agree")
    page.click("#btn-proceed")
    page.wait_for_timeout(250)

def start_custom(page, n=10, timer=False):
    page.click("#btn-start-mock")
    page.click('[data-preset="custom"]')
    page.wait_for_timeout(200)
    if not timer:
        page.uncheck("#custom-timer")
    page.fill("#custom-count", str(n))
    page.click("#btn-config-start")
    page.wait_for_timeout(250)
    pass_gate(page)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: console_errors.append(str(e)))

    page.goto(URL, wait_until="networkidle")

    # A. Home renders, sample bank loaded (64 questions)
    check("A1 home visible", page.is_visible("#screen-home"))
    page.wait_for_timeout(400)
    total_q = page.evaluate("banks.reduce((n,b)=>n+b.questions.length,0)")
    check("A2 sample bank loaded", total_q == 64, str(total_q))

    # B. Start Full Mock -> config -> p2027 preset
    page.click("#btn-start-mock")
    check("B1 config modal", page.is_visible("#modal-config"))
    presets = page.locator("#modal-config .preset")
    check("B2 three presets", presets.count() == 3, str(presets.count()))
    page.click('[data-preset="p2027"]')
    page.click("#btn-config-start")
    check("B3 instructions screen", page.is_visible("#screen-instructions"))
    check("B4 proceed disabled", page.is_disabled("#btn-proceed"))
    pass_gate(page)
    check("B5 proceed enabled", page.is_enabled("#btn-proceed") or page.is_visible("#screen-exam"))
    check("B6 exam screen", page.is_visible("#screen-exam"))
    # 2027 preset: sample bank only has 64 Q → 64-question test + warning toast
    qcount = page.inner_text("#q-count")
    check("B7 pool-limited test", "of 64" in qcount, qcount)

    # C. Palette logic: answer Q1
    page.click("#q-opts .opt >> nth=1")
    page.click("#btn-save-next")
    check("C1 answered count 1", page.inner_text("#c-a") == "1", page.inner_text("#c-a"))
    cell1 = page.locator(".qcell >> nth=0")
    check("C2 cell green", "s-a" in (cell1.get_attribute("class") or ""), cell1.get_attribute("class"))
    # Clear Response on Q2
    page.click("#q-opts .opt >> nth=0")
    page.click("#btn-clear")
    check("C3 clear -> not answered", page.inner_text("#c-na") == "1", page.inner_text("#c-na"))
    # Mark For Review & Next
    page.click("#btn-mark-next")
    check("C4 marked count 1", page.inner_text("#c-m") == "1", page.inner_text("#c-m"))
    # Save & Mark For Review
    page.click("#q-opts .opt >> nth=2")
    page.click("#btn-save-mark")
    check("C5 answered+marked", page.inner_text("#c-am") == "1", page.inner_text("#c-am"))

    # D. Submit flow: 2 steps
    page.click("#btn-submit")
    check("D1 submit modal 1", page.is_visible("#modal-submit1"))
    page.click("#s1-yes")
    check("D2 submit modal 2", page.is_visible("#modal-submit2"))
    page.click("#s2-no")
    check("D3 cancel back to exam", page.is_visible("#screen-exam"))

    # E. Timer present (64 Q → 64 min)
    t = page.inner_text("#timer")
    check("E1 timer running", t.startswith("01:0") or t.startswith("00:5"), t)

    # F. Persistence: reload -> resume dialog
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(600)
    check("F1 resume dialog", page.is_visible("#modal-confirm"), page.inner_text("#modal-confirm").strip()[:60])
    page.click("#confirm-no")
    page.wait_for_timeout(300)

    # G. Import validation: bad file
    bad = {"name": "Bad", "questions": [{"subject": "Astrology", "q": "x", "opts": ["a"], "ans": 9}]}
    page.set_input_files("#file-import", {"name": "bad.json", "mimeType": "application/json", "buffer": json.dumps(bad).encode()})
    page.wait_for_timeout(500)
    check("G1 bad import rejected", page.is_visible("#modal-errors"), page.inner_text("#err-title"))
    page.click("#err-close")

    # G2. Good import
    good = {"name": "Test Bank", "source": "t", "questions": [
        {"subject": "Physics", "chapter": "c", "q": "1+1?", "opts": ["1", "2", "3", "4"], "ans": 1, "expl": ""},
        {"subject": "Chemistry", "chapter": "c", "q": "H2O?", "opts": ["a", "b", "c", "d"], "ans": 0, "expl": ""}
    ]}
    page.set_input_files("#file-import", {"name": "good.json", "mimeType": "application/json", "buffer": json.dumps(good).encode()})
    page.wait_for_timeout(500)
    check("G2 good import accepted", page.inner_text("#toast").count("Imported") > 0 or page.is_visible("#toast"), page.inner_text("#toast"))
    page.wait_for_timeout(3800)

    # H. Full mock scoring: custom 10 questions, all correct
    start_custom(page, 10, timer=False)
    n = page.evaluate("test.qs.length")
    check("H1 custom 10 questions", n == 10, str(n))
    for i in range(n):
        ans = page.evaluate("test.qs[test.qIndex].ans")
        page.click(f"#q-opts .opt >> nth={ans}")
        page.click("#btn-save-next")
    check("H2 all answered", page.inner_text("#c-a") == "10", page.inner_text("#c-a"))
    page.click("#btn-submit")
    page.click("#s1-yes")
    page.click("#s2-yes")
    page.wait_for_timeout(400)
    check("H3 result screen", page.is_visible("#screen-result"))
    score = page.inner_text("#res-score")
    check("H4 score 40/40", score == "40", score)
    check("H5 correct 10", page.inner_text("#res-correct") == "10", page.inner_text("#res-correct"))
    # mixed: 5 wrong -> -1 each
    page.click("#btn-done")
    start_custom(page, 10, timer=False)
    for i in range(10):
        ans = page.evaluate("test.qs[test.qIndex].ans")
        wrong = (ans + 1) % 4 if i % 2 == 0 else ans
        page.click(f"#q-opts .opt >> nth={wrong}")
        page.click("#btn-save-next")
    page.click("#btn-submit")
    page.click("#s1-yes")
    page.click("#s2-yes")
    page.wait_for_timeout(400)
    score2 = page.inner_text("#res-score")
    # 5 correct*4 + 5 wrong*(-1) = 15
    check("H6 mixed score 15", score2 == "15", score2)
    browser.close()

print("\n" + "=" * 40)
if console_errors:
    print("CONSOLE ERRORS:")
    for e in console_errors[:10]:
        print("  ", e[:200])
    check("H1 no console errors", False, str(len(console_errors)) + " errors")
else:
    check("H1 no console errors", True)

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILURES'}")
sys.exit(1 if fails else 0)
