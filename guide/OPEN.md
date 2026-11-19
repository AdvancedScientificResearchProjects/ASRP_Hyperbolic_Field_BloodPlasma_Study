**English | [Русский](OPEN.ru.md)**

[← Blood Plasma Study](../README.md) · [Guide index](README.md)

<div align="center">

# Open questions and inconsistencies

</div>

## Open questions

None of the items below is resolved here: the source files were not edited. Each item names where the disagreement lives.

### Protocol documents disagree

- **Exposure time.** The protocol summary says about 1 h 12 min; issue 1 says 35-40 min per channel and issue 3 says 30 min; the per-donor logs give windows of 68 to 94 minutes (for two donors only an end time is logged). Sources: `original_research/reports/experiment_protocol_en.md`, `ISSUE_1_UPDATED.md`, `ISSUE_3_UPDATED.md`, `original_research/data/patient-*/en/README.md`.
- **Tubes and centrifugation.** Issue 3 (marked Complete) prescribes EDTA tubes, 3000 rpm for 10 min and no antibiotics for 14 days; issue 1 says anticoagulant-free tubes; the data logs and the protocol summary say 2000 rpm for 5 min, and the summary says two donors were on antibiotics. EDTA plasma would not clot unaided, so the tube type matters. **The tube and anticoagulant type is NOT VERIFIED.**
- **Consent and screening.** Informed consent and donor screening are specified in issue 3. No consent artefact is in the repository.

### The time axis

- **Clocks.** Photo timestamps (EXIF) and the protocol times in the logs do not line up for several donors: photographs precede or overlap the logged irradiation window for four donors, and for one donor photographs precede the logged centrifugation. A fixed offset of about three hours between the camera clock and the protocol clock would reconcile all of them, but none is documented. **Whether the clocks agree is NOT VERIFIED**, so no coagulation time axis can be drawn.
- **OSF date.** The registration says "before data collection" and is dated 25 January 2026; at least one donor log is dated earlier (see [Publications, patent, preregistration](PUBLICATIONS.md)).

### Counting and statistics

- **Units.** The pilot is quoted as <!--n:donors-->7<!--/n--> donors, <!--n:photos-->101<!--/n--> photographs, 40 single-channel photos, 33 "samples" (data hub), <!--n:triplets-->19<!--/n--> triplets from <!--n:triplet_donors-->5<!--/n--> donors and "41 unique comparison sets" (the 2026-03-12 report). The independent units are donors.
- **24 versus 34 multi-channel photos.** The protocol summary says 24; the previous README and the CV report say 34. They reconcile by arithmetic: 24 + 10 multi-tube photos enriched from the donor README files = 34 (an inference, not stated in the files).
- **The p-value.** The reports and the previous README quote p = 0.027 for Gemini; the exact one-sided binomial for <!--n:gemini_ch19-->11<!--/n--> of <!--n:gemini_n-->19<!--/n--> at 1/3 is <!--n:gemini_p_exact-->0.024<!--/n-->. The method behind 0.027 is not stated and no statistics script exists in the repository.
- **Letter position.** The blind map is fixed (A control, B channel 19, C channel 21); no run shuffles it.

### Inside the reports

- The 2026-02-25 text says channel 19 has the highest lysis score, while its own table gives channel 21 the higher value (0.626 against 0.595).
- The 2026-03-12 report concludes channel 19 over channel 21 over control, while its Gemini row has control at 26.3% above channel 21 at 15.8%; the 2026-02-26 report orders channel 19, control, channel 21.
- Issue 5 lists fibrinogen as "In Progress" yet reports r = 0.72, and lists PT/APTT as "Complete" while the data folders are "(planned)".

### Models and providers

- The previous README says "8 LLM + CV models"; the blinded runs used <!--n:blinded_providers-->4<!--/n--> provider families (GPT-5, Groq Llama 4 Scout, Gemini flash-lite, Perplexity sonar-pro, and Mistral in the older comparison); Claude appears only in the unblinded pass. The code's provider list names claude-sonnet-4-6, the report names Claude Opus 4.6.
- Mistral is quoted as 44.4% (comparative run, 512 px) and 49.5% (combined); the previous README's model table lists DINOv2-small while the CV report uses DINOv2-large.

### Outside the files

- **Publication.** The repository never names a published article, a DOI or a journal release, and the study documents stop at 26 March 2026. Whether a paper appeared is an external fact not verified here.
- **Patent status.** Whether KZ 2025/1095.1 has progressed beyond "Filed" is not recorded in the repository.
- **A personal e-mail address** of an external collaborator still stands in three files of the mirror folder (`ISSUE_1_UPDATED.md`, `ISSUE_2_UPDATED.md`, the mirror `README.md`), although an earlier commit removed it from the root README. Removing it needs a decision by the repository maintainers; it is not repeated on any showcase page.
- **Mirror divergence.** The mirror README (423 lines) and the root README (504 lines at the previous version) differ; the mirror is not a byte copy.
- **Issues 4, 7 and 9** exist only as table rows, so the issue list cannot be verified without GitHub.

### Not verified

EXIF-versus-protocol clock agreement; tube anticoagulant; donor consent; antibiotics (two donors per the protocol summary, not identifiable in the per-donor files); OSF registration contents; any journal publication status.
