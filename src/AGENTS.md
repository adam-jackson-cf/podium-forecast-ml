# Source instructions

- **NEVER** perform filesystem, environment, database, network, or AWS IO in `domain`, `ports`, or `application`.
- **ALWAYS** implement concrete IO in `adapters` and runtime assembly in `entrypoints`.
- **NEVER** import `adapters` or `entrypoints` from `domain`, `ports`, or `application`.
- If target, forecast cut-off, schema, or approval rules are missing, **NEVER** implement dependent domain behaviour; identify the missing rule.
