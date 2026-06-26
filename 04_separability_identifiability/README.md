# Which knobs can we read back?

**Thesis target:** Theme 04 / Separability & identifiability / Appendix D to H.

> Only three of the seven parameters can be recovered from morphology. The rest are entangled, and the analysis says so honestly.

Leave-one-out inversion on the 1,105-run library measures how well each CPM parameter is recovered from morphology (R squared of recovered vs true). Cell-medium adhesion, target volume and cell-cell adhesion are recoverable; the others are not. These are the verified numbers from the canonical benchmark, not the optimistic error metric used elsewhere.

| Metric | Value | Note |
|---|---|---|
| Recoverable | 3 of 7 | J_cm, width, J_cc cross the R2 0.30 line. |
| Best recovery | 0.62 | Cell-medium adhesion (J_cm), LOO R2. |
| Library size | 1,105 | Saltelli runs used for the benchmark. |
| Unidentifiable | 4 | lambda, temperature, contact range, neighbour order. |

## How well each parameter is recovered  (leave-one-out R squared, verified)

### Leave-one-out recovery (R squared) - gold = recoverable (R2 >= 0.30)

*(interactive chart in the HTML version)*

**What it shows.** Cell-medium adhesion (0.62), target volume (0.54) and cell-cell adhesion (0.38) are recoverable; volume elasticity, temperature, contact range and neighbour order sit below the line. Neighbour order is effectively zero.

**What it motivated (Decision: report only identifiable axes).** The pipeline reports estimates and uncertainty only for the three recoverable axes, and reports the rest as unidentified rather than guessing.

## Why some features separate better  (signal-to-noise per feature)

### Discriminability by morphology feature - signal-to-noise ratio

*(interactive chart in the HTML version)*

**What it shows.** Area and diameter carry the strongest signal across the parameter sweeps; circularity and perimeter are the noisiest, which matches their lower segmentation fidelity.

**What it motivated (Connects back to feature fidelity).** Size features anchor the inversion; shape features add little once size is fixed, consistent with the segmentation audit in Theme 02.

**Sources / tools:** identifiability_loo.csv, cpm_discriminability.json, leave-one-out inversion, XGBoost surrogate, tau-registration matcher
