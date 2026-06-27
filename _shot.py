#!/usr/bin/env python3
"""Screenshot a built page + each native-figure card, for agent evaluation.
Run with the geoenv python (has playwright+chromium):
  conda run -n geoenv python analysis/_shot.py <page.html> <outdir>
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

page_path = pathlib.Path(sys.argv[1]).resolve()
outdir = pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
url = page_path.as_uri()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    pg.goto(url, wait_until="load")
    try:
        pg.wait_for_load_state("networkidle", timeout=6000)
    except Exception:
        pass
    pg.wait_for_timeout(1200)  # fonts / layout settle
    # full page
    pg.screenshot(path=str(outdir / "full_page.png"), full_page=True)
    # each card that holds a native figure, in document order
    cards = pg.query_selector_all("section.card:has(.figwrap.native)")
    print(f"native-figure cards found: {len(cards)}")
    for i, c in enumerate(cards, 1):
        c.scroll_into_view_if_needed()
        pg.wait_for_timeout(120)
        c.screenshot(path=str(outdir / f"fig_card_{i:02d}.png"))
    b.close()
print(f"wrote screenshots to {outdir}")
