# Candidate rule matrix

Research only: these rules and designs have not been installed. The current baseline remains unchanged. Cost categories are qualitative; they are not scanner benchmarks.

See [the report](report.md) for the evidence limits and the prioritized decision. Some rows are complementary runtime or test contracts, explicitly distinguished from static lint.

## Prioritized overview

| ID | Candidate | Mechanism | Timing | Priority |
| --- | --- | --- | --- | --- |
| C01 | Precise exception handling and failure propagation | Existing tool plus bespoke control-flow rule | Next increment | high |
| C02 | Timezone-aware forecast instants | Existing tool | Next increment | high |
| C03 | Effect ownership and canonical API access | Existing tool plus bespoke boundary rule | Next increment | high |
| C04 | No unchecked Any crossing a typed boundary | Existing type checker plus runtime validation | Next increment | high |
| C05 | Whole-package cycles and protected interfaces | Existing tool | Next increment | high |
| C06 | Dependency declaration and runtime/dev separation | Existing tool | First production package | high |
| C07 | Exception tests that cannot pass at the wrong statement | Existing tool | Next increment | high |
| C08 | Structured, stable job diagnostics | Existing tool plus bespoke record-schema checks | First real ML job | medium |
| C09 | Unused definitions and unreachable subgraphs | Existing tool plus graph concept | Advisory trial after first feature | medium |
| C10 | Duplicate logic and semantic contract drift | Existing detector plus bespoke contract comparison | Advisory trial after first feature | medium |
| C11 | Coupling and change-impact budgets | Transferable design with bespoke graph metrics | Advisory trial after first feature | medium |
| C12 | Reject stateless wrapper classes without a role | Cross-language concept with bespoke AST rule | Advisory trial | medium |
| C13 | Leakage and forecast-time dataset contracts | Bespoke static guard plus runtime/data checks | First dataset and training slice | high |
| C14 | Explicit dataframe mutation boundaries | Existing tool and immutable-data design | If pandas is selected for features | medium |
| C15 | Typed model lifecycle and exhaustive state handling | Cross-language concept plus existing type checks | First model approval/publication slice | high |
| C16 | Semantic SQL extraction guard | Bespoke rule using an existing parser | First real extraction adapter | high |
| C17 | GitHub Actions security invariants | Existing tool | Next increment | high |
| C18 | PostgreSQL migration lock and rewrite safety | Existing tool | Only if this repository owns schema migrations | medium |
| C19 | Rendered infrastructure policy | Existing policy engine or bespoke typed checks | Next infrastructure increment | high |
| C20 | Handle every asynchronous result | Cross-language concept plus existing type checker | Before asynchronous work is introduced | medium |
| C21 | One source for contracts and feature order | Bespoke deterministic comparison | First pipeline contracts | high |
| C22 | Behavioural properties for gates and ML transformations | Existing test generator; complementary to lint | Gate changes and first feature slice | high |
| C23 | Gate result and scanner-coverage contracts | Bespoke integration assertions | Every new checker integration | high |

## Candidate details

### C01 — Precise exception handling and failure propagation

**Rules/mechanism:** Ruff BLE001; proposed no-success-after-failure rule

**Current gap:** BLE and TRY are not selected. B904 already covers exception chaining; it does not prevent swallowed failures.

**Proposed enforcement:** Enable BLE001; separately reject a failed job path that logs an exception then returns an ordinary success value. Preserve explicit failure outcomes or re-raise.

**Example:** Reject `except Exception: return 0`; also inspect `logging.exception(...); return 0`, which BLE001 permits.

**Acceptance outcome:** An expected failure remains a failure through the job boundary; successful and deliberate recovery paths still work.

**False-positive/coverage risk:** Legitimate top-level cleanup/recovery exists. BLE001 alone is insufficient: its logging exemption passed the isolated probe.

**Cost:** Low for BLE001; medium for scoped control-flow analysis.

