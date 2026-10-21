# Subagent assignment and return contract

The orchestrator must use *real host subagent delegation* whenever available. The roles below are task descriptions, not imaginary tools. Never invoke a tool not provided by the current runtime.

## Shared assignment payload

Pass every worker:

- Research brief and exact C1..Cn claim statements; mark observations vs hypotheses.
- Search cutoff date, language scope, accessible databases/tools, and allowed link destinations.
- Dedicated mission below and an explicit query / full-text budget.
- `read-only`, do not edit shared repo or other agents' output files; return a report to parent.
- Citation contract: title, authors, year, DOI/URL, actual source consulted, evidence passage location, abstract-only/full-text status; never invent.
- Ask for strongest overlaps **and** contradictions, not supportive papers only.

## Independent first-wave roles

**A — nearest-prior scout** (`novelty-closest` in Claude Code, `novelty_closest` in Codex): search exact phenomenon, task, mechanism, and same-domain synonyms; rank 3–8 most similar papers using methodological and claim overlap.

**B — cross-domain scout** (`novelty-adjacent` / `novelty_adjacent`): search different vocabulary, neighboring subfields, theory papers, classic work, competing benchmarks, and negative results. Identify a paper that would be missed by searching only the target project's name.

**C — skeptical reviewer** (`novelty-redteam` / `novelty_redteam`): assume the claimed contribution is already in the literature; find the strongest near-duplicate and simplest alternative explanation, plus missing controls. Distinguish "already done" from "not sufficiently tested".

**D — source auditor** (`novelty-verifier` / `novelty_verifier`): run *after* workers A–C return. Check strongest paper identifiers, version/year, actual passages, and whether the abstract/reported results support the alleged overlap. Return corrections and any missing full text. The verifier must independently open the source where access permits. Avoid treating three agents citing the same source as independent corroboration.

**Optional E — methods/confounds reviewer**: parent may spawn generic reviewer if deep mode; focus on controls, leakage, observational inference, selection bias, and cheap falsification tests.

## Return schema (Markdown or JSON; stable meanings)

```text
worker: A/B/C/D/E
mission:
searched_at: YYYY-MM-DD
search_queries: [{database, query, filters, date, examined_count}]
claim_assessments: [{claim_id, proposed_overlap, supporting_paper_ids, contrary_paper_ids, uncertainty}]
papers: [{id, title, authors, year, venue_or_preprint, doi_or_url,
          consulted: full-text | abstract | metadata-only | inaccessible,
          cited_passage_or_location, relevance, differentiating_detail}]
strongest_objection: ...
false_positive_risk: ...
false_negative_risk: ...
open_questions: ...
```

If a field cannot be verified, use `unknown` instead of inventing it.

## Example native orchestrator instruction

> Invoke the research-novelty-audit skill on this research brief. Use native subagents to parallelize independent nearest-prior, cross-domain, and adversarial searches. Have a *separate* subagent verify the 5 strongest citations after results merge. Keep each agent read-only and within standard budget. Write a claim-level audit with narrow novelty language. If subagents or web are unavailable, state this and run a clearly marked provisional review; never simulate agent returns.
