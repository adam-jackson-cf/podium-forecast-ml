---
name: "infrastructure-conventions"
description: "Use when changing Terraform, containers, shell, or CI to preserve reproducibility and controlled AWS promotion."
---

# Guidance

- Keep Terraform authoritative for AWS resources and Docker Compose authoritative for local service lifecycle. Do not define the same resource in both.
- Pin tool versions and dependencies through the established locks. Promote release images by digest; verify the intended CPU architecture.
- Use explicit configuration at service boundaries. Do not put local emulator endpoints into cloud configuration or infer production defaults.
- Bind local service ports to loopback; use least privilege and writable paths limited to the service's actual needs. Do not mount the Docker socket without a demonstrated executor requirement.
- Keep credentials outside committed configuration. Do not print environment values, connection strings, Terraform secrets or debug dumps.
- Keep Terraform state separate by environment. Terraform plans and local emulation do not establish cloud IAM, networking or runtime correctness.
- Preserve versioned datasets and release manifests across runtimes. Local resource IDs and approval state are not portable production authority.
- Keep CI permissions explicit and narrow. Preserve blocking gates and dependency locks; do not add network-dependent tests to the fast layer.
- Validate changed Terraform, Compose, Dockerfiles, shell and workflow definitions using the repository's corresponding gates.
- New executable languages require a matching formatter, lint/static checks and relevant behavioural coverage before their code is introduced.
