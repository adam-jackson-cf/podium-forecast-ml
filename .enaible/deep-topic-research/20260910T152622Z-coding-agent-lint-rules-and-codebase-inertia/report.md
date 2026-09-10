# Coding-agent linting and codebase inertia: Podium assessment

Generated: 2026-09-10T15:56:12.566158Z

## Executive Summary
The most useful next step is a small set of **semantic and structural checks**, not another blanket strict preset. The baseline already controls many local coding habits. Confirmed gaps remain in effect ownership, whole-package cycles, unchecked Any flow, precise failure handling, forecast-time construction and CI security.

This research assessed 23 candidate rule groups and enforcement designs. Seven isolated fixture scenarios compared existing checks with candidate capabilities; a separate read-only zizmor scan found two reviewable checkout credential-persistence findings. **No existing rules, application code or infrastructure were changed.** The detailed [rule matrix](rule-matrix.md) records each candidate's gap, mechanism, example, acceptance outcome, cost and false-positive risk.

For codebase inertia, prioritize dependency paths, canonical contracts and explicit lifecycle/effect boundaries. Treat clone, dead-code, class-shape and coupling metrics as calibrated review inputs. ML leakage, feature availability and approval still need runtime/data contracts; generic lint cannot establish them. The source evidence supports these mechanisms, but does not establish an optimal agent-specific rule set or quantify long-term maintenance savings.

## Table of Contents
1. Research Objectives
2. Methodology
3. Key Findings
4. Synthesis and Insights
5. Recommendations
6. Limitations and Future Research
7. References
8. Appendices

## 1. Research Objectives

**Objective**: Coding-agent lint rules and codebase inertia
**Scope**: Python 3.12, ML/data processing, PostgreSQL/SQL, Terraform/AWS, containers, shell, CI and testing. Compare present scaffold controls and transferable cross-language design rules. Research only; do not implement or loosen gates.
**Decision Context**: Choose the next rules that prevent immediate defects and long-term codebase inertia before ML implementation in podium-forecastin-ml. User confirmed the six-question brief including inertia expansion.

**Questions**:
- Which coding-agent behaviours introduce immediate defects or long-term codebase inertia, what evidence supports these effects, and which behaviours can be detected deterministically?
- Which established Python linting, typing and architecture rules address gaps in our current configuration?
- Which rules address ML/data-pipeline correctness, particularly leakage, reproducibility, schema handling and external side effects?
- Which additional SQL, Terraform, container, shell and CI rules fit our stack?
- Which design constraints from other ecosystems would transfer usefully, and how could we enforce them?
- Which candidates should we adopt first, defer or reject, considering evidence strength, overlap, false positives and maintenance cost?

## 2. Methodology

### Domain Coverage

| Domain | Questions |
| --- | --- |
| technical | 6 |

### Source Collection

Total sources logged: 41

### Method and interpretation boundaries

The confirmed six-question brief covers immediate defects, long-term codebase inertia and transferable enforcement designs. Searches and retained source records were logged through the skill scripts. Source validation uses the unchanged technical policy: twelve months preferred and twenty-four months maximum. Four older sources remain within that maximum; no undated or source-diversity waiver was used.

Forty-one source records are retained, including the local baseline inventory and an ownership-methodology source. Versioned source dates identify the release or commit publishing that immutable snapshot; they are not retrieval dates or claims about when a rule was first invented. Dated research and original engineering accounts retain their own publication dates.

The report distinguishes rule capability, practical adoption, empirical outcome evidence and proposed project adaptation. GitHub metadata is a popularity/maintenance signal only. The comparison is grounded in baseline commit 54b2c88, seven isolated synthetic scenarios, one read-only zizmor scan and two shallow repository source inspections. No project rule or application code was changed; no production model or live AWS system was tested.

Source and citation checks, including two publisher domains and two independent owner groups for each key finding, passed. GitHub-hosted content is attributed to its owning project. OpenAI/Astral are grouped conservatively because of the announced acquisition, without claiming closing was verified. A single synthesis pass was used; no independent consensus claim is made.

The installed report renderer omitted its search appendix because it reads evidence.searchLog instead of canonical evidence.searches. The delivered appendix was completed by invoking its unchanged appendix helper on the canonical evidence object. Validators, schemas and evidence were not altered to conceal this omission. Rendered completeness is checked separately in render-audit.json.

## 3. Key Findings

### 1. Codebase inertia is a distinct target; style compliance is only a partial defence

For this assessment, **codebase inertia** means the accumulating effort required to change the system safely: more coupled modules, duplicated contracts, obsolete paths, dependency assumptions and wrappers that future contributors must understand or change together. This is an operational definition for Podium, not a validated scalar score.

The reviewed agent-code study reports persistent static-analysis issues in real repositories; OpenAI's engineering account describes agents replicating existing patterns and the need for recurring structural controls. These support preventive checks, but do not establish the long-term effect of any particular rule. The study is observational and the vendor account explicitly leaves multi-year coherence unresolved. The independent Fowler/Thoughtworks commentary also distinguishes structural cleanliness from verifying real behaviour.

