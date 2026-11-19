#!/usr/bin/env python3
"""Writes guide/FIGURES.md and guide/FIGURES.ru.md: the gallery of every figure the repository holds.
    python3 tools/build_figures_page.py
Every PNG/JPG/SVG of the pre-showcase tree is either embedded on a page, listed here, or (raw photographs and the
per-donor photo folders) deliberately left out as data. tests/test_no_loss.py checks the list against git."""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = "original_research/charts/mermaid/"
RP = "original_research/reports/"
C = "original_research/charts/"
# (path or paths, EN what, RU what, EN where, RU where)
MR = "ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/charts/mermaid/"
REDRAW = [
 (M + "root_1.png", "Research overview: donors to reports; channel 19 and 21 as the hypothesis", "Обзор исследования: от доноров до отчётов; каналы 19 и 21 как гипотеза", "redraw-overview", "STUDY"),
 (M + "root_2.png", "Patent application KZ 2025/1095.1 and the studies that use the emitters", "Патентная заявка KZ 2025/1095.1 и исследования, где используются излучатели", "redraw-patent", "PUBLICATIONS"),
 (M + "root_3.png", "Seven donor collection dates and four dated reports", "Семь дат сбора по донорам и четыре датированных отчёта", "redraw-dates", "RESULTS"),
 (M + "root_4.png", "Planned time-lapse imaging system", "Планируемая система покадровой съёмки", "redraw-timelapse", "METHODS"),
 (M + "root_5.png", "Analysis pipeline: CV, LLM, comparison, statistics", "Конвейер анализа: CV, LLM, сравнение, статистика", "redraw-pipeline", "METHODS"),
 (M + "root_6.png", "Experimental protocol from blood collection to reports", "Протокол эксперимента от забора крови до отчётов", "redraw-protocol", "METHODS"),
 (M + "data_1.png", "Photographs by anonymous donor code (pie, shares and counts)", "Фотографии по анонимным кодам доноров (круг, доли и числа)", "redraw-data-photos", "DATA"),
 (M + "data_2.png", "Three condition columns with the previous README's quoted metrics (claimed only)", "Три колонки условий с приведёнными метриками прежнего README (только заявлено)", "redraw-data-metrics", "RESULTS"),
 (M + "data_3.png", "Samples to three conditions to the quoted clot count and area (claimed only)", "Образцы, три условия, приведённые число сгустков и площадь (только заявлено)", "redraw-data-flow", "RESULTS"),
 (M + "data_4.png", "Collection dates with photograph counts per donor code", "Даты сбора с числом фотографий по кодам доноров", "redraw-data-dates", "DATA"),
 (M + "osf_1.png", "OSF preregistration tree: hypothesis, sampling, analysis, variables", "Дерево регистрации OSF: гипотеза, выборка, анализ, переменные", "redraw-osf", "PUBLICATIONS"),
 (MR + "issue_2_1.png", "Research programme tree: four studies and their parts (mirror, issue 2)", "Дерево программы: четыре исследования и их части (зеркало, задача 2)", "redraw-program", "ECOSYSTEM"),
 (MR + "issue_2_2.png", "Team members linked to projects (mirror, issue 2)", "Участники команды и проекты (зеркало, задача 2)", "redraw-team", "ECOSYSTEM"),
 (MR + "issue_2retry_1.png", "Data, analysis and team structure (mirror, issue 2)", "Структура данных, анализа и команды (зеркало, задача 2)", "redraw-repo", "ECOSYSTEM"),
 (MR + "issue_2_4.png", "Programme roadmap, January to future 30 donors (mirror, issue 2)", "Дорожная карта программы, от января до будущих 30 доноров (зеркало, задача 2)", "redraw-roadmap", "ECOSYSTEM"),
 (MR + "issue_3_1.png", "Eleven-step blood plasma protocol flow (mirror, issue 3)", "Протокол по плазме крови в одиннадцать шагов (зеркало, задача 3)", "redraw-donor-flow", "METHODS"),
 (MR + "issue_5_1.png", "Biochemical integration flow (mirror, issue 5)", "Схема интеграции биохимии (зеркало, задача 5)", "redraw-biochem", "METHODS"),
 (MR + "issue_6_1.png", "Time-lapse imaging flow, issue 6 variant (mirror, issue 6)", "Схема покадровой съёмки, вариант задачи 6 (зеркало, задача 6)", "redraw-issue6-imaging", "METHODS"),
 (MR + "issue_8_1.png", "Publication plan as a Gantt chart (mirror, issue 8)", "План публикации, диаграмма Ганта (зеркало, задача 8)", "redraw-gantt", "PUBLICATIONS"),
]
# mirror file -> (kind, reference). kinds: same-bytes, same-diagram, redrawn (own row above), pie, withheld
MIRROR_MAP = [
 ("advreadme_1.png", "same-bytes", "root_1.png"), ("advreadme_2.png", "same-bytes", "root_2.png"), ("advreadme_4.png", "same-bytes", "root_4.png"),
 ("advreadme_6.png", "same-bytes", "root_6.png"), ("issue_1_1.png", "same-bytes", "root_6.png"),
 ("advreadme_3.png", "same-diagram", "root_3.png"), ("advreadme_5.png", "same-diagram", "root_5.png"), ("issue_1_2.png", "same-diagram", "root_5.png"),
 ("advdata_2.png", "same-diagram", "data_4.png"), ("advdataretry_1.png", "same-diagram", "data_1.png"),
 ("issue_2_1.png", "redrawn", "redraw-program"), ("issue_2_2.png", "redrawn", "redraw-team"), ("issue_2retry_1.png", "redrawn", "redraw-repo"),
 ("issue_2_4.png", "redrawn", "redraw-roadmap"), ("issue_3_1.png", "redrawn", "redraw-donor-flow"), ("issue_5_1.png", "redrawn", "redraw-biochem"),
 ("issue_6_1.png", "redrawn", "redraw-issue6-imaging"), ("issue_8_1.png", "redrawn", "redraw-gantt"),
 ("advp01_1.png", "pie", ""), ("advp02_1.png", "pie", ""), ("advp03_1.png", "pie", ""), ("advp04retry_1.png", "pie", ""),
 ("advp05_1.png", "pie", ""), ("advp06_1.png", "pie", ""), ("advp07_1.png", "pie", ""),
 ("advp01_2.png", "withheld", ""), ("advp02_2.png", "withheld", ""), ("advp03_2.png", "withheld", ""), ("advp04_2.png", "withheld", ""),
 ("advp05_2.png", "withheld", ""), ("advp06_2.png", "withheld", ""), ("advp07_2.png", "withheld", ""),
]
SHOWN = [
 (C + "photos_by_patient.png", "Pie chart of 101 photographs by anonymous donor code (Patient 01-07, shares only)", "Круговая диаграмма 101 фотографии по анонимным кодам доноров (Пациент 01-07, только доли)", "RESULTS"),
 (C + "comparative_results.png", "Control against channel 19 and channel 21: the previous README's summary chart", "Контроль против каналов 19 и 21: сводная диаграмма прежнего README", "RESULTS"),
 (C + "channel_effects.png", "Channel effects: the previous README's summary chart", "Эффекты каналов: сводная диаграмма прежнего README", "RESULTS"),
]
LISTED = [
 ([M + "data_1.png"], "Pie chart of photographs by donor code (same data as photos_by_patient.png)", "Круговая диаграмма фотографий по кодам доноров (те же данные, что в photos_by_patient.png)", C + "mermaid"),
 ([M + "data_2.png"], "Three columns, control, channel 19, channel 21, with the previous README's clot count, area, texture, edge and LLM values (claims, see Evidence)", "Три колонки, контроль, канал 19, канал 21, со значениями прежнего README: число сгустков, площадь, текстура, край, LLM (утверждения, см. Свидетельства)", C + "mermaid"),
 ([M + "data_3.png"], "Plasma samples to three conditions to the clot count and area quoted by the previous README (claims, see Evidence)", "Образцы плазмы, три условия, число сгустков и площадь из прежнего README (утверждения, см. Свидетельства)", C + "mermaid"),
 ([M + "data_4.png"], "Collection dates with photo counts per donor code (P01 13, P02 25, P03 16, P04 4, P05 10, P06 3, P07 30)", "Даты сбора с числом фотографий по кодам доноров (P01 13, P02 25, P03 16, P04 4, P05 10, P06 3, P07 30)", C + "mermaid"),
 ([M + "osf_1.png"], "OSF preregistration tree: hypothesis, sampling plan, analysis plan, variables", "Дерево предварительной регистрации OSF: гипотеза, план выборки, план анализа, переменные", C + "mermaid"),
]
REPORTS = [
 ("2026-02-25_ai-analysis", [("chart_clot_count.png", "Average fibrin clot count per image by channel", "Среднее число фибриновых сгустков на снимок по каналам"),
   ("chart_clot_area.png", "Total clot area (percent of image) by channel", "Суммарная площадь сгустков (процент снимка) по каналам"),
   ("chart_siglip2_stages.png", "Coagulation stage scores by channel (SigLIP2 zero-shot)", "Оценки стадий свёртывания по каналам (SigLIP2 zero-shot)"),
   ("chart_cv_metrics.png", "Classical CV metrics by channel", "Классические метрики CV по каналам"),
   ("chart_deltas.png", "Metric deltas, treatment against control", "Дельты метрик, воздействие против контроля")]),
 ("2026-02-26_llm-vision-analysis", [("chart_clot_frequency.png", "Photos with visible clots (percent) by channel", "Доля снимков с видимыми сгустками (процент) по каналам"),
   ("chart_stage_distribution.png", "Coagulation stage distribution by channel (n=55)", "Распределение стадий свёртывания по каналам (n=55)"),
   ("chart_patient_heatmap.png", "Peak coagulation stage per donor code", "Пиковая стадия свёртывания по кодам доноров"),
   ("chart_method_comparison.png", "Method comparison: detecting the gradient channel 19 > control > channel 21", "Сравнение методов: обнаружение градиента канал 19 > контроль > канал 21"),
   ("chart_lifecycle.png", "One donor code, channel 19: the whole coagulation lifecycle in sequence", "Один код донора, канал 19: весь жизненный цикл свёртывания по порядку"),
   ("chart_patient07_gradient.png", "Donor code 07: clot frequency with channel assignment inferred from EXIF (n=15)", "Код донора 07: частота сгустков при распределении по каналам, выведенном из EXIF (n=15)")]),
 ("2026-03-12_comparative-llm-analysis/charts", [("chart_ch19_winrate.png", "Channel 19 win rate by provider (blinded comparative)", "Доля выбора канала 19 по провайдерам (слепое сравнение)"),
   ("chart_stage_distribution.png", "Coagulation stage distribution by channel", "Распределение стадий свёртывания по каналам"),
   ("chart_per_patient.png", "Per-donor-code channel 19 win rate", "Доля выбора канала 19 по кодам доноров"),
   ("chart_difference_rating.png", "Difference rating, batch against comparative blinded", "Оценка различий: пакетный против слепого сравнительного режима"),
   ("chart_blinded_vs_unblinded.png", "Blinded against unblinded channel 19 identification rates", "Доли распознавания канала 19: слепой против неслепого режима"),
   ("chart_clot_detection.png", "Clot detection rates by channel", "Доли обнаружения сгустков по каналам")]),
 ("2026-03-14_cv-ml-analysis/charts", [("chart_ch19_winrate.png", "Channel 19 win rate, CV models against LLM (19 comparative sets)", "Доля выбора канала 19: модели CV против LLM (19 сравнительных наборов)"),
   ("chart_cv_vs_llm.png", "All methods, channel 19 win rate (19 comparative sets)", "Все методы, доля выбора канала 19 (19 сравнительных наборов)"),
   ("chart_per_patient.png", "DINOv2 probe: per-donor-code channel 19 win count (leave-patient-out)", "Зонд DINOv2: число выборов канала 19 по кодам доноров (leave-patient-out)"),
   ("chart_multichain.png", "Multi-chain pipeline: cropping the plasma degrades the signal", "Многоцепочечный конвейер: обрезка плазмы ухудшает сигнал")]),
]
MIRROR = "ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/charts/mermaid"


