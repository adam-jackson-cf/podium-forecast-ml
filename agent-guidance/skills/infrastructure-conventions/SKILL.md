---
name: "infrastructure-conventions"
description: "Use when changing Terraform, containers, shell, or CI."
---

# Guidance

- **ALWAYS** pin tools and dependencies through the repository lock mechanism.
- **ALWAYS** identify release images by digest and verify the required CPU architecture.
- **ALWAYS** require explicit service-boundary configuration.
- **NEVER** place local emulator endpoints in cloud configuration.
- **NEVER** infer production defaults from local configuration.
- **ALWAYS** bind exposed local service ports to loopback.
- **ALWAYS** grant a service only the permissions and writable paths used by its configured commands.
- **NEVER** mount the Docker socket unless the requested executor must issue Docker API calls.
- **NEVER** print environment values, connection strings, Terraform secrets, or credential-bearing debug output.
- **ALWAYS** keep Terraform state separate for each environment.
- **NEVER** report cloud IAM, networking, or runtime validation from a Terraform plan or local emulator result.
- **ALWAYS** keep dataset versions and release manifests stable across runtimes.
- **NEVER** treat local resource identifiers or approval state as production authority.
- **ALWAYS** declare CI permissions explicitly and grant only actions used by the job.
- **NEVER** add a network-dependent test to the fast test layer.
- **ALWAYS** evaluate rendered Compose configuration for every profile through the repository external-check entrypoint.
- If Compose inputs are missing, output is malformed, or a profile violates policy, **ALWAYS** fail the gate.
- **ALWAYS** run the repository gate for every changed Terraform, Compose, Dockerfile, shell, or workflow file.
- If a change adds an executable language, **ALWAYS** add its formatter, lint or static check, and behavioural test command in the same change.
