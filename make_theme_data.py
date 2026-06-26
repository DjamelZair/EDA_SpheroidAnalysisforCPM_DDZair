"""
make_theme_data.py - derive interactive-chart data (real numbers) from the local analysis
CSVs and write small JSON blobs into assets/data/. These are inlined into the pages at build
time so charts work both on GitHub Pages and from a local file:// preview.

Source of truth = the same CSVs the thesis notebooks use. No re-running of image-loading.
Run from analysis/:  python make_theme_data.py
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

REPO = Path("/media/djameldino/Expansion/CLL_data")
CACHE = REPO / "imaging_eda/cache"
FV = REPO / "rq1_segmentation/results/feature_validation"
OUT = Path(__file__).resolve().parent / "assets/data"
OUT.mkdir(parents=True, exist_ok=True)


def W(name, payload):
    (OUT / name).write_text(json.dumps(payload, allow_nan=False, separators=(",", ":")))
    print("wrote", name)


def r(x, n=4):
    if isinstance(x, float):
        return round(x, n)
    return x


# ---- Theme 1: drug-response timecourse (6 features x 3 drug conditions) ----------------
def timecourse():
    df = pd.read_csv(FV / "timecourse_full_features.csv").sort_values("hours")
    feats = ["total_area", "equivalent_diameter", "circularity", "solidity", "perimeter", "eccentricity"]
    nice = {"total_area": "area", "equivalent_diameter": "diameter", "circularity": "roundness",
            "solidity": "solidity", "perimeter": "perimeter", "eccentricity": "elongation"}
    out = {"features": {}, "series": [], "labels": nice}
    drugs = sorted(df["drug"].unique())
    out["series"] = drugs
    for f in feats:
        out["features"][f] = {}
        for d in drugs:
            sub = df[df["drug"] == d]
            out["features"][f][d] = [{"x": r(h, 3), "y": r(v, 4)}
                                     for h, v in zip(sub["hours"] / 24.0, sub[f])]
    W("theme1_timecourse.json", out)


# ---- Theme 1: contrast vs fragment count (originals only) ------------------------------
def contrast_frag():
    df = pd.read_csv(CACHE / "labelled_qc.csv")
    df = df[(df["is_aug"] == False) & df["michelson_contrast"].notna() & df["n_objects"].notna()]
    pts = [{"x": r(c, 4), "y": int(n)} for c, n in zip(df["michelson_contrast"], df["n_objects"])]
    W("theme1_contrast_frag.json", {"points": pts,
      "n": len(pts), "cmin": r(df["michelson_contrast"].min()), "cmax": r(df["michelson_contrast"].max())})


# ---- Theme 1: focus (Laplacian variance) distribution, originals ----------------------
def focus_hist():
    df = pd.read_csv(CACHE / "labelled_qc.csv")
    v = df[(df["is_aug"] == False)]["lap_var"].dropna().values
    v = v[v > 0]
    logv = np.log10(v)
    counts, edges = np.histogram(logv, bins=12)
    centers = [r((edges[i] + edges[i + 1]) / 2, 3) for i in range(len(counts))]
    W("theme1_focus.json", {"centers": centers, "counts": [int(c) for c in counts],
      "span_decades": r(float(logv.max() - logv.min()), 2)})


# ---- Theme 1: fragmentation by drug-mechanism class ------------------------------------
def frag_by_class():
    df = pd.read_csv(CACHE / "frame_qc.csv")
    df = df[df["drug_class"].notna() & df["frag_index"].notna()]
    g = df.groupby("drug_class")["frag_index"].agg(["median", "count"]).reset_index()
    g = g[g["count"] >= 30].sort_values("median", ascending=False)
    W("theme1_frag_class.json", {
        "labels": [str(x) for x in g["drug_class"]],
        "median": [r(float(x)) for x in g["median"]],
        "count": [int(x) for x in g["count"]]})


# ---- Theme 1: components per image (motivates CC-Dice; replaces white gallery) ---------
def ncomp_hist():
    df = pd.read_csv(CACHE / "labelled_qc.csv")
    v = df[(df["is_aug"] == False)]["n_objects"].dropna().astype(int).values
    mx = int(min(v.max(), 40))
    counts, edges = np.histogram(v, bins=range(0, mx + 2))
    labels = [str(int(e)) for e in edges[:-1]]
    W("theme1_ncomp.json", {"labels": labels, "counts": [int(c) for c in counts],
      "median": int(np.median(v)), "multi_frac": round(float((v > 1).mean()), 3)})


if __name__ == "__main__":
    timecourse()
    contrast_frag()
    focus_hist()
    frag_by_class()
    ncomp_hist()
    print("Theme 1 chart data done.")
