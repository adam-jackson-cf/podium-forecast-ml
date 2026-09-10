# Coding-agent linting and codebase inertia research

This run answers the confirmed six-question brief for `podium-forecastin-ml`.

- [Report](report.md): findings, priorities, evidence limits and search methodology.
- [Candidate matrix](rule-matrix.md): all 23 rules/designs and their acceptance outcomes.
- [Requirements](requirements.json): approved scope and hard constraints.
- [Evidence](evidence.json): normalized sources and all logged searches.
- [Source validation](validation.json), [citation audit](citation-report.json), [hard constraints](constraints-report.json) and [render audit](render-audit.json).
- [Baseline inventory](baseline/inventory.json) and [research probes](baseline/rule-probes.json).
- [Read-only workflow scan](baseline/zizmor-probe.json).
- [Repository studies](repo-analysis/): revisions, source pointers and cleanup confirmation.

## Scope and operating boundary

This is a research deliverable. No proposed rule was added to the application gates, no scanner autofix was used, and no AWS resources were accessed or changed. Synthetic fixtures were kept in a temporary research directory and removed after their inputs and results were retained. The current baseline commit is recorded in the inventory.

The research used the installed deep-topic-research scripts with schema version 2.0. Source validation passed without undated-source, diversity or threshold waivers. This was one synthesis pass; there is no multi-pass consensus artifact or claim.

## Reproducing the research audits

Use the same installed deep-topic-research skill version, Python 3.12 or later, and the canonical files in this directory. Run normalization before source validation; citation validation uses `publisher-ownership.json`. Hard constraints are defined in `requirements.json`.

The report generator has an observed search-appendix omission: it passes `evidence.searchLog` rather than the canonical evidence object to its appendix helper. The delivered appendix was generated with that unchanged helper using `evidence.searches` from the canonical evidence object. The report includes a disclosure and `render-audit.json` verifies complete search rendering and nonempty link validation. Do not add a legacy evidence alias or weaken validation to hide the omission.

Regenerating `report.md` with the unmodified generator alone will omit the completed appendix and supplementary methodology/adoption tables. Preserve or regenerate those from the recorded evidence, repository metadata and analysis before rerunning rendered completeness checks. Candidate details derive from `analysis.json` and `candidate-rules.json`; these contain no executable policy changes.

Public links identify either dated publications or immutable repository snapshots. Snapshot dates are commit/release publication dates, not original authorship dates. Tool popularity and maintenance snapshots are evidence for discovery, not ratings of individual rules or forecasts of maintenance savings.
