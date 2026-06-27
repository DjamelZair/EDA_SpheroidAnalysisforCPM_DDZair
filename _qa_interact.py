import sys, pathlib
from playwright.sync_api import sync_playwright

URL = sys.argv[1]
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
errs = []

PG = None
def shoot(card, name):
    card.scroll_into_view_if_needed(); PG.wait_for_timeout(350)
    card.screenshot(path=str(out / (name + ".png")))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    pg.on("console", lambda m: errs.append("err: " + m.text[:120]) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerr: " + str(e)[:120]))
    PG = pg
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(2500)
    cards = pg.query_selector_all("section.card:has(.iact)")
    pg.screenshot(path=str(out / "full_page.png"), full_page=True)

    # 1 MORPH: switch param button + move slider
    m = cards[0]
    shoot(m, "morph_before")
    chips = m.query_selector_all(".iact-chip")
    if len(chips) > 1: chips[1].click(); pg.wait_for_timeout(500)
    shoot(m, "morph_after_param")
    sl = m.query_selector(".iact-slider input")
    if sl:
        box = sl.bounding_box()
        pg.mouse.click(box["x"] + box["width"] * 0.85, box["y"] + box["height"] / 2)
        pg.wait_for_timeout(500)
    shoot(m, "morph_after_slider")

    # 2 MORPHOSPACE: highlight extremes + click a point
    ms = cards[1]
    shoot(ms, "morphospace_before")
    exbtn = [c for c in ms.query_selector_all(".iact-chip") if "extreme" in (c.inner_text() or "").lower()]
    if exbtn: exbtn[0].click(); pg.wait_for_timeout(400)
    shoot(ms, "morphospace_after_extremes")
    cv = ms.query_selector("canvas.iact-canvas")
    if cv:
        bb = cv.bounding_box()
        pg.mouse.click(bb["x"] + bb["width"] * 0.32, bb["y"] + bb["height"] * 0.42)
        pg.wait_for_timeout(400)
    shoot(ms, "morphospace_after_click")

    # 3 SURROGATE: switch tab
    sg = cards[2]
    shoot(sg, "surrogate_before")
    tabs = sg.query_selector_all(".iact-seg .iact-chip")
    if len(tabs) > 1: tabs[1].click(); pg.wait_for_timeout(500)
    shoot(sg, "surrogate_after_tab")

    # 4 COVERAGE: drag threshold to minimum
    cov = cards[3]
    shoot(cov, "coverage_before")
    cs = cov.query_selector(".iact-slider input")
    if cs:
        box = cs.bounding_box()
        pg.mouse.click(box["x"] + box["width"] * 0.08, box["y"] + box["height"] / 2)
        pg.wait_for_timeout(500)
    shoot(cov, "coverage_after_lowthresh")

    print("cards:", len(cards), "| errors:", errs[:8] if errs else "none")
    b.close()