**Evidence status:** Pinned Ruff differential probe confirms additional coverage and its limit.

**Sources:** [src-012](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_blind_except/rules/blind_except.rs) [src-002](https://arxiv.org/abs/2603.28592v2) [src-040](baseline/inventory.json)

### C02 — Timezone-aware forecast instants

**Rules/mechanism:** Ruff DTZ001–DTZ007, DTZ011–DTZ012 as applicable

**Current gap:** DTZ is absent. Forecast cut-offs require unambiguous instants, not implicit machine-local time.

**Proposed enforcement:** Select the supported DTZ rules for code handling instants; define explicit conversion at ingestion boundaries.

**Example:** Reject `datetime.now()` for a forecast instant; require an explicit timezone such as UTC.

**Acceptance outcome:** Naive construction fails lint; aware instants pass; time-zone boundary tests preserve the same instant.

**False-positive/coverage risk:** Calendar dates and local wall-clock business values can be valid. Distinguish their types rather than misclassifying every date as an instant.

**Cost:** Low static cost; temporal semantics still need tests.

**Evidence status:** Pinned Ruff probe flagged the naive clock that current configuration accepts.

**Sources:** [src-013](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_datetimez/rules/call_datetime_without_tzinfo.rs) [src-010](https://caterinaurban.github.io/pdf/scp2025.pdf) [src-040](baseline/inventory.json)

### C03 — Effect ownership and canonical API access

**Rules/mechanism:** Ruff TID251 configured bans; proposed EFFECT_OWNER contract

**Current gap:** Current architecture permits all standard-library imports in pure layers, including network/process/file APIs. Layer direction alone is not effect isolation.

**Proposed enforcement:** Restrict known IO APIs and client construction to owned adapters/entrypoints; use symbol-aware matching. State which dynamic imports are allowed.

**Example:** A domain import of `urllib.request.urlopen` passes the current layer check; a configured TID251 rule rejects it with an adapter-directed message.

**Acceptance outcome:** Known IO calls in domain/application fail; the same approved capability in its adapter passes; aliases are covered.

**False-positive/coverage risk:** Pure path manipulation is not file IO. Do not ban all pathlib use or claim syntactic matching detects every dynamic effect.

**Cost:** Low for explicit APIs; medium for typed/call-aware ownership checks.

**Evidence status:** Confirmed by a static differential fixture; no network call was executed.

**Sources:** [src-014](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_tidy_imports/rules/banned_api.rs) [src-035](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md) [src-040](baseline/inventory.json)

### C04 — No unchecked Any crossing a typed boundary

**Rules/mechanism:** Mypy disallow_any_explicit/disallow_any_unimported; scoped disallow_any_expr; validated decoders

**Current gap:** Mypy strict is not a ban on every Any expression. JSON-derived values can flow into an annotated variable without runtime validation.

**Proposed enforcement:** Validate external payloads in adapters, expose narrow typed ports, and apply stronger Any checks in owned core code. Treat cast as an assertion, not parsing.

**Example:** Current mypy accepts `payload=json.loads(text); runner_id: int=payload['runner_id']`; scoped disallow_any_expr rejects the unchecked flow.

**Acceptance outcome:** Wrong input shapes are rejected at the boundary; valid decoded objects enter the core without Any; typed SDK paths remain usable.

**False-positive/coverage risk:** Blanket Any-expression bans across dynamic third-party libraries can create casts or wrapper sprawl. Calibrate scope before making a blocking rule.

**Cost:** Low-to-medium incremental type-check cost; runtime validation per boundary.

**Evidence status:** Pinned mypy 1.19.1 differential probe confirms the gap.

**Sources:** [src-020](https://github.com/python/mypy/blob/v1.19.1/docs/source/error_code_list2.rst) [src-008](https://typescript-eslint.io/blog/avoiding-anys/) [src-040](baseline/inventory.json)

### C05 — Whole-package cycles and protected interfaces

**Rules/mechanism:** Import Linter acyclic_siblings; protected/independence contracts where justified

**Current gap:** Per-file allowed-layer checks do not detect cycles within an allowed layer or package-level feedback loops.

**Proposed enforcement:** Add a whole-package cycle contract at the existing package root; preserve current dependency direction. Add explicit internal APIs rather than duplicating existing layer checks.

**Example:** Two domain modules can mutually import while both satisfy the current allowed-layer map.

**Acceptance outcome:** A same-layer cycle fails and its acyclic counterpart passes; diagnostics show the edge/cycle path.

**False-positive/coverage risk:** Do not install permissive generic layer defaults, missing optional layers or ignore_imports to make the result green. Dynamic imports need a separate policy.

**Cost:** Whole-package graph construction; benchmark once the codebase grows.

**Evidence status:** Import Linter 2.15 failed the synthetic cycle and passed the repaired graph.

**Sources:** [src-021](https://github.com/seddonym/import-linter/blob/31927f1457e3df673912cb5efb0afa6dbc37585f/docs/contract_types/acyclic_siblings.md) [src-022](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md) [src-035](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md) [src-040](baseline/inventory.json)

### C06 — Dependency declaration and runtime/dev separation

**Rules/mechanism:** Deptry DEP001–DEP004

**Current gap:** The foundation deliberately installs tooling/runtime services in a dev environment. A future production package must not rely on transitively installed or dev-only libraries.

**Proposed enforcement:** Check direct, missing, unused and misplaced dependencies in production source; verify the production artifact without development dependencies.

**Example:** Importing a library only because MLflow happens to install it should fail the production dependency contract.

**Acceptance outcome:** A package with only its declared runtime dependencies can execute its owned journey; removing a required direct dependency is detected.

**False-positive/coverage risk:** CLI-only dev tools are not unused runtime dependencies. Dynamic plugins and namespace packages require an explicit discovery contract.

**Cost:** Low-to-medium source/environment inspection.

**Evidence status:** Maintained tool documented; no full-repository Deptry run or production packaging claim made.

**Sources:** [src-032](https://github.com/osprey-oss/deptry/blob/8957d25022a0b176388e089481b248a35cb1c1f3/docs/rules-violations.md) [src-023](https://github.com/jendrikseipp/vulture/blob/2c21cb0ae2afa657e36f6a397cb573608a65d79e/README.md) [src-040](baseline/inventory.json)

### C07 — Exception tests that cannot pass at the wrong statement

**Rules/mechanism:** Ruff PT011 and PT012

**Current gap:** Pytest bypass checks exist, but PT rules are not selected. A broad raises block can succeed because setup failed rather than the intended operation.

**Proposed enforcement:** Require a specific exception expectation and a single raising operation in the context; assert useful failure meaning without exact incidental message snapshots.

**Example:** Move fixture setup outside `pytest.raises`; make the contract operation the only statement expected to raise.

**Acceptance outcome:** Wrong failure reasons and setup failures do not satisfy the scenario; the intended rejected behaviour does.

**False-positive/coverage risk:** Iterator/context-manager edge cases exist. Preserve behaviour-focused scenarios instead of one test per assertion.

**Cost:** Low.

**Evidence status:** Supported stable rules verified in the installed Ruff catalog.

**Sources:** [src-015](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_pytest_style/rules/raises.rs) [src-028](https://github.com/HypothesisWorks/hypothesis/blob/cd434f23be1a3598085cf096e28e6738c63b29b3/README.md) [src-040](baseline/inventory.json)

### C08 — Structured, stable job diagnostics

**Rules/mechanism:** Ruff G004; proposed structured-event schema

**Current gap:** T20 already rejects print, but no rule establishes structured job/run/dataset/model context or consistent failure events.

**Proposed enforcement:** Use one event schema and owned logger adapter; validate required correlation fields and error status. G004 catches eager interpolated logging, not the schema itself.

**Example:** Use a stable event name and structured identifiers instead of embedding the entire job context in an f-string.

**Acceptance outcome:** A failed job emits a valid failure record with traceable identifiers, without exposing secret values.

**False-positive/coverage risk:** A logger call is not evidence that a failure propagated; avoid assuming G004 enforces structured logging or secret redaction.

**Cost:** Low static check plus focused record validation.

**Evidence status:** Capability documented; project-specific event contract remains to be designed.

**Sources:** [src-037](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_logging_format/violations.rs) [src-001](https://openai.com/index/harness-engineering/) [src-040](baseline/inventory.json)

### C09 — Unused definitions and unreachable subgraphs

**Rules/mechanism:** Vulture; declared-root graph reachability

**Current gap:** F401/F841 and ARG cover imports/locals/arguments, but not every abandoned public function, plugin or disconnected feature subtree.

**Proposed enforcement:** Combine declared entrypoints with whole-source reachability and review Vulture findings; delete only after real usage paths are accounted for.

**Example:** A never-referenced feature module with internal imports can escape a simple orphan test; root reachability can expose it.

**Acceptance outcome:** Registered entrypoints/plugins remain admitted; an intentionally unreferenced fixture is found.

**False-positive/coverage risk:** Vulture's lower-confidence labels are heuristics, not calibrated probabilities. High-confidence results overlap existing gates; public-definition findings need review.

**Cost:** Low-to-medium; whole-source graph needed for disconnected files.

**Evidence status:** Do not enable blanket deletion or convert every finding to a blocking gate.

**Sources:** [src-023](https://github.com/jendrikseipp/vulture/blob/2c21cb0ae2afa657e36f6a397cb573608a65d79e/README.md) [src-022](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md) [src-040](baseline/inventory.json)

### C10 — Duplicate logic and semantic contract drift

**Rules/mechanism:** jscpd clone detection; proposed canonical-contract comparison

**Current gap:** No clone detector or canonical schema/value drift check exists; copied feature or publication logic can diverge while each copy passes lint.

**Proposed enforcement:** Use clone reports to locate candidates, then test shared invariants or generate repeated schemas from one source.

**Example:** Two copies of odds conversion or feature-order definitions evolve separately; centralize their contract only when they share the same responsibility.

**Acceptance outcome:** A deliberate divergent copy is reported; legitimate boilerplate does not force a misleading abstraction.

**False-positive/coverage risk:** Similarity is not semantic identity. Avoid zero-duplication gates and aggressive auto-refactors that merge unrelated concepts.

**Cost:** Repository-wide token comparison; calibrate thresholds on meaningful examples.

**Evidence status:** Active project evidence; detector not benchmarked or installed as a gate here.

**Sources:** [src-025](https://github.com/kucherenko/jscpd/blob/0f8785f42332af310b7712e2d772f78fe6944758/README.md) [src-024](https://github.com/wemake-services/wemake-python-styleguide/blob/6e0b6b4c33c409a197d651f0dcfeced6798479c0/wemake_python_styleguide/violations/complexity.py) [src-002](https://arxiv.org/abs/2603.28592v2)

### C11 — Coupling and change-impact budgets

**Rules/mechanism:** Dependency-cruiser moreUnstable concept; WPS module/import/member complexity concepts

**Current gap:** Current complexity thresholds are mostly local to functions. They do not measure how many modules a change can affect.

**Proposed enforcement:** Report fan-in/fan-out, strongly connected components and transitive change reach; calibrate any hard budget by component role.

**Example:** A small helper importing many unrelated subsystems can have low local complexity and high change impact.

**Acceptance outcome:** A cross-domain coupling fixture expands the reported impact set; a composition root is recognized as a different role.

**False-positive/coverage risk:** Dependency instability is not a verdict of bad code. Raw import counts can be gamed by namespace imports or extra wrapper modules.

**Cost:** Graph-wide analysis; no fixed latency or change-effort savings claimed.

**Evidence status:** Conceptual adaptation; no threshold is recommended as empirically optimal for agents.

**Sources:** [src-022](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md) [src-024](https://github.com/wemake-services/wemake-python-styleguide/blob/6e0b6b4c33c409a197d651f0dcfeced6798479c0/wemake_python_styleguide/violations/complexity.py) [src-019](https://github.com/astral-sh/ruff/blob/18cdbb4f3d14058794420e758864795f55336334/docs/rule-proposals.md)

### C12 — Reject stateless wrapper classes without a role

**Rules/mechanism:** typescript-eslint no-extraneous-class concept

**Current gap:** Python object-choice guidance is prose; generic-name checks do not detect unnecessary class-only namespaces.

**Proposed enforcement:** Flag classes used solely as static namespaces for review; use functions/modules unless state, lifecycle, polymorphism or a data contract justifies a class.

**Example:** A class containing only static utility functions can add ceremony without owning behaviour or state.

**Acceptance outcome:** Stateless namespace wrappers are found; dataclasses, Protocols, Enums, exceptions and framework-required classes remain valid.

**False-positive/coverage risk:** One public method is not automatically a smell. A universal minimum-method rule would reject legitimate domain objects.

**Cost:** Low AST cost, but scope requires careful semantic exclusions.

**Evidence status:** Do not port the TypeScript implementation mechanically to Python.

**Sources:** [src-030](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/no-extraneous-class.mdx) [src-024](https://github.com/wemake-services/wemake-python-styleguide/blob/6e0b6b4c33c409a197d651f0dcfeced6798479c0/wemake_python_styleguide/violations/complexity.py) [src-040](baseline/inventory.json)

### C13 — Leakage and forecast-time dataset contracts

**Rules/mechanism:** Declared split/cut-off API; dataset availability and partition invariants

**Current gap:** No real training dataset exists yet. Generic lint cannot know whether a feature was available at forecast time or whether all runners stay with their race.

**Proposed enforcement:** Own the split/feature APIs, prohibit raw split/label access outside them, and validate availability times, complete-race partitions and untouched holdouts on real manifests.

**Example:** Fitting preprocessing on the combined dataset before splitting must fail an outcome check; a naive spelling-based lint can miss aliased calls.

**Acceptance outcome:** Temporal leakage, race overlap and repeated holdout use are rejected; an agreed valid snapshot passes.

**False-positive/coverage risk:** Static leakage tools have library/notebook scope limits. Do not claim full leakage freedom from a general AST linter.

**Cost:** Static checks can be cheap; complete dataset invariants scale with data and belong at the appropriate pipeline boundary.

**Evidence status:** Research tools inform design; not a turnkey CI recommendation for this script/container pipeline.

**Sources:** [src-005](https://arxiv.org/abs/2509.15971) [src-010](https://caterinaurban.github.io/pdf/scp2025.pdf) [src-036](https://github.com/semgrep/semgrep-docs/blob/e29c6d6a26b1ef5e96b9fb7985b98fee393e6edb/docs/writing-rules/data-flow/taint-mode/overview.mdx) [src-040](baseline/inventory.json)

### C14 — Explicit dataframe mutation boundaries

**Rules/mechanism:** Ruff PD002; explicit transformation ownership

**Current gap:** PD rules are absent. The repository has Arrow artifacts but has not selected the feature-processing API.

**Proposed enforcement:** Where pandas is used, prefer explicit returned transformations; keep shared snapshots immutable by contract.

**Example:** Prefer an assigned transformed frame over `inplace=True` on a shared frame.

**Acceptance outcome:** An input snapshot is unchanged by a feature transform; the transformed output satisfies its schema.

**False-positive/coverage risk:** PD002 does not detect every mutation and is not needed merely because pandas is an MLflow dependency.

**Cost:** Low static cost; mutation outcome checks on representative data.

**Evidence status:** Conditional on actual pandas use, not a reason to introduce pandas.

**Sources:** [src-016](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/pandas_vet/rules/inplace_argument.rs) [src-027](https://github.com/unionai-oss/pandera/blob/8ecdd0df0eb48bf3c53dc0be56e22647101fd516/README.md) [src-040](baseline/inventory.json)

### C15 — Typed model lifecycle and exhaustive state handling

**Rules/mechanism:** Mypy exhaustive-match; protected construction of validated/approved objects

**Current gap:** Approval and publication are not implemented. Boolean flags and generic dictionaries would allow ambiguous transitions and multiply change sites.

**Proposed enforcement:** Represent lifecycle states explicitly and make publication require the approved-state contract produced by the owned approval boundary.

**Example:** Adding a new model state should make incomplete dispatch fail; a raw candidate should not satisfy the publication interface.

**Acceptance outcome:** Unapproved and failed candidates cannot publish; every declared state has explicit handling and runtime authorization remains enforced.

**False-positive/coverage risk:** Types can be forged with casts and dataclass freezing is shallow. Static checks do not replace real approval authorization or persisted evidence.

**Cost:** Low static cost plus state-transition and authorization tests.

**Evidence status:** Optional mypy code exists in 1.19.1; full lifecycle design is proposed, not implemented.

**Sources:** [src-038](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/switch-exhaustiveness-check.mdx) [src-020](https://github.com/python/mypy/blob/v1.19.1/docs/source/error_code_list2.rst) [src-035](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md) [src-040](baseline/inventory.json)

### C16 — Semantic SQL extraction guard

**Rules/mechanism:** SQLGlot AST policy plus PostgreSQL read-only privileges

**Current gap:** SQLFluff checks SQL form and selected conventions; a read-only fixture exists, but no production extraction SQL policy is implemented.

**Proposed enforcement:** Parse the chosen dialect and reject disallowed statement/CTE operations; retain real read-only database roles and transaction constraints.

**Example:** A WITH clause containing a modifying statement must not pass merely because a query ends in SELECT.

**Acceptance outcome:** Disallowed write forms fail static checks and real database write attempts fail; permitted extraction remains usable.

**False-positive/coverage risk:** A SELECT can call a side-effecting function. Parsing alone cannot establish privilege, function behaviour or resource safety.

**Cost:** Low-to-medium parsing plus the existing real-service seam extended for the owned adapter.

**Evidence status:** Parser capability inspected; proposed application policy not coded.

**Sources:** [src-039](https://github.com/tobymao/sqlglot/blob/83abff6576cbc3b5858581b8ae9a912dec0f3304/README.md) [src-029](https://github.com/sbdchd/squawk/blob/0feae0d2ea3407c18f984623a23adff5103e996c/README.md) [src-040](baseline/inventory.json)

### C17 — GitHub Actions security invariants

**Rules/mechanism:** Zizmor artipacked, template-injection, excessive-permissions, dangerous-triggers, unpinned-uses

**Current gap:** actionlint/YAML validate syntax and selected shell issues, but do not establish these security invariants.

**Proposed enforcement:** Add a pinned, strict-collection security scan. Review checkout credential persistence and future workflow privilege/trigger changes.

**Example:** Both existing checkout steps omit `persist-credentials: false`.

**Acceptance outcome:** A risky workflow fixture produces a nonzero gate result; a reviewed safe fixture passes; collection errors cannot disappear.

**False-positive/coverage risk:** The actual probe found two medium-severity, low-confidence artipacked findings, not proven leaks. Online audits have different capabilities and prerequisites.

**Cost:** Low offline scan in this small workflow set; online audits require separate setup.

**Evidence status:** Read-only zizmor 1.30.1 probe completed; no autofix or gate change.

**Sources:** [src-033](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/audits.md) [src-034](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/integrations.md) [src-007](https://blog.packagist.com/securing-our-github-actions-workflows-with-zizmor/) [src-040](baseline/inventory.json)

### C18 — PostgreSQL migration lock and rewrite safety

**Rules/mechanism:** Squawk require-concurrent-index-creation, constraint-missing-not-valid, prefer-timestamptz and related rules

**Current gap:** SQL formatting is not migration safety. The ML repository currently does not own Nexus schema changes.

**Proposed enforcement:** Apply migration-aware rules in the repository that owns the DDL, with version-appropriate PostgreSQL semantics and rehearsal.

**Example:** Flag an index build that unnecessarily blocks writes; keep concurrent index creation outside a transaction where PostgreSQL requires it.

**Acceptance outcome:** Unsafe migration fixtures are rejected and the reviewed migration executes under realistic locking conditions.

**False-positive/coverage risk:** Rules are not blanket bans: fresh empty tables differ from populated production tables. Do not add Nexus write authority to this project.

**Cost:** Low static cost; real migration rehearsal is separate.

**Evidence status:** Deferred unless migration ownership becomes part of scope.

**Sources:** [src-029](https://github.com/sbdchd/squawk/blob/0feae0d2ea3407c18f984623a23adff5103e996c/README.md) [src-026](https://github.com/open-policy-agent/conftest/blob/fc7d7d7df851eae01067ac9a7064774722a5fb4c/docs/index.md) [src-040](baseline/inventory.json)

### C19 — Rendered infrastructure policy

**Rules/mechanism:** Conftest/Rego or equivalent Python policy over rendered Compose and Terraform plan JSON

**Current gap:** Current tests protect a specific storage module and static files. They do not yet enforce every future resource or resolved local service configuration.

**Proposed enforcement:** Check effective settings: expected image identity, no unapproved privilege/socket mounts, allowed cloud scope, approved resource types and workload-specific permissions.

**Example:** A harmless-looking override must not render a privileged container or an unintended cloud target.

**Acceptance outcome:** Unsafe rendered fixtures fail; missing/unknown required values fail explicitly; planned environment differences pass by contract.

**False-positive/coverage risk:** Rego adds a language/toolchain. A small Python policy may be simpler; do not stack overlapping scanners without an identified new invariant.

**Cost:** Low-to-medium policy evaluation; cloud plan generation has separate credentials/state boundaries.

**Evidence status:** Proposed semantic layer, not a claim that present configuration is unsafe.

**Sources:** [src-026](https://github.com/open-policy-agent/conftest/blob/fc7d7d7df851eae01067ac9a7064774722a5fb4c/docs/index.md) [src-035](https://github.com/TNG/ArchUnit/blob/8b614c6b59d272e92634ce1bbcd430fb0006fe55/README.md) [src-040](baseline/inventory.json)

### C20 — Handle every asynchronous result

**Rules/mechanism:** Mypy unused-awaitable; existing default unused-coroutine retained

**Current gap:** A discarded generic Awaitable can pass current strict mypy even though ordinary unused coroutines already have checking.

**Proposed enforcement:** Require awaiting, returning or explicitly owned task lifecycle management; introduce async-specific library lint only when that library is used.

**Example:** Calling a function returning Awaitable[int] and discarding it passes baseline but fails with unused-awaitable enabled.

**Acceptance outcome:** Discarded work is rejected; managed tasks demonstrate completion/cancellation/error handling.

**False-positive/coverage risk:** Merely assigning or discarding into a named variable is not lifecycle ownership. TypeScript's void escape illustrates why syntactic silencing is insufficient.

**Cost:** Low incremental type-check cost.

**Evidence status:** Confirmed in pinned mypy differential fixture; project currently has no async pipeline.

**Sources:** [src-020](https://github.com/python/mypy/blob/v1.19.1/docs/source/error_code_list2.rst) [src-031](https://github.com/typescript-eslint/typescript-eslint/blob/cd2e3d796b5e18cdaa4ea10fec0b87caaa8db026/packages/eslint-plugin/docs/rules/no-floating-promises.mdx) [src-040](baseline/inventory.json)

### C21 — One source for contracts and feature order

**Rules/mechanism:** Canonical schema/manifest generation and parity checks

**Current gap:** Exact wording is required in guidance, but no executable parity contract yet binds dataset schema, feature order, model metadata and publication payload.

**Proposed enforcement:** Generate or compare repeated representations from one owned contract, with explicit version/hash linkage.

**Example:** A feature-order change must invalidate an incompatible model manifest instead of silently reusing the old artifact.

**Acceptance outcome:** A deliberate contract mismatch is rejected; changing the canonical contract updates every dependent generated representation.

**False-positive/coverage risk:** Do not infer semantic equality from similar strings or merge distinct concepts such as starting price and editorial forecast price.

**Cost:** Low metadata checks; integration outcomes still need the real pipeline seam.

**Evidence status:** Proposed future invariant; field names and acceptance thresholds still need domain agreement.

**Sources:** [src-027](https://github.com/unionai-oss/pandera/blob/8ecdd0df0eb48bf3c53dc0be56e22647101fd516/README.md) [src-022](https://github.com/sverweij/dependency-cruiser/blob/2aa2e34ed8ff8a074588e21603c4fafc0edf6170/doc/rules-reference.md) [src-040](baseline/inventory.json)

### C22 — Behavioural properties for gates and ML transformations

**Rules/mechanism:** Hypothesis properties and targeted mutation-style challenges

**Current gap:** Example-based verifier tests are valuable, but coverage alone cannot prove resistance to aliases, nesting variants, false success or ML leakage.

**Proposed enforcement:** Generate valid/invalid structures and data partitions; test invariant preservation rather than exact source text or one discovered value.

**Example:** Reordering runners should not change race membership; an aliased forbidden call should remain rejected.

**Acceptance outcome:** Meaningfully different invalid cases fail while equivalent valid cases pass; production code is included in appropriate coverage when introduced.

**False-positive/coverage risk:** Generators can mirror implementation mistakes. Keep an independent behavioural oracle and the single real-service seam.

**Cost:** Bounded fast property tests; expensive journey checks remain explicitly invoked.

**Evidence status:** Complementary verification, not presented as a static lint rule.

**Sources:** [src-028](https://github.com/HypothesisWorks/hypothesis/blob/cd434f23be1a3598085cf096e28e6738c63b29b3/README.md) [src-015](https://github.com/astral-sh/ruff/blob/0.15.8/crates/ruff_linter/src/rules/flake8_pytest_style/rules/raises.rs) [src-040](baseline/inventory.json)

### C23 — Gate result and scanner-coverage contracts

**Rules/mechanism:** Failing-exit, nonempty intended scope, unknown-result and suppression-policy checks

**Current gap:** Existing guards reject many bypasses, but adding another tool introduces new output formats, ignores, baselines and collection failure modes.

**Proposed enforcement:** Test the wrapper with known findings, scanner errors and omitted inputs; map each maintained executable location to its checker.

**Example:** Zizmor SARIF output can accompany exit zero despite findings; use a verified blocking path instead of equating upload success with safety.

**Acceptance outcome:** The end-to-end gate fails on a known violation and an analysis failure; empty scope is accepted only when explicitly expected for the project phase.

**False-positive/coverage risk:** Do not confuse source-type admission with actual scanner coverage or auto-ignore generated reports by broad unreviewed patterns.

**Cost:** Small integration tests; no need to rerun the entire slow journey for each lint edit.

**Evidence status:** Required integration discipline; no existing gate was changed during this research.

**Sources:** [src-034](https://github.com/zizmorcore/zizmor/blob/a7112ad562bafa07e9a2ca7504dd04fdbb3174e3/docs/integrations.md) [src-019](https://github.com/astral-sh/ruff/blob/18cdbb4f3d14058794420e758864795f55336334/docs/rule-proposals.md) [src-040](baseline/inventory.json)