| Inertia mechanism | Useful observable signal | Detection boundary |
| --- | --- | --- |
| Copied business rules diverge | Clone candidates and mismatched canonical contracts | Similar code is not necessarily the same responsibility |
| New coupling accumulates | Cycles, forbidden dependency paths, transitive fan-out | Local function complexity misses graph structure |
| Abandoned code remains | Unreachable subgraphs and unused declarations | Plugins and public APIs require declared roots |
| Extra abstraction obscures work | Stateless wrapper classes and duplicate representations | Counts alone do not prove an abstraction is unnecessary |
| Dependencies become accidental | Imported transitive/dev-only packages and unused runtime dependencies | A successful development environment can hide packaging errors |
| Failure paths become ambiguous | Logged failures returning normal values or discarded async work | Passing lint must not be confused with preserved outcomes |

The appropriate aim is to keep these mechanisms observable and prevent clearly forbidden transitions. There is no support here for promising a particular reduction in future maintenance effort. [Harness engineering: leveraging Codex in an agent-first world, 2026-02-11] [Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild, 2026-04-26] [Harness Engineering - first thoughts, 2026-02-17] [jscpd duplicate-code detection, 2026-09-10] [Dependency-cruiser circularity, reachability and instability rules, 2026-09-09]

**Confidence**: medium

### 2. Several high-value Python additions are available in the tools already installed

The baseline was inspected at commit `54b2c88`. Its Ruff selection is broad, but it does **not** select BLE, DTZ, TID, PT or G. Mypy `strict` does not enable every optional Any or awaitable check. This is a coverage distinction, not a contradiction of the earlier green baseline.

| Candidate | New protection | Recommended timing |
| --- | --- | --- |
| C01: Ruff BLE001; proposed no-success-after-failure rule | BLE and TRY are not selected. B904 already covers exception chaining; it does not prevent swallowed failures. | Next increment |
| C02: Ruff DTZ001–DTZ007, DTZ011–DTZ012 as applicable | DTZ is absent. Forecast cut-offs require unambiguous instants, not implicit machine-local time. | Next increment |
| C03: Ruff TID251 configured bans; proposed EFFECT_OWNER contract | Current architecture permits all standard-library imports in pure layers, including network/process/file APIs. Layer direction alone is not effect isolation. | Next increment |
| C04: Mypy disallow_any_explicit/disallow_any_unimported; scoped disallow_any_expr; validated decoders | Mypy strict is not a ban on every Any expression. JSON-derived values can flow into an annotated variable without runtime validation. | Next increment |
| C05: Import Linter acyclic_siblings; protected/independence contracts where justified | Per-file allowed-layer checks do not detect cycles within an allowed layer or package-level feedback loops. | Next increment |
| C07: Ruff PT011 and PT012 | Pytest bypass checks exist, but PT rules are not selected. A broad raises block can succeed because setup failed rather than the intended operation. | Next increment |

The controlled probes are retained in [rule-probes.json](baseline/rule-probes.json). Current Ruff accepts a broad exception converted to zero and a naive clock; the proposed individual rules reject those fixtures. Current mypy accepts the illustrated JSON-to-annotated-value flow and a discarded generic awaitable; the additional checks reject them. A same-layer cycle passes the current per-file architecture checker but fails Import Linter 2.15; the corresponding acyclic graph passes.

**Two limits are particularly important.** First, the layer checker permits standard-library imports, so it admits a domain-level network API; a configured TID251 rule catches that explicit API. Second, BLE001 itself accepts a broadly caught exception if it is logged appropriately. It therefore cannot establish that a failed job remains failed. A scoped failure-propagation rule or behavioural contract is still needed.

These are synthetic coverage probes, not reported forecasting defects. No product pipeline has been built, no fixture network request was executed, and no existing gate was altered. Stable rule availability and preview/removed status were checked against the installed Ruff 0.15.8 catalog; optional mypy capabilities were checked against 1.19.1. [Mypy 1.19 Released, 2025-11-28] [Ruff BLE001 implementation and rule documentation, 2026-03-26] [Ruff DTZ001 timezone-aware datetime rule, 2026-03-26] [Ruff TID251 configurable banned APIs, 2026-03-26] [Ruff PT011 and PT012 exception-test rules, 2026-03-26] [Mypy optional error codes, 2025-12-15] [Import Linter acyclic sibling contracts, 2026-09-04] [Ruff logging-format rules including G004, 2026-03-26] [Podium baseline inventory at commit 54b2c88, 2026-09-10] [Avoiding anys with Linting and TypeScript, 2025-01-21]

**Confidence**: high

### 3. ML correctness requires contracts about data and lifecycle, not just more lint codes

The strongest ML controls concern what the data means and when it was available. A general linter cannot infer Podium's forecast cut-off, whether an editorial forecast is a valid baseline, or whether every runner from one race belongs in the same partition.

LeakageDetector and the abstract-interpretation research demonstrate useful static approaches to preprocessing and train/test contamination. Their documented notebook/library assumptions do not make them turnkey enforcement for this containerised pipeline. Semgrep offers source-to-sink rules, but cross-function and cross-file capabilities depend on the engine; a community pattern scan must not be presented as whole-program proof.

