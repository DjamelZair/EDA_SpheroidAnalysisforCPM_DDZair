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
    dict(tag="Theme 00", name="Data construction", href="00_data_inventory/index.html"),
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

# ============================ THEME 0 - DATA CONSTRUCTION & PROVENANCE ============================
# Every count below is read live from disk (find / wc -l / du), not assumed.
_CORPUS_ROWS = [
    ["Raw brightfield archive", "99,055 images", "75,043 .tif + 23,913 .jpg + 99 .png, 312 GB", "data/raw/ (delivered)"],
    ["Delivered lab metadata", "3 workbooks + legend + template", "Pooled AI metadata, keyed VID + Well, Volgnummer = patient", "data/metadata/*.xlsx (delivered)"],
    ["Hand annotations (VIA)", "6 experiments", "via_region_data JSON polygons + annotated jpgs", "3D annotations/ (delivered)"],
    ["Ground-truth masks", "51 masks", "VIA polygons rasterised to instance masks", "derived from annotations"],
    ["Frame-QC table", "12,485 frames", "contrast, focus, fragmentation per segmented frame", "built by build_tables.py"],
    ["Patient / condition join", "12,485 rows", "frames joined to 5 patients / 7 series, drug + stimulation", "built by patient_map.py"],
    ["Regionprops feature table", "6 features / frame", "area, diameter, eccentricity, solidity, perimeter, circularity", "built by extract_features.py"],
    ["Train / val / test split", "216 / 45 / 45 images", "37 / 7 / 7 original spheroids, source-stratified, seed 42", "built by build_training_dataset.py"],
    ["Classical pseudo-labels", "4,547 masks", "classical-pipeline masks for stage-1 pretraining", "built by the classical pipeline"],
]

