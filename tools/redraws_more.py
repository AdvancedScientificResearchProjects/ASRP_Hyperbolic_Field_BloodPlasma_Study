"""More redraws (see tools/build_redraws.py): data_1..4.png, osf_1.png and the distinct schemas of the mirror folder.
Output guide/assets/diagrams/redraw-<name>.{en,ru}.svg. Donor-level material (minute-level session times) is not drawn."""
import datetime
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F401,F403

CLAIM = {"en": ("◇ CLAIMED ONLY", VIOLET), "ru": ("◇ ТОЛЬКО ЗАЯВЛЕНО", VIOLET)}
ABSENT = {"en": ("✕ NOT IN REPO", AMBER), "ru": ("✕ НЕТ В РЕПО", AMBER)}
PLAN = {"en": ("◇ PLANNED", VIOLET), "ru": ("◇ В ПЛАНАХ", VIOLET)}
NOTMEAS = {"en": ("✕ NEVER MEASURED", AMBER), "ru": ("✕ НЕ ИЗМЕРЯЛОСЬ", AMBER)}
TAG = {"en": "REDRAWN FIGURE", "ru": "ПЕРЕРИСОВАННАЯ СХЕМА"}
PINK = "#f472b6"


def done(cv):
    return "\n".join(cv.o + ["</svg>\n"])


def foot(cv, text_, bottom):
    lines = wrap(text_, FS_SMALL, cv.w - 48)
    y = bottom - 20 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        cv.label(24, y + 20 * i, ln, FS_SMALL, MUTED, box=cv.w - 48)


def cx(b):
    return b[0] + b[2] / 2


def down(cv, a, b, col=MUTED):
    cv.arrow([(cx(a), a[1] + a[3]), (cx(b), b[1] - 3)], col)


def right(cv, a, b, col=MUTED):
    cv.arrow([(a[0] + a[2], a[1] + a[3] / 2), (b[0] - 3, b[1] + b[3] / 2)], col)


def head(lang, en, ru, sub_en, sub_ru, desc_en, desc_ru, W, H):
    en_ = lang == "en"
    t = en if en_ else ru
    return Canvas(W, H, t, desc_en if en_ else desc_ru, t, sub_en if en_ else sub_ru, TAG[lang])


# ---------------------------------------------------------------- data_1: photos by donor code (pie)
COUNTS = [("01", 13), ("02", 25), ("03", 16), ("04", 4), ("05", 10), ("06", 3), ("07", 30)]
COLS = [BLUE, GOLD, GREEN, TEAL, AMBER, PINK, VIOLET]


def data_photos(lang):
    en = lang == "en"
    tot = sum(n for _, n in COUNTS)
    cv = head(lang, "Photographs by donor code", "Фотографии по кодам доноров", "Previous README, data diagram 1", "Прежний README, схема данных 1",
              "Pie chart of 101 photographs by anonymous donor code: Patient 01 13, 02 25, 03 16, 04 4, 05 10, 06 3, 07 30 photographs.",
              "Круговая диаграмма 101 фотографии по анонимным кодам доноров: пациент 01 13, 02 25, 03 16, 04 4, 05 10, 06 3, 07 30 фотографий.", 1000, 580)
    cx0, cy0, r = 290, 290, 170
    a0 = -math.pi / 2
    for (code, n), col in zip(COUNTS, COLS):
        a1 = a0 + 2 * math.pi * n / tot
        large = 1 if a1 - a0 > math.pi else 0
        cv.o.append("<path d='M%.1f,%.1f L%.1f,%.1f A%d,%d 0 %d 1 %.1f,%.1f Z' fill='%s' fill-opacity='0.85' stroke='%s' stroke-width='2'/>" % (
            cx0, cy0, cx0 + r * math.cos(a0), cy0 + r * math.sin(a0), r, r, large, cx0 + r * math.cos(a1), cy0 + r * math.sin(a1), col, BG0))
        am = (a0 + a1) / 2
        cv.o.append(text("%.1f" % (cx0 + r * 0.66 * math.cos(am)), "%.1f" % (cy0 + r * 0.66 * math.sin(am) + 5), "%d%%" % round(100 * n / tot), 14, BG0, "middle", 800))
        a0 = a1
    for i, ((code, n), col) in enumerate(zip(COUNTS, COLS)):
        y = 140 + i * 40
        cv.o.append("<rect x='620' y='%d' width='18' height='18' rx='4' fill='%s'/>" % (y - 14, col))
        cv.label(650, y, ("Patient " if en else "Пациент ") + code, FS_BODY, INK, weight=700, box=140)
        cv.label(790, y, ("%d photos" if en else "%d фото") % n, FS_BODY, MUTED, box=190)
    foot(cv, ("Anonymous donor codes and shares only. Photographs are not independent observations (guide/DATA.md)." if en else
              "Только анонимные коды доноров и доли. Фотографии не независимые наблюдения (guide/DATA.ru.md)."), 560)
    return done(cv)