| Candidate | New protection | Recommended timing |
| --- | --- | --- |
| C13: Declared split/cut-off API; dataset availability and partition invariants | No real training dataset exists yet. Generic lint cannot know whether a feature was available at forecast time or whether all runners stay with their race. | First dataset and training slice |
| C14: Ruff PD002; explicit transformation ownership | PD rules are absent. The repository has Arrow artifacts but has not selected the feature-processing API. | If pandas is selected for features |
| C15: Mypy exhaustive-match; protected construction of validated/approved objects | Approval and publication are not implemented. Boolean flags and generic dictionaries would allow ambiguous transitions and multiply change sites. | First model approval/publication slice |
| C16: SQLGlot AST policy plus PostgreSQL read-only privileges | SQLFluff checks SQL form and selected conventions; a read-only fixture exists, but no production extraction SQL policy is implemented. | First real extraction adapter |
| C21: Canonical schema/manifest generation and parity checks | Exact wording is required in guidance, but no executable parity contract yet binds dataset schema, feature order, model metadata and publication payload. | First pipeline contracts |
| C22: Hypothesis properties and targeted mutation-style challenges | Example-based verifier tests are valuable, but coverage alone cannot prove resistance to aliases, nesting variants, false success or ML leakage. | Gate changes and first feature slice |

Use a small owned API for splitting, feature extraction, model approval and publication. Pair its static access rules with schema validation and properties over actual datasets: complete-race membership, no forbidden temporal overlap, explicit feature availability, stable feature order, and rejection of unapproved model artifacts. Hypothesis can generate relevant partitions and edge cases; Pandera can validate dataframe contracts when that representation is selected. These are complementary test/validation mechanisms, not static lint rules.

For SQL, AST inspection can reject modifying statements hidden in query structure, but even a SELECT can invoke a side-effecting function. The real read-only role and database behaviour remain authoritative. Likewise, typed lifecycle objects and exhaustive dispatch make missing cases visible; they do not create authorization or validate approval evidence on their own. [LeakageDetector 2.0: Analyzing Data Leakage in Jupyter-Driven Machine Learning Pipelines, 2025-09-19] [Static Analysis by Abstract Interpretation Against Data Leakage in Machine Learning, 2025-05-19] [Ruff DTZ001 timezone-aware datetime rule, 2026-03-26] [Ruff PD002 dataframe in-place mutation rule, 2026-03-26] [Pandera dataset validation framework, 2026-09-09] [Hypothesis property-based testing, 2026-09-08] [Semgrep taint-analysis scope and engine boundaries, 2026-09-09] [TypeScript ESLint exhaustive handling of union states, 2026-09-09] [SQLGlot SQL AST inspection and semantic differences, 2026-09-10] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

**Confidence**: high

### 4. Infrastructure needs semantic policy and reliable failure signalling

The existing stack covers YAML, shell, Dockerfile syntax/conventions, Terraform validation, selected IaC security checks and source-secret scanning. Those layers do not make every future workflow or rendered configuration safe.

The read-only zizmor 1.30.1 run found **two medium-severity, low-confidence `artipacked` findings**: both checkout steps omit `persist-credentials: false`. The findings and locations are preserved in [zizmor-probe.json](baseline/zizmor-probe.json). They are reviewable credential-persistence concerns, not demonstrated leaks. Packagist's original adopter account supplies practical evidence for zizmor beyond its maintainer documentation.

| Candidate | New protection | Recommended timing |
| --- | --- | --- |
| C17: Zizmor artipacked, template-injection, excessive-permissions, dangerous-triggers, unpinned-uses | actionlint/YAML validate syntax and selected shell issues, but do not establish these security invariants. | Next increment |
| C18: Squawk require-concurrent-index-creation, constraint-missing-not-valid, prefer-timestamptz and related rules | SQL formatting is not migration safety. The ML repository currently does not own Nexus schema changes. | Only if this repository owns schema migrations |
| C19: Conftest/Rego or equivalent Python policy over rendered Compose and Terraform plan JSON | Current tests protect a specific storage module and static files. They do not yet enforce every future resource or resolved local service configuration. | Next infrastructure increment |
| C23: Failing-exit, nonempty intended scope, unknown-result and suppression-policy checks | Existing guards reject many bypasses, but adding another tool introduces new output formats, ignores, baselines and collection failure modes. | Every new checker integration |

A critical integration detail is that zizmor's SARIF output mode can return exit zero despite findings. A green upload step is therefore not a blocking policy. Any selected integration must demonstrate that known findings, parser/collection failures and omitted required inputs fail the complete gate.

Conftest illustrates semantic checks over structured configuration. For Podium, either that engine or small typed Python checks could evaluate rendered Compose and approved Terraform plan representations. Rego introduces an additional language that would itself need governance. Squawk is useful for migration safety only where this repository actually owns DDL; it must not become a reason to give the ML pipeline Nexus database-write authority. [Securing our GitHub Actions workflows with zizmor, 2026-07-23] [Conftest structured configuration policy tests, 2026-09-08] [Squawk PostgreSQL migration linter, 2026-09-10] [Zizmor CI audit rules, 2026-09-09] [Zizmor integration and failing-exit semantics, 2026-09-09] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

**Confidence**: high

### 5. Borrow the enforcement model from other ecosystems, not their entire toolchains

