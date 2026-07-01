# Real spheroids, relative shifts.

**Thesis target:** Theme 05 / Drug panel & real-data inference / Appendix I & J.

> The pipeline inverts real morphology to CPM parameters; the inferred shifts on the weakly identifiable axes are read as relative changes, not biophysical effects.

Real spheroid trajectories from reference wells across five patients (seven patient-timepoint series) and a panel of drug conditions are inverted to CPM parameters on the three weakly identifiable axes. The inferred shifts are read as relative, simulation-derived changes, not absolute or biophysical values.

| Metric | Value | Note |
|---|---|---|
| Patients | 5 | Unique donors; 7 patient-timepoint series, 4 in the drug panel. |
| Read as | shifts | Relative change on the weakly identifiable axes, not absolutes. |
| Drug-panel BCR shift | weak | Tau (primary): J_cc shift -1.4, CI [-3.0, +0.2], spans zero. End-state: +4.6, CI [+2.1, +7.0], significant; the signal is in the settled morphology. |
| Reported axes | 3 | the three weakly identifiable axes (width, J_cc, J_cm). |

## The stimulus, before any drug  (the reference every drug shift is measured against)

## Real drug wells, up close  (one frame per mechanism class)

## What the drugs do to morphology  (two dose conditions, over five days)

### Drug response measured automatically from the AI segmenter - three drug conditions, every available timepoint

*(interactive chart in the HTML version)*

**What it shows.** High-dose trametinib collapses the cluster; PD098060 compacts it; low-dose trametinib leaves it intact. Every point is extracted from an AI-segmented frame, with no manual measurement. Switch the feature to see each shape axis respond.

**What it motivated (Feeds the inversion).** This is the observable the inference consumes: a per-condition shape trajectory that the CPM matcher compares against the synthetic library to produce the per-condition parameter shifts.

### Why we trust these real-data features

The real inference spheroids have no human-drawn masks to check against, so there is no real-data agreement heatmap to show here. The reliability guarantee comes from Theme 02: the segmenter was chosen because its six shape numbers agree with human ones on the held-out test set (area and diameter above the 0.85 concordance bar), and the inference uses only those same features. The trust is inherited from that audit, not re-measured on unlabelled real data.

## How each mechanism class works  (target, mechanism, and simulated spheroid effect)

## Drug panel, drug by drug  (inferred delta J_cc with intervals)

## The whole arc, in one line  (what the six themes add up to)

### End to end

99,055 raw brightfield frames, built into a working corpus (Theme 00), are read by a segmenter chosen for feature preservation rather than pixel overlap (Theme 02), because the raw signal limits the finer shape features (Theme 01). The same six features are then measured on a 1,105-run synthetic CPM library (Theme 03), which shows most real spheroids fall outside the simulated world (92% beyond p95). Leave-one-out inversion (Theme 04) finds only three weakly identifiable axes (width, J_cm, J_cc) and four non-identifiable ones, so the real-data drug inference (Theme 05) is read as relative shifts on those axes, not absolute biophysical values. **The honest limit, weak identifiability and thin coverage, is the finding, not a failure.**

## Complete analysis index  (every thesis analysis in this theme)

### Each analysis, what it shows, its thesis label, and the result

| Analysis | What it shows | Thesis label | Key result / status |
|---|---|---|---|
| Tau-registered matcher | Phase-axis tau, z-scored features, Sobol-weighted MAD, k=20, empirical posterior | sec:setup_matching | Primary matcher |
| Worked example (VID1797 F1) | One well: observed trajectory to empirical posterior intervals | app:worked_real_inference / fig:example_inversion_appendix | Shows how data narrows each parameter |
| Boundary & coverage | Neighbours at sweep endpoints; real-to-library NN distance | app:boundary_coverage / fig:boundary_saturation_appendix | ~90% of real spheroids extrapolated |
| Stimulation reproducibility | Per-parameter, how many of the 7 patient-timepoint series shift the same way under stimulation | sec:res_rq3_1 / fig:rq3_1_stability | J_cm & J_cc 7/7 agree, width 3/7 |
| Expected vs observed shift | Baseline vs stimulated medians vs a priori biological prediction | sec:res_rq3_2 / tab:rq3_2_expected | J_cm -30% (7/7), J_cc -7% (7/7) match |
| Drug-class lookup | 23 drugs by mechanism class with targets and expected effects | app:drug_classes / tab:drug_lookup | BTKi, Syk, PI3K, JAK, CXCR4, MEK, NF-kB, ... |
| Drug-panel delta J_cc | Per-drug J_cc shift, by class, bootstrap CI; tau vs end-state matcher | app:drug_panel_jcc / fig:h33_drug_panel_appendix | tau -1.4 CI [-3.0, +0.2] weak; end-state +4.6 CI [+2.1, +7.0] significant |

**Sources / tools:** real_data_inference_report.ipynb, drug panel, tau-registration matcher, bootstrap CIs, 5 patients / 7 series
