"""
build_site.py - regenerate the GitHub Pages site (landing + theme pages) in the author's
portfolio design language. Run from analysis/:  python build_site.py

Content is held as block specs per theme (faithful to the curated markdown readers and to the
source notebooks). Figures are referenced as-is from each theme's figures/ folder; nothing is
re-run or restyled. Themes without a spec yet are shown as 'pending' on the landing.
"""
from pathlib import Path
import report_utils as ru

ROOT = Path(__file__).resolve().parent
F = "figures/"  # theme-local figure dir

# RQ-tab style cross-nav shown on every built theme page
NAV = [
    dict(tag="Theme 01", name="Image EDA", href="01_image_intensity_eda/index.html"),
    dict(tag="Theme 02", name="Segmentation", href="02_segmentation/index.html"),
    dict(tag="Theme 03", name="Sim library", href="03_simulation_library/index.html"),
    dict(tag="Theme 04", name="Identifiability", href="04_separability_identifiability/index.html"),
    dict(tag="Theme 05", name="Drug / real data", href="05_drug_realdata/index.html"),
]
def nav_for(active_idx):
    out = []
    for i, n in enumerate(NAV):
        d = dict(n); d["active"] = (i == active_idx); out.append(d)
    return out


# ============================ THEME 1 - IMAGE & INTENSITY EDA ============================
import json as _json
_D = ROOT / "assets/data"
def _load(name): return _json.loads((_D / name).read_text())

GOLD = "#c8a05c"; GOLD_2 = "#a37432"; GOLD_3 = "#e7c98a"
CLL = "../assets/cll/figures/"   # on-brand dark figures, from a theme page (rel ../)
FIG1 = "../assets/cll/figures/01_image_eda/"   # on-brand white-bg thesis figures (multiply-blended)

_tc = _load("theme1_timecourse.json")
_TC_ORDER = ["total_area", "equivalent_diameter", "circularity", "solidity", "perimeter", "eccentricity"]
_drug_short = {"E4: PD098060 100 uM": "PD098060",
               "F3: trametinib 50 uM": "trametinib (high)",
               "F6: trametinib 1 uM": "trametinib (low)"}
_tc_chart = dict(features=_tc["features"], nice=_tc["labels"], order=_TC_ORDER,
                 series=[dict(key=k, label=_drug_short.get(k, k)) for k in _tc["series"]])
_cf = _load("theme1_contrast_frag.json")
_fc = _load("theme1_frag_class.json")
_fo = _load("theme1_focus.json")
_nc = _load("theme1_ncomp.json")

