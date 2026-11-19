**English | [Русский](FIGURES.ru.md)**

[← Blood Plasma Study](../README.md) · [Guide index](README.md)

<div align="center">

# Figures gallery

</div>

Every figure the repository holds is either embedded on a page of this guide or listed below with the folder it lives in. Data charts (plots, photographs) are shown as they are; the old flow-chart PNGs of the previous README are redrawn as SVG pairs, and the originals stay in place. Raw photographs (`original_research/data/**/photos`) are data, not figures, and are not listed one by one. Donors appear only as anonymous codes.

## Schemas redrawn as SVG

| Figure | What it shows | Shown on | Original |
|---|---|---|---|
| [`redraw-overview.en.svg`](assets/diagrams/redraw-overview.en.svg) | Research overview: donors to reports; channel 19 and 21 as the hypothesis | [STUDY](STUDY.md) | [`original_research/charts/mermaid/root_1.png`](../original_research/charts/mermaid/root_1.png) |
| [`redraw-patent.en.svg`](assets/diagrams/redraw-patent.en.svg) | Patent application KZ 2025/1095.1 and the studies that use the emitters | [PUBLICATIONS](PUBLICATIONS.md) | [`original_research/charts/mermaid/root_2.png`](../original_research/charts/mermaid/root_2.png) |
| [`redraw-dates.en.svg`](assets/diagrams/redraw-dates.en.svg) | Seven donor collection dates and four dated reports | [RESULTS](RESULTS.md) | [`original_research/charts/mermaid/root_3.png`](../original_research/charts/mermaid/root_3.png) |
| [`redraw-timelapse.en.svg`](assets/diagrams/redraw-timelapse.en.svg) | Planned time-lapse imaging system | [METHODS](METHODS.md) | [`original_research/charts/mermaid/root_4.png`](../original_research/charts/mermaid/root_4.png) |
| [`redraw-pipeline.en.svg`](assets/diagrams/redraw-pipeline.en.svg) | Analysis pipeline: CV, LLM, comparison, statistics | [METHODS](METHODS.md) | [`original_research/charts/mermaid/root_5.png`](../original_research/charts/mermaid/root_5.png) |
| [`redraw-protocol.en.svg`](assets/diagrams/redraw-protocol.en.svg) | Experimental protocol from blood collection to reports | [METHODS](METHODS.md) | [`original_research/charts/mermaid/root_6.png`](../original_research/charts/mermaid/root_6.png) |

## Charts and diagrams shown on the pages

| Figure | What it shows | Shown on |
|---|---|---|
| [`original_research/charts/photos_by_patient.png`](../original_research/charts/photos_by_patient.png) | Pie chart of 101 photographs by anonymous donor code (Patient 01-07, shares only) | [RESULTS](RESULTS.md) |
| [`original_research/charts/comparative_results.png`](../original_research/charts/comparative_results.png) | Control against channel 19 and channel 21: the previous README's summary chart | [RESULTS](RESULTS.md) |
| [`original_research/charts/channel_effects.png`](../original_research/charts/channel_effects.png) | Channel effects: the previous README's summary chart | [RESULTS](RESULTS.md) |

## Previous README diagrams kept as files

| Figure | What it shows | Folder |
|---|---|---|
| [`original_research/charts/mermaid/data_1.png`](../original_research/charts/mermaid/data_1.png) | Pie chart of photographs by donor code (same data as photos_by_patient.png) | `original_research/charts/mermaid` |
| [`original_research/charts/mermaid/data_2.png`](../original_research/charts/mermaid/data_2.png) | Three columns, control, channel 19, channel 21, with the previous README's clot count, area, texture, edge and LLM values (claims, see Evidence) | `original_research/charts/mermaid` |
| [`original_research/charts/mermaid/data_3.png`](../original_research/charts/mermaid/data_3.png) | Plasma samples to three conditions to the clot count and area quoted by the previous README (claims, see Evidence) | `original_research/charts/mermaid` |
| [`original_research/charts/mermaid/data_4.png`](../original_research/charts/mermaid/data_4.png) | Collection dates with photo counts per donor code (P01 13, P02 25, P03 16, P04 4, P05 10, P06 3, P07 30) | `original_research/charts/mermaid` |
| [`original_research/charts/mermaid/osf_1.png`](../original_research/charts/mermaid/osf_1.png) | OSF preregistration tree: hypothesis, sampling plan, analysis plan, variables | `original_research/charts/mermaid` |

## Report charts

Each report page of the repository embeds its own charts; they are listed here with the report that holds them.

