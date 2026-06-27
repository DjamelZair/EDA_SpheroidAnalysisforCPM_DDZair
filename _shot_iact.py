import sys, pathlib
from playwright.sync_api import sync_playwright

arg = sys.argv[1]
target = arg if arg.startswith("http") else pathlib.Path(arg).resolve().as_uri()
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
errs = []

def on_console(m):
    if m.type in ("error", "warning"):
        errs.append(m.type + ": " + m.text)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    pg.on("console", on_console)
    pg.on("pageerror", lambda e: errs.append("PAGEERR: " + str(e)))
    pg.goto(target, wait_until="load")
    pg.wait_for_timeout(2500)
    cards = pg.query_selector_all("section.card:has(.iact)")
    print("interactive cards:", len(cards))
    for i, c in enumerate(cards, 1):
        c.scroll_into_view_if_needed()
        pg.wait_for_timeout(300)
        c.screenshot(path=str(out / ("iact_%02d.png" % i)))
    print("ERRORS:", errs[:15] if errs else "none")
    b.close()