# ---------------------------------------------------------------- data_4: dates with counts
def data_dates(lang):
    en = lang == "en"
    ds = [("Jan 24", "24 янв"), ("Jan 28", "28 янв"), ("Jan 29", "29 янв"), ("Jan 30", "30 янв"), ("Jan 31", "31 янв"), ("Feb 01", "1 фев"), ("Feb 07", "7 фев")]
    cv = head(lang, "Collection dates and photographs per donor code", "Даты сбора и фотографии по кодам доноров", "Previous README, data diagram 4", "Прежний README, схема данных 4",
              "Seven boxes joined by arrows: Jan 24 P01 13 photographs, Jan 28 P02 25, Jan 29 P03 16, Jan 30 P04 4, Jan 31 P05 10, Feb 01 P06 3, Feb 07 P07 30.",
              "Семь блоков со стрелками: 24 янв P01 13 фотографий, 28 янв P02 25, 29 янв P03 16, 30 янв P04 4, 31 янв P05 10, 1 фев P06 3, 7 фев P07 30.", 1200, 250)
    bw, gap = 142, 24
    prev = None
    for i, ((d_en, d_ru), (code, n)) in enumerate(zip(ds, COUNTS)):
        x = 24 + i * (bw + gap)
        b = cv.box(x, 110, bw, d_en if en else d_ru, ["P%s (%d)" % (code, n)], stroke=GREEN, h=76, center=True)
        if prev:
            cv.arrow([(x - gap + 2, 148), (x - 2, 148)], MUTED)
        prev = b
    foot(cv, "Number in brackets: photographs of that donor code." if en else "В скобках число фотографий этого кода донора.", 230)
    return done(cv)


# ---------------------------------------------------------------- data_2: three columns of claimed values
def data_metrics(lang):
    en = lang == "en"
    cols = [("Control", "Контроль", "baseline", "базовый", TEAL, [("Clot count", "Кол-во сгустков", "8.92"), ("Area", "Площадь", "0.90%"), ("Texture", "Текстура", "4.12"), ("Edge", "Край", "0.0016"), ("LLM", "LLM", "65%")], False),
            ("Channel 19", "Канал 19", "time acceleration", "ускорение времени", VIOLET, [("Count", "Кол-во", "5.64 −37%"), ("Area", "Площадь", "0.52% −42%"), ("Texture", "Текстура", "5.26 +28%"), ("Edge", "Край", "0.0012 −25%"), ("LLM", "LLM", "78% +13%")], True),
            ("Channel 21", "Канал 21", "time deceleration", "замедление времени", BLUE, [("Count", "Кол-во", "8.69 −3%"), ("Area", "Площадь", "0.58% −35%"), ("Texture", "Текстура", "4.16 +1%"), ("Edge", "Край", "0.0034 +113%"), ("LLM", "LLM", "41% −24%")], False)]
    cv = head(lang, "Metrics by condition, as quoted", "Метрики по условиям, как приведены", "Previous README, data diagram 2", "Прежний README, схема данных 2",
              "Three columns. Control, baseline: clot count 8.92, area 0.90%, texture 4.12, edge 0.0016, LLM 65%. Channel 19, time acceleration: count 5.64 (-37%), area 0.52% (-42%), "
              "texture 5.26 (+28%), edge 0.0012 (-25%), LLM 78% (+13%), one lysis case. Channel 21, time deceleration: count 8.69 (-3%), area 0.58% (-35%), texture 4.16 (+1%), "
              "edge 0.0034 (+113%), LLM 41% (-24%). Values as quoted by the previous README; claimed only.",
              "Три колонки. Контроль, базовый: сгустков 8.92, площадь 0.90%, текстура 4.12, край 0.0016, LLM 65%. Канал 19, ускорение времени: кол-во 5.64 (-37%), площадь 0.52% (-42%), "
              "текстура 5.26 (+28%), край 0.0012 (-25%), LLM 78% (+13%), один случай лизиса. Канал 21, замедление времени: кол-во 8.69 (-3%), площадь 0.58% (-35%), текстура 4.16 (+1%), "
              "край 0.0034 (+113%), LLM 41% (-24%). Значения как в прежнем README; только заявлено.", 1200, 770)
    for i, (n_en, n_ru, s_en, s_ru, col, rows, lysis) in enumerate(cols):
        x = 24 + i * 392
        cv.panel(x, 96, 376, 540, None, col)
        cv.label(x + 188, 128, n_en if en else n_ru, 18, INK, "middle", 800, box=340)
        cv.label(x + 188, 150, (s_en if en else s_ru).upper(), FS_SMALL, col, "middle", 800, box=340)
        for j, (a, b, v) in enumerate(rows):
            cv.box(x + 28, 170 + j * 68, 320, "%s: %s" % (a if en else b, v), [], stroke=col, h=52, center=True)
        if lysis:
            cv.box(x + 28, 170 + 5 * 68, 320, "Lysis case" if en else "Случай лизиса", [], stroke=col, h=52, center=True)
    foot(cv, ("All values are quoted from the previous README and are claimed only; the clot detector behind them was rejected by the repository's own report (guide/EVIDENCE.md)." if en else
              "Все значения приведены из прежнего README и только заявлены; детектор сгустков за ними отвергнут собственным отчётом репозитория (guide/EVIDENCE.ru.md)."), 750)
    return done(cv)


