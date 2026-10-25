# Level 5 - Rock-Paper-Scissors-Spock-Lizard, final winner Scissors

**Input**: `N M`, then N lines `aR bP cS dY eL` (Y = Spock, L = Lizard). **Output**: N arrangements (M chars) such that the final winner is S. Guaranteed solvable, multiple answers accepted.

Beats (from the quote): S>P, P>R, R>L, L>Y, Y>S, S>L, L>P, P>Y, Y>R, R>S (each style beats two and loses to two; S loses to R and Y).

**Approach**: the level-4 count-vector search generalised to 5 styles (15 pair types). Heuristic first: friends of S kill enemies (R, Y), enemy vs enemy, enemy halving, then friendly ties; then perturbed random priority orders with random take-fractions, DFS over rounds, failed-state memo, escalating number of tries. Strings are materialised from the chosen plan.
Complexity: search is cheap for typical inputs; the extremely skewed large cases (e.g. 4046 R with a handful of others) need many tries (~2.5 s). Largest input total runtime ~3-4 s.

**Verification**: `check.py` simulates the bracket with the 5-style relation. All inputs pass; exhaustive for M=8 (all 213 feasible vectors) and random stress up to M=4096.
**Pitfalls**: the diagram arrows are easy to misread - the quote in the statement is the reliable source. Output is not identical to the example (multiple answers allowed).