def build(lang):
    en = lang == "en"
    suf = "" if en else ".ru"
    L = []
    a = L.append
    a("**English | [Русский](FIGURES.ru.md)**" if en else "**[English](FIGURES.md) | Русский**")
    a("")
    a("[← Blood Plasma Study](../README.md) · [Guide index](README.md)" if en else "[← Blood Plasma Study](../README.ru.md) · [Указатель гида](README.ru.md)")
    a("")
    a('<div align="center">\n\n# ' + ("Figures gallery" if en else "Галерея рисунков") + "\n\n</div>\n")
    a("Every figure the repository holds is either embedded on a page of this guide or listed below with the folder it lives in. "
      "Data charts (plots, photographs) are shown as they are; the old flow-chart PNGs of the previous README are redrawn as SVG pairs, and the originals stay in place. "
      "Raw photographs (`original_research/data/**/photos`) are data, not figures, and are not listed one by one. Donors appear only as anonymous codes."
      if en else
      "Каждый рисунок репозитория либо встроен в страницу гида, либо перечислен ниже с папкой, где он лежит. "
      "Диаграммы данных (графики, фотографии) показаны как есть; старые схемы-PNG прежнего README перерисованы в пары SVG, оригиналы остаются на месте. "
      "Сырые фотографии (`original_research/data/**/photos`) это данные, а не рисунки, и по одной не перечислены. Доноры названы только анонимными кодами.")
    a("")
    a("## " + ("Schemas redrawn as SVG" if en else "Схемы, перерисованные в SVG"))
    a("")
    a("| Figure | What it shows | Shown on | Original |" if en else "| Рисунок | Что показывает | Где показан | Исходная схема |")
    a("|---|---|---|---|")
    for orig, e, r, svg, page in REDRAW:
        a("| [`%s.%s.svg`](assets/diagrams/%s.%s.svg) | %s | [%s](%s%s.md) | [`%s`](../%s) |" % (svg, lang, svg, lang, e if en else r, page, page, suf, orig, orig))
    a("")
    a("## " + ("Charts and diagrams shown on the pages" if en else "Диаграммы, показанные на страницах"))
    a("")
    a("| Figure | What it shows | Shown on |" if en else "| Рисунок | Что показывает | Где показан |")
    a("|---|---|---|")
    for p, e, r, page in SHOWN:
        a("| [`%s`](../%s) | %s | [%s](%s%s.md) |" % (p, p, e if en else r, page, page, suf))
    a("")
    a("## " + ("Report charts" if en else "Диаграммы отчётов"))
    a("")
    a("Each report page of the repository embeds its own charts; they are listed here with the report that holds them."
      if en else "Каждый отчёт репозитория встраивает свои диаграммы; здесь они перечислены вместе с отчётом, которому принадлежат.")
    a("")
    a("| Figure | What it shows | Report |" if en else "| Рисунок | Что показывает | Отчёт |")
    a("|---|---|---|")
    for folder, items in REPORTS:
        rep = folder.split("/")[0]
        for fn, e, r in items:
            path = RP + folder + "/" + fn
            a("| [`%s`](../%s) | %s | [`%s`](../%s%s/report_%s.md) |" % (path, path, e if en else r, rep, RP, rep, "en" if en else "ru"))
    a("")
    a("## " + ("Mirror folder, file by file" if en else "Папка-зеркало, файл за файлом"))
    a("")
    a(("The 32 PNG in `%s` were compared by content with the root diagrams. 5 are byte-identical copies, 5 show the same diagram as a root figure (different render or crop), 8 are distinct schemas and are redrawn above, 7 are per-donor photo pies (data charts, listed only) and 7 are per-donor session timelines with minute-level times, which are not reproduced here (aggregates-only rule, see [Ethics](ETHICS.md))." % MR[:-1])
      if en else ("32 PNG в `%s` сверены по содержанию с корневыми схемами. 5 это побайтные копии, 5 показывают ту же схему, что корневая (другой рендер или обрезка), 8 это отдельные схемы, они перерисованы выше, 7 это круговые диаграммы фотографий по донорам (диаграммы данных, только перечислены) и 7 это хронологии сессий по донорам с поминутными временами, они здесь не воспроизводятся (правило «только агрегаты», см. [Этику](ETHICS.ru.md))." % MR[:-1]))
    a("")
    a("| Mirror file | Status | Where it is shown |" if en else "| Файл зеркала | Состояние | Где показан |")
    a("|---|---|---|")
    rd = {svg: (page, orig) for orig, _, _, svg, page in REDRAW}
    byorig = {o: (svg, page) for o, _, _, svg, page in REDRAW}
    for fn, kind, ref in MIRROR_MAP:
        f = "`%s%s`" % (MR, fn)
        link = "[`%s`](../%s%s)" % (fn, MR, fn)
        if kind in ("same-bytes", "same-diagram"):
            svg, page = byorig[M + ref]
            t = ("Identical copy of `%s`" if kind == "same-bytes" else "Same diagram as `%s`, other render") % ref if en else ("Побайтная копия `%s`" if kind == "same-bytes" else "Та же схема, что `%s`, другой рендер") % ref
            w = "[%s.%s.svg](assets/diagrams/%s.%s.svg) on [%s](%s%s.md)" % (svg, lang, svg, lang, page, page, suf)
        elif kind == "redrawn":
            page = rd[ref][0]
            t = "Distinct schema, redrawn" if en else "Отдельная схема, перерисована"
            w = "[%s.%s.svg](assets/diagrams/%s.%s.svg) on [%s](%s%s.md)" % (ref, lang, ref, lang, page, page, suf)
        elif kind == "pie":
            t = "Per-donor photo-share pie (data chart, anonymous code)" if en else "Круговая диаграмма долей фото по донору (диаграмма данных, анонимный код)"
            w = "listed only" if en else "только перечислен"
        else:
            t = "Per-donor session timeline with minute-level times" if en else "Хронология сессии донора с поминутными временами"
            w = "not reproduced here: donor-level times (aggregates-only rule)" if en else "здесь не воспроизводится: времена по донору (правило «только агрегаты»)"
        a("| %s | %s | %s |" % (link, t, w))
    a("")
    a("## " + ("Per-donor folders" if en else "Папки доноров"))
    a("")
    a("| Figures | What they are | Folder |" if en else "| Рисунки | Что это | Папка |")
    a("|---|---|---|")
    a(("| 16 PNG | One photo-distribution pie chart per donor folder, by condition (`p01_*`..`p07_*`); data of the donor folders, listed and not reproduced |"
       if en else "| 16 PNG | По круговой диаграмме распределения фотографий на папку донора, по условиям (`p01_*`..`p07_*`); данные папок доноров, перечислены, не воспроизводятся |")
      + " `original_research/data/patient-0N/photos/mermaid` |")
    a(("| JPG, HEIC | The raw and converted photographs themselves | `original_research/data/patient-0N/photos/{jpg,original}` (raw data, see [Data](DATA.md)) |"
       if en else "| JPG, HEIC | Сами сырые и конвертированные фотографии | `original_research/data/patient-0N/photos/{jpg,original}` (сырые данные, см. [Данные](DATA.ru.md)) |"))
    a("")
    a("## " + ("Generated by this restructuring" if en else "Создано этой реструктуризацией"))
    a("")
    a("The banner, the study diagrams (`study-design`, `units`, `claimed-vs-shown`, `blinded-results`, `timeline`), the navigation icons and the redraws above live in `guide/assets/`, are built by `tools/build_visuals.py` and `tools/build_redraws.py`, and carry no donor-level data."
      if en else "Баннер, диаграммы исследования (`study-design`, `units`, `claimed-vs-shown`, `blinded-results`, `timeline`), навигационные иконки и шесть перерисовок выше лежат в `guide/assets/`, собираются `tools/build_visuals.py` и `tools/build_redraws.py` и не содержат данных по донорам.")
    a("")
    return "\n".join(L)


for lang, name in (("en", "FIGURES.md"), ("ru", "FIGURES.ru.md")):
    open(os.path.join(ROOT, "guide", name), "w", encoding="utf-8").write(build(lang))
    print("wrote guide/" + name)
