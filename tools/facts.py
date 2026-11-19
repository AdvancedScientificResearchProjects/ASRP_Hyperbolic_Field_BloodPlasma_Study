#!/usr/bin/env python3
"""Every number on the showcase pages and diagrams is computed here, from the repository itself.

    python3 tools/facts.py            # print all facts

`facts()` returns a flat dict of strings. tools/build_facts.py writes them into the pages
(markers `<!--n:key-->value<!--/n-->`); tools/build_visuals.py draws the diagrams from the same dict.
Nothing is copied from older prose: counts come from the file tree, the per-donor `analysis.json`
files (counts only, never donor details), the raw blinded `results.json` files, and a few anchored
regular expressions on the report texts (the build fails when a sentence they read has changed).
The exact binomial p-values are computed here with `math.comb`; no statistics script exists in the
repository, so this is the only place they are derived. Standard library only.
"""
import glob
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AS_OF = "2026-11-19"  # date of this showcase restructuring
OR = "original_research"
# blinded comparative runs per provider (each folder holds one results.json)
PROVIDERS = [("gemini", ["fullres_comparative_blinded_gemini"]),
             ("groq", ["fullres_comparative_blinded_groq", "fullres_comparative_blinded_groq_r2", "fullres_comparative_blinded_groq_r3"]),
             ("openai", ["fullres_comparative_blinded_openai", "fullres_comparative_blinded_openai_r2", "fullres_comparative_blinded_openai_r3"]),
             ("perplexity", ["fullres_comparative_blinded_perplexity", "fullres_comparative_blinded_perplexity_r2", "fullres_comparative_blinded_perplexity_r3"])]


def p(*a):
    return os.path.join(ROOT, *a)


def read(rel):
    return open(p(rel), encoding="utf-8").read()


