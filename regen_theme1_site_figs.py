#!/usr/bin/env python3
"""
Regenerate the Theme-01 image-EDA figures so they are NATIVE to the dark-teal
site: transparent background, cream text, gold/green/clay marks that read on the
teal card. Leaves the white thesis-PDF figures in imaging_eda/figures untouched.

Strategy: the figure code (imaging_eda/imaging_data_eda.py) looks up colours live
from the shared palette dict `P` and from natrev_style's ACCENT/GREY/WARN. We
re-skin those *before* importing the figure script, monkeypatch nr()/save() for a
dark transparent theme, and write transparent PNGs straight into the site assets.
"""
import sys, matplotlib
matplotlib.use("Agg")
ROOT = "/media/djameldino/Expansion/CLL_data"
sys.path.insert(0, ROOT)
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path(ROOT) / "analysis/assets/cll/figures/01_image_eda"
OUT.mkdir(parents=True, exist_ok=True)

# ---- site palette (all readable on the teal-3 card #0d5963) ------------------
CREAM   = "#f3ecd6"; PAPER2 = "#e8dab2"
GOLD    = "#c8a05c"; GOLD_L = "#e7c98a"
GREEN   = "#6dd9a1"; SKY    = "#7fb3bd"
CLAY    = "#c44a30"; CLAY_L = "#e0795f"
MUTED   = "#a8b5b8"; SOFTGOLD = "#cdb48a"

# 1) re-skin the shared palette dict IN PLACE (marks read P[...] live)
from shared import plotting as SP
SP.P.update({
    "teal":         GOLD,      # primary data series  (was dark teal)
    "teal_light":   GREEN,
    "teal_dark":    SKY,
    "teal_pale":    "#cfe8df",
    "gold":         GREEN,      # secondary series (distinct from primary)
    "gold_light":   GOLD_L,
    "cherry":       CLAY,
    "cherry_light": CLAY_L,
    "prussian":     CREAM,      # used for max-hist + median lines
    "text_mid":     CREAM,      # in-axes annotations (full-cream, legible)
    "text_muted":   MUTED,
})

# 2) re-skin the categorical drug-class colours (distinct + teal-readable)
from imaging_eda import eda_helpers as H
# one fixed, brand-only, teal-readable colour per mechanism class so each class
# reads identically across fig01 and fig08 (no purple, no neutral grey, no
# low-luminance teal-on-teal, no near-white fill)
H.CLASS_COLOR = {
    "BTKi": "#c8a05c", "Syk i": "#6dd9a1", "PI3Ki": "#7fb3bd", "JAKi": "#e7c98a",
    "CXCR4 ant.": "#c44a30", "MEKi": "#e0795f", "NF-kB i": "#9ed8c0",
    "STAT6 i": "#bfe0e6", "MALT1i": "#cdb48a", "research": "#8fd0b0",
    "control": "#f3ecd6",
}

# 3) patch natrev_style: ACCENT/GREY/WARN + dark transparent nr() + site save()
from imaging_eda import natrev_style as NS
NS.ACCENT = GOLD; NS.GREY = MUTED; NS.WARN = CLAY

_orig_nr = NS.nr
def nr_site():
    _orig_nr()
    plt.rcParams.update({
        "figure.facecolor": "none", "axes.facecolor": "none",
        "savefig.facecolor": "none", "savefig.transparent": True,
        "text.color": CREAM, "axes.labelcolor": CREAM,
        "axes.edgecolor": SOFTGOLD, "axes.titlecolor": GOLD_L,
        "xtick.color": GOLD_L, "ytick.color": GOLD_L,
        "xtick.labelcolor": CREAM, "ytick.labelcolor": CREAM,
        "grid.color": SOFTGOLD, "grid.alpha": 0.18,
        "legend.labelcolor": CREAM,
        # left-align titles so they start at the left spine (x=0) and can never
        # collide with the panel letter parked in the left margin (x=-0.12)
        "axes.titlelocation": "left", "axes.titlepad": 8,
    })
NS.nr = nr_site

# panel letter: park fully in the left margin and pin its colour to cream so it
# is identical on every panel (site-only override; thesis figures untouched)
def panel_label_site(ax, letter, dx=-0.14, dy=1.16):
    ax.text(dx, dy, letter, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top", ha="left",
            clip_on=False, color=CREAM)
NS.panel_label = panel_label_site

WANT = {f"fig0{i}" for i in (1, 2, 3, 4, 5, 6, 7, 8, 9)}  # 04a/04b handled by prefix
def save_site(fig, name, *a, **k):
    stem = name.split("_")[0]
    if stem in WANT or name.startswith("fig04a"):
        # skip pure-micrograph plate fig04b (dark bitmap, not used on site)
        if not name.startswith("fig04b"):
            fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight",
                        transparent=True)
            print(f"  [site] {name}.png -> assets")
    plt.close(fig)
NS.save = save_site

# 4) run the figure script (import triggers top-to-bottom execution)
print("Regenerating Theme-01 figures with the site theme ...")
try:
    import imaging_eda.imaging_data_eda  # noqa: F401
except Exception as e:
    import traceback; traceback.print_exc()
    print(f"\n[partial] stopped at: {e!r} — figures saved before this point are valid.")
print("Done.")
