# Adapters

Own concrete filesystem, database, object-storage, tracking and API implementations when application requirements exist. Depend on domain and ports; do not import application or entrypoints. Keep boundary validation and explicit failure behaviour with the relevant integration. No production ML adapters are implemented yet.

The executable import policy in `quality-policy.toml` is authoritative. This directory establishes responsibility and contains no placeholder Python implementation.
