"""
figtools.py - regenerate light-background microscopy figures INTO the dark theme.

Approach: contrast-stretch the grayscale microscopy, then map luminance through a 3-stop
teal ramp so dark -> near-black, mid -> card teal, and the BRIGHTEST regions (the legend
box fills, pure-white margins) -> cream. That keeps legend boxes legible (dark text on
cream) instead of washing them into the teal. Coloured annotations are recoloured to theme
accents: reddish outline/box -> gold, green labels -> cream. Used instead of CSS blends,
which crush coloured information and contrast.
"""
import sys
import numpy as np
from PIL import Image

NEARBLACK = np.array([3, 20, 25])      # L = 0
TEAL = np.array([13, 89, 99])          # #0d5963 card teal  (mid)
CREAM = np.array([250, 243, 223])      # #faf3df            (brightest -> legend plates)
GOLD = np.array([231, 201, 138])       # #e7c98a
MIDSTOP = 0.55                          # luminance where the cream lift begins lower bound
HISTOP = 0.86                           # above this -> ramp toward cream


def _ramp(L):
    """3-stop ramp NEARBLACK -> TEAL (0..HISTOP) -> CREAM (HISTOP..1)."""
    out = np.empty(L.shape + (3,), np.float32)
    lo = L <= HISTOP
    t = np.clip(L / HISTOP, 0, 1)[..., None]
    out[lo] = (NEARBLACK[None, :] * (1 - t) + TEAL[None, :] * t)[lo]
    hi = ~lo
    t2 = np.clip((L - HISTOP) / (1 - HISTOP), 0, 1)[..., None]
    out[hi] = (TEAL[None, :] * (1 - t2) + CREAM[None, :] * t2)[hi]
    return out


def regen(src, dst, crop_top=0.0, p_lo=2.0, p_hi=98.0):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    if crop_top:
        a = a[int(a.shape[0] * crop_top):, :, :]
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    L = (0.299 * R + 0.587 * G + 0.114 * B) / 255.0
    # contrast stretch on the greyscale body so spheroids go genuinely dark
    plo, phi = np.percentile(L, p_lo), np.percentile(L, p_hi)
    Ls = np.clip((L - plo) / max(phi - plo, 1e-3), 0, 1)
    out = _ramp(Ls)
    red = (R - np.maximum(G, B) > 28) & (R > 70)
    green = (G - np.maximum(R, B) > 26) & (G > 60)
    out[green] = CREAM
    out[red] = GOLD
    out = np.clip(out, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(dst)
    print(f"{dst}: {out.shape} red->gold={int(red.sum())} green->cream={int(green.sum())} "
          f"stretch=[{plo:.2f},{phi:.2f}]")


def regen_bg(src, dst):
    """For COLOURED figures (e.g. multicolour cell lattices): replace the near-white
    background with teal so the colours pop on the dark site, and lift dark text/borders
    to cream for legibility. Colours of the cells are preserved."""
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mn = np.minimum(np.minimum(R, G), B)
    mx = np.maximum(np.maximum(R, G), B)
    white = mn > 225                       # near-white background and gutters
    dark = (mx < 80)                       # title/labels and thin cell borders
    out = a.copy()
    out[white] = np.array([13, 89, 99])    # teal-3 card colour
    out[dark] = CREAM                       # legible text on teal
    out = np.clip(out, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(dst)
    print(f"{dst}: {out.shape} white->teal={int(white.sum())} dark->cream={int(dark.sum())}")


if __name__ == "__main__":
    PORT = "/media/djameldino/Expansion/CLL_data/html portfolio/assets/cll/figures/"
    here = sys.argv[1] if len(sys.argv) > 1 else "."
    regen(PORT + "morphology/segmentation_overlay_grid.png",
          here + "/02_segmentation/fig/overlay_dark.png", crop_top=0.105)
    regen(PORT + "segmentation/hardest_case_showcase.png",
          here + "/02_segmentation/fig/hardest_dark.png")
    # Theme 3: Saltelli VTK library gallery (coloured cell lattices) -> teal background
    import os
    os.makedirs(here + "/03_simulation_library/fig", exist_ok=True)
    regen_bg("/media/djameldino/Expansion/CLL_data/rq3_inference/vtk_plots_saltelli /"
             "saltelli_gallery_n16_seed0.png",
             here + "/03_simulation_library/fig/saltelli_gallery.png")