Several cross-stack ideas transfer well without introducing TypeScript, Java or a new runtime to the application.

| Original design | Valuable transfer to Podium | Qualification |
| --- | --- | --- |
| ArchUnit architecture tests | Express package/role restrictions as executable contracts over a graph | Use Python graph tooling; Java bytecode analysis itself is not portable |
| dependency-cruiser cycles and reachability | Detect package feedback loops and unreachable subgraphs from declared roots; show the path in diagnostics | Scan all maintained modules, not only imports reachable from one entrypoint |
| TypeScript unsafe-Any checks | Keep unvalidated external shapes out of the typed core | Preserve runtime parsing; a cast is not evidence |
| TypeScript no-floating-promises | Require ownership of asynchronous results | The Python equivalent includes unused-awaitable; ordinary unused-coroutine checks already exist |
| TypeScript exhaustive switch checks | Expose missing lifecycle cases when a state is added | Pair with protected construction and runtime authorization |
| TypeScript no-extraneous-class | Flag stateless class namespaces that add ceremony without a role | Exempt legitimate structured carriers and framework contracts by design |
| Wemake module/coupling metrics | Examine module breadth and dependency burden beyond local complexity | Its human-memory-inspired thresholds are not validated agent limits |

The two source studies are retained under [repo-analysis](repo-analysis/). Import Linter and dependency-cruiser both provide useful graph-level mechanisms. The latter explicitly distinguishes orphan modules, reachability and dependency instability, and cautions against treating the metric as an absolute judgment.

The broader lesson is to build analyzers at the right semantic level: tokens for simple local patterns, resolved symbols/types for API use, graphs for architectural boundaries, and data/state validation for runtime contracts. For bespoke checks, include a diagnostic that names the violated boundary, shows relevant evidence and points to the canonical repair location. [Avoiding anys with Linting and TypeScript, 2025-01-21] [Typed Linting with Project Service, 2025-05-29] [Mypy optional error codes, 2025-12-15] [Import Linter acyclic sibling contracts, 2026-09-04] [Dependency-cruiser circularity, reachability and instability rules, 2026-09-09] [Wemake Python styleguide design complexity rules, 2026-09-10] [TypeScript ESLint no-extraneous-class rule, 2026-09-09] [TypeScript ESLint no-floating-promises rule, 2026-09-09] [ArchUnit architecture tests, 2026-09-08] [TypeScript ESLint exhaustive handling of union states, 2026-09-09]

**Confidence**: high

### 6. Adopt by demonstrated project value; popularity and stricter settings are not sufficient

“Highly rated” is treated here as a combination of maintainer quality, observable adoption, recent maintenance and fit. The research found no credible rule-by-rule ranking that establishes reduced long-term inertia for coding agents. Repository stars are discovery signals, not performance evidence.

Start with the confirmed coverage gaps, then evaluate the checks that need real pipeline structures. Keep heuristic smell reports advisory until legitimate patterns and false positives are understood. This is a proposed adoption policy, not a relaxation of existing mandatory gates.

| Avoid as a blanket default | Reason |
| --- | --- |
| Ruff ALL or a complete additional strict preset | New and conflicting/opinionated rules can arrive with upgrades; the maintained proposal guidance favours concrete benefit and non-overlap |
| Restoring PD901's blanket df-name ban | Ruff removed it as overly strict; specific domain naming can remain guidance without reviving this rule |
| TRY003 everywhere | Shared domain error types can help, but one-off exception subclasses may add needless abstraction |
| Vulture-driven automatic removal | Public, dynamic and framework-discovered code needs real usage evidence |
| Zero-duplication or universal fan-out/class-size limits | These can incentivise wrappers, namespace tricks and inappropriate sharing |
| Claiming a scanner proves leakage freedom or model approval | These require data and operational evidence |
| Equating a report upload with a failing quality gate | SARIF and other report modes can have different exit semantics |

METR's context-specific randomized study reinforces the need to measure actual work outcomes rather than perceived gains; it does not evaluate these lint rules or current agents. For adoption, record true/false findings, repair churn, repeat violations and time to complete representative changes. No savings or scanner runtime benchmark is claimed here. [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity, 2025-07-10] [Ruff TRY003 exception-message design rule, 2026-03-26] [Ruff removed PD901 naming rule, 2026-03-26] [Ruff criteria for proposing new lint rules, 2026-09-10] [Vulture unused-code checks and confidence limits, 2026-04-30] [jscpd duplicate-code detection, 2026-09-10] [Zizmor integration and failing-exit semantics, 2026-09-09] [Ruff rule selection and fix safety guidance, 2026-09-10]

**Confidence**: medium

## 4. Synthesis and Insights

