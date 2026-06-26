# Figure-presentation brief — thesis EDA site

**For:** the data-analysis agent producing the figures embedded in this site
(`/media/djameldino/Expansion/CLL_data/analysis`, GitHub Pages, repo
`DjamelZair/EDA_SpheroidAnalysisforCPM_DDZair`, five themes).

**Goal:** the design of the site is settled and the user likes it — what is missing is the
*analysis*. Produce real, correct, publication-quality figures whose **visual styling matches the
site** so they drop into the existing cards without looking foreign. Style serves the data, never the
other way round. Read this whole file before generating any figure.

---

## 1. The look you must match

The site is a **deep-teal canvas with warm paper text and gold accents**, two signal colours
(green = good/positive, clay-red = bad/loss). Typography is editorial: a condensed display face,
a serif italic for emphasis, a mono for labels. Your figures sit inside teal cards, so their
**data marks** must use this palette — not matplotlib defaults (no `C0` blue, no `tab10`).

```
Canvas / structure   teal-1 #052e36   teal-2 #0a4a55   teal-3 #0d5963   teal-4 #15616d
Text / paper         paper  #f3ecd6   cream  #faf3df   paper-2 #e8dab2
Accent (primary)     gold   #c8a05c   gold-2 #a37432   gold-3 #e7c98a
Signal — positive    green  #6dd9a1
Signal — negative    clay   #c44a30
Muted / secondary    muted  #8a9b9f   muted-2 #a8b5b8
```

Series colour priority: **gold → green → clay → teal-4 → muted**. Use green/clay only when they
carry meaning (improvement vs loss, significant vs not, treated vs control). For sequential/heatmap
data use a teal→gold ramp; for diverging data use clay ←→ green through a neutral cream.

Fonts: **DM Sans** for tick labels and body numbers, **JetBrains Mono** for axis titles,
annotations and units (uppercase, slightly tracked). If those aren't installed, fall back to
DejaVu Sans / a monospace and note it — do not silently use Arial/Inter.

## 2. Background — keep figures white, the site blends them

Do **not** bake the teal background into the PNG. Render on a **white** (or transparent) background
so the same file stays usable in the thesis PDF. The site wraps light figures in
`.figwrap.light`, which pads them in teal and applies `mix-blend-mode: multiply; opacity:.96` so the
white melts into the card. For that blend to look clean:

- pure-white figure background (`#ffffff`), no off-white panels, no drop shadows baked in;
- avoid large solid black fills (they go muddy under multiply) — use the dark teal `#052e36` for
  "ink" instead of `#000000`;
- keep ink/text dark enough to survive the multiply (teal-1 `#052e36` or `#1a3f47` for axis text).

If a figure genuinely needs a dark field (e.g. a microscopy panel), render it dark and the embedder
will use plain `.figwrap` (no blend) — flag which mode each figure is built for.

## 3. Matplotlib starter (copy-paste, then build the analysis on top)

```python
import matplotlib as mpl, matplotlib.pyplot as plt

TEAL1, TEAL2, TEAL4 = "#052e36", "#0a4a55", "#15616d"
GOLD, GREEN, CLAY, MUTED = "#c8a05c", "#6dd9a1", "#c44a30", "#8a9b9f"
SERIES = [GOLD, GREEN, CLAY, TEAL4, MUTED]

mpl.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "font.family": "DM Sans", "font.size": 11,
    "axes.edgecolor": TEAL1, "axes.labelcolor": TEAL1, "text.color": TEAL1,
    "xtick.color": TEAL1, "ytick.color": TEAL1,
    "axes.prop_cycle": mpl.cycler(color=SERIES),
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#d9d2bd", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.titleweight": "bold", "legend.frameon": False,
})
# axis titles / annotations in mono:
# ax.set_xlabel("TIME (H)", fontfamily="JetBrains Mono", fontsize=9, letterspacing-ish via labelpad)
```

Sizing: single-column figures ~7×4.5 in, wide cards ~11×4.5 in, square heatmaps ~6×6 in. Export
**PNG at 300 DPI** (the site uses PNG); also keep an SVG/PDF master where practical for the thesis.

## 4. Per-figure rules

- **One question per figure.** State it before plotting; the figure must answer exactly that.
- **One takeaway sentence** per figure — plain academic English, no hype. This becomes the card's
  `.verdict` line on the site, so write it as a finding ("J_cm drops 30% in 7/7 patients"), not a
  description ("a bar chart of J_cm").
- **Uncertainty is mandatory** where it exists: CIs/error bars/bootstrap bands, n stated in-figure,
  and draw the zero/null reference line when an interval can cross it.
- **Numbers must match the canonical thesis values** already on the site (e.g. drug-panel BCR-axis
  ΔJ_cc: tau −1.4 CI [−3.0, +0.2] weak, end-state +4.6 CI [+2.1, +7.0] significant). Do not invent
  or re-round. If your computation disagrees with a published site number, **stop and flag it** —
  don't quietly overwrite.
- **No chartjunk:** no 3-D, no rainbow, no dual hidden axes, no gradient fills behind bars, legends
  only when >1 series, direct-label lines where it's cleaner than a legend.
- **Honest scales:** bar charts start at zero; if you truncate an axis, mark it. Log scales labelled.
- **Accessibility:** don't rely on green-vs-clay alone — pair colour with shape/marker/position so
  the contrast survives colour-blindness and the multiply blend.

## 5. Delivery

Save figures under `assets/cll/figures/<theme>/` (existing subfolders: `morphology`, `segmentation`,
`cpm`). Use lowercase snake_case names that say what the figure shows
(`drug_panel_jcc_forest.png`, not `fig12.png`). For each figure return: filename, the one-line
takeaway (for the `.verdict`), n / source notebook, and whether it's a **light** (white, blended) or
**dark** (microscopy) figure so the page is wrapped correctly. Do not touch the HTML/CSS — the curate
role embeds the figures; you supply the analysis.
```
deliverable per figure:
  path:      assets/cll/figures/05_drug_realdata/drug_panel_jcc_forest.png
  mode:      light            # light = white bg (blended) | dark = microscopy
  takeaway:  "Panel-wide BCR-axis shift is weak under tau (−1.4, CI crosses 0) and significant only at end-state (+4.6)."
  n/source:  7 patients · real_data_inference_report.ipynb
```
```