def must(pattern, text, what, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit("facts.py: cannot find %s (pattern %r) - the source sentence changed" % (what, pattern))
    return m


def ru_plural(n, one, few, many):
    n = abs(int(n))
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def binom_tail(k, n, q=1 / 3):
    """Exact one-sided P(X >= k) for X ~ Binomial(n, q)."""
    return sum(math.comb(n, i) * q ** i * (1 - q) ** (n - i) for i in range(k, n + 1))


def count(pattern):
    return len(glob.glob(p(pattern), recursive=True))


def tally(folders):
    """Counts of most_coagulated verdicts (ch19 / control / ch21) over the runs of one provider."""
    t = {"ch19": 0, "control": 0, "ch21": 0}
    for fo in folders:
        r = json.load(open(p(OR, "results", fo, "results.json"), encoding="utf-8"))
        for c in r["comparisons"]:
            for prov in c["providers"].values():
                mc = (prov.get("structured") or {}).get("most_coagulated")
                if mc in t:
                    t[mc] += 1
    return t


def facts():
    f = {"as_of": AS_OF}
    # dataset
    f["donors"] = str(len(glob.glob(p(OR, "data", "patient-*"))))
    photos = 0
    for fn in glob.glob(p(OR, "data", "patient-*", "en", "analysis.json")):
        photos += len(json.load(open(fn, encoding="utf-8"))["photos"])
    f["photos"] = str(photos)
    f["heic"] = str(len([x for x in glob.glob(p(OR, "data", "patient-*", "photos", "original", "*")) if x.lower().endswith(".heic")]))
    pdfs = glob.glob(p(OR, "data", "patient-*", "*.pdf"))
    f["pdfs"] = str(len(pdfs))
    f["pdf_mb"] = str(round(sum(os.path.getsize(x) for x in pdfs) / 1e6))
    f["notebook_mb"] = "%.1f" % (os.path.getsize(p(OR, "notebooks", "cv_analysis.ipynb")) / 1e6)
    f["result_files"] = str(count(OR + "/results/**/*.json"))
    f["result_folders"] = str(len([d for d in glob.glob(p(OR, "results", "*")) if os.path.isdir(d)]))
    f["ml_result_files"] = str(len(glob.glob(p(OR, "scripts", "cv_analysis", "ml_results", "*.json"))))
    f["scripts_py"] = str(count(OR + "/scripts/**/*.py"))
    lines = 0
    for fn in glob.glob(p(OR, "scripts", "**", "*.py"), recursive=True):
        lines += len(open(fn, encoding="utf-8", errors="replace").read().split("\n"))
    f["scripts_lines"] = str(lines)
    f["reports_dated"] = str(len(glob.glob(p(OR, "reports", "2026-*"))))
    f["charts_png"] = str(count(OR + "/charts/*.png"))
    f["mermaid_png"] = str(count(OR + "/charts/mermaid/*.png"))
    f["issue_docs"] = str(count("ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS/Hyperbolic_Field_BloodPlasma_Study/ISSUE_*_UPDATED.md"))
    f["mirror_files"] = str(len([x for x in glob.glob(p("ADVANCED_SCIENTIFIC_RESEARCH_PROJECTS", "**", "*"), recursive=True) if os.path.isfile(x)]))

    # blinded runs
    cmp_ = read(OR + "/reports/2026-03-12_comparative-llm-analysis/report_en.md")
    g = json.load(open(p(OR, "results", "fullres_comparative_blinded_gemini", "results.json"), encoding="utf-8"))
    f["triplets"] = str(g["metadata"]["total_comparisons"])
    f["triplet_donors"] = str(len({c["patient"] for c in g["comparisons"]}))
    tot_runs = 0
    for name, folders in PROVIDERS:
        t = tally(folders)
        n = sum(t.values())
        f["%s_n" % name] = str(n)
        f["%s_ch19" % name], f["%s_ctrl" % name], f["%s_ch21" % name] = str(t["ch19"]), str(t["control"]), str(t["ch21"])
        f["%s_pct" % name] = "%.1f" % (100.0 * t["ch19"] / n)
        f["%s_runs" % name] = str(len(folders))
        tot_runs += len(folders)
    f["blinded_runs"] = str(tot_runs)
    f["blinded_providers"] = str(len(PROVIDERS))
    f["gemini_p_exact"] = "%.3f" % binom_tail(int(f["gemini_ch19"]), int(f["gemini_n"]))
    f["dino_p_exact"] = "%.3f" % binom_tail(9, 19)
    f["chance_pct"] = "33.3"
    must(r'BLIND_MAP = \{"0": "A", "19": "B", "21": "C"\}', read(OR + "/scripts/llm_analysis/data.py"), "fixed blind map")
    must(r"\*\*Gemini 2\.5\*\* \| 1 \| 19 \| 11 \| 5 \| 3 \| \*\*57\.9%\*\*", cmp_, "report Gemini row")

    cv = read(OR + "/reports/2026-03-14_cv-ml-analysis/report_en.md")
    f["dino_full"] = must(r"DINOv2-large \*\*full photo\*\* \| \*\*([\d.]+)%\*\*", cv, "DINOv2 full photo").group(1)
    f["dino_sam"] = must(r"DINOv2-large \*\*SAM-2 crop\*\* \| ([\d.]+)%", cv, "DINOv2 SAM crop").group(1)
    m = must(r"\*\*DINOv2-large probe\*\* \| 9/19 \(([\d.]+)%\) \| ([\d.]+) \|", cv, "DINOv2 probe")
    f["dino_probe"], f["dino_probe_p"] = m.group(1), m.group(2)
    f["cv_false_pos"] = must(r"CV segment analysis\*\* \(SAM-2 \+ HSV\) \| (\d+)%\+ false positive",
                             read(OR + "/reports/2026-02-26_llm-vision-analysis/report_en.md"), "CV false positives").group(1)
    m = must(r"\*\*(\d+)% ch19 unblinded vs (\d+)% ch19 blinded\*\*", cmp_, "priming example")
    f["perplexity_unblinded"], f["perplexity_blinded"] = m.group(1), m.group(2)

    # figures of the previous README (kept in archive/)
    arch = read("archive/README_2026-11-19_pre-showcase.md")
    f["issues_listed"] = str(len(re.findall(r"^\| \[#\d+\]\(", arch, re.M)))
    # Russian number + noun phrases (the noun agrees with the number)
    for key, forms, short in (("photos", ("фотография", "фотографии", "фотографий"), "photos_ru"),
                              ("donors", ("донор", "донора", "доноров"), "donors_ru"),
                              ("triplets", ("триплет", "триплета", "триплетов"), "triplets_ru"),
                              ("pdfs", ("протокол", "протокола", "протоколов"), "pdfs_ru"),
                              ("result_files", ("файл", "файла", "файлов"), "result_files_ru"),
                              ("issue_docs", ("документ", "документа", "документов"), "issue_docs_ru"),
                              ("ml_result_files", ("файл", "файла", "файлов"), "ml_result_files_ru")):
        f[short] = "%s %s" % (f[key], ru_plural(f[key], *forms))
    return f


def badges(lang, F):
    """Computed shields.io badges for the README header (the URL carries the numbers)."""
    from urllib.parse import quote
    names = {"en": ("donors", "photographs", "blinded runs"),
             "ru": ("доноров", "фотографий", "слепых прогонов")}[lang]
    items = [(names[0], F["donors"], "1f6feb", "Donors"), (names[1], F["photos"], "8957e5", "Photographs"),
             (names[2], F["blinded_runs"], "34d399", "Blinded runs")]
    return "\n".join("![%s](https://img.shields.io/badge/%s-%s-%s?style=flat-square)"
                     % (alt, quote(label.replace("-", "--").replace(" ", "_"), safe="_-"),
                        quote(msg.replace("-", "--").replace(" ", "_"), safe="_-"), col)
                     for label, msg, col, alt in items)


if __name__ == "__main__":
    for k, v in facts().items():
        print("%-28s %s" % (k, v))
