# Search and evidence protocol

## Four search families

1. **Exact / construct:** `"[phenomenon]" AND "[task]"`, named metrics, datasets, and failure modes.
2. **Mechanism / explanations:** proposed mechanism and its alternatives, including older non-LLM fields (software reliability, program analysis, causal inference, information retrieval, human factors).
3. **Method and design:** baseline, controlled ablation, experimental unit, negative controls, construct validity, confounds, measurement method.
4. **Citation neighborhood:** reference lists, "cited by", direct follow-ups, and adjacent workshop/preprint versions if tools support this.

In the search log, record *the actual literal query* and database. Do not pretend that searches occurred on Google Scholar, arXiv, Semantic Scholar, OpenAlex, Crossref, DBLP, ACM DL, IEEE Xplore or PubMed if the host did not query them.

## Candidate triage

Order: title/abstract screen -> read methods and findings -> cross-check discussion and limitations -> check bibliography/versions for strongest overlaps. Prioritize direct primary sources. Keep a clear boundary between `candidate` and `verified evidence`.

When feasible, check each decisive closest-prior finding against *full text* and specify page/section/table/figure or quoted passage. A title alone does not justify an overlap assessment. A result sourced solely from abstract must say so.

Citation metadata: authors, full title, year, venue/status, stable original URL/DOI, which version was read, access date. Distinguish arXiv preprint from conference paper. Duplicated arXiv/conference versions should be one underlying work unless materially revised.

## Overlap classification for each claim

- `already established`: direct equivalent question/result demonstrated by reliably reviewed work.
- `substantially overlapping`: major methodological, mechanistic, or empirical overlap, but demonstrable substantive difference might remain.
- `plausibly underexplored`: scoped search identified no direct explanation but close work exists; *not* a global novelty assertion.
- `insufficient evidence`: blocked search, inaccessible full text, poor terminology coverage, conflicting results, or ambiguous claim.

Evidence confidence: `high` means relevant primary sources were directly inspected and verified; `medium` means mix of abstract and partial full text; `low` means metadata, summaries, inaccessible, or narrow search coverage. This confidence describes **the audit's evidence**, not the probability of being novel.

## Stop and escalate conditions

- Stop early and reframe if a kill-shot paper already answers the exact claim; still check whether mechanism/boundary conditions remain unknown.
- Escalate a contradiction if two primary studies seem incompatible; compare design, population, measures, dates, and baselines.
- Do not stop after finding zero papers. Try cross-domain synonyms and citation neighborhood before assigning `plausibly underexplored`.
- Record truncation if source access fails, credentials are missing, paid searches are blocked, or date coverage is unclear.
- Do not automatically execute experiments, buy access, or use paid APIs without authorization.
