# Source scope

Load `.agents/skills/python-conventions/SKILL.md` from the repository root for Python changes. Domain, ports and application use the standard library and permitted internal dependencies only. Keep concrete IO in adapters and assembly in entrypoints; adapters retain responsibility for effectful operations even when static checks cannot follow object aliases, dataflow or dynamic dispatch. The executable layer policy remains canonical, and the package-cycle check supplements rather than replaces it. Do not implement target, cut-off or approval rules from guesses.