| Figure | What it shows | Report |
|---|---|---|
| [`original_research/reports/2026-02-25_ai-analysis/chart_clot_count.png`](../original_research/reports/2026-02-25_ai-analysis/chart_clot_count.png) | Average fibrin clot count per image by channel | [`2026-02-25_ai-analysis`](../original_research/reports/2026-02-25_ai-analysis/report_en.md) |
| [`original_research/reports/2026-02-25_ai-analysis/chart_clot_area.png`](../original_research/reports/2026-02-25_ai-analysis/chart_clot_area.png) | Total clot area (percent of image) by channel | [`2026-02-25_ai-analysis`](../original_research/reports/2026-02-25_ai-analysis/report_en.md) |
| [`original_research/reports/2026-02-25_ai-analysis/chart_siglip2_stages.png`](../original_research/reports/2026-02-25_ai-analysis/chart_siglip2_stages.png) | Coagulation stage scores by channel (SigLIP2 zero-shot) | [`2026-02-25_ai-analysis`](../original_research/reports/2026-02-25_ai-analysis/report_en.md) |
| [`original_research/reports/2026-02-25_ai-analysis/chart_cv_metrics.png`](../original_research/reports/2026-02-25_ai-analysis/chart_cv_metrics.png) | Classical CV metrics by channel | [`2026-02-25_ai-analysis`](../original_research/reports/2026-02-25_ai-analysis/report_en.md) |
| [`original_research/reports/2026-02-25_ai-analysis/chart_deltas.png`](../original_research/reports/2026-02-25_ai-analysis/chart_deltas.png) | Metric deltas, treatment against control | [`2026-02-25_ai-analysis`](../original_research/reports/2026-02-25_ai-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_clot_frequency.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_clot_frequency.png) | Photos with visible clots (percent) by channel | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_stage_distribution.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_stage_distribution.png) | Coagulation stage distribution by channel (n=55) | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_patient_heatmap.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_patient_heatmap.png) | Peak coagulation stage per donor code | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_method_comparison.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_method_comparison.png) | Method comparison: detecting the gradient channel 19 > control > channel 21 | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_lifecycle.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_lifecycle.png) | One donor code, channel 19: the whole coagulation lifecycle in sequence | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-02-26_llm-vision-analysis/chart_patient07_gradient.png`](../original_research/reports/2026-02-26_llm-vision-analysis/chart_patient07_gradient.png) | Donor code 07: clot frequency with channel assignment inferred from EXIF (n=15) | [`2026-02-26_llm-vision-analysis`](../original_research/reports/2026-02-26_llm-vision-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_ch19_winrate.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_ch19_winrate.png) | Channel 19 win rate by provider (blinded comparative) | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_stage_distribution.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_stage_distribution.png) | Coagulation stage distribution by channel | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_per_patient.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_per_patient.png) | Per-donor-code channel 19 win rate | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_difference_rating.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_difference_rating.png) | Difference rating, batch against comparative blinded | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_blinded_vs_unblinded.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_blinded_vs_unblinded.png) | Blinded against unblinded channel 19 identification rates | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_clot_detection.png`](../original_research/reports/2026-03-12_comparative-llm-analysis/charts/chart_clot_detection.png) | Clot detection rates by channel | [`2026-03-12_comparative-llm-analysis`](../original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md) |
| [`original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_ch19_winrate.png`](../original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_ch19_winrate.png) | Channel 19 win rate, CV models against LLM (19 comparative sets) | [`2026-03-14_cv-ml-analysis`](../original_research/reports/2026-03-14_cv-ml-analysis/report_en.md) |
| [`original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_cv_vs_llm.png`](../original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_cv_vs_llm.png) | All methods, channel 19 win rate (19 comparative sets) | [`2026-03-14_cv-ml-analysis`](../original_research/reports/2026-03-14_cv-ml-analysis/report_en.md) |
| [`original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_per_patient.png`](../original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_per_patient.png) | DINOv2 probe: per-donor-code channel 19 win count (leave-patient-out) | [`2026-03-14_cv-ml-analysis`](../original_research/reports/2026-03-14_cv-ml-analysis/report_en.md) |
| [`original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_multichain.png`](../original_research/reports/2026-03-14_cv-ml-analysis/charts/chart_multichain.png) | Multi-chain pipeline: cropping the plasma degrades the signal | [`2026-03-14_cv-ml-analysis`](../original_research/reports/2026-03-14_cv-ml-analysis/report_en.md) |

## Mirror folder and per-donor folders

| Figures | What they are | Folder |
|---|---|---|
| 32 PNG | Mermaid renders of the diagrams of the mirror folder's README, issue and protocol texts (`advreadme_*`, `advdata_*`, `advp01_*`..`advp07_*`, `issue_*`); the mirror repeats the same material as the root | `ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/charts/mermaid` |
| 16 PNG | One photo-distribution pie chart per donor folder, by condition (`p01_*`..`p07_*`); listed as data of the donor folders, not reproduced | `original_research/data/patient-0N/photos/mermaid` |
| JPG, HEIC | The raw and converted photographs themselves | `original_research/data/patient-0N/photos/{jpg,original}` (raw data, see [Data](DATA.md)) |

## Generated by this restructuring

The banner, the six study diagrams (`study-design`, `units`, `claimed-vs-shown`, `blinded-results`, `timeline`), the navigation icons and the six redraws above live in `guide/assets/`, are built by `tools/build_visuals.py` and `tools/build_redraws.py`, and carry no donor-level data.
