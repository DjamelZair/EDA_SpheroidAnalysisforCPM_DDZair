# What the data demands.

**Thesis target:** Theme 01 / Data exploratory analysis / Appendix A.1.

> The imaging reads size and gross shape robustly, but contrast, focus and fragmentation limit the finer boundary features, the same loss that later caps CPM-parameter identifiability.

Brightfield microscopy of patient-derived CLL spheroids is low-contrast, unevenly lit, and frequently fragmented under drug treatment. This analysis characterises what the images **are** (intensity, contrast, focus, illumination and fragmentation) and what the dataset **contains**, then traces each property to the segmentation, metric and feature choice it drove downstream.

| Metric | Value | Note |
|---|---|---|
| Raw frames | 99k | Local archive; 12,485 in the real inference set. |
| Hand-annotated | 51 | About 0.05% of the corpus, the defining constraint. |
| Contrast covered by aug. | ~100% | Focus ~91%; validates the heavy-aug U-Net. |
| Real wells out-of-library | ~90% | Why the thesis reports relative shifts, not absolutes. |

## A. What is the dataset?  (cohort & the defining constraint)

### Corpus scale and label scarcity - hover for counts

*(interactive chart in the HTML version)*

**What it shows.** Only 51 of roughly 99,000 frames are hand-annotated (about 0.05%), expanded to 306 by augmentation. The held-out test set is 45 frames.

**What it motivated (Decision: two-stage training).** A 1-in-1000 label ratio motivates the two-stage training strategy: pretrain on classical pseudo-labels, then fine-tune on the 51 ground-truth masks.

### What the pipeline does, end to end - raw frame to outline to shape numbers

![](../assets/cll/figures/what_we_do_strip.png)

**What it shows.** A microscopy frame goes in, the AI draws the spheroid outline, and a handful of shape numbers come out. Those numbers are the observables every later stage consumes.

**What it motivated (Frames the whole pipeline).** Fixes the unit of analysis: the segmenter is judged on whether these shape numbers are trustworthy, not on raw pixel overlap.

## B. What does the raw signal look like?  (why a learned segmenter, not thresholding)

### Contrast vs fragment count - 51 annotated frames

*(interactive chart in the HTML version)*

**What it shows.** Contrast spans roughly 0.46 to 1.0 across the annotated set, and higher contrast couples to more fragments, because separating fragments exposes bright background between dark material.

**What it motivated (Decision: learned segmenter + contrast-conditional preprocessing).** The wide, regime-dependent contrast (and the fragment-debris intensity overlap it creates) is why a single global threshold cannot work and a learned segmenter is needed, with contrast-conditional preprocessing in the classical baseline.

### Focus spread across frames - Laplacian variance, log scale

*(interactive chart in the HTML version)*

**What it shows.** Brightfield focus spans about 0.9 orders of magnitude, and background illumination is uneven.

**What it motivated (Decision: restrict inversion features).** Both inject noise into boundary-derived shape features, the exact perimeter and circularity features the CPM inference relies on, so inversion is restricted to features that survive segmentation noise.

## C. What is the object structure?  (the segmentation criterion: feature fidelity)

### Components per annotated image - how multi-object the masks are

*(interactive chart in the HTML version)*

**What it shows.** Most frames are not a single object (median 8 components; about 70% have more than one), and fragment sizes span four orders of magnitude, from the main body down to specks below 100 px.

**What it motivated (Decision: CC-Dice + largest component).** Standard Dice is dominated by the largest component and is blind to small fragments, so CC-Dice (equal weight per component) is the right metric, and post-processing keeps the largest connected component.

## D. Fragmentation vs treatment  (biology preview, associative)

### Fragmentation by drug-mechanism class - median fragmentation index, classes with n>=30

*(interactive chart in the HTML version)*

**What it shows.** Syk-inhibitor and CXCR4-antagonist wells are the most fragmented; BTK, NF-kB and MALT1 inhibitors sit lowest. Counts are large and unequal and metadata are plate-level, so this is read as an association.

**What it motivated (Preview: RQ3 mechanism, associative only).** Previews the RQ3 mechanism story (drug class changes cohesion), and shows the most drug-responsive classes are hardest to segment, so feature fidelity is the right criterion.

## E. Drug response, measured automatically  (the payoff: morphology to mechanism)

### Drug response measured automatically from the AI segmenter - three drug conditions, every available timepoint

*(interactive chart in the HTML version)*

**What it shows.** High-dose trametinib collapses the cluster; PD098060 compacts it; low-dose trametinib leaves it intact. Every point is extracted from an AI-segmented frame, with no manual measurement.

**What it motivated (Feeds RQ2 / RQ3 inference).** This is the observable the inference consumes: a per-condition shape trajectory that the CPM matcher compares against the synthetic library.

### Sources (canonical, executable)

This reader consolidates and re-orders the data EDA into the thesis's decision order. Interactive charts are computed from the same local CSVs the notebooks use (`imaging_eda/cache/labelled_qc.csv`, `frame_qc.csv`, `rq1_segmentation/results/feature_validation/timecourse_full_features.csv`); raster panels are the on-brand figures from the thesis figure set. Open the source notebooks for the full code and every panel:

**`thesis_submission/notebooks/RQ1_segmentation/01_data_eda.ipynb`** and **`imaging_eda/imaging_data_eda.ipynb`**.

An earlier broad notebook, `data/cll_spheroid_eda_complete.ipynb`, is catalogued as a referenced orphan in `_provenance_notes.md`.

## Complete analysis index  (every thesis analysis in this theme)

### Each analysis, what it shows, its thesis label, and the result

| Analysis | What it shows | Thesis label | Key result / status |
|---|---|---|---|
| Full data EDA | Intensity, contrast, focus, fragmentation, cohort over 51 annotated frames | appendix:data:eda | Shown interactively above |
| Data augmentation | 11 geometric + photometric ops, 51 originals to 255 augmented pairs | app:aug / tab:aug_ops | 5 augmentations per original |
| Patient mapping & split | Train/val/test 216/45/45 images (37/9/8 spheroids), plate-level stratification | app:patient_mapping / tab:patient_mapping | P1043 noted in train and test |

**Sources / tools:** 01_data_eda.ipynb, imaging_data_eda.ipynb, labelled_qc.csv, frame_qc.csv, timecourse_full_features.csv, Chart.js + scikit-image
