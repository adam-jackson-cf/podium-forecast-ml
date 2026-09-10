# Verification toolchain

Use Python 3.12 and uv 0.10.0, then run from the repository root:

```sh
uv sync --frozen
uv run --frozen python scripts/bootstrap_tools.py
export PATH="$PWD/.tools/bin:$PATH"
```

The committed `tools.lock.json` pins Terraform, TFLint, Trivy, actionlint,
ShellCheck, Hadolint and Gitleaks for macOS Apple Silicon and Linux x86-64.
Python quality tools are pinned separately by `pyproject.toml` and `uv.lock`.
Other operating systems and architectures fail explicitly.

The bootstrap downloads official versioned release artifacts, verifies their
SHA256 against the committed manifest, and installs only the named binary.
Archive members are read directly; archive paths are never extracted. Existing
cached downloads are verified on every run, allowing a subsequent offline run.
A checksum mismatch fails without replacing an existing installed executable;
inspect and explicitly remove the corrupt cache artifact before retrying.
The bootstrap does not execute downloaded programs. Fast checks execute them.

`.tools/bin` and `.tools/downloads` are local ignored outputs. Each download
uses an HTTPS connection with a 30-second socket timeout, a bounded response
size and a bounded redirect count. Release updates require reviewing official
release assets, updating both platform entries and checksums, rerunning the
bootstrap and verification, and retaining the manifest change in review.

Checksum provenance: Terraform hashes were taken from HashiCorp's official
`terraform_1.14.7_SHA256SUMS`; other hashes were taken from the SHA256 digest
fields of the respective official GitHub tagged-release asset APIs. Checksums
establish artifact identity against the reviewed lock; signature verification
is not implemented by this bootstrap.
