# Repository instructions

- **ALWAYS** implement only the requested scope.
- **NEVER** claim that scaffold checks establish model quality, Nexus integration, AWS behaviour, or production readiness.
- **ALWAYS** keep user-facing setup, operation, and verification instructions in `README.md` files.
- **NEVER** expose secrets. Verify environment-variable presence without printing values.
- **NEVER** commit data extracts, credentials, generated models, or Terraform state.
- **ALWAYS** treat `quality-policy.toml` and `pyproject.toml` as the executable policy for numeric thresholds, naming constraints, import rules, and enabled checks.
- **NEVER** duplicate executable-policy values in instruction files.
- **ALWAYS** preserve exact existing wording when reusing a contract, label, constraint, or user-specified phrase.
- **NEVER** suppress failures, loosen gates, add skip flags, or add production mocks, placeholders, or fallback paths to obtain a passing result.
- **ALWAYS** replace obsolete designs and remove code that exists only for the obsolete design.
- **ALWAYS** report the commands executed, their results, and every unverified acceptance criterion.
- If a static check cannot follow runtime dataflow, **ALWAYS** verify the affected IO ownership, failure propagation, or asynchronous lifecycle from code and behavioural tests.
- If a requested product rule is absent, **NEVER** invent it; stop dependent work and identify the missing decision.

## Conditional guidance

| Condition | Read |
| --- | --- |
| When constructing a todo list or plan of any type, use the plan judge agent as an independent subagent and act on its feedback | `agent-guidance/agents/plan_judge.toml` |
| When defining a solution, use the kiss agent as an independent subagent review of your approach and act on its feedback | `agent-guidance/agents/kiss.toml` |
| Before coding, when a proposal changes runtime or repository architecture—components, contracts, dependencies, ownership, lifecycle, IO/failure behaviour, compatibility, trust boundaries—use the program-design judge as an independent subagent and act on its feedback | `agent-guidance/agents/program_design_judge.toml` |
| When deciding or changing behavioral-instruction architecture, progressive disclosure, or whether guidance belongs in instructions, a skill, or an agent role, use the guidance-architecture judge as an independent subagent and act on its feedback | `agent-guidance/agents/guidance_architecture_judge.toml` |
| When designing or reviewing automated test scenarios, oracles, fixtures, assertions, smoke journeys, or verification gates, use the test judge and testing conventions | `agent-guidance/agents/test_judge.toml` and `agent-guidance/skills/testing-conventions/SKILL.md` |

