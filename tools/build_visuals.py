#!/usr/bin/env python3
"""Generates the showcase visuals of the Blood Plasma Study (never hand-edit the SVG output; edit this file).

    python3 tools/build_visuals.py

Output (English and Russian twin for every picture)
    guide/assets/banner/hero-banner.{en,ru}.svg           generated illustration, not a screenshot
    guide/assets/diagrams/study-design.{en,ru}.svg        donors -> three conditions -> photographs -> analyses
    guide/assets/diagrams/units.{en,ru}.svg               donors, photographs, triplets: what the independent unit is
    guide/assets/diagrams/claimed-vs-shown.{en,ru}.svg    what the texts say versus what the repository shows
    guide/assets/diagrams/blinded-results.{en,ru}.svg     share of triplets where the provider picked channel 19, by provider
    guide/assets/diagrams/timeline.{en,ru}.svg            registration, four reports, last update, planned paper
    guide/assets/icons/*.svg                              navigation icons

Every number printed on a picture comes from tools/facts.py (computed from the repository at build time).
Every date on the timeline is checked against the repository text it is taken from; the build aborts when it is
missing. Rules (ASRP visual standard): <title>, <desc>, viewBox on every SVG; text is measured and must fit its
container (the build aborts otherwise); a status is a word paired with a shape, never colour alone; one token set
(tools/svgkit.py). No donor-level data is drawn anywhere.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F401,F403  (tokens, text(), Canvas, write(), ...)
import facts as factsmod  # noqa: E402

F = factsmod.facts()
ROOT = factsmod.ROOT


def fmt(s):
    return s.format(**F)


STATE = {
    "en": {"shown": ("■ SHOWN", GREEN), "partly": ("◧ PARTLY", GOLD), "claimed": ("◇ CLAIMED ONLY", VIOLET),
           "absent": ("✕ NOT IN REPO", AMBER), "weak": ("◧ WEAK", GOLD), "chance": ("✕ AT CHANCE", AMBER),
           "plan": ("◇ PLANNED", VIOLET), "done": ("■ DONE", GREEN), "rejected": ("✕ REJECTED BY REPO", AMBER)},
    "ru": {"shown": ("■ ПОКАЗАНО", GREEN), "partly": ("◧ ЧАСТИЧНО", GOLD), "claimed": ("◇ ТОЛЬКО ЗАЯВЛЕНО", VIOLET),
           "absent": ("✕ НЕТ В РЕПО", AMBER), "weak": ("◧ СЛАБО", GOLD), "chance": ("✕ УРОВЕНЬ СЛУЧАЙНОСТИ", AMBER),
           "plan": ("◇ В ПЛАНАХ", VIOLET), "done": ("■ СДЕЛАНО", GREEN), "rejected": ("✕ ОТВЕРГНУТО В РЕПО", AMBER)},
}


def foot(cv, parts, bottom, color=MUTED, weight=400):
    lines = []
    for p in ([parts] if isinstance(parts, str) else parts):
        lines += wrap(p, FS_SMALL, cv.w - 48, weight >= 600)
    y = bottom - 20 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        cv.label(24, y + 20 * i, ln, FS_SMALL, color, weight=weight, box=cv.w - 48)
    return len(lines)


def svg_done(cv):
    return "\n".join(cv.o + ["</svg>\n"])


# --- hero banner -----------------------------------------------------------------------------
BANNER = {
    "en": {
        "title": "Blood Plasma Study",
        "kicker": "HYPERBOLIC FIELD · EXPLORATORY PILOT",
        "tag": "HYPOTHESIS-GENERATING",
        "sub": ["Plasma photographed after two field settings", "and an untreated control; read by CV and AI"],
        "vials": ["control", "ch 19", "ch 21"],
        "chips": ["{donors} donors · {photos} photos", "{triplets} blinded triplets", "{blinded_runs} blinded runs"],
        "foot": "no clotting-time or biochemical data in the repository",
        "desc": ("Generated illustration, not a screenshot. Three test tubes labelled control, channel 19 and channel 21 on the left; "
                 "the title; three figures computed from the repository: {donors} donors and {photos} photographs, {triplets} blinded "
                 "triplets, {blinded_runs} blinded provider runs. Footer: no clotting-time or biochemical data in the repository."),
    },
    "ru": {
        "title": "Blood Plasma Study",
        "kicker": "ГИПЕРБОЛИЧЕСКОЕ ПОЛЕ · ПОИСКОВЫЙ ПИЛОТ",
        "tag": "ГЕНЕРИРУЕТ ГИПОТЕЗЫ",
        "sub": ["Плазма на фото после двух настроек поля", "и без обработки; читают CV и ИИ"],
        "vials": ["контроль", "кан. 19", "кан. 21"],
        "chips": ["{donors_ru} · {photos} фото", "{triplets_ru} вслепую", "{blinded_runs} слепых прогонов"],
        "foot": "данных о времени свёртывания и биохимии в репозитории нет",
        "desc": ("Сгенерированная иллюстрация, не скриншот. Слева три пробирки: контроль, канал 19 и канал 21; заголовок; три числа, "
                 "посчитанные по репозиторию: {donors_ru} и {photos} фотографий, {triplets_ru} для слепой оценки, {blinded_runs} слепых "
                 "прогонов провайдеров. Подвал: данных о времени свёртывания и биохимии в репозитории нет."),
    },
}


def banner(lang):
    c = BANNER[lang]
    W, H = 1200, 330
    o = [svg_open(W, H, c["title"], fmt(c["desc"]))]
    cols = [MUTED, TEAL, VIOLET]
    for i, (lab, col) in enumerate(zip(c["vials"], cols)):
        x = 90 + i * 150
        o.append("<rect x='%d' y='60' width='56' height='170' rx='24' fill='%s' fill-opacity='0.35' stroke='%s' stroke-width='2.4'/>" % (x, PANEL, col))
        level = [128, 118, 150][i]
        o.append("<rect x='%d' y='%d' width='48' height='%d' rx='18' fill='%s' fill-opacity='0.45'/>" % (x + 4, level, 226 - level, col))
        o.append("<rect x='%d' y='52' width='64' height='12' rx='5' fill='%s'/>" % (x - 4, col))
        o.append(text(x + 28, 262, lab, FS_SMALL, INK, "middle", 700))
    tx = 520
    box = W - tx - 36
    o.append(text(tx, 66, c["kicker"], FS_KICKER, TEAL, "start", 700, 2, box))
    o.append(text(W - 36, 36, c["tag"], FS_SMALL, MUTED, "end", 700, 2, 520))
    o.append(text(tx, 128, c["title"], 54, INK, "start", 800, 0, box))
    for i, line in enumerate(c["sub"]):
        o.append(text(tx, 170 + 28 * i, line, 21, MUTED, "start", 400, 0, box))
    x = tx
    for i, chip in enumerate(c["chips"]):
        chip = chip.format(**F)
        w = text_width(chip, FS_KICKER, True) + 28
        if x + w > W - 30:
            raise SystemExit("chips overflow the banner: %r" % chip)
        col = [GOLD, TEAL, GREEN][i]
        o.append("<rect x='%.1f' y='246' width='%.1f' height='38' rx='19' fill='%s' fill-opacity='0.08' stroke='%s'/>" % (x, w, col, col))
        o.append(text("%.1f" % (x + w / 2), 271, chip, FS_KICKER, INK, "middle", 700))
        x += w + 12
    o.append(text(24, H - 14, c["foot"], FS_SMALL, MUTED, "start", 400, 0, 560))
    o.append("</svg>\n")
    return "\n".join(o)


# --- study design ----------------------------------------------------------------------------
DESIGN = {
    "en": {
        "title": "How the pilot is built",
        "sub": "Left to right: samples, photographs, readers",
        "tag": "STUDY DESIGN",
        "desc": ("Flow from left to right. {donors} donors give plasma. Each donor's plasma is split into three conditions: untreated control, "
                 "channel 19 (labelled time acceleration) and channel 21 (labelled time deceleration), exposed for roughly an hour. The tubes are "
                 "photographed with a phone on an LED panel, giving {photos} photographs. Three kinds of reader score the photographs: classical "
                 "computer vision, computer-vision and zero-shot models, and LLM vision providers, run unblinded and blinded ({blinded_runs} blinded "
                 "runs by {blinded_providers} providers). No clotting-time or biochemical measurement exists in the repository."),
        "c1": ("{donors} donors", ["Plasma, split into three conditions", "Collection and centrifugation by an external specialist"]),
        "conds": [("Control", "no exposure", MUTED), ("Channel 19", "label: time acceleration", TEAL), ("Channel 21", "label: time deceleration", VIOLET)],
        "c3": ("{photos} photographs", ["Phone camera on an LED panel", "{heic} HEIC originals, JPG copies", "stills, not a time-lapse series"]),
        "readers": [("Classical CV", "SAM-2 segmentation + colour rules", "rejected"),
                    ("CV and zero-shot models", "DINOv2 probe, SigLIP2, BiomedCLIP", "weak"),
                    ("LLM vision providers", "{blinded_providers} blinded + 1 unblinded pass", "partly")],
        "absent": "Not in the repository: clotting time, fibrinogen, D-dimer, PT/APTT, emitter specification.",
        "foot": "Source: experiment_protocol_en.md, original_research/README.md, the four dated reports.",
    },
    "ru": {
        "title": "Как устроен пилот",
        "sub": "Слева направо: образцы, фотографии, читатели",
        "tag": "ДИЗАЙН ИССЛЕДОВАНИЯ",
        "desc": ("Поток слева направо. {donors_ru} дают плазму. Плазма каждого донора делится на три условия: контроль без воздействия, "
                 "канал 19 (метка: ускорение времени) и канал 21 (метка: замедление времени); экспозиция около часа. Пробирки фотографируют "
                 "телефоном на светодиодной панели: {photos} фотографий. Фотографии оценивают три вида читателей: классическое компьютерное зрение, "
                 "модели зрения и zero-shot, и LLM-провайдеры с видением, вслепую и без слепоты ({blinded_runs} слепых прогонов, "
                 "{blinded_providers} провайдера). Измерений времени свёртывания и биохимии в репозитории нет."),
        "c1": ("{donors_ru}", ["Плазма, делится на три условия", "Забор и центрифугирование: внешний специалист"]),
        "conds": [("Контроль", "без воздействия", MUTED), ("Канал 19", "метка: ускорение времени", TEAL), ("Канал 21", "метка: замедление времени", VIOLET)],
        "c3": ("{photos} фотографий", ["Камера телефона на LED-панели", "{heic} оригиналов HEIC и копии JPG", "отдельные кадры, не time-lapse"]),
        "readers": [("Классический CV", "SAM-2 сегментация + цветовые правила", "rejected"),
                    ("CV и zero-shot модели", "DINOv2 probe, SigLIP2, BiomedCLIP", "weak"),
                    ("LLM-провайдеры с видением", "{blinded_providers} слепых + 1 без слепоты", "partly")],
        "absent": "Нет в репозитории: время свёртывания, фибриноген, D-димер, PT/APTT, спецификация излучателей.",
        "foot": "Источник: experiment_protocol_ru.md, original_research/README.md, четыре датированных отчёта.",
    },
}


def design(lang):
    c = DESIGN[lang]
    st = STATE[lang]
    W, H = 1200, 560
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], c["sub"], c["tag"])
    t, body = c["c1"]
    cv.box(24, 150, 250, fmt(t), [fmt(b) for b in body], stroke=GOLD, h=170, valign="top")
    xs, bw = 330, 250
    ys = [100, 205, 310]
    for (nm, sub, col), y in zip(c["conds"], ys):
        cv.box(xs, y, bw, nm, [sub], stroke=col, h=82, valign="top")
        cv.arrow([(274, 235), (xs - 3, y + 41)], col)
    t, body = c["c3"]
    cv.box(640, 150, 240, fmt(t), [fmt(b) for b in body], stroke=BLUE, h=170, valign="top")
    for y in ys:
        cv.arrow([(xs + bw, y + 41), (637, 235)], BLUE)
    rx, rw = 930, 246
    for i, (nm, sub, state) in enumerate(c["readers"]):
        y = 100 + i * 112
        label, col = st[state]
        cv.box(rx, y, rw, nm, [fmt(sub)], status=[(label, col)], stroke=col, h=108, valign="top", title_size=14)
        cv.arrow([(880, 235), (rx - 3, y + 54)], col)
    cv.box(24, 420, W - 48, None, [fmt(c["absent"])], stroke=AMBER, h=72, center=True)
    foot(cv, c["foot"], H - 18)
    return svg_done(cv)


# --- units -----------------------------------------------------------------------------------
UNITS = {
    "en": {
        "title": "What counts as one observation",
        "sub": "Counts shrink at every step; the independent unit is the donor",
        "tag": "UNITS OF ANALYSIS",
        "desc": ("Four boxes with arrows. {donors} donors. {photos} photographs, which are not independent, since one donor yields many. "
                 "{triplets} blinded triplets (one photo per condition) drawn from {triplet_donors} donors. Provider verdicts: Gemini {gemini_n}, "
                 "Perplexity {perplexity_n}, GPT-5 {openai_n} and Groq {groq_n} over repeated runs of the same triplets, so they are repeats, not new data."),
        "boxes": [("{donors} donors", ["The independent units. Fewer than ten.", "Sample size of the whole pilot"], GOLD),
                  ("{photos} photographs", ["Many per donor; not independent", "40 labelled single-condition photos, the rest multi-tube or unlabelled"], BLUE),
                  ("{triplets} triplets", ["One photo per condition, from {triplet_donors} donors", "The input of every blinded comparison"], TEAL),
                  ("{blinded_runs} runs", ["Repeats of the same triplets by {blinded_providers} providers", "Gemini {gemini_n} verdicts, Groq {groq_n}, GPT-5 {openai_n}, Perplexity {perplexity_n}"], VIOLET)],
        "foot": "A p-value on {triplets} triplets from {triplet_donors} donors cannot speak for donors in general; repeated runs do not add donors.",
    },
    "ru": {
        "title": "Что считается одним наблюдением",
        "sub": "Числа сужаются на каждом шаге; независимая единица это донор",
        "tag": "ЕДИНИЦЫ АНАЛИЗА",
        "desc": ("Четыре блока со стрелками. {donors_ru}. {photos} фотографий, они не независимы: один донор даёт много снимков. "
                 "{triplets_ru} для слепой оценки (по одному снимку на условие) от {triplet_donors} доноров. Вердикты провайдеров: Gemini {gemini_n}, "
                 "Perplexity {perplexity_n}, GPT-5 {openai_n} и Groq {groq_n} по повторным прогонам тех же триплетов: это повторы, а не новые данные."),
        "boxes": [("{donors_ru}", ["Независимые единицы. Меньше десяти.", "Размер выборки всего пилота"], GOLD),
                  ("{photos} фотографий", ["Много на донора; не независимы", "40 снимков с одной меткой условия, остальные многопробирочные или без метки"], BLUE),
                  ("{triplets_ru}", ["По снимку на условие, от {triplet_donors} доноров", "Вход каждого слепого сравнения"], TEAL),
                  ("{blinded_runs} прогонов", ["Повторы тех же триплетов у {blinded_providers} провайдеров", "Gemini {gemini_n} вердиктов, Groq {groq_n}, GPT-5 {openai_n}, Perplexity {perplexity_n}"], VIOLET)],
        "foot": "p-значение на {triplets} триплетах от {triplet_donors} доноров не говорит о донорах вообще; повторные прогоны доноров не добавляют.",
    },
}


def units(lang):
    c = UNITS[lang]
    W, H = 1200, 360
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], c["sub"], c["tag"])
    bw, gap, y, h = 270, 40, 110, 150
    for i, (t, body, col) in enumerate(c["boxes"]):
        x = 24 + i * (bw + gap)
        cv.box(x, y, bw, fmt(t), [fmt(b) for b in body], stroke=col, h=h, valign="top")
        if i:
            cv.arrow([(x - gap + 3, y + h / 2), (x - 3, y + h / 2)], MUTED)
    foot(cv, fmt(c["foot"]), H - 40)
    return svg_done(cv)


# --- claimed vs shown ------------------------------------------------------------------------
CLAIM = {
    "en": {
        "title": "What is claimed and what the repository shows",
        "desc": ("Six rows, left to right: topic, what the texts say, what the data and code show, and a state word. Effect on clotting: README says "
                 "hypothesis validated; reports call the best CV result suggestive but inconclusive, p {dino_probe_p} (partly). Significance: README lists "
                 "p = 0.027 as significant; one run of {triplets} verdicts, exact one-sided p {gemini_p_exact}, position confounded with channel (weak). "
                 "Clot counts: -37 and -42 percent in the README; the CV detector behind them has over {cv_false_pos} percent false positives per the repo's own "
                 "report (rejected). Biochemistry: fibrinogen r = 0.72 reported, no data (not in repo). Patent: README says technology protected; "
                 "it is an application (claimed only). Publication: planned April-May 2026, no manuscript (planned)."),
        "sub": "Left: the texts. Right: what the files in this repository support",
        "tag": "CLAIMED VS SHOWN",
        "cols": ["TOPIC", "CLAIMED (README, issues)", "SHOWN (data, code, reports)", "STATE"],
        "rows": [
            ("Effect", "Hypothesis supported: channel 19 accelerates and 21 delays coagulation", "Best CV result suggestive but inconclusive (p {dino_probe_p}); no clotting-time data", "partly"),
            ("Significance", "p = 0.027 (Gemini): Significant", "One run, {triplets} verdicts, exact one-sided p {gemini_p_exact}; letter B is always channel 19", "weak"),
            ("Clot counts", "37% fewer clots, 42% smaller area on channel 19", "The detector behind them has over {cv_false_pos}% false positives, says the repo's own report", "rejected"),
            ("Biochemistry", "Fibrinogen r = 0.72, D-dimer only on channel 19", "No data, n or method; data folders marked planned", "absent"),
            ("Patent", "Research uses technology protected by patent", "KZ 2025/1095.1 is an application, filed; the repository does not name the applicants", "claimed"),
            ("Paper", "Peer-reviewed publication, April-May 2026", "No manuscript or submission record in the repository", "plan"),
        ],
        "foot": ["A claim is filed under what supports it in the files, not under how confidently it is worded.", "Sources: see guide/EVIDENCE.md, one source path per row."],
    },
    "ru": {
        "title": "Что заявлено и что показывает репозиторий",
        "desc": ("Шесть строк слева направо: тема, что говорят тексты, что показывают данные и код, слово-состояние. Эффект на свёртывание: README "
                 "пишет, что гипотеза подтверждена; отчёты называют лучший результат CV наводящим, но неубедительным, p {dino_probe_p} (частично). "
                 "Значимость: README называет p = 0.027 значимым; один прогон из {triplets} вердиктов, точное одностороннее p {gemini_p_exact}, "
                 "позиция смешана с каналом (слабо). Число сгустков: -37 и -42 процента в README; у CV-детектора за ними более {cv_false_pos} "
                 "процентов ложных срабатываний по собственному отчёту репозитория (отвергнуто). Биохимия: фибриноген r = 0.72 заявлен, данных "
                 "нет (нет в репо). Патент: README пишет, что технология защищена; это заявка (только заявлено). Статья: планировалась на "
                 "апрель-май 2026, рукописи нет (в планах)."),
        "sub": "Слева тексты. Справа то, что подтверждают файлы репозитория",
        "tag": "ЗАЯВЛЕНО И ПОКАЗАНО",
        "cols": ["ТЕМА", "ЗАЯВЛЕНО (README, задачи)", "ПОКАЗАНО (данные, код, отчёты)", "СОСТОЯНИЕ"],
        "rows": [
            ("Эффект", "Гипотеза подтверждена: канал 19 ускоряет, канал 21 замедляет свёртывание", "Лучший результат CV: наводящий, но неубедительный (p {dino_probe_p}); данных о времени свёртывания нет", "partly"),
            ("Значимость", "p = 0.027 (Gemini): значимо", "Один прогон, {triplets} вердиктов, точное одностороннее p {gemini_p_exact}; буква B всегда канал 19", "weak"),
            ("Сгустки", "На канале 19 на 37% меньше сгустков, на 42% меньше площадь", "У детектора за ними более {cv_false_pos}% ложных срабатываний по собственному отчёту репо", "rejected"),
            ("Биохимия", "Фибриноген r = 0.72, D-димер только на канале 19", "Нет данных, n и метода; папки данных помечены как планируемые", "absent"),
            ("Патент", "Исследование использует технологию, защищённую патентом", "KZ 2025/1095.1 это заявка (подана); репозиторий не называет заявителей", "claimed"),
            ("Статья", "Рецензируемая публикация, апрель-май 2026", "Рукописи и записи о подаче в репозитории нет", "plan"),
        ],
        "foot": ["Утверждение относят к тому, что его поддерживает в файлах, а не к тому, как уверенно оно сформулировано.", "Источники: guide/EVIDENCE.ru.md, по одному пути на строку."],
    },
}


def claimed(lang):
    c = CLAIM[lang]
    st = STATE[lang]
    W, H = 1200, 826
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], fmt(c["sub"]), c["tag"])
    x0, x1, x2, x3 = 24, 160, 560, 1000
    w1, w2, w3 = 390, 430, 176
    ytop = 98
    cv.label(x0, ytop + 10, c["cols"][0], FS_KICKER, TEAL, weight=700, box=130)
    cv.label(x1, ytop + 10, c["cols"][1], FS_KICKER, TEAL, weight=700, box=w1)
    cv.label(x2, ytop + 10, c["cols"][2], FS_KICKER, TEAL, weight=700, box=w2)
    cv.label(x3, ytop + 10, c["cols"][3], FS_KICKER, TEAL, weight=700, box=w3)
    rh, gap = 90, 8
    for i, (topic, claim, shown, state) in enumerate(c["rows"]):
        y = ytop + 26 + i * (rh + gap)
        label, col = st[state]
        cv.label(x0, y + rh / 2 + 5, topic, FS_BODY, INK, weight=700, box=130)
        cv.box(x1, y, w1 - 12, None, [fmt(claim)], stroke=BLUE, h=rh)
        cv.box(x2, y, w2 - 12, None, [fmt(shown)], stroke=col, h=rh)
        cv.box(x3, y, w3, None, [], status=[(label, col)], stroke=col, h=rh, center=True)
    foot(cv, c["foot"], H - 14)
    return svg_done(cv)


# --- blinded results (bars) -------------------------------------------------------------------
BARS = {
    "en": {
        "title": "Blinded comparison: how often channel 19 was picked",
        "sub": "Verdicts naming channel 19 as most coagulated; chance is {chance_pct}%",
        "tag": "BLINDED RESULTS",
        "desc": ("Horizontal bars, share of blinded verdicts that named channel 19 as the most coagulated sample, with a chance line at {chance_pct} "
                 "percent. Gemini {gemini_pct} percent over {gemini_n} verdicts, one run (above chance, one run). Perplexity {perplexity_pct} percent over "
                 "{perplexity_n}, Groq {groq_pct} over {groq_n}, GPT-5 {openai_pct} over {openai_n} (at or below chance). Counts are recomputed from the raw "
                 "results files."),
        "names": {"gemini": "Gemini 2.5 flash-lite", "perplexity": "Perplexity sonar-pro", "groq": "Groq Llama 4 Scout", "openai": "GPT-5"},
        "n": "{n} verdicts, {r} run(s)", "chance": "chance {chance_pct}%",
        "state": {"above": "◧ ABOVE CHANCE, ONE RUN", "near": "✕ AT CHANCE", "below": "✕ BELOW CHANCE"},
        "foot": ["Letter B is always channel 19 in these runs, so a lean toward letter B looks like a lean toward channel 19.", "Source: original_research/results/fullres_comparative_blinded_*/results.json, recounted by tools/facts.py."],
    },
    "ru": {
        "title": "Слепое сравнение: как часто выбирали канал 19",
        "sub": "Вердикты с каналом 19 как самым свёрнутым; случайность {chance_pct}%",
        "tag": "СЛЕПЫЕ РЕЗУЛЬТАТЫ",
        "desc": ("Горизонтальные столбцы: доля слепых вердиктов, назвавших канал 19 самым свёрнутым образцом, и линия случайности {chance_pct} "
                 "процента. Gemini {gemini_pct} процента из {gemini_n} вердиктов, один прогон (выше случайности, один прогон). Perplexity "
                 "{perplexity_pct} из {perplexity_n}, Groq {groq_pct} из {groq_n}, GPT-5 {openai_pct} из {openai_n} (на уровне случайности или ниже). "
                 "Числа пересчитаны по сырым файлам результатов."),
        "names": {"gemini": "Gemini 2.5 flash-lite", "perplexity": "Perplexity sonar-pro", "groq": "Groq Llama 4 Scout", "openai": "GPT-5"},
        "n": "{n} вердиктов, прогонов: {r}", "chance": "случайность {chance_pct}%",
        "state": {"above": "◧ ВЫШЕ, ОДИН ПРОГОН", "near": "✕ ПРИМЕРНО СЛУЧАЙНО", "below": "✕ НИЖЕ СЛУЧАЙНОСТИ"},
        "foot": ["Буква B в этих прогонах всегда канал 19, поэтому тяга к букве B выглядит как тяга к каналу 19.", "Источник: original_research/results/fullres_comparative_blinded_*/results.json, пересчитано tools/facts.py."],
    },
}


def bars(lang):
    c = BARS[lang]
    W, H = 1200, 520
    cv = Canvas(W, H, c["title"], fmt(c["desc"]), c["title"], fmt(c["sub"]), c["tag"])
    x0, x1 = 300, 860  # axis 0 .. 100 %
    span = x1 - x0
    top = 140
    order = ["gemini", "perplexity", "groq", "openai"]
    for i, k in enumerate(order):
        y = top + i * 78
        pct = float(F[k + "_pct"])
        state = "above" if pct > 40 else ("near" if pct > 30 else "below")
        col = GOLD if state == "above" else AMBER
        cv.label(24, y + 18, c["names"][k], FS_BODY, INK, weight=700, box=250)
        cv.label(24, y + 40, c["n"].format(n=F[k + "_n"], r=F[k + "_runs"]), FS_SMALL, MUTED, box=250)
        cv.o.append("<rect x='%d' y='%d' width='%d' height='34' rx='6' fill='%s' stroke='%s'/>" % (x0, y, span, PANEL, LINE))
        cv.o.append("<rect x='%d' y='%d' width='%.1f' height='34' rx='6' fill='%s' fill-opacity='0.85'/>" % (x0, y, span * pct / 100, col))
        cv.label(x0 + span * pct / 100 + 10, y + 23, "%s%%" % F[k + "_pct"], FS_BODY, INK, weight=700, box=70)
        cv.label(x1 + 90, y + 23, c["state"][state], FS_SMALL, col, weight=800, box=230)
    cx = x0 + span * float(F["chance_pct"]) / 100
    cv.o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='6 5'/>" % (cx, top - 14, cx, top + 4 * 78 - 14, TEAL))
    cv.label(cx, top - 22, fmt(c["chance"]), FS_SMALL, TEAL, "middle", 700, box=200)
    for tick in (0, 25, 50, 75, 100):
        tx = x0 + span * tick / 100
        cv.label(tx, top + 4 * 78 + 6, "%d%%" % tick, FS_SMALL, MUTED, "middle", box=60)
    foot(cv, c["foot"], H - 16)
    return svg_done(cv)


# --- timeline ---------------------------------------------------------------------------------
# (date shown, text, state, file that carries the date, needle searched in that file)
TIMELINE = [
    ("2026-01-25", {"en": "OSF preregistration dated; text says registered before data collection", "ru": "Дата предварительной регистрации OSF; в тексте: до сбора данных"},
     "done", "OSF_PREREGISTRATION.md", "January 25, 2026"),
    ("2026-02-25", {"en": "Report 1: CV and ML analysis (ASRP Science-LLM)", "ru": "Отчёт 1: CV и ML анализ (ASRP Science-LLM)"},
     "done", "original_research/reports/2026-02-25_ai-analysis/report_en.md", "February 25, 2026"),
    ("2026-02-26", {"en": "Report 2: unblinded LLM vision pass; CV detector rejected", "ru": "Отчёт 2: проход LLM без слепоты; CV-детектор отвергнут"},
     "done", "original_research/reports/2026-02-26_llm-vision-analysis/report_en.md", "2026-02-26"),
    ("2026-03-12", {"en": "Report 3: blinded comparison by providers (v5.1)", "ru": "Отчёт 3: слепое сравнение провайдеров (v5.1)"},
     "done", "original_research/reports/2026-03-12_comparative-llm-analysis/report_en.md", "2026-03-12"),
    ("2026-03-14", {"en": "Report 4: CV and ML models, leave-one-set-out", "ru": "Отчёт 4: CV и ML модели, leave-one-set-out"},
     "done", "original_research/reports/2026-03-14_cv-ml-analysis/report_en.md", "2026-03-14"),
    ("2026-03-26", {"en": "Last content update stated in the README", "ru": "Последнее обновление содержания по README"},
     "done", "README.md", "26 March 2026"),
    ("Apr-May 2026", {"en": "Peer-reviewed paper planned (issue 8); no manuscript here", "ru": "Планировалась статья (задача 8); рукописи здесь нет"},
     "plan", "ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/ISSUE_8_UPDATED.md", "April-May 2026"),
]
TL = {
    "en": {"title": "Dated milestones in the repository", "sub": "Every date is read from the file that carries it", "tag": "TIMELINE",
           "foot": "The last dated file is 26 March 2026; later commits are template and privacy hygiene, not content.",
           "desc": ("Seven dated rows: OSF preregistration 2026-01-25; four reports on 2026-02-25, 2026-02-26, 2026-03-12 and 2026-03-14; "
                    "the README's last content update 2026-03-26; and, as a plan only, a peer-reviewed paper expected April-May 2026, for which "
                    "the repository holds no manuscript.")},
    "ru": {"title": "Датированные вехи в репозитории", "sub": "Каждая дата прочитана из файла, который её содержит", "tag": "ХРОНОЛОГИЯ",
           "foot": "Последний датированный файл: 26 марта 2026; более поздние коммиты это шаблон и приватность, а не содержание.",
           "desc": ("Семь датированных строк: предварительная регистрация OSF 2026-01-25; четыре отчёта 2026-02-25, 2026-02-26, 2026-03-12 и "
                    "2026-03-14; последнее обновление содержания README 2026-03-26; и только как план рецензируемая статья на апрель-май 2026, "
                    "для которой в репозитории нет рукописи.")},
}


def timeline(lang):
    c = TL[lang]
    st = STATE[lang]
    W = 1200
    rh = 66
    H = 130 + rh * len(TIMELINE) + 30
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], c["sub"], c["tag"])
    for i, (date, txt, state, path, needle) in enumerate(TIMELINE):
        if needle not in open(os.path.join(ROOT, path), encoding="utf-8").read():
            raise SystemExit("timeline: %r not found in %s" % (needle, path))
        y = 100 + i * rh
        label, col = st[state]
        cv.o.append("<circle cx='60' cy='%d' r='8' fill='%s' stroke='%s' stroke-width='2.4'/>" % (y + 26, BG0, col))
        if i < len(TIMELINE) - 1:
            cv.o.append("<line x1='60' y1='%d' x2='60' y2='%d' stroke='%s' stroke-width='2'%s/>" % (y + 36, y + rh + 16, LINE, " stroke-dasharray='5 6'" if state == "plan" or TIMELINE[i + 1][2] == "plan" else ""))
        cv.label(90, y + 32, date, FS_BODY, INK, weight=700, box=150)
        cv.label(260, y + 32, txt[lang], FS_BODY, INK, box=640)
        cv.label(940, y + 32, label, FS_SMALL, col, weight=800, box=240)
    foot(cv, c["foot"], H - 14)
    return svg_done(cv)


# --- icons -----------------------------------------------------------------------------------
def icon(col, body, title):
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\" width=\"64\" height=\"64\" role=\"img\">\n"
            "<title>%s</title>\n<desc>Navigation icon: %s.</desc>\n<rect x=\"2\" y=\"2\" width=\"60\" height=\"60\" rx=\"12\" fill=\"#101826\" "
            "stroke=\"%s\" stroke-width=\"3\"/>\n<g fill='none' stroke='%s' stroke-width='2.6' stroke-linecap='round' "
            "stroke-linejoin='round'>%s</g>\n</svg>\n" % (title, title, col, col, body))


ICONS = {
    "study": (TEAL, "<circle cx='32' cy='32' r='16'/><circle cx='32' cy='32' r='5'/><path d='M32 12v8M32 44v8M12 32h8M44 32h8'/>", "the study"),
    "design": (GOLD, "<path d='M24 14h16M27 14v14L17 48a4 4 0 0 0 4 6h22a4 4 0 0 0 4-6L37 28V14'/><path d='M22 42h20'/>", "design and protocol"),
    "data": (BLUE, "<ellipse cx='32' cy='20' rx='15' ry='6'/><path d='M17 20v24c0 3 7 6 15 6s15-3 15-6V20M17 32c0 3 7 6 15 6s15-3 15-6'/>", "data and photographs"),
    "methods": (VIOLET, "<rect x='14' y='14' width='36' height='36' rx='5'/><path d='M22 42v-8M30 42V24M38 42v-12M46 42v-5'/>", "analysis methods"),
    "evidence": (AMBER, "<circle cx='28' cy='28' r='13'/><path d='M38 38l12 12M23 28l4 4 7-8'/>", "evidence"),
    "results": (GREEN, "<path d='M14 48V16M14 48h38'/><path d='M22 40l8-10 8 5 10-16'/>", "results as reported"),
    "publications": (VIOLET, "<rect x='16' y='12' width='32' height='40' rx='4'/><path d='M23 22h18M23 30h18M23 38h10'/>", "publications and IP"),
    "ecosystem": (BLUE, "<circle cx='32' cy='32' r='6'/><circle cx='32' cy='14' r='4'/><circle cx='48' cy='41' r='4'/>"
                        "<circle cx='16' cy='41' r='4'/><path d='M32 26V18M37 35l8 4M27 35l-8 4'/>", "ecosystem and team"),
    "navigation": (GREEN, "<path d='M20 14v36M20 22h10M20 34h10M20 46h10'/><rect x='30' y='17' width='20' height='10' rx='2'/>"
                          "<rect x='30' y='29' width='20' height='10' rx='2'/><rect x='30' y='41' width='20' height='10' rx='2'/>", "navigation"),
    "open": (GOLD, "<circle cx='32' cy='32' r='18'/><path d='M26 27a6 6 0 1 1 9 5c-2 1-3 2-3 4M32 43v2'/>", "open questions"),
    "ethics": (AMBER, "<rect x='17' y='29' width='30' height='21' rx='4'/><path d='M23 29v-6a9 9 0 0 1 18 0v6M32 38v6'/>", "ethics and security"),
    "figures": (TEAL, "<rect x='12' y='14' width='40' height='36' rx='5'/><circle cx='24' cy='26' r='4'/><path d='M14 46l12-12 8 8 6-6 10 10'/>", "figures"),
    "archive": (MUTED, "<rect x='12' y='14' width='40' height='11' rx='3'/><path d='M16 25v25h32V25M26 34h12'/>", "archive"),
}


def main():
    for lang in ("en", "ru"):
        write("guide/assets/banner/hero-banner.%s.svg" % lang, banner(lang))
        write("guide/assets/diagrams/study-design.%s.svg" % lang, design(lang))
        write("guide/assets/diagrams/units.%s.svg" % lang, units(lang))
        write("guide/assets/diagrams/claimed-vs-shown.%s.svg" % lang, claimed(lang))
        write("guide/assets/diagrams/blinded-results.%s.svg" % lang, bars(lang))
        write("guide/assets/diagrams/timeline.%s.svg" % lang, timeline(lang))
    for name, (col, body, title) in ICONS.items():
        write("guide/assets/icons/%s.svg" % name, icon(col, body, title))


if __name__ == "__main__":
    main()