THEME0 = [
    dict(type="hero",
         meta=["Theme 00", "Data construction & provenance", "Appendix A.0"],
         title='How the working data was <span class="it">built</span>.',
         caption="From two lab archives to the tables every later theme reads",
         lede="None of the analysis CSVs were handed over. They were constructed from 99,055 raw "
              "brightfield frames and five delivered metadata workbooks: matched to patients, "
              "segmented, measured, and split. This theme shows that construction with code.",
         summary="Before any result, the raw delivery had to become a working corpus. This theme "
                 "traces it end to end: (A) the raw data as delivered, counted from disk; (B) the "
                 "match that links image filenames to patient and condition metadata; (C) the derived "
                 "working tables, each shown as input to construction step to output; and (D) the "
                 "constructed corpus every later theme consumes. Every count is read live from disk."),
    dict(type="kpis", items=[
        dict(lbl="Raw images", num="99,055", desc="75,043 tif + 23,913 jpg + 99 png; 312 GB, two lab archives.", numeric=True),
        dict(lbl="Delivered metadata", num="3+2", desc="3 Pooled AI workbooks + legend + template (VID, Well, Volgnummer).", gold=True),
        dict(lbl="Hand annotations", num="51", desc="VIA polygons rasterised to masks; ~0.05% of the corpus.", gold=True, numeric=True),
        dict(lbl="Derived corpus", num="12,485", desc="Frames matched, QC'd and feature-extracted, all constructed.", numeric=True),
    ]),

    # ---- A. RAW DATA AS DELIVERED ----
    dict(type="section", title='A. The raw data, <span class="it">as delivered</span>',
         right="counted from disk, not assumed"),
    dict(type="prose", text=
         "The lab delivered two archives (Vivek Muniraj, 2025) totalling **312 GB** under "
         "`data/raw/`. Nothing here is derived: these are the original IncuCyte brightfield "
         "time-lapses and the metadata workbooks. Every count below comes from `find` and `wc -l` "
         "run against the disk."),
    dict(type="code",
         title="Raw archive layout and image census", sub="read live with du / find",
         io=["2 delivered archives", "extracted IncuCyte trees", "99,055 frames"],
         src="$ du -sh data/raw  |  $ find data/raw -iname '*.tif' | wc -l",
         code="data/raw/                                              # 312 GB, delivered\n"
              "|- O20250116 ... 1st final data transfer.tar.gz   88 GB -> Drug screens/ (14 exp) + NK/\n"
              "'- 20250123 ... 2nd final data transfer.7z        71 GB -> Btk/ Refractory/ Ongoing/ T/\n"
              "        leaf image folders are named 'IncuCyte export'\n\n"
              "$ find data/raw -iname '*.tif' | wc -l        # 75,043\n"
              "$ find data/raw -iname '*.jpg' | wc -l        # 23,913\n"
              "$ find data/raw -iname '*.png' | wc -l        #     99\n"
              "                                              # = 99,055 brightfield frames\n\n"
              "filename encodes everything:  VID1797_E4_1_00d03h00m.tif\n"
              "                              |VID-| |well| |  |-timepoint-|\n"
              "                                          field  (00d03h00m = 3 h elapsed)",
         note="The filename is the primary key for every downstream join: VID (video/experiment), "
              "Well (plate position, one spheroid), field and elapsed timepoint."),
    dict(type="code",
         title="Delivered metadata workbooks", sub="lab .xlsx under data/metadata/",
         io=["5 delivered .xlsx", "one sheet per experiment", "VID + Well + Volgnummer"],
         src="data/metadata/*.xlsx  (+ metadata_legend.xlsx data dictionary)",
         code="Btk inhibitors - Pooled AI metadata.xlsx      (8 experiment sheets)\n"
              "Drug screen 1 - Pooled AI metadata.xlsx       (13 experiment sheets)\n"
              "Refractory patients - Pooled AI metadata.xlsx (3 experiment sheets)\n"
              "Template_IncuCyte_metadata_list_for_AI_MH.xlsx  (blank schema)\n"
              "metadata_legend.xlsx                            (data dictionary)\n\n"
              "columns:  Experiment | VID | Well | Volgnummer | Sex | Birth year | IGHV |\n"
              "          Rai Stage | Stimulation | Treatment | Target | Concentration (nM) | ...\n\n"
              "legend:   VID        = Video ID (one IncuCyte experiment)\n"
              "          Well       = position in the plate, unique per spheroid\n"
              "          Volgnummer = number of the patient's blood draw  <-- patient identity",
         note="Volgnummer is the canonical patient id; VID is the experiment id. They are kept apart "
              "on purpose (one patient can span several VIDs, see the match below)."),
    dict(type="table",
         title="One real metadata block (BTK inhibitor screen, patient 273)",
         head=["Experiment", "VID", "Well", "Volgnummer", "Sex", "IGHV", "Stimulation", "Treatment", "Target"],
         rows=[
             ["20211025 BTKi prol.", "1169", "A1", "273", "Male", "Mutated (VH3)", "unstim", "untreated", "-"],
             ["20211025 BTKi prol.", "1169", "A2", "273", "Male", "Mutated (VH3)", "unstim", "untreated", "-"],
             ["20211025 BTKi prol.", "1169", "A3", "273", "Male", "Mutated (VH3)", "unstim", "ibrutinib", "BTK"],
         ],
         note="Three wells of one patient (Volgnummer 273): A1/A2 untreated, A3 ibrutinib. The plate "
              "layout itself encodes the drug screen. The full workbook carries 100+ columns (flow "
              "cytometry, cytogenetics del13q14/TP53, clinical labs); the site uses only the join keys "
              "and the shape-relevant fields."),

    # ---- B. THE MATCH ----
    dict(type="section", title='B. The <span class="it">match</span>: images to patients and conditions',
         right="filename decode, then a keyed join"),
    dict(type="prose", text=
         "The images arrive as bare filenames; the biology lives in the workbooks. Matching the two "
         "is the join at the heart of the dataset. It is a two-stage design: decode the filename "
         "into structured fields, then join those fields to the metadata on `(VID, Well)`."),
    dict(type="code",
         title="Stage 1: decode the filename", sub="shared/io.py",
         io=["image stem", "regex", "VID / Well / field / timepoint"],
         src="shared/io.py:66, 97",
         code="_VID_PATTERN = re.compile(r\"^(VID\\d+)_([A-Z]\\d+)_(\\d+)_(\\d+d\\d+h\\d+m)(.*)$\")\n\n"
              "def parse_vid_stem(stem):                 # 'VID1797_E4_1_00d03h00m'\n"
              "    m = _VID_PATTERN.match(stem)\n"
              "    return {\"vid\":   m.group(1),          # VID1797\n"
              "            \"well\":  m.group(2),          # E4\n"
              "            \"field\": m.group(3),          # 1\n"
              "            \"timepoint\": m.group(4)}      # 00d03h00m  -> 180 min",
         note="Older frames use a BF_ / Brightfield_ convention without a VID; those fall back to an "
              "(experiment, Well) key instead."),
    dict(type="code",
         title="Stage 2: join filename fields to patient + condition", sub="imaging_eda/patient_map.py",
         io=["frame_qc.csv", "merge on (VID, Well)", "patient + treatment per frame"],
         src="imaging_eda/patient_map.py:58, 68, 105",
         code="# Volgnummer IS the patient; build a (VID, Well) -> patient lookup\n"
              "M[\"patient\"] = M[\"Volgnummer\"].map(_norm_vid)\n"
              "vw = M.set_index([\"VID\", \"Well\"])[\"patient\"].to_dict()\n\n"
              "# attach patient, drug, target, stimulation to every segmented frame\n"
              "qc = pd.read_csv(\"frame_qc.csv\")\n"
              "j  = qc.merge(meta, on=[\"VID\", \"Well\"], how=\"left\")     # <-- the join\n"
              "j.to_csv(\"frame_patient_treatment.csv\")",
         note="Excel contamination is handled here: VIDs arrive as 1797.0 and wells as A01, "
              "normalised to VID1797 / A1 before the join."),
    dict(type="code",
         title="The patient roster: 5 patients, 7 series", sub="run_cross_patient_inference.py",
         io=["6 VID experiments", "hardcoded roster", "5 unique patients"],
         src="rq3_inference/results_chapter/run_cross_patient_inference.py:46",
         code="PATIENTS = [                       # (VID, patient_id)\n"
              "    (1087, \"2089\"),               #  patient 2089\n"
              "    (1873, \"706_t1\"),             #  patient 706, timepoint 1\n"
              "    (2017, \"706_t2\"),             #          706, timepoint 2   <- one patient,\n"
              "    (2319, \"706_t3\"),             #          706, timepoint 3      three VIDs\n"
              "    (1964, \"EE5.1_refractory\"),   #  refractory patient\n"
              "    (2359, \"708\"),               #  patient 708\n"
              "]   #  VID1797 -> patient 267 (control only)\n"
              "    #  5 unique patients  ->  7 patient-timepoint series",
         note="This is why the cohort is 5 patients but 7 series: patient 706 was sampled "
              "longitudinally across three separate IncuCyte runs. VID is never the patient."),
    dict(type="table",
         title="The roster as data: 7 VID series resolve to 5 patients",
         head=["VID series", "Patient", "In drug panel?", "Note"],
         rows=[
             ["VID1087", "2089", "yes", "drug screen"],
             ["VID1797", "267", "no", "controls / stimulation only"],
             ["VID1873", "706 (t1)", "yes", "longitudinal, timepoint 1"],
             ["VID2017", "706 (t2)", "yes", "longitudinal, timepoint 2"],
             ["VID2319", "706 (t3)", "yes", "longitudinal, timepoint 3"],
             ["VID1964", "EE5.1", "yes", "refractory patient"],
             ["VID2359", "708", "yes", "drug screen"],
         ],
         note="Five unique patients (2089, 267, 706, 708, EE5.1); patient 706 appears three times. "
              "The drug panel covers four of the five (267 has no drug wells)."),

    # ---- C. DERIVED WORKING TABLES ----
    dict(type="section", title='C. The derived working <span class="it">tables</span>',
         right="input to construction step to output"),
    dict(type="prose", text=
         "With frames matched to biology, the working tables are computed. Each one below is shown "
         "as its provenance triple: the raw **input**, the **construction step** in code, and the "
         "**output** file it writes, so it is clear the tables were generated, not received."),
    dict(type="code",
         title="Shape features from masks (regionprops)", sub="rq3_inference/extract_features.py",
         io=["binary mask", "skimage regionprops", "per_image_features.csv (405 rows)"],
         src="rq3_inference/extract_features.py:128",
         code="from skimage.measure import regionprops\n\n"
              "def compute_spheroid_features(mask):\n"
              "    p = regionprops(mask)[0]                      # the one spheroid region\n"
              "    area, perim = int(p.area), float(p.perimeter)\n"
              "    return {\"total_area\": area,\n"
              "            \"equivalent_diameter\": _equivalent_diameter(p),\n"
              "            \"eccentricity\": float(p.eccentricity),\n"
              "            \"solidity\":     float(p.solidity),\n"
              "            \"perimeter\":    perim,\n"
              "            \"circularity\":  4*math.pi*area / perim**2}",
         note="These six numbers are the observables every later theme consumes. Output header: "
              "image_id, model, total_area, equivalent_diameter, eccentricity, solidity, perimeter, circularity."),
    dict(type="code",
         title="Frame quality table (contrast, focus, fragmentation)", sub="imaging_eda/build_tables.py",
         io=["mask + raw TIFF", "per-frame metrics", "frame_qc.csv (12,485 rows)"],
         src="imaging_eda/build_tables.py:174, 195",
         code="# intensity / contrast / focus, per frame\n"
              "p5, p95 = np.percentile(gray, [5, 95])\n"
              "michelson_contrast = (p95 - p5) / (p95 + p5)\n"
              "lap_var            = filters.laplace(gray).var()      # focus\n\n"
              "# fragmentation, from the connected components of the mask\n"
              "areas = [r.area for r in regionprops(measure.label(mask))]\n"
              "frag_index = 1.0 - max(areas) / sum(areas)            # 0 = one blob\n\n"
              "res.to_csv('imaging_eda/cache/frame_qc.csv')          # 12,485 frames",
         note="frame_qc.csv is the spine of Theme 01 and the coverage analysis: 12,485 rows, "
              "40 columns of QC + join keys."),
    dict(type="table",
         title="One well over time, as it lands in frame_qc.csv (VID1087 A9, STAT6 inhibitor)",
         head=["well", "drug", "class", "hours", "michelson", "focus (lap)", "n comp.", "area px", "frag index"],
         rows=[
             ["A9", "AS1517499", "STAT6 i", "0", "0.841", "0.032", "3", "134,874", "0.021"],
             ["A9", "AS1517499", "STAT6 i", "6", "0.815", "0.042", "6", "148,026", "0.189"],
             ["A9", "AS1517499", "STAT6 i", "12", "0.794", "0.039", "4", "143,256", "0.213"],
         ],
         note="A real slice of the derived spine: one drug well sampled over time, each row a frame "
              "with its contrast, focus and fragmentation computed from the mask and the raw TIFF. "
              "The fragmentation index climbs as the cluster starts to break apart."),
    dict(type="code",
         title="Train / val / test split (source-stratified, seed 42)", sub="build_training_dataset.py",
         io=["51 spheroids x 6 frames", "stratified shuffle", "train/val/test .txt"],
         src="rq1_segmentation/scripts/dataset/build_training_dataset.py:344",
         code="rng = np.random.RandomState(42)\n"
              "for source in df[\"source\"].unique():        # stratify by source plate\n"
              "    idx = df[df.source == source].index.values\n"
              "    rng.shuffle(idx)\n"
              "    #  ~70 / 15 / 15  ->  train / val / test\n"
              "for split in [\"train\", \"val\", \"test\"]:\n"
              "    (out / f\"{split}.txt\").write_text(\"\\n\".join(ids[split]))\n\n"
              "#  wc -l splits/*.txt  ->  train 216,  val 45,  test 45\n"
              "#  original spheroids  ->  37 / 7 / 7   (six frames each)",
         note="The genuinely plate-stratified 5-fold CV split (patient/plate held out) is a separate "
              "generator, train_pseudolabel.make_folds, used for the pseudo-label model."),

    # ---- D. THE CONSTRUCTED CORPUS ----
    dict(type="section", title='D. The constructed working <span class="it">corpus</span>',
         right="every row traceable to a raw input"),
    dict(type="table",
         title="From raw delivery to working tables, each traceable to its source",
         head=["Asset", "Count (from disk)", "What it is", "Origin"],
         rows=_CORPUS_ROWS,
         note="Delivered inputs are the raw archive, the metadata workbooks and the VIA annotations; "
              "everything else in this table was constructed by the scripts named above. The "
              "51-to-99,055 label ratio (about 0.05%) is the constraint that drives the two-stage "
              "training in Theme 02."),
    dict(type="chart", id="t0_corpus", fn="barH",
         title="Corpus scale and label scarcity", sub="hover for counts",
         data=dict(labels=["Raw archive", "Inference set", "Pseudo-labels", "Augmented train",
                           "Ground-truth", "Held-out test"],
                   datasets=[dict(label="frames", data=[99055, 12485, 4547, 306, 51, 45], color=GOLD)],
                   logx=True, xlabel="number of frames (log scale)", dec=0),
         note="Only 51 of 99,055 frames are hand-annotated (about 0.05%), expanded to 306 by "
              "augmentation. The held-out test set is 45 frames.",
         informs="A 1-in-2000 label ratio motivates the two-stage training strategy: pretrain on "
                 "4,547 classical pseudo-labels, then fine-tune on the 51 ground-truth masks.",
         informs_tag="Decision: two-stage training"),

    # ---- interactive: explore the constructed corpus (from Complete_EDA.ipynb section 4) ----
    dict(type="section", title='The built <span class="it">corpus</span>, feature by feature',
         right="the six derived features, interactively"),
    dict(type="interactive", widget="featdist", json="theme0_features.json",
         intro="The six shape features, computed by regionprops over the 557 annotated spheroid "
               "objects (the same table built in section C). Switch the feature, toggle a log axis "
               "to watch the size features de-skew, and split by plate to see the held-out VID3201 "
               "batch effect. These are the real distributions the segmenter must preserve.",
         informs="Two construction decisions fall straight out of this: the size features (area, "
                 "diameter, perimeter) are heavily right-skewed and get log-scaled before modelling, "
                 "and VID3201 sits apart from the other plates, which is why the split is stratified "
                 "by plate rather than shuffled.",
         informs_tag="Beyond the thesis: interactive corpus"),
    dict(type="interactive", widget="compose", json="theme0_composition.json",
         intro="The 12,485 inference frames are not a balanced set. Break them down by drug-mechanism "
               "class, patient, stimulation or condition, and switch count versus percent. The "
               "imbalance is the point: CXCR4-antagonist wells (6,239) and the longitudinal patient 706 "
               "dominate, and drug frames outnumber controls roughly seven to one.",
         informs="This imbalance is exactly why the training split is stratified by plate rather than "
                 "shuffled, and why the drug-panel results in Theme 05 are read per class rather than "
                 "pooled naively.",
         informs_tag="Beyond the thesis: interactive composition"),

    # ---- augmentation: shared offline set + the U-Net's heavier online policy ----
    dict(type="section", title='Augmentation: a <span class="it">shared</span> set, plus a heavier U-Net policy',
         right="two different things, often confused"),
    dict(type="interactive", widget="augcover", json="theme0_augcoverage.json",
         intro="The offline augmented training set (51 originals expanded to 306 pairs) is shared by "
               "every candidate model. Does it span the image-quality regimes the real frames actually "
               "show? Switch between contrast, intensity and focus: the filled curve is the 12,485 real "
               "frames, the gold line the augmented set, the dashed line the 51 originals.",
         informs="Contrast (100%) and focus (91%) are well covered, but only 18% of real frames fall in "
                 "the augmented brightness range: intensity is the one regime the training set "
                 "under-samples. This is the offline set, separate from the 'heavy augmentation' U-Net "
                 "policy detailed in Theme 02.",
         informs_tag="Offline set, shared by all models"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 00', chips=[
        dict(t="shared/io.py", gold=True), dict(t="imaging_eda/patient_map.py"),
        dict(t="imaging_eda/build_tables.py"), dict(t="rq3_inference/extract_features.py"),
        dict(t="build_training_dataset.py"), dict(t="data/metadata/*.xlsx"), dict(t="Complete EDA Msc Thesis.ipynb")]),
    dict(type="bigcta", title='Next: what the <span class="it">signal</span> looks like.',
         links=[dict(t="Theme 01 &middot; Image & intensity EDA &rarr;", href="01_image_intensity_eda/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]

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
                 "and fragmentation), then traces each property to the segmentation, metric and "
                 "feature choice it drove downstream. The dataset inventory itself, who and how "
                 "much, now lives in Theme 00."),
    dict(type="kpis", items=[
        dict(lbl="Hand-annotated", num="51", desc="About 0.05% of the corpus, the defining constraint.", gold=True, numeric=True),
        dict(lbl="Contrast covered by aug.", num="~100%", desc="Offline augmented set (shared by all models).", gold=True),
        dict(lbl="Focus covered by aug.", num="~91%", desc="Laplacian-variance range spanned by augmentation.", numeric=True),
        dict(lbl="Real wells out-of-library", num="~90%", desc="Why the thesis reports relative shifts, not absolutes.", numeric=True),
    ]),

    dict(type="section", title='First, what a real <span class="it">spheroid</span> looks like',
         right="actual frames from the corpus"),
    dict(type="interactive", widget="examples", json="theme1_realframes.json",
         intro="Before the distributions, the concrete thing: real brightfield frames from the corpus, "
               "cropped around the spheroid, with the U-Net outline in gold. Click through a cohesive "
               "spheroid, one fragmenting under drug, and the hard cases (blurred, low-contrast, "
               "unevenly lit) that the rest of this page quantifies.",
         informs="Every distribution below is a summary over thousands of frames like these. This is "
                 "what the segmenter and the feature extraction actually operate on.",
         informs_tag="The concrete object behind the numbers"),

    dict(type="section", title='A. What does the raw <span class="it">signal</span> look like?',
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
    dict(type="interactive", widget="qcdist", json="theme1_qc_intensity.json",
         intro="Pixel intensity across the real frames. The filled curve is the spheroid (foreground), "
               "the gold line the bright field (background): two overlapping modes. Switch to over-time "
               "to see frame brightness drift.",
         informs="The two intensity modes overlap once debris is present, so a single global threshold "
                 "cannot separate object from background: a learned segmenter is needed.",
         informs_tag="Decision: learned segmenter"),
    dict(type="interactive", widget="qcdist", json="theme1_qc_contrast.json",
         intro="Michelson contrast across the corpus, and how it drifts over the imaging time course. "
               "Contrast is wide and regime-dependent.",
         informs="Contrast is wide, regime-dependent and drifting, which is why the classical baseline "
                 "needs contrast-conditional preprocessing and the production segmenter is learned.",
         informs_tag="Decision: contrast-conditional preprocessing"),
    dict(type="interactive", widget="qcdist", json="theme1_qc_focus.json",
         intro="Focus (Laplacian variance) on a log scale: a sharp main cluster and a blurred tail. "
               "Two independent focus measures agree, so the spread is real.",
         informs="Out-of-focus frames blur the boundary-derived perimeter and circularity features, "
                 "reinforcing the restriction of inversion to features that survive segmentation noise.",
         informs_tag="Decision: restrict inversion features"),
    dict(type="interactive", widget="qcdist", json="theme1_qc_illumination.json",
         intro="Background illumination unevenness (coefficient of variation), and how it worsens over "
               "the time course as debris accumulates.",
         informs="Uneven background biases any intensity-based boundary, another reason the inversion "
                 "leans on shape features that tolerate illumination drift.",
         informs_tag="Decision: restrict inversion features"),

    dict(type="section", title='B. What is the object <span class="it">structure</span>?',
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
    dict(type="interactive", widget="fragstruct", json="theme1_fragstruct.json",
         intro="Three views of how fragmented the masks are: the count of connected components per "
               "frame, how much of the area the largest component holds, and how fragmentation rises "
               "over the time course.",
         informs="Because masks are multi-object but area-dominated, ordinary Dice would ignore the "
                 "small fragments, so CC-Dice scores every component, and post-processing keeps the "
                 "largest one.",
         informs_tag="Decision: CC-Dice + largest component"),

    dict(type="section", title='C. A glimpse of the drug-response <span class="it">payoff</span>',
         right="preview only &middot; full analysis in Theme 05"),
    dict(type="chart", id="t1_frag", fn="barH",
         title="Fragmentation by drug-mechanism class", sub="median fragmentation index, classes with n>=30",
         data=dict(labels=_fc["labels"],
                   datasets=[dict(label="median fragmentation index", data=_fc["median"], color="#c8a05c")],
                   xlabel="median fragmentation index", dec=3),
         note="A single teaser: Syk-inhibitor and CXCR4-antagonist wells fragment most; BTK, NF-kB and "
              "MALT1 inhibitors sit lowest. Counts are large, unequal and plate-level, so this is read "
              "as an association only. The full drug-response analysis, auto-measured trajectories, "
              "per-drug inferred shifts and the BCR axis, lives in "
              "[Theme 05](../05_drug_realdata/index.html).",
         informs="Previews the RQ3 drug-response story and shows the most drug-responsive classes are "
                 "the hardest to segment, which is exactly why the segmenter is chosen on feature "
                 "preservation rather than pixel overlap.",
         informs_tag="Preview only: full drug panel in Theme 05"),

    dict(type="section", title='D. From image quality to library <span class="it">coverage</span>',
         right="why the thesis reports relative shifts"),
    dict(type="interactive", widget="qualcoverage", json="theme1_qualcoverage.json",
         intro="Each dot is one real control well (n=48). Switch the image-quality metric to see which "
               "one predicts how far the well sits from its nearest synthetic spheroid: blur (focus) "
               "does, contrast does not, and more-fragmented wells sit slightly closer.",
         informs="Distance rises with blur (focus r=+0.43) but is flat against contrast (r=+0.05); "
                 "more-fragmented wells sit slightly closer (r=-0.30), since the library's dispersed "
                 "synthetic morphologies resemble broken spheroids. Either way, image quality shapes "
                 "coverage, so the inference is reported as relative shifts rather than absolutes.",
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
    dict(type="section", title='A tunable <span class="it">quality bar</span>',
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

# leaderboard: 8 models, real values (dice / shape-number agreement CCC).
# CC-Dice is intentionally NOT a leaderboard column: it was computed only for the
# nnU-Net / SAM2 / classical variants, never for the U-Net or pseudo-label models,
# so a per-model CC-Dice ranking would be ungrounded for the headline model. The
# measured CC-Dice subset is reported separately below.
_LB = dict(
    metrics=[dict(key="ccc", label="Shape-number agreement (CCC)", min=0, max=1.0, mid=0.5),
             dict(key="dice", label="Pixel overlap (Dice)", min=0.7, max=0.85, mid=0.79)],
    models=[
        dict(label="U-Net (heavy aug.)", dice=0.829, ccc=0.683, winner=True),
        dict(label="Pseudo-label + fine-tune", dice=0.811, ccc=0.464),
        dict(label="SAM2 (grayscale)", dice=0.787, ccc=0.473),
        dict(label="SAM2 (multi-channel)", dice=0.768, ccc=0.434),
        dict(label="Rule-based baseline", dice=0.760, ccc=0.378),
        dict(label="nnU-Net (default)", dice=0.757, ccc=0.305),
        dict(label="nnU-Net + cleanup", dice=0.799, ccc=0.285),
        dict(label="nnU-Net (multi-channel)", dice=0.755, ccc=0.270),
    ])

# CC-Dice (component-aware overlap, Jaus 2024), MEASURED MODELS ONLY. Source:
# rq1_segmentation/all_results.json (mean_cc_dice_all / ranking_by_cc_dice_45image).
# U-Net (heavy aug.) and the pseudo-label model were never scored on CC-Dice.
_CCDICE = dict(
    title="Component-aware overlap (CC-Dice), measured models only",
    head=["Model", "CC-Dice (mean, 45-image)", "Note"],
    rows=[
        ["nnU-Net (default)", "0.299", "Highest CC-Dice; still merges fragments (800 GT to 436 pred)"],
        ["nnU-Net (multi-channel)", "0.295", "Multi-channel does not fix merging"],
        ["SAM2 (multi-channel)", "0.100", "Over-fragments (800 GT to 1156 pred)"],
        ["Classical (heuristic ROI)", "0.034 to 0.132", "Range across classical variants"],
        ["U-Net (heavy aug.)", "not computed", "CC-Dice never scored for the U-Net; the old 0.18 was a ceiling claim, not a measurement"],
        ["Pseudo-label + fine-tune", "not computed", "CC-Dice never scored for this model"],
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

    dict(type="interactive", widget="drugstrip", json="theme2_overlay.json",
         intro="The U-Net's call (gold outline) on real treated frames it never saw in training. Pick a "
               "condition and a day: the shape numbers beside it are read straight off the mask.",
         informs="The unit of evaluation is these extracted numbers, not the pixel mask, which is why "
                 "the segmenter is chosen on feature preservation.",
         informs_tag="Why feature preservation, not pixels"),

    dict(type="section", title='Model <span class="it">leaderboard</span>', right="switch the metric"),
    dict(type="chart", id="t2_lb", fn="lbboard", height=420,
         title="Ranking flips with the metric", sub="click to switch",
         toggle=[("ccc", "Shape-number agreement"), ("dice", "Pixel overlap")],
         data=_LB,
         note="Pixel overlap is nearly flat (0.755 to 0.829) and picks the U-Net by a hair. "
              "Shape-number agreement ranks the U-Net first by a wide margin and is the only metric "
              "that reflects what the next stage consumes.",
         informs="The segmenter is selected on shape-number agreement (Lin's CCC against the six CPM "
                 "features), not pixel Dice. The heavy-aug U-Net is the only model above the 0.85 bar.",
         informs_tag="Decision: rank by feature preservation"),
    dict(type="table",
         title=_CCDICE["title"], head=_CCDICE["head"], rows=_CCDICE["rows"],
         note="CC-Dice (component-aware overlap) motivates the fragment handling, but it was only "
              "scored for the nnU-Net, SAM2 and classical variants, never for the U-Net or "
              "pseudo-label models, so it is kept off the headline ranking above. Where it was "
              "measured, nnU-Net leads (0.30), and even that merges most fragments. Source: "
              "all_results.json (mean_cc_dice_all)."),
    dict(type="code",
         title="What 'U-Net (heavy aug.)' actually means", sub="the winner's training-time policy",
         io=["shared offline set", "U-Net online policy", "standard vs heavy"],
         src="rq1_segmentation/scripts/unet/run_experiments.py:70, 84",
         code="# EVERY model trains on the same offline-augmented set (51 -> 306 pairs).\n"
              "# 'Heavy augmentation' is the winning U-Net's stronger ON-THE-FLY policy,\n"
              "# applied per batch during training, NOT a different dataset.\n\n"
              "def aug_standard(res):                    def aug_heavy(res):\n"
              "    Resize, HFlip, VFlip, Rotate90            Resize, HFlip, VFlip, Rotate90\n"
              "    ShiftScaleRotate(0.05, 0.1, 15)          ShiftScaleRotate(0.10, 0.2, 30)   # stronger\n"
              "    ElasticTransform(alpha=30)               ElasticTransform(alpha=50)        # stronger\n"
              "    RandomBrightnessContrast(0.15)           RandomBrightnessContrast(0.30)    # stronger\n"
              "    GaussNoise(p=0.2)                        GaussNoise(10-50, p=0.4)          # stronger\n"
              "                                             GridDistortion(0.3)              # + extra\n"
              "                                             GaussianBlur(3-7)                # + extra\n"
              "                                             CoarseDropout(8 x 32px)          # + extra",
         note="So the leaderboard winner is the resnet34 U-Net trained with aug_heavy: three transforms "
              "the standard policy does not use (grid distortion, blur, coarse dropout) plus roughly "
              "double the strength on the rest. That heavier regularisation, not a different training "
              "set, is what the name refers to (the shared offline set is shown in Theme 00)."),

    dict(type="interactive", widget="heatmap", json="theme2_reliability.json",
         intro="Concordance (Lin's CCC) between each model's shape number and the human one, 8 models "
               "by 6 features. Click a cell for its value; cells outlined in cream clear the 0.85 "
               "radiomics reliability bar.",
         informs="Only the U-Net crosses 0.85, and only on area and diameter; roundness and elongation "
                 "are unreliable for almost every model. This sets the operational feature set for RQ3 "
                 "(area, diameter, solidity, perimeter, circularity; eccentricity dropped).",
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
    dict(type="interactive", widget="timelapse", json="theme2_f3.json",
         intro="The hardest test frame (VID3201 F3, trametinib 50 uM). Drag the slider across five days "
               "at four-hour cadence to watch the spheroid break into many pieces.",
         informs="Under high-dose drug, pixel overlap drops for every model while area and diameter "
                 "stay reliable and roundness collapses. This split is the whole reason the "
                 "feature-preservation audit was needed, and why F3 is reported separately.",
         informs_tag="Validates the feature-preservation audit"),
    dict(type="chart", id="t2_f3", fn="barH", height=360,
         title="Classical pipeline on the hardest frame", sub="top 10 of the classical preproc / segmenter sweep",
         data=_F3,
         note="This is the classical-pipeline sweep (the deep models, including the heavy-aug "
              "U-Net, are in the showcase above). Even the best classical combination reaches only "
              "about 0.45 Dice on this frame; no configuration rescues it.",
         informs="Confirms F3 is a genuine ceiling, not a tuning artefact.",
         informs_tag="Bounds the hardest case"),

    dict(type="section", title='The <span class="it">leaderboard</span>, in detail',
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

# ---- Theme 3 data: CPM parameter sweeps (how each parameter changes cluster size) ----
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
         lede="With a segmenter that preserves the six shape numbers (Theme 02), those same features "
              "can now be measured on simulated spheroids, so real and synthetic morphology become "
              "directly comparable. Seven simulation parameters, swept one at a time and jointly, build the "
              "library the real spheroids are matched against.",
         summary="The pipeline only works because the identical six features are measured on real and "
                 "synthetic spheroids. A Cellular Potts Model with seven parameters (cell-cell and "
                 "cell-medium adhesion, contact range, neighbour order, volume elasticity, target "
                 "volume, and motility) is sampled to build a reference library of morphology "
                 "trajectories. This theme shows how each parameter changes the simulated cluster, and "
                 "accounts for which runs were usable."),
    dict(type="kpis", items=[
        dict(lbl="CPM parameters", num="7", desc="Swept one-at-a-time and jointly (Saltelli).", numeric=True),
        dict(lbl="Sampled vectors", num="1,152", desc="Saltelli design over the 7 parameters.", numeric=True),
        dict(lbl="Usable runs", num="1,105", desc="After dropping degenerate masks.", gold=True, numeric=True),
        dict(lbl="Dropped", num="47", desc="Empty or single-pixel masks, removed.", numeric=True),
    ]),
    dict(type="section", title='How each <span class="it">parameter</span> changes morphology',
         right="one-at-a-time sweeps"),
    dict(type="chart", id="t3_sweep", fn="sweepline", height=400,
         title="Cluster area vs parameter level", sub="switch the parameter",
         toggle=[(k, _sw_nice[k]) for k in _SW_ORDER], data=_SWEEP,
         note="Target volume (width) and cell-cell adhesion move cluster area the most; neighbour "
              "order and motility barely move it on their own.",
         informs="Identifies which parameters leave a size signature in morphology, the precondition "
                 "for being identifiable later.",
         informs_tag="Sets up the identifiability question"),
    dict(type="section", title='From <span class="it">parameter to spheroid</span>',
         right="live morph, beyond the thesis"),
    dict(type="interactive", widget="morph", json="theme3_morph.json",
         intro="The thesis only shows static sweep curves. Here you grab a parameter (target volume or "
               "cell-cell adhesion J_cc) and watch a real rendered spheroid grow or compact while its "
               "cluster-area curve tracks the move.",
         informs="Binds the rendered CPM lattice to the swept parameter, so size and shape respond as "
                 "you drag, not just a line plot.",
         informs_tag="Beyond the thesis: live morph"),
    dict(type="section", title='What the <span class="it">library</span> looks like',
         right="16 random samples at the final step"),
    dict(type="interactive", widget="gallery", json="theme3_gallery.json",
         intro="Sixteen sampled parameter vectors rendered at the final simulation step. Click any "
               "spheroid to read its area, circularity and solidity: the samples span compact, loosely "
               "packed and fully dispersed morphologies.",
         informs="The sampled parameter space produces a wide morphological range, the diversity the "
                 "inversion relies on.",
         informs_tag="Shows the library's morphological spread"),
    dict(type="section", title='Across the <span class="it">morphospace</span>',
         right="1,105 samples, click any one"),
    dict(type="interactive", widget="morphospace", json="theme3_morphospace.json",
         intro="Every dot is one of 1,105 synthetic spheroids. Click one to read the exact seven CPM "
               "parameters that produced it and the morphology that resulted. Swap the axes, recolour "
               "by any parameter, or highlight the morphological extremes.",
         informs="Turns the library from a 16-panel gallery into a navigable map, where any point "
                 "reveals its generating parameters and shape.",
         informs_tag="Beyond the thesis: navigable library"),
    dict(type="section", title='Which parameters <span class="it">drive</span> cluster size?',
         right="Sobol indices, direct vs total effect"),
    dict(type="interactive", widget="sobolgap", json="theme3_sobolgap.json",
         intro="For each parameter, the solid gold bar is its direct effect on cluster area (Sobol S1) "
               "and the sky extension is its interactions with the other parameters (up to the total "
               "effect ST). A large gap means the parameter acts mostly through interactions.",
         informs="Target volume dominates; volume elasticity and the adhesion parameters carry sizeable "
                 "interaction effects. These interactions limit how cleanly a single parameter can be "
                 "read back from morphology.",
         informs_tag="Interactions bound identifiability"),
    dict(type="section", title='The <span class="it">surrogate</span>, opened up',
         right="XGBoost, cross-validated"),
    dict(type="interactive", widget="surrogate", json="theme3_surrogate.json",
         intro="A gradient-boosted surrogate predicts each shape feature from the seven parameters. Toggle "
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
         informs="140 of the 152 real wells (92%) sit beyond the p95 nearest-neighbour distance of the "
                 "synthetic cloud, and 114 (75%) beyond p99: most real spheroids are extrapolated, not "
                 "interpolated. This one number is the reason the inference is reported as relative "
                 "shifts, not absolute parameters (Themes 04 and 05 build on it).",
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
    dict(type="bigcta", title='Next: which parameters are <span class="it">identifiable</span>?',
         links=[dict(t="Theme 04 &middot; Identifiability &rarr;", href="04_separability_identifiability/index.html", primary=True),
                dict(t="Back to index", href="index.html")]),
]

THEME4 = [
    dict(type="hero",
         meta=["Theme 04", "Separability & identifiability", "Appendix D to H"],
         title='Which parameters are <span class="it">recoverable</span>?',
         caption="Leave-one-out inversion on the 1,105-run library",
         lede="The parameter interactions and the thin real-world coverage seen in Theme 03 predict "
              "that some parameters will be unreadable; leave-one-out inversion quantifies exactly which. "
              "None of the seven reach the identifiable band: three are weakly identifiable, four are "
              "non-identifiable, and the analysis says so honestly.",
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
    dict(type="section", title='Which parameters are <span class="it">identifiable</span>?',
         right="leave-one-out recovery"),
    dict(type="interactive", widget="idbars", json="theme4_identifiability.json",
         intro="Per-parameter recovery R-squared from the inversion benchmark. Two matchers: the "
               "tau-registered matcher (primary) compares the whole trajectory after aligning its "
               "phase, so it is the more conservative test; the end-state matcher (secondary) compares "
               "only the settled morphology. Where they disagree, the settled shape carries the signal. "
               "The dashed line is the identifiable bar at R-squared 0.70 (the thesis bar from "
               "METHODS.md); click a bar for its Pearson correlation, sample count and error.",
         informs="No parameter reaches the 0.70 identifiable bar: cell-medium adhesion, target volume "
                 "and contact are only weakly identifiable, and the rest are non-identifiable. This is "
                 "the spine of RQ2.",
         informs_tag="Beyond the thesis: interactive identifiability"),
    dict(type="section", title='Feature to parameter <span class="it">sensitivity</span>',
         right="surrogate Sobol total-effect weights"),
    dict(type="interactive", widget="heatmap", json="theme4_discriminability_heatmap.json",
         intro="How much each shape feature responds to each CPM parameter, as XGBoost-surrogate Sobol "
               "total-effect weights (per-parameter min-max normalised, clipped at 0.05). Brighter gold means "
               "more sensitive; click a cell to read its value. All seven parameters are shown: width and volume "
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
         summary="Real spheroid trajectories from reference wells across five patients (seven "
                 "patient-timepoint series) and a panel of drug conditions are inverted to CPM "
                 "parameters on the three weakly identifiable axes. "
                 "The inferred shifts are read as relative, simulation-derived changes, not absolute or "
                 "biophysical values."),
    dict(type="kpis", items=[
        dict(lbl="Patients", num="5", desc="Unique donors; 7 patient-timepoint series, 4 in the drug panel.", numeric=True),
        dict(lbl="Read as", num="shifts", desc="Relative change on the weakly identifiable axes, not absolutes.", gold=True),
        dict(lbl="Drug-panel BCR shift", num="weak", desc="Tau (primary): J_cc shift -1.4, CI [-3.0, +0.2], spans zero. End-state: +4.6, CI [+2.1, +7.0], significant; the signal is in the settled morphology."),
        dict(lbl="Reported axes", num="3", desc="the three weakly identifiable axes (width, J_cc, J_cm).", numeric=True),
    ]),
    dict(type="section", title='What the <span class="it">drugs</span> do to morphology',
         right="two dose conditions, over five days"),
    dict(type="interactive", widget="drugstrip", json="theme5_drugstrip.json",
         intro="Two treated spheroids over five days, with the AI-segmented outline in cherry. Pick a "
               "drug and a day: high-dose trametinib disintegrates the cluster (area collapses ~8x), "
               "while PD098060 keeps it cohesive but contracts it inward (solidity rises to 0.92).",
         informs="Distinct drugs leave distinct, separable trajectories, which is exactly the signal "
                 "the inversion reads: high-dose trametinib as a loss of cohesion, PD098060 as "
                 "compaction.",
         informs_tag="Separable drug signatures"),
    dict(type="chart", id="t5_timecourse", fn="timecourse", height=440,
         title="Drug response measured automatically from the AI segmenter",
         sub="three drug conditions, every available timepoint",
         toggle=[(f, _tc["labels"][f]) for f in _TC_ORDER],
         data=_tc_chart,
         note="High-dose trametinib collapses the cluster; PD098060 compacts it; low-dose "
              "trametinib leaves it intact. Every point is extracted from an AI-segmented frame, "
              "with no manual measurement. Switch the feature to see each shape axis respond.",
         informs="This is the observable the inference consumes: a per-condition shape trajectory "
                 "that the CPM matcher compares against the synthetic library to produce the "
                 "per-condition parameter shifts.",
         informs_tag="Feeds the inversion"),
    dict(type="prose", title="Why we trust these real-data features",
         text="The real inference spheroids have no human-drawn masks to check against, so there is no "
              "real-data agreement heatmap to show here. The reliability guarantee comes from Theme 02: "
              "the segmenter was chosen because its six shape numbers agree with human ones on the "
              "held-out test set (area and diameter above the 0.85 concordance bar), and the inference "
              "uses only those same features. The trust is inherited from that audit, not re-measured "
              "on unlabelled real data."),
    dict(type="section", title='How each mechanism <span class="it">class</span> works',
         right="target, mechanism, and simulated spheroid effect"),
    dict(type="interactive", widget="drugmech", json="theme5_drugmech.json",
         intro="The panel spans ten mechanism classes. Click one to see what it targets, how it acts on "
               "a CLL cell, and a stylised simulation of the effect on the spheroid: cells spread apart "
               "(looser) or pull together (more compact) relative to the unstimulated baseline, driven "
               "by the class's inferred cell-cell adhesion shift.",
         informs="Most classes hit the B-cell-receptor axis (BTK, Syk, PI3K), which maintains the "
                 "adhesion that holds the spheroid together, so the prior is loosening. The inferred "
                 "shifts are mostly weak and non-significant; only the MEK inhibitor clears the "
                 "heuristic, and even that on four wells. The honest read is small, uncertain effects.",
         informs_tag="Beyond the thesis: mechanism to morphology"),
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
    dict(type="section", title='The whole arc, in one <span class="it">line</span>',
         right="what the six themes add up to"),
    dict(type="prose", title="End to end",
         text="99,055 raw brightfield frames, built into a working corpus (Theme 00), are read by a "
              "segmenter chosen for feature preservation rather than pixel overlap (Theme 02), because "
              "the raw signal limits the finer shape features (Theme 01). The same six features are "
              "then measured on a 1,105-run synthetic CPM library (Theme 03), which shows most real "
              "spheroids fall outside the simulated world (92% beyond p95). Leave-one-out inversion "
              "(Theme 04) finds only three weakly identifiable axes (width, J_cm, J_cc) and four "
              "non-identifiable ones, so the real-data drug inference (Theme 05) is read as relative "
              "shifts on those axes, not absolute biophysical values. **The honest limit, weak "
              "identifiability and thin coverage, is the finding, not a failure.**"),
    dict(type="tools", label='<span class="it">Sources</span> &middot; Theme 05', chips=[
        dict(t="real_data_inference_report.ipynb", gold=True), dict(t="drug panel"),
        dict(t="tau-registration matcher"), dict(t="bootstrap CIs"), dict(t="5 patients / 7 series")]),
    dict(type="bigcta", title='Back to the <span class="it">overview</span>.',
         links=[dict(t="All analysis themes &rarr;", href="index.html", primary=True)]),
]


THEME_SPECS = {0: ("Data construction & provenance - CLL CPM thesis", THEME0),
               1: ("Image &amp; intensity EDA - CLL CPM thesis", THEME1),
               2: ("Segmentation &amp; feature preservation - CLL CPM thesis", THEME2),
               3: ("Simulation library - CLL CPM thesis", THEME3),
               4: ("Separability &amp; identifiability - CLL CPM thesis", THEME4),
               5: ("Drug panel &amp; real-data inference - CLL CPM thesis", THEME5)}


# ============================ LANDING ====================================================
LANDING_THEMES = [
    dict(num="Theme 00", name='Data <span class="it">construction</span>',
         lede="Not an inventory of given CSVs but the provenance of built ones: 99,055 raw frames and "
              "five metadata workbooks, matched to patients, segmented, measured and split, shown with "
              "the actual construction code.",
         metric="Appendix A.0 &middot; RQ1", href="00_data_inventory/index.html", ready=True),
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
              "stimulation and drug class across five patients (seven patient-timepoint series) and the drug panel.",
         metric="Appendix I, J &middot; RQ3", href="05_drug_realdata/index.html", ready=True, featured=True),
]

LANDING_TAPE = [
    "Data construction", "99,055 raw frames matched, segmented, split (all built)",
    "Image EDA", "99k frames, 51 hand-annotated",
    "Reproducibility audited", "only U-Net (heavy aug.) crosses the 0.85 reliability bar",
    "Cellular Potts simulation", "1,152 sampled, 1,105 usable runs",
    "Identifiability", "width, J_cc and J_cm weakly identifiable; the rest non-identifiable",
    "Real-data inference", "reference wells across 5 patients (7 series) + drug panel, relative shifts on the weakly identifiable axes",
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