# ---------------------------------------------------------------- data_3
def data_flow(lang):
    en = lang == "en"
    cv = head(lang, "Samples, conditions and quoted values", "Образцы, условия и приведённые значения", "Previous README, data diagram 3", "Прежний README, схема данных 3",
              "Plasma samples split into control (normal time: 8.92 clots, 0.90% area), channel 19 (faster time: 5.64 clots, 0.52% area, +28% texture) and channel 21 (slower time: 8.69 clots, 0.58% area, +113% edge). Values claimed only.",
              "Образцы плазмы делятся на контроль (норма: 8.92 сгустков, площадь 0.90%), канал 19 (быстрее: 5.64 сгустков, площадь 0.52%, +28% текстуры) и канал 21 (медленнее: 8.69 сгустков, площадь 0.58%, +113% края). Значения только заявлены.", 1200, 530)
    src = cv.box(24, 190, 250, "Plasma samples" if en else "Образцы плазмы", [], stroke=GOLD, h=64, center=True)
    rows = [("Control" if en else "Контроль", "Normal time" if en else "Норма", TEAL, ["8.92 clots" if en else "8.92 сгустков", "0.90% area" if en else "0.90% площадь"], False),
            ("Channel 19" if en else "Канал 19", "Faster time" if en else "Быстрее", VIOLET, ["5.64 clots" if en else "5.64 сгустков", "0.52% area" if en else "0.52% площадь", "+28% texture" if en else "+28% текстура"], True),
            ("Channel 21" if en else "Канал 21", "Slower time" if en else "Медленнее", BLUE, ["8.69 clots" if en else "8.69 сгустков", "0.58% area" if en else "0.58% площадь", "+113% edge" if en else "+113% край"], True)]
    for i, (n, sl, col, vals, claim) in enumerate(rows):
        y = 96 + i * 120
        b = cv.box(420, y, 270, n, [sl], stroke=col, h=96, center=True)
        v = cv.box(830, y, 330, None, vals, stroke=col, h=96, center=True)
        cv.arrow([(274, 222), (340, 222), (340, y + 48), (417, y + 48)], col)
        cv.arrow([(690, y + 48), (827, y + 48)], col)
    foot(cv, ("Values are quoted from the previous README and are claimed only (guide/EVIDENCE.md)." if en else
              "Значения приведены из прежнего README и только заявлены (guide/EVIDENCE.ru.md)."), 510)
    return done(cv)


