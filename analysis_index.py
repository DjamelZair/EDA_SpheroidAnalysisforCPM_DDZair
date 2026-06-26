"""
analysis_index.py - the complete per-theme index of EVERY thesis analysis.

Source: the thesis master list (47 analyses). Each row = (analysis, what it shows,
thesis label, key result / status). Rendered as a "Complete analysis index" table on each
theme page so an examiner can see the full depth, not only the interactive highlights.
Numbers are quoted from the thesis tables/sections; nothing invented.
"""

# rows: [analysis, what it shows, thesis label, key result / status]
INDEX = {
    0: [  # Theme 1 - image / intensity EDA
        ["Full data EDA", "Intensity, contrast, focus, fragmentation, cohort over 51 annotated frames",
         "appendix:data:eda", "Shown interactively above"],
        ["Data augmentation", "11 geometric + photometric ops, 51 originals to 255 augmented pairs",
         "app:aug / tab:aug_ops", "5 augmentations per original"],
        ["Patient mapping & split", "Train/val/test 216/45/45 images (37/9/8 spheroids), plate-level stratification",
         "app:patient_mapping / tab:patient_mapping", "P1043 noted in train and test"],
    ],
    1: [  # Theme 2 - segmentation & feature preservation
        ["Classical baseline", "ROI extraction + multi-Otsu vs simpler alternatives, per-stage justification",
         "app:classical_justification", "Justifies ROI + 3-class Otsu"],
        ["Segmentation candidates", "8 models on the fixed 216/45/45 split",
         "app:baselines_table / tab:baselines", "Classical, U-Net x2, nnU-Net x3, SAM2 x2"],
        ["Training configuration", "Encoder, loss, augmentation, schedule, plate-level CV per model",
         "app:experimental_setup / tab:hyperparams", "ResNet34, BCE+Dice"],
        ["U-Net feature CCC", "Per-feature CCC and ICC(3,1) of U-Net vs manual masks (45-image test)",
         "sec:res_rq1_1 / tab:rq1_1_features", "Diameter 0.95, area 0.94, eccentricity 0.10 lost"],
        ["Dice vs CCC ranking", "All 8 models ranked by pixel Dice vs mean feature CCC",
         "sec:res_rq1_2 / tab:rq1_2_fidelity", "U-Net ties Dice 0.83, wins CCC 0.68 vs 0.31 (shown above)"],
        ["U-Net config ablation", "Test Dice across 13 U-Net variants during selection",
         "app:aug_ablation / fig:aug_ablation", "Heavy-aug config selected"],
        ["ICC / CCC heatmaps", "Full ICC and CCC matrices, 8 models x 6 features",
         "app:segmentation_heatmaps", "Shown above (heatmap)"],
        ["Post-processing sweep", "Change in mean feature CCC under 11 strategies, all 8 segmenters",
         "app:ccc_postproc / fig:ccc_postproc_sweep", "Cleanup is cosmetic for preservation (shown above)"],
        ["Residual-refiner", "Two-stage classical + learned correction",
         "app:refiner_failure / tab:refiner", "Negative result: collapses to identity"],
        ["F3 time series", "Most fragmented test frame across 4 days at 4 h cadence",
         "app:f3_timeseries / fig:f3_timeseries", "Shown above (hardest case)"],
        ["Metric formulas", "CCC, ICC(3,1), nRMSE, Dice, CC-Dice, component-count error",
         "app:metric_formulas", "Definitions"],
    ],
    2: [  # Theme 3 - simulation library
        ["CPM configuration", "1536x1152 lattice, blob r=250 px, 1000 MCS, 100 frames, 9 (OAT) / 3 (Saltelli) seeds",
         "app:cpm_sim_settings / tab:sim_settings", "CompuCell3D 4.5.0"],
        ["OAT sweep grid", "Per-parameter levels for the one-at-a-time sweep",
         "app:oat_sweep_grid / tab:sweeps", "76,500 snapshots, shown above"],
        ["Saltelli design & yield", "Saltelli N=128, d=7, 1152 runs; degenerate dropped",
         "sec:setup_sim_data", "1,105 viable, 47 dropped (shown above)"],
        ["VTK feature extraction", "CC3D lattice to binary mask to 6 features via skimage.regionprops",
         "app:cpm:vtk", "Reproducibility note (Appendix C)"],
        ["Sobol estimators", "Jansen first- and total-order estimators, paired sampling design",
         "app:sobol_estimators", "Schematic + equations"],
        ["Reproducibility", "GPU A100, Python 3.10, PyTorch 2.3.1, CC3D 4.5.0, seed 42, AI-tool disclosure",
         "app:reproducibility / tab:reproducibility", "Fixed seeds, full environment"],
    ],
    3: [  # Theme 4 - separability / identifiability
        ["Surrogate configuration", "XGBoost: 500 trees, depth 6, LR 0.05, subsample 0.8, L2=1, 5-fold CV",
         "app:surrogate_cv / tab:xgboost", "Forward surrogate (theta to features)"],
        ["Surrogate CV R2", "5-fold CV R2 of the surrogate per morphology feature",
         "sec:setup_xgboost / fig:surrogate_cv", "R2 0.66 (eccentricity) to 0.97 (circularity)"],
        ["Surrogate comparison", "XGBoost vs random forest vs Gaussian process on 1,105 samples",
         "tab:surrogate_benchmark", "XGBoost best on 5/6 features, mean R2 0.822"],
        ["Sobol matrix", "First- and total-order Sobol indices per (parameter, feature)",
         "sec:res_rq2_2 / fig:rq2_2_drivers", "Size driven by width S_T~0.91; J_cc only via interactions"],
        ["Per-parameter Sobol bars", "Largest S_T each parameter reaches across features",
         "app:sobol_bars / fig:sobol_bars", "Sensitivity ranking w > J_cm > J_cc"],
        ["SA baseline comparison", "Parameter rank under 6 measures (Spearman, SRC, XGB, Morris, PAWN, Sobol)",
         "app:sa_baselines / tab:sa_baselines", "Rank consistent: w~1, J_cm~2, J_cc~3"],
        ["LOO recovery R2", "Per-parameter recovered vs true over 1,105 runs, with identifiability tiers",
         "sec:res_rq2_1 / tab:rq2_1_identifiability", "w 0.64, J_cm 0.61, J_cc 0.34 (weakly identifiable; shown above)"],
        ["Synthetic inversion diagnostics", "Distance-metric, posterior coverage, Wasserstein, k-sensitivity",
         "app:synthetic_diagnostics", "Robustness checks"],
        ["LOO scatter", "Recovered vs true scatter, one panel per parameter, R2 inset",
         "app:synthetic_diagnostics / fig:loo_scatter", "Per-parameter recovery"],
        ["Eccentricity ablation", "LOO R2 with 5 features vs with perfect eccentricity added",
         "sec:res_rq2_3 / tab:rq2_3_ceiling", "Delta R2 <= 0.05; ceiling is simulator, not segmentation"],
        ["LOO benchmark settings", "Deployment matcher settings; ground-truth upper ceiling",
         "sec:setup_loo", "Same matcher as real data"],
        ["Active learning POC", "Surrogate-selected vs random vs oracle candidate selection",
         "app:active_learning / fig:active_learning_poc", "Reduces NN distance to under-covered wells"],
    ],
    4: [  # Theme 5 - drug panel & real-data inference
        ["Tau-registered matcher", "Phase-axis tau, z-scored features, Sobol-weighted MAD, k=20, empirical posterior",
         "sec:setup_matching", "Primary matcher"],
        ["Worked example (VID1797 F1)", "One well: observed trajectory to empirical posterior intervals",
         "app:worked_real_inference / fig:example_inversion_appendix", "Shows how data narrows each parameter"],
        ["Boundary & coverage", "Neighbours at sweep endpoints; real-to-library NN distance",
         "app:boundary_coverage / fig:boundary_saturation_appendix", "~90% of real spheroids extrapolated"],
        ["Stimulation reproducibility", "Per-parameter, how many of 7 patients shift the same way under stimulation",
         "sec:res_rq3_1 / fig:rq3_1_stability", "J_cm & J_cc 7/7 agree, width 3/7"],
        ["Expected vs observed shift", "Baseline vs stimulated medians vs a priori biological prediction",
         "sec:res_rq3_2 / tab:rq3_2_expected", "J_cm -30% (7/7), J_cc -7% (7/7) match"],
        ["Drug-class lookup", "23 drugs by mechanism class with targets and expected effects",
         "app:drug_classes / tab:drug_lookup", "BTKi, Syk, PI3K, JAK, CXCR4, MEK, NF-kB, ..."],
        ["Drug-panel delta J_cc", "Per-drug J_cc shift, by class, bootstrap CI; tau vs end-state matcher",
         "app:drug_panel_jcc / fig:h33_drug_panel_appendix", "Value under revision"],
    ],
}

SECTION_TITLE = 'Complete analysis <span class="it">index</span>'
SECTION_RIGHT = "every thesis analysis in this theme"


def index_blocks(theme_idx):
    rows = INDEX.get(theme_idx)
    if not rows:
        return []
    return [
        dict(type="section", title=SECTION_TITLE, right=SECTION_RIGHT),
        dict(type="table",
             title="Each analysis, what it shows, its thesis label, and the result",
             head=["Analysis", "What it shows", "Thesis label", "Key result / status"],
             rows=rows),
    ]
