# Infrastructure scope

Load `.agents/skills/infrastructure-conventions/SKILL.md` from the repository root. Terraform owns AWS resource definitions; Compose owns local services. Preserve separate environment state and explicit local configuration. Mocked Terraform provider tests prove configuration assertions only, not AWS service behaviour. Keep human commands and operational guidance in README.md files.
