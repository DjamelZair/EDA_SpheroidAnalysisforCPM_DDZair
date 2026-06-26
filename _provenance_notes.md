# Provenance and Superseded-Item Notes

Pointers only. **Nothing listed here has been moved or deleted.** Physical archiving (if
wanted) is a later, separate step. GB-scale directories are explicitly left in place.

---

## 1. Superseded / redundant artefacts (list only)

### Notebooks - un-executed twins (keep the `_executed` version)
- `rq1_segmentation/eda/03_augmentation_eda.ipynb` -> use `03_augmentation_eda_executed.ipynb`
- `rq1_segmentation/eda/classical_eda.ipynb` -> use `classical_eda_executed.ipynb`
- `rq1_segmentation/eda/integrated_comparison.ipynb` -> use `integrated_comparison_executed.ipynb`
- `rq1_segmentation/eda/nnunet_grayscale_vs_multichannel.ipynb` -> use the `_executed` version
- Same twins are mirrored under `thesis_submission/notebooks/RQ1_segmentation/`.

### Simulation outputs - superseded recovery copies
- `rq3_inference/cll_saltelli_outputs/` and `cll_saltelli_outputs (2)/` -> superseded by
  `cll_saltelli_outputs (3)/` (the merged 1105-sample canonical set). GB-scale; leave in place.
- `rq3_inference/latticeplots/` vs `latticeplots (2)/` -> duplicate; canonical one unconfirmed.

### HTML reports - duplicates / superseded
- `rq3_inference/cll_discriminability_notebook.html` -> duplicate of `cll_discriminability_report.html`.
- `rq3_inference/cll_width_outputs/width_discriminability_report.html` -> superseded by full Sobol.
- `rq1_segmentation/preprocess_validation/eda2/preprocess_validation_old/` -> superseded by `_v2`.
- `rq1_segmentation/preprocess_validation/eda2/_archive/` (non-`_v2` files) -> superseded.
- `rq1_segmentation/preprocess_validation/analysis_outputs/meeting3_*` -> meeting-specific, not thesis.
- `ThesisWriting/reports/_archive/baseline_gallery.html` -> superseded by `baseline_gallery_v2.html`.
- `Preprocess_Validation_Balanced/balanced_preprocess_validation.html` -> superseded by eda2_v2.

### Legacy code - superseded by the tau-registration matcher (2026-05-27 pivot)
- `rq3_inference/matching/cpm_nurnberg_pipeline.py`, `spheroid_calibration_pipeline.py`.
- `rq3_inference/results_chapter/wass_invert_real.py` -> comparison baseline only.
- `rq3_inference/plot_vtk_cells.py`, `plot_vtk_binary.py`, `generate_report.py` -> early debug/reporting.

### Already-archived (do not touch; large)
- `_archive/` (68 MB); `rq1_segmentation/results/_archive/` (1.2 GB old checkpoints);
  `outputs/_archive/diagnostics_v2/` (24 MB).

---

## 2. "Additional validation" - keep and index, do not polish
Real experiments that are not part of the canonical chain but should remain visible:
- `rq1_segmentation/eda/nnunet_test_validation.ipynb`
- `rq1_segmentation/eda/pseudo_label_validation.ipynb`
- `rq1_segmentation/eda/classical_input_selection.ipynb`

---

## 3. Orphaned / early notebooks (not folded into the curated themes)
- `data/cll_spheroid_eda_complete.ipynb` - early broad "complete-pipeline" EDA. Useful unique
  content (dataset inventory, IncuCyte native-metric drug trajectories, area-to-TargetVolume
  prior), but: (a) its 21 figures are not on disk (`data/figures_eda/` is empty) and are not
  embedded inline, so they cannot be shown as-is without re-running (disallowed - raw data is
  HPC-only); (b) its Section 8 (Nurnberg-vs-ABC framework choice) is a supervisor-meeting
  planning artefact superseded by the adopted tau-registration matcher. **Decision needed:**
  leave as orphaned reference, or (if you can provide data access) regenerate its figures so
  its unique panels can be embedded.
- `rq3_inference/results_chapter/make_figure_alternatives.py` - likely figure-style scratch;
  archive candidate if confirmed as such.

---

## 4. Figures routed to a different theme
- `imaging_eda/figures/fig_feature_preservation_boundary.*` - compares segmenters on feature
  preservation; this is an **RQ1 selection** figure (Theme 2), not raw-image EDA. Excluded
  from the Theme 1 reader; belongs with Theme 2.
- `imaging_eda/figures/fig_pipeline_overview.*`, `make_pipeline_figure.py` - pipeline schematic
  (methods figure), not EDA.

---

## 5. Unresolved provenance questions (need user input)
1. Confirm `cll_spheroid_eda_complete.ipynb` handling (orphan vs regenerate) - section 3 above.
2. `make_figure_alternatives.py` - purpose.
3. `coords_io.py` VTK parse is annotated "round-trip lossless (VTK parse untested)" - flagged
   for verification before publication; does not affect curation.
4. `latticeplots/` vs `latticeplots (2)/` - which is canonical.
