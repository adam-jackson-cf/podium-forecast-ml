# Repository instructions

This repository establishes the local development and verification foundation for Workstream B - ML predictive forecasting. Implement only the requested scope; a green scaffold does not establish model or AWS readiness.

- Keep user-facing setup, operation and verification instructions in `README.md` files. `docs/local-solution-assessment.md` is the requested architecture assessment, not a runbook.
- Never expose secrets. Verify presence only. Keep data extracts, credentials, generated models and Terraform state out of Git.
- Preserve canonical wording and contracts. Replace obsolete designs rather than retain parallel legacy paths.
- Do not suppress failures, loosen gates, add skip flags, or insert production mocks or placeholders to obtain green results.
- Use `quality-policy.toml` and `pyproject.toml` as the canonical executable policy; do not duplicate numeric thresholds in instructions.
- Report what was executed, what passed, and what remains unverified. Distinguish scaffold smoke results from model quality and actual Nexus integration.

## Load only relevant guidance

| Work | Read |
| --- | --- |
| Python creation or refactoring | `.agents/skills/python-conventions/SKILL.md` |
| Tests, smoke journeys or verification changes | `.agents/skills/testing-conventions/SKILL.md` |
| Containers, Terraform, shell or CI changes | `.agents/skills/infrastructure-conventions/SKILL.md` |
| Implementation assignment | `.agents/roles/python-implementer.md` |
| Independent design review | `.agents/roles/design-reviewer.md` |
| Independent scenario/outcome review | `.agents/roles/test-reviewer.md` |

Role files are on-demand instruction briefs, not registered runtime agents. Read a brief only for the assigned role; do not preload every role. Follow scoped `AGENTS.md` when entering its directory.
