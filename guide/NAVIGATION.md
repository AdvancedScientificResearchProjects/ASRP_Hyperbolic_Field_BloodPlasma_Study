**English | [Русский](NAVIGATION.ru.md)**

[← Blood Plasma Study](../README.md) · [Guide index](README.md)

<div align="center">

# Navigation and structure

</div>

## Navigation and structure

Where to start depends on the question:

| If you want | Read |
|---|---|
| What the study is and how it was run | [The study](STUDY.md), then `original_research/reports/experiment_protocol_en.md` |
| Whether the claims hold | [Evidence](EVIDENCE.md), each row with its source path |
| The numbers as reported, and how to read them | [Results](RESULTS.md) |
| Every chart and diagram, with its folder | [Figures gallery](FIGURES.md) |
| The photographs and counts | [Data and photographs](DATA.md), then `original_research/data/` |
| The analysis code and the four dated reports | [Analysis methods](METHODS.md), then `original_research/scripts/` and `original_research/reports/` |
| Patent, registration, paper | [Publications, patent, preregistration](PUBLICATIONS.md) |
| What is unresolved | [Open questions](OPEN.md) |

The repository has three parts. `original_research/` holds everything the experiment produced (data, code, results, reports, charts). `ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/` is a mirror of the programme hub: the programme README and the issue documents. It is not byte-identical to the root README (a divergent copy, <!--n:mirror_files-->47<!--/n--> files), so the root and the mirror can disagree. `OSF_PREREGISTRATION.md` holds the registration text. The front page and `guide/` were added on 2026-11-19; no existing file was moved, changed or deleted, and the previous README is kept byte for byte in [`archive/`](../archive/README_2026-11-19_pre-showcase.md).

### Folder tree

<!-- tree -->
```
Hyperbolic_Field_BloodPlasma_Study/
├── README.md                               # front page (English)
├── README.ru.md                            # front page (Russian)
├── guide/                                  # detail pages X.md + X.ru.md; assets/ = generated SVG
├── archive/                                # the previous README, kept byte for byte
├── tools/                                  # showcase tooling: facts, visuals, excerpts, no-loss check
├── tests/                                  # regression gate for the showcase
├── OSF_PREREGISTRATION.md                  # the OSF preregistration text (bilingual)
├── original_research/                      # all data, code, results and reports
│   ├── README.md                           # entry to the research folder
│   ├── data/                               # 7 donor folders: photos, protocol PDFs, per-donor logs (sensitive)
│   ├── processed/                          # combined per-donor JSON
│   ├── results/                            # 47 LLM result files in 48 run folders
│   ├── reports/                            # protocol + 4 dated analysis reports (EN and RU)
│   ├── scripts/                            # 22 Python files: llm_analysis/, cv_analysis/
│   ├── notebooks/                          # cv_analysis.ipynb, 42.9 MB
│   ├── charts/                             # 3 summary charts + 11 Mermaid PNG
│   ├── en/                                 # English documentation hub
│   └── ru/                                 # Russian documentation hub
└── ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/  # mirror of the programme hub: README + 6 issue documents (47 files)
```
<!-- /tree -->

### Quick links

- [Back to the front page](../README.md)
- [Guide index](README.md)
- [Patent connection](PUBLICATIONS.md#patent-connection)
- [Key results](RESULTS.md#results-as-reported)
- [Photo gallery and data](DATA.md#data-and-photographs)
- [Reports](METHODS.md#reports)
- [Research team](ECOSYSTEM.md#research-team)
- [Active issues](ECOSYSTEM.md#active-issues-and-tasks)
- [ASRP ecosystem](ECOSYSTEM.md#asrp-ecosystem)
- [Contact](ETHICS.md#contact)

## Reports and issue documents

The four dated reports are in `original_research/reports/` (each with an English and a Russian file) and are listed with links on [Analysis methods](METHODS.md#reports). The issue documents (`ISSUE_1_UPDATED.md` to `ISSUE_8_UPDATED.md`, <!--n:issue_docs-->6<!--/n--> files) hold the protocol (issue 3), the programme hub (issue 2), the biochemical plan (issue 5), the photography system (issue 6) and the publication plan (issue 8); they are in the mirror folder `ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/`.