- The existing scaffold's green status is relative to its declared gates. The differential fixtures demonstrate additional coverage, not previously observed product failures. They should become candidate-rule acceptance examples if implementation is approved. [Podium baseline inventory at commit 54b2c88, 2026-09-10] [Ruff criteria for proposing new lint rules, 2026-09-10]
- A reliable coding-agent rule should make a bad outcome hard to express and explain the safe repair. A size or naming warning that merely encourages more wrappers can shift complexity instead of reducing it. [Harness engineering: leveraging Codex in an agent-first world, 2026-02-11] [Wemake Python styleguide design complexity rules, 2026-09-10] [TypeScript ESLint no-extraneous-class rule, 2026-09-09]
- Canonical contracts and whole-package analysis reduce the number of independent places that future work must keep consistent. This is the closest practical link between deterministic checks and the user's codebase-inertia concern; the expected maintenance benefit remains a hypothesis to measure. [Dependency-cruiser circularity, reachability and instability rules, 2026-09-09] [Pandera dataset validation framework, 2026-09-09] [ArchUnit architecture tests, 2026-09-08]
- Citation independence was assessed using source-owning projects rather than treating every GitHub-hosted document as Microsoft-authored. OpenAI and Astral were conservatively grouped together because of the announced acquisition; this is not a claim that closing was verified. [OpenAI to acquire Astral, 2026-03-19] [Ruff rule selection and fix safety guidance, 2026-09-10]
- The source mix contains tool documentation, original engineering accounts and research. An adopter story corroborates practical use, while a preprint or release document answers a different question. These evidence types are not interchangeable proof of agent-specific effectiveness. [Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild, 2026-04-26] [Securing our GitHub Actions workflows with zizmor, 2026-07-23] [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity, 2025-07-10]

## 5. Recommendations

1. **First increment: enable narrow, available rules and test the missing failure cases**

   Rationale: Prioritize C01, C02 and C07 using the pinned Ruff version, plus explicit scope for C04. Preserve current rules. Require valid/invalid fixtures and real failure propagation; the logged-exception probe shows why BLE001 alone is not enough. [Ruff BLE001 implementation and rule documentation, 2026-03-26] [Ruff DTZ001 timezone-aware datetime rule, 2026-03-26] [Ruff PT011 and PT012 exception-test rules, 2026-03-26] [Mypy optional error codes, 2025-12-15] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

   Priority: high

2. **Add effect ownership and same-layer cycle protection before feature growth**

   Rationale: Implement C03 and C05 against the current package root and adapter boundaries. Keep existing layer direction canonical. The source study and isolated graph probe show protection not supplied by per-file allowed-import checks. [Ruff TID251 configurable banned APIs, 2026-03-26] [Import Linter acyclic sibling contracts, 2026-09-04] [ArchUnit architecture tests, 2026-09-08] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

   Priority: high

3. **Add workflow security with a verified blocking integration**

   Rationale: Review the two C17 findings and introduce C23 at the same time. A deliberately risky fixture must fail the complete workflow; reporting-only success cannot stand in for enforcement. [Securing our GitHub Actions workflows with zizmor, 2026-07-23] [Zizmor CI audit rules, 2026-09-09] [Zizmor integration and failing-exit semantics, 2026-09-09] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

   Priority: high

4. **Design data, model-state and publication contracts with the first real pipeline slice**

   Rationale: C13, C15, C16, C21 and C22 need the agreed target, forecast cut-off, baseline provenance and real schema/API ownership. Extend the single real-service seam and use bounded property checks; do not substitute nominal types or pattern lint for runtime evidence. [LeakageDetector 2.0: Analyzing Data Leakage in Jupyter-Driven Machine Learning Pipelines, 2025-09-19] [Static Analysis by Abstract Interpretation Against Data Leakage in Machine Learning, 2025-05-19] [Pandera dataset validation framework, 2026-09-09] [Hypothesis property-based testing, 2026-09-08] [TypeScript ESLint exhaustive handling of union states, 2026-09-09] [SQLGlot SQL AST inspection and semantic differences, 2026-09-10] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

   Priority: high

5. **Add dependency/runtime and rendered-infrastructure policy when those surfaces are introduced**

   Rationale: C06 should validate the first production package without dev-only assumptions; C19 should evaluate effective configuration, using Python policy or Conftest according to maintenance cost. Keep C18 in the actual migration-owning repository. [Deptry dependency rules, 2026-09-06] [Conftest structured configuration policy tests, 2026-09-08] [Squawk PostgreSQL migration linter, 2026-09-10] [Podium baseline inventory at commit 54b2c88, 2026-09-10]

   Priority: high

6. **Trial heuristic anti-inertia signals without changing existing mandatory gates**

   Rationale: Use C09–C12 to gather concrete evidence about abandoned code, duplication, abstraction and coupling. Promote a new heuristic only after legitimate patterns and false positives are covered. Reject blanket ALL, revived removed rules and automatic threshold-driven refactoring. [Vulture unused-code checks and confidence limits, 2026-04-30] [jscpd duplicate-code detection, 2026-09-10] [Wemake Python styleguide design complexity rules, 2026-09-10] [TypeScript ESLint no-extraneous-class rule, 2026-09-09] [Ruff rule selection and fix safety guidance, 2026-09-10] [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity, 2025-07-10]

   Priority: medium

## 6. Limitations and Future Research

