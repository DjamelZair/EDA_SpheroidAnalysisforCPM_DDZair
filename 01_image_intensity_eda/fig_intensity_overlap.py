"""
Theme 01 (image intensity) motivation figure.

Question: can a frame be told apart as "annotated" vs "unannotated" by brightness alone?
If the two sets share an intensity range, the annotated/background distinction cannot be
thresholded and must be learned.

Honest comparison note: the annotated images/ PNGs are already contrast-stretched, so a raw
PNG-vs-raw-tif comparison would be apples to oranges. I therefore compare RAW source frames on
both sides: the annotated originals matched back to their raw .tif acquisitions (n=20 that exist
in the corpus; VID2356/VID2357 were not transferred to the inference corpus), against a random
sample of unannotated deployment frames. Both read as raw 8-bit grey.

Output: assets/cll/figures/01_image_intensity_eda/intensity_overlap_annotated_vs_unannotated.png
"""
import os, re, glob
import numpy as np, pandas as pd
from PIL import Image
import matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = "/media/djameldino/Expansion/CLL_data"
OUT  = f"{ROOT}/analysis/assets/cll/figures/01_image_intensity_eda"
os.makedirs(OUT, exist_ok=True)

# ---- site palette (from FIGURE_STYLE_BRIEF.md) ----
TEAL1, TEAL4 = "#052e36", "#15616d"
GOLD, GREEN, CLAY, MUTED = "#c8a05c", "#6dd9a1", "#c44a30", "#8a9b9f"
SERIES = [GOLD, GREEN, CLAY, TEAL4, MUTED]

# DM Sans / JetBrains Mono if present, else note the fallback (brief rule).
fam = {f.name for f in font_manager.fontManager.ttflist}
BODY = "DM Sans" if "DM Sans" in fam else "DejaVu Sans"
MONO = "JetBrains Mono" if "JetBrains Mono" in fam else "DejaVu Sans Mono"
if BODY == "DejaVu Sans":
    print("NOTE: DM Sans / JetBrains Mono not installed; falling back to DejaVu (per brief).")

mpl.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "font.family": BODY, "font.size": 11,
    "axes.edgecolor": TEAL1, "axes.labelcolor": TEAL1, "text.color": TEAL1,
    "xtick.color": TEAL1, "ytick.color": TEAL1,
    "axes.prop_cycle": mpl.cycler(color=SERIES),
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#d9d2bd", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.titleweight": "bold", "legend.frameon": False,
})
def mono(ax, x=None, y=None):
    if x: ax.set_xlabel(x, fontfamily=MONO, fontsize=9)
    if y: ax.set_ylabel(y, fontfamily=MONO, fontsize=9)

# ---- data: match annotated originals to their raw .tif, sample unannotated frames ----
rng = np.random.default_rng(0)
fi = pd.read_csv(f"{ROOT}/imaging_eda/cache/frame_index.csv")
idx = dict(zip(fi.stem, fi.path))
ann_stems = [os.path.basename(f)[:-4] for f in glob.glob(f"{ROOT}/data/segmentation_dataset/images/*.png")
             if "__aug" not in f]
def cands(s): return {s, s.rstrip("L"), re.sub(r"-1L$", "", s), re.sub(r"L$", "", s)}
matched = [idx[c] for s in ann_stems for c in cands(s) if c in idx]
matched = list(dict.fromkeys(matched))

def read_raw(p): return np.asarray(Image.open(p).convert("L")).astype(np.float32)
def frame_stats(paths, per_px):
    means, pool = [], []
    for p in paths:
        if not os.path.exists(p): continue
        g = read_raw(p); means.append(g.mean())
        pool.append(g.ravel()[rng.integers(0, g.size, per_px)])
    return np.array(means), np.concatenate(pool)

a_mean, a_pool = frame_stats(matched, 3000)
unann = fi[~fi.path.isin(set(matched))].sample(180, random_state=2).path.tolist()
n_mean, n_pool = frame_stats(unann, 1000)

# ---- overlap statistics ----
def ovl(x, y, lo, hi, bins=60):
    e = np.linspace(lo, hi, bins + 1)
    hx, _ = np.histogram(x, e, density=True); hy, _ = np.histogram(y, e, density=True)
    return float(np.minimum(hx, hy).sum() * (e[1] - e[0]))
from scipy.stats import rankdata
lab = np.r_[np.ones(len(a_mean)), np.zeros(len(n_mean))]; val = np.r_[a_mean, n_mean]
r = rankdata(val); auc = (r[lab == 1].sum() - len(a_mean) * (len(a_mean) + 1) / 2) / (len(a_mean) * len(n_mean))
auc = max(auc, 1 - auc)
ovl_px = ovl(a_pool, n_pool, 0, 255); ovl_mean = ovl(a_mean, n_mean, 0, 255)
print(f"n annotated raw {len(a_mean)} | n unannotated {len(n_mean)} | "
      f"OVL_px {ovl_px:.2f} OVL_mean {ovl_mean:.2f} AUC {auc:.2f}")

# ---- figure: one question, two views ----
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)

# (a) pooled raw pixel intensity
bins = np.arange(0, 257, 4)
ax[0].hist(n_pool, bins=bins, density=True, color=TEAL4, alpha=0.55, label=f"unannotated (n={len(n_mean)})")
ax[0].hist(a_pool, bins=bins, density=True, histtype="step", color=GOLD, lw=2.0,
           label=f"annotated (n={len(a_mean)})")
ax[0].set_title("Raw pixel intensity")
mono(ax[0], "GREY LEVEL (0-255)", "DENSITY")
ax[0].legend(loc="upper left")
ax[0].text(0.97, 0.95, f"overlap {ovl_px:.2f}", transform=ax[0].transAxes, ha="right", va="top",
           fontfamily=MONO, fontsize=10, color=TEAL1)

# (b) per-frame mean intensity, with markers (shape + colour, not colour alone)
jit = rng.uniform(-0.12, 0.12, len(n_mean))
ax[1].scatter(n_mean, 0.0 + jit, s=22, color=TEAL4, marker="o", alpha=0.7, label=f"unannotated (n={len(n_mean)})")
ax[1].scatter(a_mean, 1.0 + rng.uniform(-0.12, 0.12, len(a_mean)), s=34, color=GOLD, marker="^",
              edgecolor=TEAL1, linewidth=0.4, label=f"annotated (n={len(a_mean)})")
ax[1].axvline(n_mean.mean(), color=TEAL4, lw=1.2, ls="--")
ax[1].axvline(a_mean.mean(), color=GOLD, lw=1.4, ls="--")
ax[1].set_yticks([0, 1]); ax[1].set_yticklabels(["unann.", "annot."], fontfamily=MONO, fontsize=9)
ax[1].set_ylim(-0.6, 1.6); ax[1].set_xlim(110, 200)
ax[1].set_title("Per-frame mean intensity")
mono(ax[1], "MEAN GREY LEVEL (0-255)")
ax[1].text(0.97, 0.95, f"means {a_mean.mean():.0f} vs {n_mean.mean():.0f}\nseparation AUC {auc:.2f}",
           transform=ax[1].transAxes, ha="right", va="top", fontfamily=MONO, fontsize=10, color=TEAL1)

fig.suptitle("Annotated and unannotated frames share one intensity range",
             fontsize=13, fontweight="bold", color=TEAL1)
dst = f"{OUT}/intensity_overlap_annotated_vs_unannotated.png"
fig.savefig(dst)
print("wrote", dst)
