# Eight candidates, one winner.

**Thesis target:** Theme 02 / Segmentation & feature fidelity / Appendix B.

> Pixel overlap cannot tell the candidates apart. The metric that matters for the downstream pipeline can, and it exposes a structural failure mode in three of them.

Eight segmenters were compared on the same 45-image test set: a rule-based baseline, three nnU-Net variants, two SAM2 variants, a heavy-augmentation U-Net, and a pseudo-label pretrain. The winner is chosen on the metric the next stage consumes: **do the AI-derived shape numbers agree with the human-annotated ones?** By that measure the heavy-augmentation U-Net wins by a wide margin, even though three models edge it on pixel overlap.

| Metric | Value | Note |
|---|---|---|
| Chosen model | U-Net | Heavy augmentation; only model crossing the reliability bar. |
| Models compared | 8 | All on the same 45-image test set. |
| Best pixel Dice | 0.829 | U-Net; nnU-Net essentially tied at 0.831. |
| Reliability bar | &ge; 0.85 | Concordance threshold from the radiomics standard (IBSI). |

### What the chosen segmenter produces - real frames, three drug conditions, three days

![](fig/overlay_dark.png)

**What it shows.** The gold outline is the U-Net's call on frames it never saw in training; the boxes show the shape numbers (area, circularity, solidity) extracted from each.

**What it motivated (Why feature fidelity, not pixels).** The unit of evaluation is these extracted numbers, not the pixel mask.

## Model leaderboard  (switch the metric)

### Ranking flips with the metric - click to switch

*(interactive chart in the HTML version)*

**What it shows.** Pixel overlap is nearly flat (0.755 to 0.829) and picks the U-Net by a hair. Shape-number agreement ranks the U-Net first by a wide margin and is the only metric that reflects what the next stage consumes.

**What it motivated (Decision: rank by feature fidelity).** The segmenter is selected on shape-number agreement (Lin's CCC against the six CPM features), not pixel Dice. The heavy-aug U-Net is the only model above the 0.85 bar.

### Per-feature reliability scoreboard - 8 models x 6 shape numbers

![](../assets/cll/figures/segmentation/icc_ccc_heatmap.png)

**What it shows.** Each cell is the agreement between AI-derived and human-derived value of one shape number. Gold-outlined cells cross the 0.85 bar. Only the U-Net crosses, on area and diameter; roundness and elongation are unreliable for almost every model.

**What it motivated (Decision: operational feature set).** Sets the operational feature set for RQ3: area, diameter, solidity, perimeter, circularity; eccentricity is dropped, perimeter is U-Net-only.

## Cleanup impact  (overlap recovers, agreement does not)

### Pixel overlap with vs without cleanup - a small post-processing step

*(interactive chart in the HTML version)*

**What it shows.** The chosen U-Net (heavy aug.) is shown for reference: its masks need no cleanup, so the two bars are identical at 0.829. A morphological cleanup lifts nnU-Net pixel overlap by up to +0.044; the rule-based baseline barely benefits because its masks are already sparse.

**What it motivated (Negative result: cleanup is cosmetic for fidelity).** On the metric that matters for the next stage this cleanup does not move the needle: it rescues pixel overlap, not shape-number reliability.

## Hardest case  (a fully fragmented spheroid)

### When the spheroid disintegrates - VID3201 F3, trametinib 50 uM, full time-lapse

![](fig/hardest_dark.png)

**What it shows.** Under high-dose drug the spheroid breaks into many pieces. Pixel overlap drops for every model; area and diameter stay reliable while roundness and elongation collapse.

**What it motivated (Validates the feature-fidelity audit).** This split is the entire reason the audit was needed, and why F3 is reported separately rather than excluded.

### Classical pipeline on the hardest frame - top 10 of the classical preproc / segmenter sweep

*(interactive chart in the HTML version)*

**What it shows.** This is the classical-pipeline sweep (the deep models, including the heavy-aug U-Net, are in the showcase above). Even the best classical combination reaches only about 0.45 Dice on this frame; no configuration rescues it.

**What it motivated (Bounds the hardest case).** Confirms F3 is a genuine ceiling, not a tuning artefact.

**Sources / tools:** 05_feature_validation.ipynb, ICC(3,1) + Lin's CCC, per_feature_error.csv, seg_postproc.json, seg_f3.json, U-Net / SAM2 / nnU-Net
