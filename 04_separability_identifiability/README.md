# Which knobs can we read back?

**Thesis target:** Theme 04 / Separability & identifiability / Appendix D to H.

> None of the seven parameters reach the identifiable band. Three are weakly identifiable and the other four are non-identifiable, and the analysis says so honestly.

Leave-one-out inversion on the 1,105-run library measures how well each CPM parameter is recovered from morphology (R squared of recovered vs true). Cell-medium width, cell-medium adhesion and cell-cell adhesion are weakly identifiable; the other four are non-identifiable. These are the verified numbers from the recovery benchmark, not the optimistic error metric used elsewhere.

| Metric | Value | Note |
|---|---|---|
| Weakly identifiable | 3 of 7 | width, J_cm, J_cc clear the R2 0.30 weak bar; none reach identifiable. |
| Best recovery | 0.64 | Cell width, LOO R2 (weakly identifiable). |
| Library size | 1,105 | Saltelli runs used for the benchmark. |
| Non-identifiable | 4 | lambda, temperature, contact range, neighbour order. |

## How well each parameter is recovered  (leave-one-out R squared, verified)

### Leave-one-out recovery (R squared) - gold = weakly identifiable (R2 >= 0.30)

*(interactive chart in the HTML version)*

**What it shows.** Cell width (0.64), cell-medium adhesion (0.61) and cell-cell adhesion (0.34) are the three weakly identifiable parameters; volume elasticity, temperature, contact range and neighbour order are non-identifiable. Neighbour order is effectively zero.

**What it motivated (Decision: report only the weakly identifiable axes).** The pipeline reports estimates and uncertainty only for the three weakly identifiable axes, and reports the rest as non-identifiable rather than guessing.

## Why some features separate better  (signal-to-noise per feature)

### Discriminability by morphology feature - signal-to-noise ratio

*(interactive chart in the HTML version)*

**What it shows.** Area and diameter carry the strongest signal across the parameter sweeps; circularity and perimeter are the noisiest, which matches their lower feature preservation.

**What it motivated (Connects back to feature preservation).** Size features anchor the inversion; shape features add little once size is fixed, consistent with the segmentation audit in Theme 02.

## Which knobs are identifiable?  (leave-one-out recovery)

## Feature to parameter importance  (discriminability heatmap)

## Complete analysis index  (every thesis analysis in this theme)

### Each analysis, what it shows, its thesis label, and the result

| Analysis | What it shows | Thesis label | Key result / status |
|---|---|---|---|
| Surrogate configuration | XGBoost: 500 trees, depth 6, LR 0.05, subsample 0.8, L2=1, 5-fold CV | app:surrogate_cv / tab:xgboost | Forward surrogate (theta to features) |
| Surrogate CV R2 | 5-fold CV R2 of the surrogate per morphology feature | sec:setup_xgboost / fig:surrogate_cv | R2 0.66 (eccentricity) to 0.97 (circularity) |
| Surrogate comparison | XGBoost vs random forest vs Gaussian process on 1,105 samples | tab:surrogate_benchmark | XGBoost best on 5/6 features, mean R2 0.822 |
| Sobol matrix | First- and total-order Sobol indices per (parameter, feature) | sec:res_rq2_2 / fig:rq2_2_drivers | Size driven by width S_T~0.91; J_cc only via interactions |
| Per-parameter Sobol bars | Largest S_T each parameter reaches across features | app:sobol_bars / fig:sobol_bars | Sensitivity ranking w > J_cm > J_cc |
| SA baseline comparison | Parameter rank under 6 measures (Spearman, SRC, XGB, Morris, PAWN, Sobol) | app:sa_baselines / tab:sa_baselines | Rank consistent: w~1, J_cm~2, J_cc~3 |
| LOO recovery R2 | Per-parameter recovered vs true over 1,105 runs, with identifiability tiers | sec:res_rq2_1 / tab:rq2_1_identifiability | w 0.64, J_cm 0.61, J_cc 0.34 (weakly identifiable; shown above) |
| Synthetic inversion diagnostics | Distance-metric, posterior coverage, Wasserstein, k-sensitivity | app:synthetic_diagnostics | Robustness checks |
| LOO scatter | Recovered vs true scatter, one panel per parameter, R2 inset | app:synthetic_diagnostics / fig:loo_scatter | Per-parameter recovery |
| Eccentricity ablation | LOO R2 with 5 features vs with perfect eccentricity added | sec:res_rq2_3 / tab:rq2_3_ceiling | Delta R2 <= 0.05; ceiling is simulator, not segmentation |
| LOO benchmark settings | Deployment matcher settings; ground-truth upper ceiling | sec:setup_loo | Same matcher as real data |
| Active learning POC | Surrogate-selected vs random vs oracle candidate selection | app:active_learning / fig:active_learning_poc | Reduces NN distance to under-covered wells |

**Sources / tools:** tab:rq2_1_identifiability (tau), cpm_discriminability.json, leave-one-out inversion, XGBoost surrogate, tau-registration matcher
