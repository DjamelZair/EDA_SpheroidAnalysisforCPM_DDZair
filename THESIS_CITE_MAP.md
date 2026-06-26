# Thesis cite map

Handoff for the thesis text agent. Each curated analysis theme is published on GitHub Pages
and maps to the LaTeX appendix / section it supports. Repoint the appendix links from the old
Google Drive file to these fixed URLs.

**Pages base URL:** https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/

| Theme | Page URL | Supports (LaTeX label) | Thesis section |
|---|---|---|---|
| Landing (index) | `<base>/` | (entry point) | Appendix A to J overview |
| 01 Image & intensity EDA | `<base>/01_image_intensity_eda/` | `appendix:data:eda` | Appendix A.1 (replaces the Drive link) |
| 02 Segmentation & feature fidelity | `<base>/02_segmentation/` | `app:segmentation` family | Appendix B, RQ1 |
| 03 Simulation library | `<base>/03_simulation_library/` | `sec:setup_sim_data`, `app:synthetic_diagnostics` | Appendix C and F |
| 04 Separability & identifiability | `<base>/04_separability_identifiability/` | identifiability appendices (see note) | Appendix D to H, RQ2 |
| 05 Drug panel & real-data inference | `<base>/05_drug_realdata/` | `app:real_inference_diagnostics`, drug panel | Appendix I and J, RQ3 |

Full URLs:
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/01_image_intensity_eda/
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/02_segmentation/
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/03_simulation_library/
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/04_separability_identifiability/
- https://djamelzair.github.io/EDA_SpheroidAnalysisforCPM_DDZair/05_drug_realdata/

## The Appendix A.1 fix
The appendix currently cites a Google Drive file at the `appendix:data:eda` itemize. Replace
that single `\href{...drive...}{Full Data Exploratory Analysis.}` item with the Theme 01 URL
above (and optionally the landing URL for the full set).

## Note on Theme 04
Theme 04 is the **synthetic** identifiability analysis (leave-one-out recovery R-squared on the
1,105-run library), so its natural home is the identifiability appendices (D to H). The earlier
brief grouped Themes 04 and 05 both under `app:real_inference_diagnostics`; if that single
anchor is preferred, Theme 04 can point there, but the content is synthetic identifiability,
not real-data inference. Pick the label that matches the appendix structure and adjust this row.

## Reproducibility
The site regenerates from `build_site.py` (pages), `make_theme_data.py` (chart data from the
analysis CSVs), and `figtools.py` (microscopy figures recoloured into the theme). Numbers come
from the canonical sources: `cpm_sweeps.json`, `identifiability_loo.csv` (verified LOO R2:
J_cm 0.62, width 0.54, J_cc 0.38), and the segmentation feature-validation tables.
