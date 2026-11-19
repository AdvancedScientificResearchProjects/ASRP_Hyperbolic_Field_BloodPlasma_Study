#!/usr/bin/env python3
"""Folder tree for guide/NAVIGATION*.md, built from the real tree and the computed facts.

`render(lang, F)` walks the files git knows about (tracked or not ignored), checks that every path of the
spec exists, and aborts when a tracked top-level entry is missing from the spec, so the printed tree
cannot drift from the repository. Comments are in `en` / `ru`; `{key}` placeholders are facts.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (path, English comment, Russian comment, children)
SPEC = [
    ("README.md", "front page (English)", "главная страница (английская)"),
    ("README.ru.md", "front page (Russian)", "главная страница (русская)"),
    ("guide/", "detail pages X.md + X.ru.md; assets/ = generated SVG", "страницы-детали X.md + X.ru.md; assets/ = сгенерированные SVG"),
    ("archive/", "the previous README, kept byte for byte", "прежний README, сохранён байт в байт"),
    ("tools/", "showcase tooling: facts, visuals, excerpts, no-loss check", "инструменты витрины: факты, визуалы, выдержки, проверка без потерь"),
    ("tests/", "regression gate for the showcase", "регрессионный гейт витрины"),
    ("OSF_PREREGISTRATION.md", "the OSF preregistration text (bilingual)", "текст предварительной регистрации OSF (двуязычный)"),
    ("original_research/", "all data, code, results and reports", "все данные, код, результаты и отчёты", [
        ("original_research/README.md", "entry to the research folder", "вход в папку исследования"),
        ("original_research/data/", "{donors} donor folders: photos, protocol PDFs, per-donor logs (sensitive)", "{donors} папок доноров: фото, PDF-протоколы, журналы (чувствительно)"),
        ("original_research/processed/", "combined per-donor JSON", "сводный JSON по донорам"),
        ("original_research/results/", "{result_files} LLM result files in {result_folders} run folders", "{result_files_ru} результатов LLM в {result_folders} папках прогонов"),
        ("original_research/reports/", "protocol + {reports_dated} dated analysis reports (EN and RU)", "протокол + {reports_dated} отчёта анализа (EN и RU)"),
        ("original_research/scripts/", "{scripts_py} Python files: llm_analysis/, cv_analysis/", "{scripts_py} файла Python: llm_analysis/, cv_analysis/"),
        ("original_research/notebooks/", "cv_analysis.ipynb, {notebook_mb} MB", "cv_analysis.ipynb, {notebook_mb} МБ"),
        ("original_research/charts/", "{charts_png} summary charts + {mermaid_png} Mermaid PNG", "{charts_png} сводных графика + {mermaid_png} PNG Mermaid"),
        ("original_research/en/", "English documentation hub", "английский документационный хаб"),
        ("original_research/ru/", "Russian documentation hub", "русский документационный хаб"),
    ]),
    ("ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/", "mirror of the programme hub: README + {issue_docs} issue documents ({mirror_files} files)",
     "зеркало хаба программы: README + {issue_docs_ru} задач ({mirror_files} файла)"),
]
IGNORED_TOP = {".git", ".gitignore", ".gitattributes", ".DS_Store"}


def tracked():
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], capture_output=True, text=True,
                         cwd=ROOT).stdout.split("\n")
    return [x for x in out if x]


def render(lang, F):
    files = tracked()
    tops = {x.split("/")[0] for x in files}
    spec_tops = {e[0].rstrip("/").split("/")[0] for e in SPEC}
    missing = sorted(t for t in tops - spec_tops if t not in IGNORED_TOP)
    if missing:
        raise SystemExit("tools/tree.py: tracked top-level entries missing from SPEC: %s" % missing)
    col = 1 if lang == "en" else 2
    rows = []

    def exists(path):
        q = path.rstrip("/")
        return any(f == q or f.startswith(q + "/") for f in files) or os.path.exists(os.path.join(ROOT, q))

    def emit(entries, prefix, top):
        for i, e in enumerate(entries):
            last = i == len(entries) - 1
            if not exists(e[0]):
                raise SystemExit("tools/tree.py: path in SPEC does not exist: %s" % e[0])
            name = e[0] if top else e[0].rstrip("/").split("/")[-1] + ("/" if e[0].endswith("/") else "")
            rows.append((prefix + ("└── " if last else "├── "), name, e[col].format(**F)))
            if len(e) > 3 and e[3]:
                emit(e[3], prefix + ("    " if last else "│   "), False)

    rows.append(("", "Hyperbolic_Field_BloodPlasma_Study/", ""))
    emit(SPEC, "", True)
    width = max(len(a) + len(b) for a, b, c in rows if c) + 2
    out = []
    for a, b, c in rows:
        out.append((a + b).ljust(width) + "# " + c if c else a + b)
    return "\n".join(out)
