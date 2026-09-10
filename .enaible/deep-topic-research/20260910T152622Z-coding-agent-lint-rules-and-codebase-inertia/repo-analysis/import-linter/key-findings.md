# Source inspection findings

Question coverage: q2 and q5.

At commit 31927f1457e3df673912cb5efb0afa6dbc37585f, the acyclic sibling contract implementation owns graph-cycle checks in src/importlinter/contracts/acyclic_siblings.py:36-214. Its check method delegates cycle-breaker nomination to Grimp and returns a kept/broken contract result; lines110-154 drill into descendant packages. The documented depth controls drilldown, not whether deeply located edges contribute to parent cycles.

The layers implementation in src/importlinter/contracts/layers.py:130-181 combines illegal dependency detection and undeclared-module detection. Exhaustiveness requires containers; supplying exhaustive without containers is rejected. This matters because adding the tool must not silently adopt a more permissive generic layering contract than Podium currently permits.

The local isolated research fixture showed that two mutually importing modules within one permitted Podium layer receive zero findings from the current per-file architecture checker, while Import Linter2.15 fails its acyclic sibling contract; removing the cycle makes the same contract pass. This is a synthetic coverage probe, not a discovered cycle in Podium. Results and complete fixture text are in ../../baseline/rule-probes.json.

Analyzers: CodeGraph index and symbol queries; Python AST counts/hashes for the inspected implementation files; official released Import Linter on an isolated authored fixture. The upstream source checkout itself was not installed or executed. Metadata and file hashes are retained in metadata.json.