- Agent-specific, longitudinal evidence for individual lint rules is limited. The observational technical-debt study and original vendor/adopter accounts are not controlled tests of this proposed rule set; no maintenance saving is claimed.
- The Podium product pipeline does not exist yet. Seven synthetic probe scenarios and one read-only workflow scan establish bounded checker behaviour, not real model, data or publication correctness.
- The zizmor findings are medium severity and low confidence. Offline scanning did not run online-only audits or establish exploitability.
- Repository metadata provides popularity and maintenance signals, not a service-level guarantee. Latest repository snapshots can differ from released packages; where availability mattered, pinned Ruff/mypy and released Import Linter/zizmor were checked directly.
- Four retained sources are older than the preferred twelve-month window but within the unchanged twenty-four-month technical policy. Current versioned source supports their present capability context; the older METR study is not generalized to current agents.
- Semgrep advanced data-flow capability depends on engine/edition and scope. General static rules cannot fully establish dataset leakage freedom, SQL side-effect freedom or authorization.
- Rule cost categories are qualitative estimates, not measured scanner benchmarks. Complex thresholds, dead-code and clone heuristics require representative code before calibration.
- Single-pass synthesis was used; no independent multi-pass consensus is claimed. Source, citation, owner-independence, hard-constraint and rendered-report checks are separate audits.
- One deliberately invalid symlink fixture in dependency-cruiser could not be indexed. The inspected implementation/documentation files were read and hashed; no conclusion depends on that fixture. Both temporary checkouts were removed.

## 7. References