THEME1 = [
    dict(type="hero",
         meta=["Theme 01", "Data exploratory analysis", "Appendix A.1"],
         title='What the <span class="gold">data</span> <span class="it">demands</span>.',
         caption="Patient-derived CLL spheroid &middot; brightfield &middot; AI-drawn outline",
         lede="The imaging reads size and gross shape robustly, but contrast, focus and "
              "fragmentation limit the finer boundary features, the same loss that later caps "
              "CPM-parameter identifiability.",
         summary="Brightfield microscopy of patient-derived CLL spheroids is low-contrast, "
                 "unevenly lit, and frequently fragmented under drug treatment. This analysis "
                 "characterises what the images **are** (intensity, contrast, focus, illumination "
                 "and fragmentation) and what the dataset **contains**, then traces each property "
                 "to the segmentation, metric and feature choice it drove downstream."),
    dict(type="kpis", items=[
        dict(lbl="Raw frames", num="99k", desc="Local archive; 12,485 in the real inference set.", numeric=True),
        dict(lbl="Hand-annotated", num="51", desc="About 0.05% of the corpus, the defining constraint.", gold=True, numeric=True),
        dict(lbl="Contrast covered by aug.", num="~100%", desc="Focus ~91%; validates the heavy-aug U-Net.", gold=True),
        dict(lbl="Real wells out-of-library", num="~90%", desc="Why the thesis reports relative shifts, not absolutes.", numeric=True),
    ]),

    dict(type="section", title='A. What is the <span class="it">dataset</span>?',
         right="cohort & the defining constraint"),
    dict(type="chart", id="t1_corpus", fn="barH",
         title="Corpus scale and label scarcity", sub="hover for counts",
         data=dict(labels=["Raw archive", "Inference set", "Pseudo-labels", "Augmented train",
                           "Ground-truth", "Held-out test"],
                   datasets=[dict(label="frames", data=[99000, 12485, 4552, 306, 51, 45], color=GOLD)],
                   logx=True, xlabel="number of frames (log scale)", dec=0),
         note="Only 51 of roughly 99,000 frames are hand-annotated (about 0.05%), expanded to 306 "
              "by augmentation. The held-out test set is 45 frames.",
         informs="A 1-in-1000 label ratio motivates the two-stage training strategy: pretrain on "
                 "classical pseudo-labels, then fine-tune on the 51 ground-truth masks.",
         informs_tag="Decision: two-stage training"),
    dict(type="figure", img=CLL + "what_we_do_strip.png",
         ttl="What the pipeline does, end to end", sub="raw frame to outline to shape numbers",
         alt="raw microscopy, AI segmentation outline, extracted shape numbers",
         shows="A microscopy frame goes in, the AI draws the spheroid outline, and a handful of "
               "shape numbers come out. Those numbers are the observables every later stage consumes.",
         informs="Fixes the unit of analysis: the segmenter is judged on whether these shape numbers "
                 "are trustworthy, not on raw pixel overlap.",
         informs_tag="Frames the whole pipeline"),
    dict(type="figure", img=FIG1 + "fig01_dataset_composition.png", native=True,
         ttl="Dataset composition", sub="annotated split &middot; real set by class &middot; sampling depth",
         alt="stacked bars of labelled images by split, real frames by treatment class, and timepoints per well",
         shows="The 51 ground-truth frames expand to about 255 augmented pairs across the "
               "train/val/test split; the ~12k-frame inference corpus is dominated by "
               "CXCR4-antagonist and control wells, each sampled at a median of 20 timepoints over "
               "roughly 5.5 days.",
         informs="The label scarcity and the class imbalance together drive the plate-stratified "
                 "split and the two-stage training that pretrains on pseudo-labels before fine-tuning "
                 "on the 51 masks.",
         informs_tag="Cohort & the defining constraint"),
    dict(type="figure", img=FIG1 + "fig06_augmentation_coverage.png", native=True,
         ttl="Does augmentation cover the real regimes?", sub="real vs augmented vs 51 originals",
         alt="contrast, mean-intensity and focus distributions for real, augmented and original frames",
         shows="Augmentation spans 100% of the real contrast range and 91% of the focus "
               "(Laplacian-variance) range, but only 18% of the mean-intensity range; brightness "
               "is the axis it covers least.",
         informs="Confirms the heavy-augmentation U-Net is trained across the contrast and focus "
                 "regimes it will meet at inference; the intensity gap is the one residual exposure.",
         informs_tag="Validates heavy augmentation"),

    dict(type="section", title='B. What does the raw <span class="it">signal</span> look like?',
         right="why a learned segmenter, not thresholding"),
    dict(type="chart", id="t1_contrast", fn="scatter",
         title="Contrast vs fragment count", sub="51 annotated frames",
         data=dict(points=_cf["points"], xlabel="Michelson contrast", ylabel="fragments per image"),
         note="Contrast spans roughly 0.46 to 1.0 across the annotated set, and higher contrast "
              "couples to more fragments, because separating fragments exposes bright background "
              "between dark material.",
         informs="The wide, regime-dependent contrast (and the fragment-debris intensity overlap it "
                 "creates) is why a single global threshold cannot work and a learned segmenter is "
                 "needed, with contrast-conditional preprocessing in the classical baseline.",
         informs_tag="Decision: learned segmenter + contrast-conditional preprocessing"),
    dict(type="chart", id="t1_focus", fn="barV",
         title="Focus spread across frames", sub="Laplacian variance, log scale",
         data=dict(labels=[f"{c:.1f}" for c in _fo["centers"]],
                   datasets=[dict(label="frames", data=_fo["counts"], color=GOLD_2)],
                   xlabel="log10 Laplacian variance (sharper to the right)", ylabel="frames", dec=0),
         note=f"Brightfield focus spans about {_fo['span_decades']} orders of magnitude, and "
              "background illumination is uneven.",
         informs="Both inject noise into boundary-derived shape features, the exact "
                 "perimeter and circularity features the CPM inference relies on, so inversion is "
                 "restricted to features that survive segmentation noise.",
         informs_tag="Decision: restrict inversion features"),
    dict(type="figure", img=FIG1 + "fig02_intensity_dynamic_range.png", native=True,
         ttl="Intensity and dynamic range", sub="pooled pixels &middot; frame brightness &middot; 8-bit usage",
         alt="pooled pixel-intensity histogram, per-frame brightness, dynamic-range usage and black/white points",
         shows="Pooled pixel intensity is bimodal (a dark spheroid on a bright field); per-frame "
               "brightness clusters near mid-range, and frames use a median of 86% of the available "
               "8-bit range.",
         informs="The two intensity modes overlap once debris is present, so a single global "
                 "threshold cannot separate object from background, so a learned segmenter is needed.",
         informs_tag="Decision: learned segmenter"),
    dict(type="figure", img=FIG1 + "fig03_contrast.png", native=True,
         ttl="Contrast: level, polarity, drift, batch", sub="Michelson contrast across the corpus",
         alt="contrast histogram, polarity, contrast drift over time and batch variation",
         shows="Michelson contrast centres near 0.55 with only 0.6% of frames inverted (dark-on-light "
               "dominates), climbs over the time course (about 0.55 to 0.71), and varies between "
               "experiment batches.",
         informs="Contrast is wide, regime-dependent and drifting, which is why the classical "
                 "baseline needs contrast-conditional preprocessing and the production segmenter is "
                 "learned.",
         informs_tag="Decision: contrast-conditional preprocessing"),
    dict(type="figure", img=FIG1 + "fig04a_sharpness.png", native=True,
         ttl="Focus is bimodal and metric-agnostic", sub="Laplacian variance, log scale",
         alt="focus-measure histogram, agreement between two focus metrics, sharpness over time",
         shows="Focus splits into a sharp main cluster and a blurred tail on a log scale, and two "
               "independent focus measures (Laplacian variance and Tenengrad) agree, so the spread is "
               "real, not an artefact of one metric.",
         informs="Out-of-focus frames blur the boundary-derived perimeter and circularity features, "
                 "reinforcing the restriction of inversion to features that survive segmentation noise.",
         informs_tag="Decision: restrict inversion features"),
    dict(type="figure", img=FIG1 + "fig05_illumination.png", native=True,
         ttl="Illumination is uneven and worsens over time", sub="background coefficient of variation",
         alt="background-CV histogram, illumination drift over time, and an uneven-illumination exemplar",
         shows="Background illumination is uneven (CV about 0.2 to 0.25) and grows worse over the "
               "time course; the exemplar shows the shading and debris across the field (the dark "
               "disc at the centre is the spheroid itself).",
         informs="Uneven background biases any intensity-based boundary, another reason the inversion "
                 "leans on shape features that tolerate illumination drift.",
         informs_tag="Decision: restrict inversion features"),

    dict(type="section", title='C. What is the object <span class="it">structure</span>?',
         right="the segmentation criterion: feature preservation"),
    dict(type="chart", id="t1_ncomp", fn="barV", height=340,
         title="Components per annotated image", sub="how multi-object the masks are",
         data=dict(labels=_nc["labels"],
                   datasets=[dict(label="images", data=_nc["counts"], color="#a37432")],
                   xlabel="connected components in the image", ylabel="images", dec=0),
         note=f"Most frames are not a single object (median {_nc['median']} components; about "
              f"{int(_nc['multi_frac']*100)}% have more than one), and fragment sizes span four "
              "orders of magnitude, from the main body down to specks below 100 px.",
         informs="Standard Dice is dominated by the largest component and is blind to small "
                 "fragments, so CC-Dice (equal weight per component) is the right metric, and "
                 "post-processing keeps the largest connected component.",
         informs_tag="Decision: CC-Dice + largest component"),
    dict(type="figure", img=FIG1 + "fig07_fragmentation_structure.png", native=True,
         ttl="Fragment structure of the masks", sub="counts &middot; area concentration &middot; over time",
         alt="fragment-count histogram, largest-component area fraction, GT-vs-model components, disintegration over time",
         shows="Only about 20% of frames are a single cohesive object; most carry a long tail of "
               "fragments while the largest component still holds nearly all the area, and "
               "disintegration increases over the time course.",
         informs="Because masks are multi-object but area-dominated, ordinary Dice would ignore the "
                 "small fragments, so CC-Dice scores every component, and post-processing keeps the "
                 "largest one.",
         informs_tag="Decision: CC-Dice + largest component"),

    dict(type="section", title='D. Fragmentation vs <span class="it">treatment</span>',
         right="biology preview, associative"),
    dict(type="chart", id="t1_frag", fn="barH",
         title="Fragmentation by drug-mechanism class", sub="median fragmentation index, classes with n>=30",
         data=dict(labels=_fc["labels"],
                   datasets=[dict(label="median fragmentation index", data=_fc["median"], color="#c8a05c")],
                   xlabel="median fragmentation index", dec=3),
         note="Syk-inhibitor and CXCR4-antagonist wells are the most fragmented; BTK, NF-kB and "
              "MALT1 inhibitors sit lowest. Counts are large and unequal and metadata are "
              "plate-level, so this is read as an association.",
         informs="Previews the RQ3 drug-response story (drug class changes cohesion), and shows the "
                 "most drug-responsive classes are hardest to segment, so feature preservation is the "
                 "right criterion.",
         informs_tag="Preview: RQ3 mechanism, associative only"),
    dict(type="figure", img=FIG1 + "fig08_fragmentation_vs_treatment.png", native=True,
         ttl="Which mechanism classes fragment most", sub="by class &middot; effect vs control &middot; trajectory",
         alt="fragmentation by mechanism class, effect size vs control, and disintegration trajectory over time",
         shows="Syk-inhibitor and CXCR4-antagonist wells fragment most relative to control and the "
               "gap widens over the time course; per-class differences are significant but, with "
               "plate-level metadata, are read as associations.",
         informs="The most drug-responsive classes are also the hardest to segment cleanly, which is "
                 "exactly why the segmenter is chosen on feature preservation rather than pixel "
                 "overlap.",
         informs_tag="Preview: RQ3 mechanism, associative only"),

    dict(type="section", title='E. Drug response, measured <span class="it">automatically</span>',
         right="the payoff: morphology to mechanism"),
    dict(type="chart", id="t1_timecourse", fn="timecourse", height=440,
         title="Drug response measured automatically from the AI segmenter",
         sub="three drug conditions, every available timepoint",
         toggle=[(f, _tc["labels"][f]) for f in _TC_ORDER],
         data=_tc_chart,
         note="High-dose trametinib collapses the cluster; PD098060 compacts it; low-dose "
              "trametinib leaves it intact. Every point is extracted from an AI-segmented frame, "
              "with no manual measurement.",
         informs="This is the observable the inference consumes: a per-condition shape trajectory "
                 "that the CPM matcher compares against the synthetic library.",
         informs_tag="Feeds RQ2 / RQ3 inference"),

    dict(type="section", title='F. From image quality to library <span class="it">coverage</span>',
         right="why the thesis reports relative shifts"),
    dict(type="figure", img=FIG1 + "fig09_quality_coverage_link.png", native=True,
         ttl="Image quality predicts distance from the library", sub="real to nearest-synthetic distance",
         alt="real-to-synthetic NN distance against fragmentation, contrast and focus",
         shows="How far a real well sits from its nearest synthetic spheroid grows with fragmentation "
               "(r=0.30) and focus (r=0.43) but not with contrast (r=0.05): the qualities hardest to "
               "segment are also the least covered by the simulation library.",
         informs="This is the mechanism behind the ~90% of real wells that fall outside the synthetic "
                 "library, and the reason the inference is reported as relative shifts rather than "
                 "absolute parameter values.",
         informs_tag="Why relative shifts, not absolutes"),

    dict(type="prose", title="Sources (canonical, executable)",
         text="This reader consolidates and re-orders the data EDA into the thesis's decision "
              "order. Interactive charts are computed from the same local CSVs the notebooks use "
              "(`imaging_eda/cache/labelled_qc.csv`, `frame_qc.csv`, "
              "`rq1_segmentation/results/feature_validation/timecourse_full_features.csv`); raster "
              "panels are the on-brand figures from the thesis figure set. Open the source "
              "notebooks for the full code and every panel:\n\n"
              "**`thesis_submission/notebooks/RQ1_segmentation/01_data_eda.ipynb`** and "
              "**`imaging_eda/imaging_data_eda.ipynb`**.\n\n"
              "An earlier broad notebook, `data/cll_spheroid_eda_complete.ipynb`, is catalogued as "
              "a referenced orphan in `_provenance_notes.md`."),
    dict(type="section", title='Set your own <span class="it">quality bar</span>',
         right="interactive, beyond the thesis"),
    dict(type="interactive", widget="qcthreshold", json="theme1_qc_threshold.json",
         intro="The thesis fixes quality thresholds once. Here you pick a quality metric and drag the "
               "bar to see exactly how many of the 12,480 frames survive.",
         informs="Turns the fixed QC cutoffs into something you can interrogate across the whole corpus.",
         informs_tag="Beyond the thesis: live QC"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 01', chips=[
        dict(t="01_data_eda.ipynb", gold=True), dict(t="imaging_data_eda.ipynb", gold=True),
        dict(t="labelled_qc.csv"), dict(t="frame_qc.csv"), dict(t="timecourse_full_features.csv"),
        dict(t="Chart.js + scikit-image")]),
    dict(type="bigcta", title='Next: <span class="it">choosing the segmenter</span>.',
         links=[dict(t="Theme 02 &middot; Segmentation &rarr;", href="02_segmentation/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]



# ============================ THEME 2 - SEGMENTATION & FEATURE PRESERVATION ==============
_CD = ROOT / "assets/cll/data"
def _loadc(name): return _json.loads((_CD / name).read_text())

CLL2 = "../assets/cll/figures/"
MUTED = "#a8b5b8"

# leaderboard: 8 models, real values (dice / CC-Dice / shape-number agreement CCC)
_LB = dict(
    metrics=[dict(key="ccc", label="Shape-number agreement (CCC)", min=0, max=1.0, mid=0.5),
             dict(key="dice", label="Pixel overlap (Dice)", min=0.7, max=0.85, mid=0.79),
             dict(key="cc_dice", label="Component-aware overlap (CC-Dice)", min=0, max=0.25, mid=0.15)],
    models=[
        dict(label="U-Net (heavy aug.)", dice=0.829, cc_dice=0.18, ccc=0.683, winner=True),
        dict(label="Pseudo-label + fine-tune", dice=0.811, cc_dice=0.157, ccc=0.464),
        dict(label="SAM2 (grayscale)", dice=0.787, cc_dice=0.116, ccc=0.473),
        dict(label="SAM2 (multi-channel)", dice=0.768, cc_dice=0.081, ccc=0.434),
        dict(label="Rule-based baseline", dice=0.760, cc_dice=0.040, ccc=0.378),
        dict(label="nnU-Net (default)", dice=0.757, cc_dice=0.172, ccc=0.305),
        dict(label="nnU-Net + cleanup", dice=0.799, cc_dice=0.204, ccc=0.285),
        dict(label="nnU-Net (multi-channel)", dice=0.755, cc_dice=0.167, ccc=0.270),
    ])

_pp = _loadc("seg_postproc.json")["best"]
_pp_labels = list(_pp.keys())
# include the chosen heavy-aug U-Net (0.829, no cleanup applicable: its masks need none)
_pp_names = ["U-Net (heavy aug.)"] + [k.replace("_", " ") for k in _pp_labels]
_pp_none = [0.829] + [_pp[k]["dice_none"] for k in _pp_labels]
_pp_best = [0.829] + [_pp[k]["mean_dice"] for k in _pp_labels]
_PP = dict(labels=_pp_names,
           datasets=[dict(label="without cleanup", data=_pp_none, color=MUTED),
                     dict(label="with best cleanup", data=_pp_best, color="#c8a05c")],
           ylabel="pixel Dice", min=0.7, max=0.85, dec=2)

_f3 = _loadc("seg_f3.json")["top"][:10]
_F3 = dict(labels=[f'{t["preproc"]} / {t["seg"]}' for t in _f3],
           datasets=[dict(label="Dice on F3", data=[t["dice"] for t in _f3], color="#a37432")],
           xlabel="Dice on the hardest frame", min=0, max=0.5, dec=2)

THEME2 = [
    dict(type="hero", bg="assets/hero_spheroid_overlay.png",
         meta=["Theme 02", "Segmentation & feature preservation", "Appendix B"],
         title='Eight <span class="gold">candidates</span>, one <span class="it">winner</span>.',
         caption="VID3201 F3 &middot; U-Net (heavy aug.) outline in cherry",
         lede="Pixel overlap cannot tell the candidates apart. The metric that matters for the "
              "downstream pipeline can, and it exposes a structural failure mode in three of them.",
         summary="Eight segmenters were compared on the same 45-image test set: a rule-based "
                 "baseline, three nnU-Net variants, two SAM2 variants, a heavy-augmentation U-Net, "
                 "and a pseudo-label pretrain. The winner is chosen on the metric the next stage "
                 "consumes: **do the AI-derived shape numbers agree with the human-annotated ones?** "
                 "By that measure the heavy-augmentation U-Net wins by a wide margin, even though "
                 "three models edge it on pixel overlap."),
    dict(type="kpis", items=[
        dict(lbl="Chosen model", num="U-Net", desc="Heavy augmentation; only model crossing the reliability bar.", gold=True),
        dict(lbl="Models compared", num="8", desc="All on the same 45-image test set.", numeric=True),
        dict(lbl="Best pixel Dice", num="0.829", desc="U-Net; nnU-Net essentially tied at 0.831.", gold=True, numeric=True),
        dict(lbl="Reliability bar", num="&ge; 0.85", desc="Concordance threshold from the radiomics standard (IBSI).", numeric=True),
    ]),

    dict(type="figure", img="fig/overlay_dark.png",
         ttl="What the chosen segmenter produces", sub="real frames, three drug conditions, three days",
         alt="real microscopy with the AI segmentation outline in gold",
         shows="The gold outline is the U-Net's call on frames it never saw in training; the boxes "
               "show the shape numbers (area, circularity, solidity) extracted from each.",
         informs="The unit of evaluation is these extracted numbers, not the pixel mask.",
         informs_tag="Why feature preservation, not pixels"),

    dict(type="section", title='Model <span class="it">leaderboard</span>', right="switch the metric"),
    dict(type="chart", id="t2_lb", fn="lbboard", height=420,
         title="Ranking flips with the metric", sub="click to switch",
         toggle=[("ccc", "Shape-number agreement"), ("dice", "Pixel overlap"), ("cc_dice", "Component-aware")],
         data=_LB,
         note="Pixel overlap is nearly flat (0.755 to 0.829) and picks the U-Net by a hair. "
              "Shape-number agreement ranks the U-Net first by a wide margin and is the only metric "
              "that reflects what the next stage consumes.",
         informs="The segmenter is selected on shape-number agreement (Lin's CCC against the six CPM "
                 "features), not pixel Dice. The heavy-aug U-Net is the only model above the 0.85 bar.",
         informs_tag="Decision: rank by feature preservation"),

    dict(type="figure", img=CLL2 + "segmentation/icc_ccc_heatmap.png",
         ttl="Per-feature reliability scoreboard", sub="8 models x 6 shape numbers",
         alt="heatmap of agreement scores across models and features",
         shows="Each cell is the agreement between AI-derived and human-derived value of one shape "
               "number. Gold-outlined cells cross the 0.85 bar. Only the U-Net crosses, on area and "
               "diameter; roundness and elongation are unreliable for almost every model.",
         informs="Sets the operational feature set for RQ3: area, diameter, solidity, perimeter, "
                 "circularity; eccentricity is dropped, perimeter is U-Net-only.",
         informs_tag="Decision: operational feature set"),

    dict(type="section", title='Cleanup <span class="it">impact</span>',
         right="overlap recovers, agreement does not"),
    dict(type="chart", id="t2_pp", fn="barV", height=360,
         title="Pixel overlap with vs without cleanup", sub="a small post-processing step",
         data=_PP,
         note="The chosen U-Net (heavy aug.) is shown for reference: its masks need no cleanup, so "
              "the two bars are identical at 0.829. A morphological cleanup lifts nnU-Net pixel "
              "overlap by up to +0.044; the rule-based baseline barely benefits because its masks "
              "are already sparse.",
         informs="On the metric that matters for the next stage this cleanup does not move the "
                 "needle: it rescues pixel overlap, not shape-number reliability.",
         informs_tag="Negative result: cleanup is cosmetic for feature preservation"),

    dict(type="section", title='Hardest <span class="it">case</span>', right="a fully fragmented spheroid"),
    dict(type="figure", img="fig/hardest_dark.png",
         ttl="When the spheroid disintegrates", sub="VID3201 F3, trametinib 50 uM, full time-lapse",
         alt="a heavily fragmented spheroid time-lapse, day 0 to day 4",
         shows="Under high-dose drug the spheroid breaks into many pieces. Pixel overlap drops for "
               "every model; area and diameter stay reliable while roundness and elongation collapse.",
         informs="This split is the entire reason the audit was needed, and why F3 is reported "
                 "separately rather than excluded.",
         informs_tag="Validates the feature-preservation audit"),
    dict(type="chart", id="t2_f3", fn="barH", height=360,
         title="Classical pipeline on the hardest frame", sub="top 10 of the classical preproc / segmenter sweep",
         data=_F3,
         note="This is the classical-pipeline sweep (the deep models, including the heavy-aug "
              "U-Net, are in the showcase above). Even the best classical combination reaches only "
              "about 0.45 Dice on this frame; no configuration rescues it.",
         informs="Confirms F3 is a genuine ceiling, not a tuning artefact.",
         informs_tag="Bounds the hardest case"),

    dict(type="section", title='Explore the <span class="it">leaderboard</span>',
         right="pixel overlap vs feature preservation"),
    dict(type="interactive", widget="modelscatter", json="theme2_model_explorer.json",
         intro="Every segmenter plotted by pixel overlap (Dice) against shape-number agreement (CCC). "
               "Click one to see its per-feature reliability and why the ranking flips.",
         informs="Makes the central finding tangible: the best-overlap model is not the most "
                 "trustworthy for shape numbers.",
         informs_tag="Beyond the thesis: navigable leaderboard"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 02', chips=[
        dict(t="05_feature_validation.ipynb", gold=True), dict(t="ICC(3,1) + Lin's CCC"),
        dict(t="per_feature_error.csv"), dict(t="seg_postproc.json"), dict(t="seg_f3.json"),
        dict(t="U-Net / SAM2 / nnU-Net")]),
    dict(type="bigcta", title='Next: the <span class="it">synthetic library</span>.',
         links=[dict(t="Theme 03 &middot; Simulation library &rarr;", href="03_simulation_library/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]

# ===================== THEMES 3, 4, 5 ============================================
CLLF = "../assets/cll/figures/"
MUT = "rgba(168,181,184,0.55)"

# ---- Theme 3 data: CPM parameter sweeps (how each knob changes cluster size) ----
_sw = _loadc("cpm_sweeps.json")
_SW_ORDER = ["width", "contact", "contact_no", "neighbor", "lambda", "temp"]
_sw_nice = {"width": "target volume (width)", "contact": "cell-cell adhesion",
            "contact_no": "contact range", "neighbor": "neighbour order",
            "lambda": "volume elasticity", "temp": "motility (temperature)"}
_SWEEP = dict(order=_SW_ORDER, nice=_sw_nice,
              levels={k: _sw[k]["levels"] for k in _SW_ORDER},
              area={k: _sw[k]["features"]["total_area"] for k in _SW_ORDER})

# ---- Theme 4 data: verified leave-one-out R2 (canonical identifiability_loo.csv) ----
_R2 = [("target volume (width)", 0.635), ("cell-medium adhesion (J_cm)", 0.615),
       ("cell-cell adhesion (J_cc)", 0.344), ("contact range", 0.167),
       ("motility (temperature)", 0.164), ("volume elasticity (lambda)", 0.126),
       ("neighbour order", -0.069)]
_R2_COL = [("#c8a05c" if v >= 0.30 else MUT) for _, v in _R2]
_DISC = sorted(_loadc("cpm_discriminability.json"), key=lambda x: -x["snr"])

THEME3 = [
    dict(type="hero",
         meta=["Theme 03", "Synthetic CPM library", "Appendix C & F"],
         title='The <span class="gold">simulator</span>, <span class="it">characterised</span>.',
         caption="Cellular Potts Model spheroid, synthetic lattice",
         lede="Seven simulation knobs, swept one at a time and jointly, build the synthetic "
              "library the real spheroids are matched against.",
         summary="A Cellular Potts Model with seven parameters (cell-cell and cell-medium adhesion, "
                 "contact range, neighbour order, volume elasticity, target volume, and motility) is "
                 "sampled to build a reference library of morphology trajectories. This theme shows "
                 "how each knob changes the simulated cluster, and accounts for which runs were "
                 "usable."),
    dict(type="kpis", items=[
        dict(lbl="CPM parameters", num="7", desc="Swept one-at-a-time and jointly (Saltelli).", numeric=True),
        dict(lbl="Sampled vectors", num="1,152", desc="Saltelli design over the 7 parameters.", numeric=True),
        dict(lbl="Usable runs", num="1,105", desc="After dropping degenerate masks.", gold=True, numeric=True),
        dict(lbl="Dropped", num="47", desc="Empty or single-pixel masks, removed.", numeric=True),
    ]),
    dict(type="section", title='How each <span class="it">knob</span> changes morphology',
         right="one-at-a-time sweeps"),
    dict(type="chart", id="t3_sweep", fn="sweepline", height=400,
         title="Cluster area vs parameter level", sub="switch the parameter",
         toggle=[(k, _sw_nice[k]) for k in _SW_ORDER], data=_SWEEP,
         note="Target volume (width) and cell-cell adhesion move cluster area the most; neighbour "
              "order and motility barely move it on their own.",
         informs="Identifies which knobs leave a size signature in morphology, the precondition "
                 "for being identifiable later.",
         informs_tag="Sets up the identifiability question"),
    dict(type="section", title='Tune it yourself: <span class="it">knob to spheroid</span>',
         right="live morph, beyond the thesis"),
    dict(type="interactive", widget="morph", json="theme3_morph.json",
         intro="The thesis only shows static sweep curves. Here you grab a knob (target volume or "
               "cell-cell adhesion J_cc) and watch a real rendered spheroid grow or compact while its "
               "cluster-area curve tracks the move.",
         informs="Binds the rendered CPM lattice to the swept parameter, so size and shape respond as "
                 "you drag, not just a line plot.",
         informs_tag="Beyond the thesis: live morph"),
    dict(type="section", title='What the <span class="it">library</span> looks like',
         right="16 random samples at the final step"),
    dict(type="figure", img="fig/saltelli_gallery.png",
         ttl="Sixteen synthetic spheroids from the simulation library", sub="final MCS, one replicate",
         alt="gallery of 16 simulated CPM spheroids spanning the parameter space",
         shows="Each panel is one sampled parameter vector rendered at the final simulation step, "
               "with cells coloured individually. The samples span compact, loosely packed, and "
               "fully dispersed morphologies.",
         informs="Confirms visually that the sampled parameter space produces a wide morphological "
                 "range, the diversity the inversion relies on.",
         informs_tag="Shows the library's morphological spread"),
    dict(type="section", title='Walk the <span class="it">morphospace</span>',
         right="1,105 samples, click any one"),
    dict(type="interactive", widget="morphospace", json="theme3_morphospace.json",
         intro="Every dot is one of 1,105 synthetic spheroids. Click one to read the exact seven CPM "
               "parameters that produced it and the morphology that resulted. Swap the axes, recolour "
               "by any knob, or highlight the morphological extremes.",
         informs="Turns the library from a 16-panel gallery into a navigable map, where any point "
                 "reveals its generating parameters and shape.",
         informs_tag="Beyond the thesis: navigable library"),
    dict(type="section", title='Which knobs <span class="it">drive</span> cluster size?',
         right="Sobol indices, direct vs total effect"),
    dict(type="figure", img=CLLF + "cpm/sobol_S1_vs_ST.png",
         ttl="Sobol first-order vs total effect", sub="share of variance in cluster area",
         alt="Sobol S1 and ST bars per parameter",
         shows="Direct effect (S1) is how much a knob alone moves area; total effect (ST) adds its "
               "interactions with the other knobs. A large gap means the knob acts mostly through those interactions.",
         informs="Target volume dominates; cell-cell and cell-medium adhesion carry sizeable "
                 "interaction effects. These interactions limit how cleanly a single knob can be "
                 "read back from morphology.",
         informs_tag="Interactions bound identifiability"),
    dict(type="section", title='The <span class="it">surrogate</span>, opened up',
         right="XGBoost, cross-validated"),
    dict(type="interactive", widget="surrogate", json="theme3_surrogate.json",
         intro="A gradient-boosted surrogate predicts each shape feature from the seven knobs. Toggle "
               "between how well it predicts (per-feature cross-validated R-squared, click a bar for "
               "the five folds) and what drives each feature (Sobol direct, total, and interaction gap).",
         informs="Circularity is near-perfectly predictable while eccentricity is the weak link; the "
                 "direct-versus-total toggle makes interaction effects something you can manipulate.",
         informs_tag="Beyond the thesis: interactive sensitivity"),
    dict(type="section", title='Does the simulator <span class="it">cover reality</span>?',
         right="real wells vs the synthetic world"),
    dict(type="interactive", widget="coverage", json="theme3_coverage.json",
         intro="The synthetic library (grey) and the 152 real spheroid wells (control, stimulated and "
               "drug; coloured) projected into "
               "the same PCA morphospace. Drag the threshold to see how many real wells fall outside "
               "the simulated world.",
         informs="Most real spheroids sit on the rim or outside the synthetic cloud, the reason the "
                 "thesis reports relative shifts rather than absolute parameters.",
         informs_tag="Beyond the thesis: live coverage"),
    dict(type="chart", id="t3_yield", fn="barH", height=240,
         title="Library yield", sub="sampled to usable",
         data=dict(labels=["Sampled (Saltelli)", "Usable", "Dropped (degenerate)"],
                   datasets=[dict(label="runs", data=[1152, 1105, 47],
                                  color=["#a8b5b8", "#c8a05c", "#c44a30"])],
                   xlabel="number of runs", dec=0),
         note="Of 1,152 sampled parameter vectors, 1,105 produced usable masks; 47 were dropped as "
              "empty or single-pixel (degenerate) spheroids.",
         informs="The usable 1,105-run library is the single reference set for all matching and "
                 "identifiability analysis.",
         informs_tag="Defines the reference library"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 03', chips=[
        dict(t="cpm_sweeps.json", gold=True), dict(t="CompuCell3D"), dict(t="Saltelli design"),
        dict(t="VTK feature extraction"), dict(t="1,105-run library")]),
    dict(type="bigcta", title='Next: which knobs are <span class="it">identifiable</span>?',
         links=[dict(t="Theme 04 &middot; Identifiability &rarr;", href="04_separability_identifiability/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]

THEME4 = [
    dict(type="hero",
         meta=["Theme 04", "Separability & identifiability", "Appendix D to H"],
         title='Which knobs can we <span class="it">read back</span>?',
         caption="Leave-one-out inversion on the 1,105-run library",
         lede="None of the seven parameters reach the identifiable band. Three are weakly identifiable "
              "and the other four are non-identifiable, and the analysis says so honestly.",
         summary="Leave-one-out inversion on the 1,105-run library measures how well each CPM "
                 "parameter is recovered from morphology (R squared of recovered vs true). Cell-medium "
                 "width, cell-medium adhesion and cell-cell adhesion are weakly identifiable; the other four are non-identifiable. "
                 "These are the verified numbers from the recovery benchmark, not the optimistic "
                 "error metric used elsewhere."),
    dict(type="kpis", items=[
        dict(lbl="Weakly identifiable", num="3 of 7", desc="width, J_cm, J_cc clear the R2 0.30 weak bar; none reach identifiable.", gold=True),
        dict(lbl="Best recovery", num="0.64", desc="Cell width, LOO R2 (weakly identifiable).", gold=True, numeric=True),
        dict(lbl="Library size", num="1,105", desc="Saltelli runs used for the benchmark.", numeric=True),
        dict(lbl="Non-identifiable", num="4", desc="lambda, temperature, contact range, neighbour order.", numeric=True),
    ]),
    dict(type="section", title='How well each parameter is <span class="it">recovered</span>',
         right="leave-one-out R squared, verified"),
    dict(type="chart", id="t4_r2", fn="barH", height=360,
         title="Leave-one-out recovery (R squared)", sub="gold = weakly identifiable (R2 >= 0.30)",
         data=dict(labels=[n for n, _ in _R2],
                   datasets=[dict(label="LOO R2", data=[v for _, v in _R2], color=_R2_COL)],
                   xlabel="R squared (recovered vs true)", min=-0.1, max=0.8, dec=2),
         note="Cell width (0.64), cell-medium adhesion (0.61) and cell-cell adhesion (0.34) are the "
              "three weakly identifiable parameters; volume elasticity, temperature, contact range and "
              "neighbour order are non-identifiable. Neighbour order is effectively zero.",
         informs="The pipeline reports estimates and uncertainty only for the three weakly identifiable "
                 "axes, and reports the rest as non-identifiable rather than guessing.",
         informs_tag="Decision: report only the weakly identifiable axes"),
    dict(type="section", title='Why some features <span class="it">separate</span> better',
         right="signal-to-noise per feature"),
    dict(type="chart", id="t4_snr", fn="barH", height=320,
         title="Discriminability by morphology feature", sub="signal-to-noise ratio",
         data=dict(labels=[d["feature"].replace("_", " ") for d in _DISC],
                   datasets=[dict(label="SNR", data=[round(d["snr"], 2) for d in _DISC], color="#c8a05c")],
                   xlabel="signal-to-noise ratio", dec=2),
         note="Area and diameter carry the strongest signal across the parameter sweeps; circularity "
              "and perimeter are the noisiest, which matches their lower feature preservation.",
         informs="Size features anchor the inversion; shape features add little once size is fixed, "
                 "consistent with the segmentation audit in Theme 02.",
         informs_tag="Connects back to feature preservation"),
    dict(type="section", title='Which knobs are <span class="it">identifiable</span>?',
         right="leave-one-out recovery"),
    dict(type="interactive", widget="idbars", json="theme4_identifiability.json",
         intro="Per-parameter recovery R-squared from the inversion benchmark, under the tau-registered "
               "matcher (primary) or the end-state matcher (secondary). The dashed line is the "
               "identifiable bar at R-squared 0.70; click a bar for its Pearson correlation, sample "
               "count and error.",
         informs="No parameter reaches the 0.70 identifiable bar: cell-medium adhesion, target volume "
                 "and contact are only weakly identifiable, and the rest are non-identifiable. This is "
                 "the spine of RQ2.",
         informs_tag="Beyond the thesis: interactive identifiability"),
    dict(type="section", title='Feature to parameter <span class="it">sensitivity</span>',
         right="surrogate Sobol total-effect weights"),
    dict(type="interactive", widget="heatmap", json="theme4_discriminability_heatmap.json",
         intro="How much each shape feature responds to each CPM knob, as XGBoost-surrogate Sobol "
               "total-effect weights (per-knob min-max normalised, clipped at 0.05). Brighter gold means "
               "more sensitive; click a cell to read its value. All seven knobs are shown: width and volume "
               "elasticity drive size, while contact J and cell-medium adhesion drive shape.",
         informs="Area and circularity carry most of the recoverable signal, consistent with the "
                 "identifiability ranking above.",
         informs_tag="Beyond the thesis: clickable matrix"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 04', chips=[
        dict(t="tab:rq2_1_identifiability (tau)", gold=True), dict(t="cpm_discriminability.json"),
        dict(t="leave-one-out inversion"), dict(t="XGBoost surrogate"), dict(t="tau-registration matcher")]),
    dict(type="bigcta", title='Next: the real <span class="it">drug data</span>.',
         links=[dict(t="Theme 05 &middot; Drug & real data &rarr;", href="05_drug_realdata/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]

THEME5 = [
    dict(type="hero",
         meta=["Theme 05", "Drug panel & real-data inference", "Appendix I & J"],
         title='Real spheroids, <span class="it">relative shifts</span>.',
         caption="Patient-derived spheroids under drug treatment",
         lede="The pipeline inverts real morphology to CPM parameters; the inferred shifts on the "
              "weakly identifiable axes are read as relative changes, not biophysical effects.",
         summary="Real spheroid trajectories from reference wells across seven patients and a panel of "
                 "drug conditions are inverted to CPM parameters on the three weakly identifiable axes. "
                 "The inferred shifts are read as relative, simulation-derived changes, not absolute or "
                 "biophysical values."),
    dict(type="kpis", items=[
        dict(lbl="Patients", num="7", desc="Reference wells inverted across 7 patients.", numeric=True),
        dict(lbl="Read as", num="shifts", desc="Relative change on the weakly identifiable axes, not absolutes.", gold=True),
        dict(lbl="Drug-panel BCR shift", num="weak", desc="Tau (primary): J_cc shift -1.4, CI [-3.0, +0.2], spans zero. End-state: +4.6, CI [+2.1, +7.0], significant; the signal is in the settled morphology."),
        dict(lbl="Reported axes", num="3", desc="the three weakly identifiable axes (width, J_cc, J_cm).", numeric=True),
    ]),
    dict(type="section", title='What the <span class="it">drugs</span> do to morphology',
         right="three dose conditions"),
    dict(type="figure", img=CLLF + "morphology/drug_strip_high_dose.png",
         ttl="High-dose trametinib collapses the cluster", sub="MEK inhibitor, 50 uM",
         alt="time strip of a high-dose-treated spheroid disintegrating",
         shows="The cluster loses cohesion and breaks apart over the time course.",
         informs="An end-state shift in the inferred contact parameters.",
         informs_tag="Relative shift on the contact axes"),
    dict(type="figure", img=CLLF + "morphology/drug_strip_pd098060.png",
         ttl="PD098060 compacts the cluster", sub="MEK pathway, 100 uM",
         alt="time strip of a PD098060-treated spheroid compacting",
         shows="The cluster stays cohesive but contracts, a different morphological signature from "
               "high-dose trametinib.",
         informs="Distinct drugs leave distinct, separable trajectories.",
         informs_tag="Separable drug signatures"),
    dict(type="figure", img=CLLF + "morphology/feature_trajectories.png",
         ttl="Feature trajectories under treatment", sub="extracted automatically per condition",
         alt="morphology feature trajectories over time per drug condition",
         shows="Per-condition shape trajectories, the observable the matcher compares against the "
               "synthetic library.",
         informs="These trajectories drive the inversion that produces the per-condition parameter "
                 "shifts.",
         informs_tag="Feeds the inversion"),
    dict(type="figure", img=CLLF + "morphology/icc_ccc_heatmap.png",
         ttl="Feature agreement on the real data", sub="AI-derived vs reference",
         alt="heatmap of feature agreement on real data",
         shows="Agreement between AI-derived and reference shape numbers on the real spheroids, the "
               "same reliability check applied in Theme 02.",
         informs="Confirms the real-data features used for inversion are the reliable ones.",
         informs_tag="Closes the loop with RQ1"),
    dict(type="section", title='Drug panel, <span class="it">drug by drug</span>',
         right="inferred delta J_cc with intervals"),
    dict(type="interactive", widget="forest", json="theme5_drug_forest.json",
         intro="Every drug's inferred cell-cell adhesion shift (median, with the q25 to q75 spread "
               "across its wells), grouped by mechanism class. Click a drug to see the wells behind it. "
               "Significance here is a heuristic (the spread excludes zero), not a formal test. The "
               "pooled BCR-axis shift (bootstrap CI) is weak under tau (-1.4, interval crosses zero) "
               "and significant only at end-state (+4.6).",
         informs="Reads the whole panel at once and ties each estimate back to its underlying wells.",
         informs_tag="Beyond the thesis: drug-by-drug detail"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 05', chips=[
        dict(t="real_data_inference_report.ipynb", gold=True), dict(t="drug panel"),
        dict(t="tau-registration matcher"), dict(t="bootstrap CIs"), dict(t="7 patients")]),
    dict(type="bigcta", title='Back to the <span class="it">overview</span>.',
         links=[dict(t="All analysis themes &rarr;", href="index.html", primary=True)]),
]


THEME_SPECS = {0: ("Image &amp; intensity EDA - CLL CPM thesis", THEME1),
               1: ("Segmentation &amp; feature preservation - CLL CPM thesis", THEME2),
               2: ("Simulation library - CLL CPM thesis", THEME3),
               3: ("Separability &amp; identifiability - CLL CPM thesis", THEME4),
               4: ("Drug panel &amp; real-data inference - CLL CPM thesis", THEME5)}


# ============================ LANDING ====================================================
LANDING_THEMES = [
    dict(num="Theme 01", name='Image &amp; intensity <span class="it">EDA</span>',
         lede="What the segmentation, feature-extraction and inference stages must cope with in the "
              "raw brightfield data, and how the dataset composes. Every figure states the method "
              "choice it motivated.",
         metric="Appendix A.1 &middot; RQ1", href="01_image_intensity_eda/index.html", ready=True),
    dict(num="Theme 02", name='Segmentation &amp; feature <span class="it">preservation</span>',
         lede="Eight segmenters compared on the metric the pipeline consumes - do AI-derived shape "
              "numbers agree with human ones? Only the heavy-aug U-Net clears the 0.85 reliability bar.",
         metric="Appendix B &middot; RQ1", href="02_segmentation/index.html", ready=True),
    dict(num="Theme 03", name='Simulation <span class="it">library</span>',
         lede="The synthetic CPM library: how each parameter changes morphology, how the runs "
              "distribute, and how 1,152 sampled vectors became 1,105 usable.",
         metric="Appendix C, F &middot; RQ2", href="03_simulation_library/index.html", ready=True),
    dict(num="Theme 04", name='Separability &amp; <span class="it">identifiability</span>',
         lede="Which CPM parameters are identifiable from morphology - SNR discriminability, Sobol "
              "sensitivity, leave-one-out recovery. None reach the identifiable band; width, J_cc and J_cm are weakly identifiable.",
         metric="Appendix D-H &middot; RQ2", href="04_separability_identifiability/index.html", ready=True),
    dict(num="Theme 05 &middot; Headline", name='Drug panel &amp; real-data <span class="it">inference</span>',
         lede="Inverting real spheroid morphology to CPM parameters, and whether inferred shifts track "
              "stimulation and drug class across seven patients and the drug panel.",
         metric="Appendix I, J &middot; RQ3", href="05_drug_realdata/index.html", ready=True, featured=True),
]

LANDING_TAPE = [
    "Image EDA", "99k frames, 51 hand-annotated",
    "Reproducibility audited", "only U-Net (heavy aug.) crosses the 0.85 reliability bar",
    "Cellular Potts simulation", "1,152 sampled, 1,105 usable runs",
    "Identifiability", "width, J_cc and J_cm weakly identifiable; the rest non-identifiable",
    "Real-data inference", "reference wells across 7 patients + drug panel, relative shifts on the weakly identifiable axes",
]

LANDING_HERO = dict(
    title='CLL spheroid morphology <span class="it">to</span><br>'
          'CPM <span class="gold">parameters</span>.',
    lead="The exploratory data analysis and analytics behind the MSc thesis, curated so an examiner "
         "can see the depth of the work. *Each study reads as 'here is what I found and why it shaped "
         "the method'.*",
    image="assets/hero_spheroid_healthy.png",
    kpis=[dict(v="51", l="Hand-annotated frames"), dict(v="U-Net", l="Chosen segmenter", gold=True),
          dict(v="1,105", l="Synthetic runs", gold=True), dict(v="&ge; 0.85", l="Reliability bar")],
)


def main():
    built, pending = [], []
    for i, t in enumerate(LANDING_THEMES):
        tdir = NAV[i]["href"].split("/")[0]
        if i in THEME_SPECS:
            import analysis_index as ai
            title, blocks = THEME_SPECS[i]
            # insert the complete-analysis index just before the tools block, so every
            # thesis analysis in this theme is present, not only the interactive highlights
            ti = next((j for j, b in enumerate(blocks) if b["type"] == "tools"), len(blocks))
            blocks = blocks[:ti] + ai.index_blocks(i) + blocks[ti:]
            (ROOT / tdir).mkdir(exist_ok=True)
            ru.render_theme_html(title=title, blocks=blocks, rel_root="../",
                                 prev_next=nav_for(i), out_path=ROOT / tdir / "index.html")
            ru.render_theme_markdown(title=title, blocks=blocks,
                                     out_path=ROOT / tdir / "README.md")
            built.append(tdir)
            t["ready"] = True
        else:
            t["ready"] = False
            pending.append(tdir)
    ru.render_landing(themes=LANDING_THEMES, tape=LANDING_TAPE, hero=LANDING_HERO,
                      out_path=ROOT / "index.html")
    print("Built theme pages:", built)
    print("Pending:", pending)


if __name__ == "__main__":
    main()
