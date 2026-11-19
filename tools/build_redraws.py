#!/usr/bin/env python3
"""Redraws the six Mermaid PNG schemas of the previous README (original_research/charts/mermaid/root_1..6.png)
as house-style EN + RU SVG pairs (same nodes, edges, labels and numbers; nothing added except status words
on boxes that state a claim the repository does not prove).

    python3 tools/build_redraws.py

Output: guide/assets/diagrams/redraw-<name>.{en,ru}.svg
    overview   <- root_1.png   research overview (donors to reports)
    patent     <- root_2.png   patent application connection
    dates      <- root_3.png   collection dates and the four dated reports (old caption: "Hypothesis validation")
    timelapse  <- root_4.png   time-lapse imaging system
    pipeline   <- root_5.png   analysis pipeline
    protocol   <- root_6.png   experimental protocol
No donor names appear; donor codes (Patient 01..07) are anonymous, as in the original figure.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F401,F403

CLAIM = {"en": ("◇ CLAIMED ONLY", VIOLET), "ru": ("◇ ТОЛЬКО ЗАЯВЛЕНО", VIOLET)}
APPL = {"en": ("◇ APPLICATION, NOT A GRANTED PATENT", VIOLET), "ru": ("◇ ЗАЯВКА, НЕ ВЫДАННЫЙ ПАТЕНТ", VIOLET)}
PLAN = {"en": ("◇ PLANNED SYSTEM", VIOLET), "ru": ("◇ ПЛАНИРУЕМАЯ СИСТЕМА", VIOLET)}
TAG = {"en": "REDRAWN FIGURE", "ru": "ПЕРЕРИСОВАННАЯ СХЕМА"}


def done(cv):
    return "\n".join(cv.o + ["</svg>\n"])


def foot(cv, parts, bottom):
    lines = []
    for p in ([parts] if isinstance(parts, str) else parts):
        lines += wrap(p, FS_SMALL, cv.w - 48)
    y = bottom - 20 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        cv.label(24, y + 20 * i, ln, FS_SMALL, MUTED, box=cv.w - 48)


def center_x(b):
    return b[0] + b[2] / 2


def down(cv, a, b, col=MUTED):
    cv.arrow([(center_x(a), a[1] + a[3]), (center_x(b), b[1] - 3)], col)


# ---------------------------------------------------------------- 1 overview
def overview(lang):
    en = lang == "en"
    t = "Research overview" if en else "Обзор исследования"
    sub = "Previous README, diagram 1: from donors to reports" if en else "Прежний README, схема 1: от доноров до отчётов"
    desc = ("Flow chart. Blood donors, 7 patients, then plasma separation, then hyperbolic field exposure, which branches into four: "
            "time-lapse photography, channel 19 (time acceleration, claimed only), channel 21 (time deceleration, claimed only) and control (no exposure). "
            "Photography continues to AI/ML analysis, statistical analysis and scientific reports."
            if en else
            "Блок-схема. Доноры крови, 7 пациентов, затем центрифугирование, затем воздействие гиперболического поля, которое делится на четыре: "
            "покадровая съёмка, канал 19 (ускорение времени, только заявлено), канал 21 (замедление времени, только заявлено) и контроль (без воздействия). "
            "Съёмка продолжается анализом ИИ/МЛ, статистическим анализом и научными отчётами.")
    W, H = 1200, 810
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    b1 = cv.box(450, 100, 300, "Blood donors" if en else "Доноры крови", ["7 patients" if en else "7 пациентов"], stroke=GOLD, h=76, center=True)
    b2 = cv.box(450, 206, 300, "Plasma separation" if en else "Центрифугирование", [], stroke=TEAL, h=52, center=True)
    b3 = cv.box(400, 288, 400, "Hyperbolic field exposure" if en else "Воздействие гиперболического поля", [], stroke=BLUE, h=52, center=True)
    down(cv, b1, b2)
    down(cv, b2, b3)
    ys = 400
    xs = [24, 312, 600, 888]
    ph = cv.box(xs[0], ys, 276, "Time-lapse photography" if en else "Покадровая съёмка", [], stroke=GOLD, h=60, center=True)
    c19 = cv.box(xs[1], ys, 276, "Channel 19" if en else "Канал 19", ["Time acceleration" if en else "Ускорение времени"],
                 status=[CLAIM[lang]], stroke=VIOLET, h=100, center=True)
    c21 = cv.box(xs[2], ys, 276, "Channel 21" if en else "Канал 21", ["Time deceleration" if en else "Замедление времени"],
                 status=[CLAIM[lang]], stroke=VIOLET, h=100, center=True)
    ct = cv.box(xs[3], ys, 276, "Control" if en else "Контроль", ["No exposure" if en else "Без воздействия"], stroke=TEAL, h=76, center=True)
    for b in (ph, c19, c21, ct):
        cv.arrow([(600, 340), (center_x(b), b[1] - 3)], BLUE)
    prev = ph
    for i, name in enumerate(["AI/ML analysis" if en else "Анализ ИИ/МЛ", "Statistical analysis" if en else "Статистический анализ",
                              "Scientific reports" if en else "Научные отчёты"]):
        b = cv.box(24, ys + 100 + i * 90, 276, name, [], stroke=[VIOLET, AMBER, GREEN][i], h=52, center=True)
        down(cv, prev, b)
        prev = b
    foot(cv, ("Time acceleration and deceleration are the study's hypothesis; the repository's data do not establish them (guide/EVIDENCE.md)."
              if en else "Ускорение и замедление времени это гипотеза исследования; данные репозитория их не устанавливают (guide/EVIDENCE.ru.md)."), H - 16)
    return done(cv)


# ---------------------------------------------------------------- 2 patent
def patent(lang):
    en = lang == "en"
    t = "Patent application and the studies that use its emitters" if en else "Патентная заявка и исследования, где используются её излучатели"
    t = "Patent link of the study" if en else "Связь исследования с патентной заявкой"
    sub = "Previous README, diagram 2" if en else "Прежний README, схема 2"
    desc = ("Flow chart. KZ 2025/1095.1, Fractal FBHFS patent, 14 March 2025 (an application, not a granted patent), protects (claimed) the hyperbolic field emitters, "
            "which are used in three studies: Blood Plasma Study, DAAT Crystal Study and Agricultural Study."
            if en else
            "Блок-схема. KZ 2025/1095.1, Фрактальная БСГП, 14 марта 2025 (заявка, не выданный патент), защищает (заявлено) излучатели гиперболических полей, "
            "которые используются в трёх исследованиях: исследование кровяной плазмы, исследование кристаллов DAAT и сельскохозяйственное исследование.")
    W, H = 1200, 440
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    pt = cv.box(24, 130, 290, "KZ 2025/1095.1", ["Fractal FBHFS patent" if en else "Фрактальная БСГП", "14 March 2025" if en else "14 марта 2025"],
                status=[APPL[lang]], stroke=GOLD, h=190, center=True)
    em = cv.box(450, 150, 250, "Hyperbolic field emitters" if en else "Излучатели гиперболических полей", [], stroke=AMBER, h=100, center=True)
    cv.arrow([(314, 225), (447, 225)], GOLD)
    cv.label(318, 210, "PROTECTS" if en else "ЗАЩИЩАЕТ", FS_SMALL, INK, weight=600, box=130)
    cv.label(318, 255, "(claimed)" if en else "(заявлено)", FS_SMALL, VIOLET, weight=600, box=130)
    targets = [("Blood Plasma Study" if en else "Исследование кровяной плазмы", TEAL),
               ("DAAT Crystal Study" if en else "Исследование кристаллов DAAT", BLUE),
               ("Agricultural Study" if en else "Сельскохозяйственное исследование", GREEN)]
    for i, (nm, col) in enumerate(targets):
        y = 100 + i * 100
        b = cv.box(880, y, 296, nm, [], stroke=col, h=76, center=True)
        cy = y + 38
        cv.arrow([(700, 200 if i == 0 else 225 if i == 1 else 250), (730, 200 if i == 0 else 225 if i == 1 else 250),
                  (730, cy), (877, cy)], col)
        cv.label(742, cy - 8, "USED IN" if en else "ИСПОЛЬЗУЮТСЯ В", FS_SMALL, INK, weight=600, box=135)
    foot(cv, ("An application is an IP claim, not a granted patent; the repository does not name the applicants. See guide/PUBLICATIONS.md."
              if en else "Заявка это притязание, а не выданный патент; репозиторий не называет заявителей. См. guide/PUBLICATIONS.ru.md."), H - 16)
    return done(cv)


# ---------------------------------------------------------------- 3 dates
DON = [("2026-01-24", "01"), ("2026-01-28", "02"), ("2026-01-29", "03"), ("2026-01-30", "04"),
       ("2026-01-31", "05"), ("2026-02-01", "06"), ("2026-02-07", "07")]
REP = [("2026-02-25", "AI analysis", "Анализ ИИ"), ("2026-02-26", "LLM vision", "LLM-зрение"),
       ("2026-03-12", "Comparative", "Сравнительный"), ("2026-03-14", "CV/ML analysis", "Анализ CV/МЛ")]


def dates(lang):
    en = lang == "en"
    t = "Collection dates and dated reports" if en else "Даты сбора и датированные отчёты"
    sub = "Previous README, diagram 3 (captioned: hypothesis validation)" if en else "Прежний README, схема 3 (подпись: валидация гипотезы)"
    desc = ("Two rows of dated boxes joined by arrows. Donor collections: Patient 01 on 2026-01-24, 02 on 01-28, 03 on 01-29, 04 on 01-30, 05 on 01-31, 06 on 02-01, 07 on 02-07. "
            "Then four reports: AI analysis 2026-02-25, LLM vision 2026-02-26, comparative 2026-03-12, CV/ML analysis 2026-03-14."
            if en else
            "Два ряда датированных блоков со стрелками. Сборы по донорам: пациент 01 24.01.2026, 02 28.01, 03 29.01, 04 30.01, 05 31.01, 06 01.02, 07 07.02. "
            "Затем четыре отчёта: анализ ИИ 25.02.2026, LLM-зрение 26.02.2026, сравнительный 12.03.2026, анализ CV/МЛ 14.03.2026.")
    W, H = 1200, 420
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    cv.label(24, 112, "DONOR COLLECTIONS" if en else "СБОРЫ ПО ДОНОРАМ", FS_KICKER, MUTED, weight=800, box=400)
    bw, gap = 142, 24
    prev = None
    for i, (d, n) in enumerate(DON):
        x = 24 + i * (bw + gap)
        b = cv.box(x, 126, bw, d, [("Patient " if en else "Пациент ") + n], stroke=GREEN, h=76, center=True, title_size=15)
        if prev:
            cv.arrow([(x - gap + 2, 164), (x - 2, 164)], MUTED)
        prev = b
    cv.label(24, 252, "DATED REPORTS" if en else "ДАТИРОВАННЫЕ ОТЧЁТЫ", FS_KICKER, MUTED, weight=800, box=400)
    bw2, gap2 = 250, 45
    for i, (d, e, r) in enumerate(REP):
        x = 24 + i * (bw2 + gap2)
        cv.box(x, 266, bw2, d, [e if en else r], stroke=BLUE, h=76, center=True)
        if i:
            cv.arrow([(x - gap2 + 2, 304), (x - 2, 304)], MUTED)
    foot(cv, ("The old caption called this diagram hypothesis validation; it shows only dates, not a validation (guide/EVIDENCE.md)."
              if en else "Прежняя подпись называла схему валидацией гипотезы; она показывает только даты, а не валидацию (guide/EVIDENCE.ru.md)."), H - 16)
    return done(cv)


# ---------------------------------------------------------------- 4 timelapse
def timelapse(lang):
    en = lang == "en"
    t = "Time-lapse imaging system" if en else "Система покадровой съёмки"
    sub = "Previous README, diagram 4" if en else "Прежний README, схема 4"
    desc = ("Flow chart left to right. Plasma samples, then time-lapse camera, then image capture at 1 frame per 5 minutes, then preprocessing, "
            "which branches to LLM analysis and CV analysis, both ending in a comparison. This describes a planned system; the dataset is still photographs."
            if en else
            "Блок-схема слева направо. Образцы плазмы, затем камера 4K, затем съёмка кадра раз в 5 минут, затем предобработка, "
            "которая делится на анализ LLM и анализ CV, оба заканчиваются сравнением. Это описание планируемой системы; набор данных остаётся отдельными снимками.")
    W, H = 1200, 380
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    bw, y, h = 170, 170, 96
    bx = [24, 24 + 205, 24 + 410, 24 + 615]
    b1 = cv.box(bx[0], y, bw, "Plasma samples" if en else "Образцы плазмы", [], stroke=GOLD, h=h, center=True)
    b2 = cv.box(bx[1], y, bw, "Time-lapse camera" if en else "Камера 4K", [], stroke=TEAL, h=h, center=True, status=[PLAN[lang]] if False else [])
    b3 = cv.box(bx[2], y, bw, "Image capture" if en else "Съёмка кадров", ["1 frame / 5 min" if en else "1 кадр / 5 мин"], stroke=BLUE, h=h, center=True)
    b4 = cv.box(bx[3], y, bw, "Preprocessing" if en else "Предобработка", [], stroke=GREEN, h=h, center=True)
    for a, b in ((b1, b2), (b2, b3), (b3, b4)):
        cv.arrow([(a[0] + a[2], y + h / 2), (b[0] - 3, y + h / 2)], MUTED)
    b5 = cv.box(850, 110, 170, "LLM analysis" if en else "Анализ LLM", [], stroke=VIOLET, h=70, center=True)
    b6 = cv.box(850, 250, 170, "CV analysis" if en else "Анализ CV", [], stroke=AMBER, h=70, center=True)
    b7 = cv.box(1050, 170, 126, "Comparison" if en else "Сравнение", [], stroke=GOLD, h=h, center=True)
    cv.arrow([(bx[3] + bw, y + 30), (830, y + 30), (830, 145), (847, 145)], GREEN)
    cv.arrow([(bx[3] + bw, y + 66), (830, y + 66), (830, 285), (847, 285)], GREEN)
    cv.arrow([(1020, 145), (1035, 145), (1035, 200), (1047, 200)], MUTED)
    cv.arrow([(1020, 285), (1035, 285), (1035, 235), (1047, 235)], MUTED)
    cv.label(24, 120, PLAN[lang][0], FS_SMALL, VIOLET, weight=800, box=300)
    foot(cv, ("Describes a planned system; the dataset in the repository is still smartphone photographs (guide/METHODS.md)."
              if en else "Описывает планируемую систему; набор данных в репозитории пока остаётся снимками со смартфона (guide/METHODS.ru.md)."), H - 16)
    return done(cv)


# ---------------------------------------------------------------- 5 pipeline
def pipeline(lang):
    en = lang == "en"
    t = "Analysis pipeline" if en else "Конвейер анализа"
    sub = "Previous README, diagram 5" if en else "Прежний README, схема 5"
    desc = ("Flow chart. Raw images, then preprocessing, which splits into stage 1 CV analysis (SAM-2, SigLIP2, DINOv2) and stage 2 LLM vision (Claude Opus 4.6). "
            "Both feed stage 3 comparative cross-validation, then stage 4 statistical (ANOVA, t-tests, p-values), then final reports."
            if en else
            "Блок-схема. Сырые изображения, затем предобработка, которая делится на этап 1 CV-анализ (SAM-2, SigLIP2, DINOv2) и этап 2 LLM-зрение (Claude Opus 4.6). "
            "Оба ведут к этапу 3 сравнительная кросс-валидация, затем этап 4 статистический (ANOVA, t-тесты, p-значения), затем итоговые отчёты.")
    W, H = 1200, 700
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    b1 = cv.box(440, 100, 320, "Raw images" if en else "Сырые изображения", [], stroke=GOLD, h=48, center=True)
    b2 = cv.box(440, 176, 320, "Preprocessing" if en else "Предобработка", [], stroke=TEAL, h=48, center=True)
    down(cv, b1, b2)
    s1 = cv.box(180, 260, 340, "Stage 1: CV analysis" if en else "Этап 1: CV-анализ", ["SAM-2, SigLIP2, DINOv2"], stroke=BLUE, h=80, center=True)
    s2 = cv.box(680, 260, 340, "Stage 2: LLM vision" if en else "Этап 2: LLM-зрение", ["Claude Opus 4.6"], stroke=VIOLET, h=80, center=True)
    cv.arrow([(560, 224), (560, 242), (350, 242), (350, 257)], TEAL)
    cv.arrow([(640, 224), (640, 242), (850, 242), (850, 257)], TEAL)
    s3 = cv.box(380, 388, 440, "Stage 3: Comparative" if en else "Этап 3: Сравнительный", ["Cross-validation" if en else "Кросс-валидация"], stroke=GREEN, h=80, center=True)
    cv.arrow([(350, 340), (350, 364), (560, 364), (560, 385)], MUTED)
    cv.arrow([(850, 340), (850, 364), (640, 364), (640, 385)], MUTED)
    s4 = cv.box(380, 504, 440, "Stage 4: Statistical" if en else "Этап 4: Статистический", ["ANOVA, t-tests, p-values" if en else "ANOVA, t-тесты, p-значения"], stroke=AMBER, h=80, center=True)
    down(cv, s3, s4)
    b7 = cv.box(440, 616, 320, "Final reports" if en else "Итоговые отчёты", [], stroke=VIOLET, h=48, center=True)
    down(cv, s4, b7)
    return done(cv)


# ---------------------------------------------------------------- 6 protocol
def protocol(lang):
    en = lang == "en"
    t = "Experimental protocol" if en else "Протокол эксперимента"
    sub = "Previous README, diagram 6" if en else "Прежний README, схема 6"
    desc = ("Flow chart. Blood collection, 4 tubes per donor; centrifugation, 2000 RPM for 5 minutes; plasma separation, redistribute to samples; "
            "irradiation, about 1 hour 12 minutes, which branches into photography (before, during, after), channel 19 acceleration, channel 21 deceleration "
            "and control with no exposure. Photography continues to AI/ML analysis (multi-provider), statistics (ANOVA, t-tests) and reports (scientific papers). "
            "The protocol documents of the repository disagree on exposure time, tube type and centrifugation settings."
            if en else
            "Блок-схема. Забор крови, 4 пробирки на донора; центрифугирование, 2000 об/мин 5 минут; отбор плазмы, перераспределение по образцам; "
            "облучение, около 1 часа 12 минут, которое делится на фотографирование (до, во время, после), канал 19 ускорение, канал 21 замедление "
            "и контроль без воздействия. Съёмка продолжается анализом ИИ/МЛ (несколько провайдеров), статистикой (ANOVA, t-тесты) и отчётами (научные статьи). "
            "Протокольные документы репозитория расходятся по времени облучения, типу пробирок и режиму центрифугирования.")
    W, H = 1200, 1060
    cv = Canvas(W, H, t, desc, t, sub, TAG[lang])
    chain = [("Blood collection" if en else "Забор крови", "4 tubes per donor" if en else "4 пробирки на донора", GOLD),
             ("Centrifugation" if en else "Центрифугирование", "2000 RPM, 5 min" if en else "2000 об/мин, 5 мин", TEAL),
             ("Plasma separation" if en else "Отбор плазмы", "Redistribute to samples" if en else "Распределить по образцам", BLUE),
             ("Irradiation" if en else "Облучение", "~1h 12min" if en else "около 1 ч 12 мин", AMBER)]
    prev = None
    boxes = []
    for i, (n, l, col) in enumerate(chain):
        b = cv.box(450, 100 + i * 98, 300, n, [l], stroke=col, h=76, center=True)
        if prev:
            down(cv, prev, b)
        prev = b
        boxes.append(b)
    ys = 100 + 4 * 98 + 4
    ph = cv.box(24, ys, 276, "Photography" if en else "Фотографирование", ["Before, during, after" if en else "До, во время, после"], stroke=GREEN, h=76, center=True)
    c19 = cv.box(312, ys, 276, "Channel 19" if en else "Канал 19", ["Acceleration" if en else "Ускорение"], status=[CLAIM[lang]], stroke=VIOLET, h=100, center=True)
    c21 = cv.box(600, ys, 276, "Channel 21" if en else "Канал 21", ["Deceleration" if en else "Замедление"], status=[CLAIM[lang]], stroke=VIOLET, h=100, center=True)
    ct = cv.box(888, ys, 276, "Control" if en else "Контроль", ["No exposure" if en else "Без воздействия"], stroke=TEAL, h=76, center=True)
    for b in (ph, c19, c21, ct):
        cv.arrow([(600, boxes[-1][1] + 76), (center_x(b), b[1] - 3)], AMBER)
    prev = ph
    for i, (n, l, col) in enumerate([("AI/ML analysis" if en else "Анализ ИИ/МЛ", "Multi-provider" if en else "Несколько провайдеров", VIOLET),
                                     ("Statistics" if en else "Статистика", "ANOVA, t-tests" if en else "ANOVA, t-тесты", AMBER),
                                     ("Reports" if en else "Отчёты", "Scientific papers" if en else "Научные статьи", BLUE)]):
        b = cv.box(24, ys + 100 + i * 90, 276, n, [l], stroke=col, h=68, center=True)
        down(cv, prev, b)
        prev = b
    foot(cv, ("The protocol documents disagree on exposure time, tube type and centrifugation settings (guide/OPEN.md); the diagram keeps the old README's values."
              if en else "Протокольные документы расходятся по времени облучения, типу пробирок и режиму центрифугирования (guide/OPEN.ru.md); схема сохраняет значения прежнего README."), H - 16)
    return done(cv)


def main():
    for lang in ("en", "ru"):
        for name, fn in (("overview", overview), ("patent", patent), ("dates", dates),
                         ("timelapse", timelapse), ("pipeline", pipeline), ("protocol", protocol)):
            write("guide/assets/diagrams/redraw-%s.%s.svg" % (name, lang), fn(lang))


if __name__ == "__main__":
    main()