[1] Harness engineering: leveraging Codex in an agent-first world. OpenAI. (2026-02-11). URL: [source](https://openai.com/index/harness-engineering/)
[2] Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild. Liu et al. / arXiv. (2026-04-26). URL: [source](https://arxiv.org/abs/2603.28592v2)
[3] Harness Engineering - first thoughts. Birgitta Boeckeler / Martin Fowler. (2026-02-17). URL: [source](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html)
[4] Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. METR. (2025-07-10). URL: [source](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
[5] LeakageDetector 2.0: Analyzing Data Leakage in Jupyter-Driven Machine Learning Pipelines. LeakageDetector research authors / arXiv. (2025-09-19). URL: [source](https://arxiv.org/abs/2509.15971)
[6] Mypy 1.19 Released. Mypy maintainers. (2025-11-28). URL: [source](https://mypy-lang.blogspot.com/2025/11/mypy-119-released.html)
[7] Securing our GitHub Actions workflows with zizmor. Private Packagist. (2026-07-23). URL: [source](https://blog.packagist.com/securing-our-github-actions-workflows-with-zizmor/)
[8] Avoiding anys with Linting and TypeScript. typescript-eslint maintainers. (2025-01-21). URL: [source](https://typescript-eslint.io/blog/avoiding-anys/)
[9] Typed Linting with Project Service. typescript-eslint maintainers. (2025-05-29). URL: [source](https://typescript-eslint.io/blog/project-service/)
[10] Static Analysis by Abstract Interpretation Against Data Leakage in Machine Learning. Abstract interpretation research authors. (2025-05-19). URL: [source](https://caterinaurban.github.io/pdf/scp2025.pdf)
[11] OpenAI to acquire Astral. OpenAI. (2026-03-19). URL: [source](https://openai.com/index/openai-to-acquire-astral/)
[12] Ruff BLE001 implementation and rule documentation. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_blind_except/rules/blind_except.rs)
[13] Ruff DTZ001 timezone-aware datetime rule. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_datetimez/rules/call_datetime_without_tzinfo.rs)
[14] Ruff TID251 configurable banned APIs. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_tidy_imports/rules/banned_api.rs)
[15] Ruff PT011 and PT012 exception-test rules. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_pytest_style/rules/raises.rs)
[16] Ruff PD002 dataframe in-place mutation rule. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/pandas_vet/rules/inplace_argument.rs)
[17] Ruff TRY003 exception-message design rule. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/tryceratops/rules/raise_vanilla_args.rs)
[18] Ruff removed PD901 naming rule. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/pandas_vet/rules/assignment_to_df.rs)
[19] Ruff criteria for proposing new lint rules. astral-sh/ruff. (2026-09-10). URL: [source](https://github.com/astral-sh/ruff/blob/18cdbb4f3d14058794420e758864795f55336334/docs/rule-proposals.md)
[20] Mypy optional error codes. python/mypy. (2025-12-15). URL: [source](https://github.com/python/mypy/blob/v1.19.1/docs/source/error_code_list2.rst)
[21] Import Linter acyclic sibling contracts. seddonym/import-linter. (2026-09-04). URL: [source](https://github.com/seddonym/import-linter/blob/31927f1457e3df673912cb5efb0afa6dbc37585f/docs/contract_types/acyclic_siblings.md)
[22] Dependency-cruiser circularity, reachability and instability rules. sverweij/dependency-cruiser. (2026-09-09). URL: [source](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md)
[23] Vulture unused-code checks and confidence limits. jendrikseipp/vulture. (2026-04-30). URL: [source](https://github.com/jendrikseipp/vulture/blob/2c21cb0ae2afa657e36f6a397cb573608a65d79e/README.md)
[24] Wemake Python styleguide design complexity rules. wemake-services/wemake-python-styleguide. (2026-09-10). URL: [source](https://github.com/wemake-services/wemake-python-styleguide/blob/6e0b6b4c33c409a197d651f0dcfeced6798479c0/wemake_python_styleguide/violations/complexity.py)
[25] jscpd duplicate-code detection. kucherenko/jscpd. (2026-09-10). URL: [source](https://github.com/kucherenko/jscpd/blob/0f8785f42332af310b7712e2d772f78fe6944758/README.md)
[26] Conftest structured configuration policy tests. open-policy-agent/conftest. (2026-09-08). URL: [source](https://github.com/open-policy-agent/conftest/blob/fc7d7d7df851eae01067ac9a7064774722a5fb4c/docs/index.md)
[27] Pandera dataset validation framework. unionai-oss/pandera. (2026-09-09). URL: [source](https://github.com/unionai-oss/pandera/blob/8ecdd0df0eb48bf3c53dc0be56e22647101fd516/README.md)
[28] Hypothesis property-based testing. HypothesisWorks/hypothesis. (2026-09-08). URL: [source](https://github.com/HypothesisWorks/hypothesis/blob/cd434f23be1a3598085cf096e28e6738c63b29b3/README.md)
[29] Squawk PostgreSQL migration linter. sbdchd/squawk. (2026-09-10). URL: [source](https://github.com/sbdchd/squawk/blob/0feae0d2ea3407c18f984623a23adff5103e996c/README.md)
[30] TypeScript ESLint no-extraneous-class rule. typescript-eslint/typescript-eslint. (2026-09-09). URL: [source](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/no-extraneous-class.mdx)
[31] TypeScript ESLint no-floating-promises rule. typescript-eslint/typescript-eslint. (2026-09-09). URL: [source](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/no-floating-promises.mdx)
[32] Deptry dependency rules. osprey-oss/deptry. (2026-09-06). URL: [source](https://github.com/osprey-oss/deptry/blob/8957d25022a0b176388e089481b248a35cb1c1f3/docs/rules-violations.md)
[33] Zizmor CI audit rules. zizmorcore/zizmor. (2026-09-09). URL: [source](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/audits.md)
[34] Zizmor integration and failing-exit semantics. zizmorcore/zizmor. (2026-09-09). URL: [source](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/integrations.md)
[35] ArchUnit architecture tests. TNG/ArchUnit. (2026-09-08). URL: [source](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md)
[36] Semgrep taint-analysis scope and engine boundaries. semgrep/semgrep-docs. (2026-09-09). URL: [source](https://github.com/semgrep/semgrep-docs/blob/e29c6d6a26b1ef5e96b9fb7985b98fee393e6edb/docs/writing-rules/data-flow/taint-mode/overview.mdx)
[37] Ruff logging-format rules including G004. astral-sh/ruff. (2026-03-26). URL: [source](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_logging_format/violations.rs)
[38] TypeScript ESLint exhaustive handling of union states. typescript-eslint/typescript-eslint. (2026-09-09). URL: [source](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/switch-exhaustiveness-check.mdx)
[39] SQLGlot SQL AST inspection and semantic differences. tobymao/sqlglot. (2026-09-10). URL: [source](https://github.com/tobymao/sqlglot/blob/83abff6576cbc3b5858581b8ae9a912dec0f3304/README.md)
[40] Podium baseline inventory at commit 54b2c88. Podium local baseline. (2026-09-10). URL: [source](baseline/inventory.json)
[41] Ruff rule selection and fix safety guidance. astral-sh/ruff. (2026-09-10). URL: [source](https://github.com/astral-sh/ruff/blob/18cdbb4f3d14058794420e758864795f55336334/docs/linter.md)

## 8. Appendices

### Appendix A: Search Methodology

- [q1] coding agents long term maintainability technical debt code duplication empirical study 2025 2026 (web.search)
- [q1] site:openai.com harness engineering architectural constraints custom linters 2026 (web.search)
- [q2] Python architectural linting import linter Ruff mypy strict unnecessary abstractions coding agents (web.search)
- [q3] machine learning pipelines static analysis data leakage linting 2025 2026 (web.search)
- [q1] harness engineering leveraging Codex agent first world architectural constraints linters (web.search)
- [q4] site:docs.zizmor.sh audit excessive-permissions artipacked template-injection (web.search)
- [q5] site:dependency-cruiser.js.org forbidden circular orphan instability (web.search)
- [q6] site:metr.org 2025 experienced open source developers AI slowdown randomized (web.search)
- [q2] site:mypy-lang.blogspot.com "1.19" (web.search)
- [q3] machine learning data leakage static analysis 2025 paper pipelines (web.search)
- [q4] zizmor GitHub Actions security audits template injection artipacked (web.search)
- [q5] import linter exhaustive layers independence contracts dependency cruiser cycles typescript eslint no floating promises (web.search)
- [q5] site:typescript-eslint.io/blog 2025 typed linting (web.search)
- [q6] site:docs.astral.sh ruff all rules not recommended conflict (web.search)
- [q2] site:deptry.com DEP001 DEP002 DEP003 DEP004 (web.search)
- [q4] site:conftest.dev terraform plan docker compose policy testing (web.search)
- [q6] site:openai.com Astral acquisition 2026 (web.search)
- [q3] site:scikit-learn.org common pitfalls data leakage random_state 2025 (web.search)
- [q4] site:docs.aws.amazon.com prescriptive guidance terraform policy as code security 2025 (web.search)
- [q5] site:rust-lang.github.io rust clippy await_holding_lock must_use 2026 (web.search)


### Appendix B: Popularity and maintenance signals

Observed during this engagement. Counts and commit dates are captured in [repository-metadata.json](source-material/repository-metadata.json). These are not rule-quality scores, maintenance guarantees or evidence that an individual rule helps agents. Recent activity may include routine updates. Release compatibility is evaluated separately.

| Tool/project | Observed stars | Observed latest commit | Primary capability source |
| --- | --- | --- | --- |
| astral-sh/ruff | 49,574 | 2026-09-10 | [src-041](https://github.com/astral-sh/ruff/blob/18cdbb4f3d14058794420e758864795f55336334/docs/linter.md) |
| python/mypy | 20,637 | 2026-09-09 | [src-020](https://github.com/python/mypy/blob/v1.19.1/docs/source/error_code_list2.rst) |
| seddonym/import-linter | 1,166 | 2026-09-04 | [src-021](https://github.com/seddonym/import-linter/blob/31927f1457e3df673912cb5efb0afa6dbc37585f/docs/contract_types/acyclic_siblings.md) |
| semgrep/semgrep | 16,580 | 2026-09-04 | [src-036](https://github.com/semgrep/semgrep-docs/blob/e29c6d6a26b1ef5e96b9fb7985b98fee393e6edb/docs/writing-rules/data-flow/taint-mode/overview.mdx) |
| fpgmaas/deptry | 1,476 | 2026-09-06 | [src-032](https://github.com/osprey-oss/deptry/blob/8957d25022a0b176388e089481b248a35cb1c1f3/docs/rules-violations.md) |
| jendrikseipp/vulture | 4,806 | 2026-04-30 | [src-023](https://github.com/jendrikseipp/vulture/blob/2c21cb0ae2afa657e36f6a397cb573608a65d79e/README.md) |
| kucherenko/jscpd | 6,179 | 2026-09-10 | [src-025](https://github.com/kucherenko/jscpd/blob/0f8785f42332af310b7712e2d772f78fe6944758/README.md) |
| wemake-services/wemake-python-styleguide | 2,898 | 2026-09-10 | [src-024](https://github.com/wemake-services/wemake-python-styleguide/blob/6e0b6b4c33c409a197d651f0dcfeced6798479c0/wemake_python_styleguide/violations/complexity.py) |
| zizmorcore/zizmor | 6,474 | 2026-09-09 | [src-033](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/audits.md) |
| sbdchd/squawk | 1,170 | 2026-09-10 | [src-029](https://github.com/sbdchd/squawk/blob/0feae0d2ea3407c18f984623a23adff5103e996c/README.md) |
| open-policy-agent/conftest | 3,259 | 2026-09-08 | [src-026](https://github.com/open-policy-agent/conftest/blob/fc7d7d7df851eae01067ac9a7064774722a5fb4c/docs/index.md) |
| sverweij/dependency-cruiser | 7,159 | 2026-09-09 | [src-022](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md) |
| typescript-eslint/typescript-eslint | 16,389 | 2026-09-09 | [src-008](https://typescript-eslint.io/blog/avoiding-anys/) |
| pandera-dev/pandera | 4,452 | 2026-09-09 | [src-027](https://github.com/unionai-oss/pandera/blob/8ecdd0df0eb48bf3c53dc0be56e22647101fd516/README.md) |
| HypothesisWorks/hypothesis | 8,953 | 2026-09-08 | [src-028](https://github.com/HypothesisWorks/hypothesis/blob/cd434f23be1a3598085cf096e28e6738c63b29b3/README.md) |
| tobymao/sqlglot | 9,604 | 2026-09-10 | [src-039](https://github.com/tobymao/sqlglot/blob/83abff6576cbc3b5858581b8ae9a912dec0f3304/README.md) |
| TNG/ArchUnit | 3,830 | 2026-09-08 | [src-035](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md) |

### Appendix C: Local evidence and scope

- [Baseline inventory](baseline/inventory.json): exact committed gate files and hashes.
- [Differential probes](baseline/rule-probes.json): complete authored fixtures and command results.
- [Zizmor probe](baseline/zizmor-probe.json): actual workflow findings and exit code.
- [Selected Ruff rule metadata](baseline/ruff-selected-rules.json): installed-version status and documented limits.
- [Import Linter study](repo-analysis/import-linter/key-findings.md) and [dependency-cruiser study](repo-analysis/dependency-cruiser/key-findings.md): immutable revisions, code pointers and inspection limits.
- [Temporary checkout cleanup](repo-analysis/cleanup.json): both source checkouts and synthetic fixture directories removed.
- [Detailed candidate matrix](rule-matrix.md): all 23 assessments.

### Appendix D: Audit artifacts

- [Requirements](requirements.json) and [domain plan](domain-plan.json).
- [Normalized evidence](evidence.json) and [source validation](validation.json).
- [Analysis](analysis.json), [citation audit](citation-report.json) and [owner grouping](publisher-ownership.json).
- [Hard constraints](constraints-report.json) and [render audit](render-audit.json).
