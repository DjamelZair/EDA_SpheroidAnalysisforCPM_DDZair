# From real spheroids to mechanism.

**Thesis target:** Theme 05 / Drug panel & real-data inference / Appendix I & J.

> The pipeline inverts real morphology to CPM parameters, and the inferred shifts track stimulation and drug class across patients.

Real spheroid trajectories from 152 control wells and a panel of drug conditions are inverted to CPM parameters on the three recoverable axes. The inferred shifts are read as relative changes, not absolute values, and the drug-class pattern is consistent with the known biology.

| Metric | Value | Note |
|---|---|---|
| Control wells | 152 | Reference distribution across patients. |
| Read as | shifts | Relative change on identifiable axes, not absolutes. |
| Strongest rescue | BTKi | Significant J_cc shift; CXCR4 and JAK none. |
| Reported axes | 3 | width, J_cc, J_cm only. |

## What the drugs do to morphology  (three dose conditions)

### High-dose trametinib collapses the cluster - MEK inhibitor, 50 uM

![](../assets/cll/figures/morphology/drug_strip_high_dose.png)

**What it shows.** The cluster loses cohesion and breaks apart over the time course.

**What it motivated (Drug effect is mechanistic, not just size).** A large, end-state-specific shift in the inferred contact parameters.

### PD098060 compacts the cluster - MEK pathway, 100 uM

![](../assets/cll/figures/morphology/drug_strip_pd098060.png)

**What it shows.** The cluster stays cohesive but contracts, a different morphological signature from high-dose trametinib.

**What it motivated (Separable drug signatures).** Distinct drugs leave distinct, separable trajectories.

### Feature trajectories under treatment - extracted automatically per condition

![](../assets/cll/figures/morphology/feature_trajectories.png)

**What it shows.** Per-condition shape trajectories, the observable the matcher compares against the synthetic library.

**What it motivated (Feeds the inversion).** These trajectories drive the inversion that produces the per-condition parameter shifts.

### Feature agreement on the real data - AI-derived vs reference

![](../assets/cll/figures/morphology/icc_ccc_heatmap.png)

**What it shows.** Agreement between AI-derived and reference shape numbers on the real spheroids, the same reliability check applied in Theme 02.

**What it motivated (Closes the loop with RQ1).** Confirms the real-data features used for inversion are the reliable ones.

**Sources / tools:** real_data_inference_report.ipynb, drug panel, tau-registration matcher, bootstrap CIs, 152 control wells
