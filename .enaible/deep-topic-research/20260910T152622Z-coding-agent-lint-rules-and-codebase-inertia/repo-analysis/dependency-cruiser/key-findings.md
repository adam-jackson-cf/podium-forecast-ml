# Source inspection findings

Question coverage: q1 and q5.

At commit 2aa2e34ed8ff8a074588e21603c4fafc0edf6170, src/analyze/derive/circular.mjs:24-45 attaches explicit cycle evidence to a dependency; the graph lookup returns a cycle path. This supports diagnostics that show the dependency path, rather than just naming an offending import.

The source reference doc/rules-reference.md:485-529 distinguishes orphan modules from ordinary entrypoints and warns that starting only at one entrypoint misses unvisited orphan files. Lines531 onward describe reachability from declared roots, a stronger model for dead subgraphs. Lines1224 onward define dependency instability and explicitly caution that it is a metric rather than a universal quality judgment; entrypoints can legitimately score differently from shared modules.

Transfer to Python: build a whole maintained-source graph, declare valid runtime/CLI/plugin/test roots, then use dependency paths and unreachable-subgraph evidence. Do not install the JavaScript tool in the Python project merely to obtain this conceptual design. No Node dependencies or upstream test suite were executed. CodeGraph symbol indexing plus targeted implementation/document inspection and file hashing formed the source analysis.

Upstream ignore-known and suppression examples are not recommendations for this repository. Preserving existing violations behind ignored-baseline files would conflict with its current gate policy.