# ---------------------------------------------------------------- osf_1
def osf(lang):
    en = lang == "en"
    cv = head(lang, "OSF preregistration structure", "Структура предварительной регистрации OSF", "Previous README, OSF diagram", "Прежний README, схема OSF",
              "Tree. OSF preregistration has four branches. Primary hypothesis H1: hyperbolic field exposure produces measurable changes. Sampling plan: 5-10 donors, 30-60 plasma samples. "
              "Analysis plan: ANOVA with post-hoc analysis, p below .05 significance. Variables: clot formation time and clot degradation rate, both never measured in the repository.",
              "Дерево. Предварительная регистрация OSF имеет четыре ветви. Основная гипотеза H1: воздействие гиперболического поля вызывает измеримые изменения. План выборки: 5-10 доноров, 30-60 образцов плазмы. "
              "План анализа: ANOVA с пост-хок анализом, значимость p < .05. Переменные: время образования сгустка и скорость деградации сгустка, оба не измерялись в репозитории.", 1200, 560)
    root = cv.box(425, 96, 350, "OSF preregistration" if en else "Регистрация OSF", [], stroke=GOLD, h=52, center=True)
    kids = [("Primary hypothesis" if en else "Основная гипотеза", RED if False else AMBER, 24, 260),
            ("Sampling plan" if en else "План выборки", BLUE, 320, 260),
            ("Analysis plan" if en else "План анализа", VIOLET, 616, 260),
            ("Variables" if en else "Переменные", TEAL, 912, 264)]
    leaves = [[("H1", ["Hyperbolic field exposure produces measurable changes" if en else "Воздействие гиперболического поля вызывает измеримые изменения"], None)],
              [("5-10 donors" if en else "5-10 доноров", [], None), ("30-60 plasma samples" if en else "30-60 образцов плазмы", [], None)],
              [("ANOVA with post-hoc" if en else "ANOVA с пост-хок анализом", [], None), ("p < .05 significance" if en else "p < .05 значимость", [], None)],
              [("Clot formation time" if en else "Время образования сгустка", [], NOTMEAS[lang]), ("Clot degradation rate" if en else "Скорость деградации сгустка", [], NOTMEAS[lang])]]
    for (name, col, x, w), lv in zip(kids, leaves):
        k = cv.box(x, 200, w, name, [], stroke=col, h=52, center=True)
        cv.arrow([(600, 148), (600, 174), (cx(k), 174), (cx(k), 197)], col)
        y = 290
        for (t, body, st) in lv:
            hh = 140 if body else (96 if st else 72)
            b = cv.box(x + 28, y, w - 28, t, body, status=[st] if st else [], stroke=col, h=hh, center=True)
            cv.arrow([(x + 14, y + 26), (x + 25, y + 26)], col)
            y += hh + 14
        cv.o.append("<line x1='%s' y1='252' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (x + 14, x + 14, y - 14 - 26 + 10, col))
    foot(cv, ("The registration states the design; the clot-time outcomes were never measured and photographs stand in for them (guide/PUBLICATIONS.md)." if en else
              "Регистрация задаёт дизайн; исходы по времени свёртывания не измерялись, их заменяют фотографии (guide/PUBLICATIONS.ru.md)."), 540)
    return done(cv)


# ---------------------------------------------------------------- issue_2_1: programme structure
def program(lang):
    en = lang == "en"
    cv = head(lang, "Research programme structure", "Структура программы исследований", "Programme issue 2 (mirror folder)", "Задача 2 (папка-зеркало)",
              "Tree. ASRP Hyperbolic Field Research Program 2026-2027 has four branches. Blood Plasma Study: coagulation analysis, time-lapse imaging (planned), biochemical analysis (not in repo). DAAT Crystal Study: human-crystal interaction. "
              "Agricultural Study: plant growth, fungi cultivation. Emitter Programs: control software, AI algorithms.",
              "Дерево. Программа исследований гиперболических полей ASRP 2026-2027 имеет четыре ветви. Исследование кровяной плазмы: анализ свёртываемости, покадровая съёмка (в планах), биохимический анализ (нет в репо). Исследование кристаллов DAAT: взаимодействие человек-кристалл. "
              "Сельскохозяйственное исследование: рост растений, выращивание грибов. Программы излучателей: ПО управления, ИИ-алгоритмы.", 1200, 650)
    top = cv.box(350, 96, 500, "ASRP Hyperbolic Field Research Program 2026-2027" if en else "Программа исследований гиперболических полей ASRP 2026-2027", [], stroke=GOLD, h=72, center=True)
    kids = [("Blood Plasma Study" if en else "Исследование кровяной плазмы", AMBER, [("Coagulation analysis" if en else "Анализ свёртываемости", None), ("Time-lapse imaging" if en else "Покадровая съёмка", PLAN[lang]), ("Biochemical analysis" if en else "Биохимический анализ", ABSENT[lang])]),
            ("DAAT Crystal Study" if en else "Исследование кристаллов DAAT", TEAL, [("Human-crystal interaction" if en else "Взаимодействие человек-кристалл", None)]),
            ("Agricultural Study" if en else "Сельскохозяйственное исследование", GREEN, [("Plant growth" if en else "Рост растений", None), ("Fungi cultivation" if en else "Выращивание грибов", None)]),
            ("Emitter Programs" if en else "Программы излучателей", BLUE, [("Control software" if en else "ПО управления", None), ("AI algorithms" if en else "ИИ-алгоритмы", None)])]
    for i, (name, col, ch) in enumerate(kids):
        x = 24 + i * 292
        k = cv.box(x, 210, 262, name, [], stroke=col, h=72, center=True)
        cv.arrow([(600, 168), (600, 190), (cx(k), 190), (cx(k), 207)], col)
        y = 306
        for t, st in ch:
            h = 82 if st else 72
            cv.box(x + 28, y, 234, t, [], status=[st] if st else [], stroke=col, h=h, center=True)
            cv.arrow([(x + 14, y + h / 2), (x + 25, y + h / 2)], col)
            y += h + 14
        cv.o.append("<line x1='%s' y1='282' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (x + 14, x + 14, y - 14 - (82 if ch[-1][1] else 72) / 2, col))
    foot(cv, ("Status words follow guide/EVIDENCE.md: no biochemical data are in the repository and time-lapse is a planned system." if en else
              "Слова-статусы по guide/EVIDENCE.ru.md: биохимических данных в репозитории нет, покадровая съёмка планируемая система."), 630)
    return done(cv)


# ---------------------------------------------------------------- issue_2_2: team to projects
def team(lang):
    en = lang == "en"
    cv = head(lang, "Team and projects", "Команда и проекты", "Programme issue 2 (mirror folder)", "Задача 2 (папка-зеркало)",
              "Two columns. Team: Denis Banchenko CEO / physics; Valeria Ovseannicova CBE / biomedical; Mykhailo Kapustin CTO / IT and AI; Kyryl Zmiienko chief AI engineer; Alexandr Ovsyannikov head hardware engineer. "
              "Projects: Blood Plasma (Valeria and Denis), DAAT Crystal (Denis), Agricultural (Mykhailo), Emitter Programs (Mykhailo and Alexandr). Edges: Denis to Blood Plasma and DAAT Crystal; Valeria to Blood Plasma; Mykhailo to Agricultural and Emitter Programs; Kyryl to Blood Plasma; Alexandr to Emitter Programs.",
              "Две колонки. Команда: Denis Banchenko CEO / физика; Valeria Ovseannicova CBE / биомедицина; Mykhailo Kapustin CTO / IT и ИИ; Kyryl Zmiienko главный инженер ИИ; Alexandr Ovsyannikov главный инженер по оборудованию. "
              "Проекты: кровяная плазма (Valeria и Denis), кристаллы DAAT (Denis), сельскохозяйственный (Mykhailo), программы излучателей (Mykhailo и Alexandr). Связи: Denis к плазме и кристаллам; Valeria к плазме; Mykhailo к сельскохозяйственному и излучателям; Kyryl к плазме; Alexandr к излучателям.", 1200, 560)
    cv.panel(24, 96, 400, 420, "TEAM" if en else "КОМАНДА", LINE)
    cv.panel(776, 96, 400, 420, "PROJECTS" if en else "ПРОЕКТЫ", LINE)
    people = [("Denis Banchenko", "CEO / Physics" if en else "CEO / физика", GOLD), ("Valeria Ovseannicova", "CBE / Biomedical" if en else "CBE / биомедицина", AMBER),
              ("Mykhailo Kapustin", "CTO / IT & AI" if en else "CTO / IT и ИИ", TEAL), ("Kyryl Zmiienko", "Chief AI Engineer" if en else "Главный инженер ИИ", BLUE),
              ("Alexandr Ovsyannikov", "Head Hardware Engineer" if en else "Главный инженер по оборудованию", GREEN)]
    pj = [("Blood Plasma" if en else "Кровяная плазма", "Valeria + Denis", AMBER), ("DAAT Crystal" if en else "Кристаллы DAAT", "Denis", VIOLET),
          ("Agricultural" if en else "Сельскохозяйственный", "Mykhailo", GREEN), ("Emitter Programs" if en else "Программы излучателей", "Mykhailo + Alexandr", BLUE)]
    pb = []
    for i, (n, r, c) in enumerate(people):
        pb.append(cv.box(44, 140 + i * 74, 360, n, [r], stroke=c, h=68, center=True))
    qb = []
    for i, (n, r, c) in enumerate(pj):
        qb.append(cv.box(796, 150 + i * 90, 360, n, [r], stroke=c, h=68, center=True))
    for a, b, c in ((0, 0, AMBER), (0, 1, VIOLET), (1, 0, AMBER), (2, 2, GREEN), (2, 3, BLUE), (3, 0, AMBER), (4, 3, BLUE)):
        cv.arrow([(404, pb[a][1] + 31), (793, qb[b][1] + 33)], c)
    return done(cv)


# ---------------------------------------------------------------- issue_2retry_1: repository structure
def repo(lang):
    en = lang == "en"
    cv = head(lang, "Data, analysis and team", "Данные, анализ и команда", "Programme issue 2 (mirror folder)", "Задача 2 (папка-зеркало)",
              "Chain of six steps: raw data, processed, results (data panel), then notebooks (Jupyter), scripts (Python), reports (analysis panel). The team panel has Valeria lead, Denis physics, Alexandr electrical, all linked to data, and Kyryl AI/ML linked to analysis.",
              "Цепочка из шести шагов: сырые данные, обработанные, результаты (панель данных), затем ноутбуки (Jupyter), скрипты (Python), отчёты (панель анализа). Панель команды: Valeria лидер, Denis физика, Alexandr электрика связаны с данными, Kyryl ИИ/МЛ связан с анализом.", 1200, 450)
    cv.panel(14, 96, 590, 124, "DATA" if en else "ДАННЫЕ", LINE)
    cv.panel(614, 96, 572, 124, "ANALYSIS" if en else "АНАЛИЗ", LINE)
    steps = [("Raw data" if en else "Сырые данные", TEAL), ("Processed" if en else "Обработанные", BLUE), ("Results" if en else "Результаты", GREEN),
             ("Notebooks" if en else "Ноутбуки", GOLD), ("Scripts" if en else "Скрипты", AMBER), ("Reports" if en else "Отчёты", VIOLET)]
    bs = []
    for i, (n, c) in enumerate(steps):
        bs.append(cv.box(24 + i * 192, 140, 170, n, ["Jupyter" if i == 3 else "Python"] if i in (3, 4) else [], stroke=c, h=70, center=True))
        if i:
            cv.arrow([(24 + i * 192 - 22, 172), (24 + i * 192 - 2, 172)], MUTED)
    cv.panel(14, 270, 1172, 140, "TEAM" if en else "КОМАНДА", LINE)
    tm = [("Valeria", "Lead" if en else "Лидер", AMBER, 24, (130, 220)), ("Denis", "Physics" if en else "Физика", BLUE, 224, (310, 220)),
          ("Alexandr", "Electrical" if en else "Электрика", GREEN, 424, (490, 220)), ("Kyryl", "AI/ML" if en else "ИИ/МЛ", VIOLET, 824, (910, 220))]
    for n, r, c, x, (ax, ay) in tm:
        b = cv.box(x, 320, 170, n, [r], stroke=c, h=70, center=True)
        cv.arrow([(x + 85, 318), (x + 85, 224)], c)
    return done(cv)


# ---------------------------------------------------------------- issue_2_4: roadmap
def roadmap(lang):
    en = lang == "en"
    cv = head(lang, "Programme roadmap", "Дорожная карта программы", "Programme issue 2 (mirror folder)", "Задача 2 (папка-зеркало)",
              "Seven boxes with arrows: Jan 24-31 data collection; Feb 01-07 donors P06 and P07; Feb 25-26 AI/LLM analysis; Mar 12-14 comparative analysis; Mar 18-26 issues and repository; Apr-May peer review and publication (planned); future, 30 donors (planned).",
              "Семь блоков со стрелками: 24-31 янв сбор данных; 1-7 фев доноры P06 и P07; 25-26 фев анализ ИИ/LLM; 12-14 мар сравнительный анализ; 18-26 мар задачи и репозиторий; апр-май рецензирование и публикация (в планах); в будущем 30 доноров (в планах).", 1200, 330)
    items = [("Jan 24-31" if en else "24-31 янв", "Data collection" if en else "Сбор данных", None, GREEN), ("Feb 01-07" if en else "1-7 фев", "P06, P07", None, GREEN),
             ("Feb 25-26" if en else "25-26 фев", "AI/LLM analysis" if en else "Анализ ИИ/LLM", None, BLUE), ("Mar 12-14" if en else "12-14 мар", "Comparative analysis" if en else "Сравнительный анализ", None, BLUE),
             ("Mar 18-26" if en else "18-26 мар", "Issues & repo" if en else "Задачи и репозиторий", None, TEAL), ("Apr-May" if en else "апр-май", "Peer review" if en else "Рецензия, публикация", PLAN[lang], VIOLET),
             ("Future" if en else "В будущем", "30 donors" if en else "30 доноров", PLAN[lang], VIOLET)]
    for i, (d, n, st, c) in enumerate(items):
        x = 24 + i * 166
        cv.box(x, 110, 142, d, [n], status=[st] if st else [], stroke=c, h=150, center=True)
        if i:
            cv.arrow([(x - 22, 185), (x - 2, 185)], MUTED)
    foot(cv, ("April-May peer review and 30 donors are plans; the repository has no manuscript and 7 donors (guide/EVIDENCE.md)." if en else
              "Рецензирование в апреле-мае и 30 доноров это планы; в репозитории нет рукописи и 7 доноров (guide/EVIDENCE.ru.md)."), 310)
    return done(cv)


# ---------------------------------------------------------------- issue_3_1: protocol flow
def donor_flow(lang):
    en = lang == "en"
    steps = [("Donor recruitment", "Набор доноров", None), ("Blood collection", "Забор крови", None), ("Plasma separation", "Разделение плазмы", None), ("Triplet prep", "Подготовка триплетов", None),
             ("HF exposure", "Воздействие ГП", None), ("Time-lapse", "Покадровая съёмка", PLAN[lang]), ("Coagulation analysis", "Анализ свёртываемости", None), ("Biochemical markers", "Биохимические маркеры", ABSENT[lang]),
             ("LLM/CV analysis", "Анализ LLM/CV", None), ("Statistics", "Статистика", None), ("Final report", "Финальный отчёт", None)]
    cv = head(lang, "Blood plasma protocol flow", "Ход протокола по плазме крови", "Programme issue 3 (mirror folder)", "Задача 3 (папка-зеркало)",
              "Eleven steps in order: donor recruitment, blood collection, plasma separation, triplet preparation, hyperbolic-field exposure, time-lapse (planned), coagulation analysis, biochemical markers (not in repo), LLM/CV analysis, statistics, final report.",
              "Одиннадцать шагов по порядку: набор доноров, забор крови, разделение плазмы, подготовка триплетов, воздействие гиперболического поля, покадровая съёмка (в планах), анализ свёртываемости, биохимические маркеры (нет в репо), анализ LLM/CV, статистика, финальный отчёт.", 1200, 500)
    cols = [GOLD, TEAL, BLUE, AMBER, GREEN, VIOLET, TEAL, AMBER, BLUE, GREEN, GOLD]
    pos = []
    for i, (e, r, st) in enumerate(steps):
        row, c = divmod(i, 4)
        x, y = 24 + c * 300, 96 + row * 150
        b = cv.box(x, y, 250, ("%d. " % (i + 1)) + (e if en else r), [], status=[st] if st else [], stroke=cols[i], h=96, center=True)
        pos.append(b)
        if i:
            if c:
                cv.arrow([(x - 50 + 2, y + 48), (x - 2, y + 48)], MUTED)
            else:
                pb = pos[i - 1]
                cv.arrow([(pb[0] + 125, pb[1] + 96), (pb[0] + 125, pb[1] + 123), (x + 125, y - 27), (x + 125, y - 3)], MUTED)
    return done(cv)


# ---------------------------------------------------------------- issue_5_1: biochemical integration
def biochem(lang):
    en = lang == "en"
    cv = head(lang, "Biochemical integration", "Интеграция биохимии", "Programme issue 5 (mirror folder)", "Задача 5 (папка-зеркало)",
              "Plasma leads to coagulation and to biochemical (not in repo); both lead to image analysis, then LLM/CV correlation, then statistics, then a report.",
              "Плазма ведёт к свёртываемости и к биохимии (нет в репо); обе ведут к анализу изображений, затем корреляция LLM/CV, затем статистика, затем отчёт.", 1200, 330)
    X = lambda i: 24 + i * 194
    W_ = 176
    a = cv.box(X(0), 140, 172, "Plasma" if en else "Плазма", [], stroke=TEAL, h=70, center=True,pad=10)
    b = cv.box(X(1), 100, 172, "Coagulation" if en else "Свёртываемость", [], stroke=BLUE, h=70, center=True,pad=10)
    c = cv.box(X(1), 190, 172, "Biochemical" if en else "Биохимия", [], status=[ABSENT[lang]], stroke=AMBER, h=88, center=True,pad=10)
    d = cv.box(X(2), 140, 172, "Image analysis" if en else "Анализ изображений", [], stroke=GOLD, h=70, center=True,pad=10)
    e = cv.box(X(3), 140, 172, "LLM/CV", ["Correlation" if en else "Корреляция"], stroke=GREEN, h=70, center=True,pad=10)
    f = cv.box(X(4), 140, 172, "Statistics" if en else "Статистика", [], stroke=VIOLET, h=70, center=True,pad=10)
    g = cv.box(X(5), 140, 172, "Report" if en else "Отчёт", [], stroke=PINK, h=70, center=True,pad=10)
    cv.arrow([(a[0] + 172, 160), (X(1) - 2, 132)], MUTED)
    cv.arrow([(a[0] + 172, 190), (X(1) - 2, 232)], MUTED)
    cv.arrow([(X(1) + 172, 132), (X(2) - 2, 160)], MUTED)
    cv.arrow([(X(1) + 172, 232), (X(2) - 2, 190)], MUTED)
    for p, q in ((d, e), (e, f), (f, g)):
        right(cv, p, q)
    foot(cv, "No biochemical data are in the repository (guide/EVIDENCE.md)." if en else "Биохимических данных в репозитории нет (guide/EVIDENCE.ru.md).", 310)
    return done(cv)


# ---------------------------------------------------------------- issue_8_1: publication gantt
def gantt(lang):
    en = lang == "en"
    d0 = datetime.date(2026, 3, 1)
    bars = []
    s = d0
    for name_en, name_ru, days in (("Manuscript draft", "Черновик рукописи", 30), ("Internal review", "Внутреннее рецензирование", 14),
                                   ("External peer review", "Внешнее рецензирование", 30), ("Final edits", "Финальная правка", 7), ("Publication", "Публикация", 7)):
        bars.append((name_en if en else name_ru, s, s + datetime.timedelta(days=days)))
        s = s + datetime.timedelta(days=days)
    cv = head(lang, "Publication timeline (plan)", "Сроки публикации (план)", "Programme issue 8 (mirror folder)", "Задача 8 (папка-зеркало)",
              "Gantt chart, all planned. Preparation: manuscript draft 2026-03-01 for 30 days, internal review 14 days, external peer review 30 days. Publication: final edits 7 days, publication 7 days, ending 2026-05-28.",
              "Диаграмма Ганта, всё в планах. Подготовка: черновик рукописи с 2026-03-01 на 30 дней, внутреннее рецензирование 14 дней, внешнее рецензирование 30 дней. Публикация: финальная правка 7 дней, публикация 7 дней, до 2026-05-28.", 1200, 570)
    x0, x1 = 300, 1176
    ppd = (x1 - x0) / 88.0
    cv.label(24, 112, "PREPARATION" if en else "ПОДГОТОВКА", FS_KICKER, MUTED, weight=800, box=250)
    for k in range(0, 89, 7):
        x = x0 + k * ppd
        cv.o.append("<line x1='%.1f' y1='122' x2='%.1f' y2='%d' stroke='%s' stroke-dasharray='3 6'/>" % (x, x, 120 + 5 * 58 + 20, LINE))
        cv.label(x, 120 + 5 * 58 + 38, (d0 + datetime.timedelta(days=k)).isoformat()[5:], FS_SMALL, MUTED, "middle", box=60)
    for i, (n, a, b) in enumerate(bars):
        y = 130 + i * 58 + (24 if i >= 3 else 0)
        if i == 3:
            cv.label(24, y - 18, "PUBLICATION" if en else "ПУБЛИКАЦИЯ", FS_KICKER, MUTED, weight=800, box=250)
        cv.label(24, y + 14, n, FS_BODY, INK, weight=700, box=270)
        cv.label(24, y + 33, "%s to %s" % (a.isoformat(), b.isoformat()) if en else "%s - %s" % (a.isoformat(), b.isoformat()), FS_SMALL, MUTED, box=270)
        xa, xb = x0 + (a - d0).days * ppd, x0 + (b - d0).days * ppd
        cv.o.append("<rect x='%.1f' y='%d' width='%.1f' height='30' rx='7' fill='%s' fill-opacity='0.25' stroke='%s' stroke-width='1.8' stroke-dasharray='6 4'/>" % (xa, y, xb - xa, PANEL, VIOLET))
    cv.label(1176, 505, PLAN[lang][0] + ("  (dashed = planned)" if en else "  (пунктир = план)"), FS_SMALL, VIOLET, "end", 800, box=400)
    foot(cv, ("A plan only: the repository holds no manuscript or submission record (guide/EVIDENCE.md). The original's red render-date marker is not drawn." if en else
              "Только план: рукописи и записи о подаче в репозитории нет (guide/EVIDENCE.ru.md). Красная метка даты рендера оригинала не рисуется."), 556)
    return done(cv)


ALL = [("data-photos", data_photos), ("data-dates", data_dates), ("data-metrics", data_metrics), ("data-flow", data_flow), ("osf", osf),
       ("program", program), ("team", team), ("repo", repo), ("roadmap", roadmap), ("donor-flow", donor_flow), ("biochem", biochem), ("gantt", gantt)]


def main():
    for lang in ("en", "ru"):
        for name, fn in ALL:
            write("guide/assets/diagrams/redraw-%s.%s.svg" % (name, lang), fn(lang))


if __name__ == "__main__":
    main()
