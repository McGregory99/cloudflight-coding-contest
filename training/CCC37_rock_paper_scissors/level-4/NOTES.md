# Level 4 - arrange so the final winner is Scissors (3 styles)

**Input**: `N M`, then N lines `aR bP cS`. **Output**: N arrangements of M chars with those counts such that the full tournament (all log2(M) rounds) is won by an S fighter. At least one solution is guaranteed; multiple accepted.

**Approach**: same engine as level 3, but the search runs over all log2(M) rounds on count vectors and the goal is "one fighter left and it is S". Enemies of S (those that beat it: R) are eliminated first by their killers (P), then remaining enemies pair among themselves (halving), friends tie; random restarts / perturbed priorities with DFS + failed-state memo handle tight cases. Plan -> string by bucket materialisation.
Complexity: O(rounds * tries) count operations + O(M log M) string building.

**Verification**: `check.py` simulates the full bracket, validates counts and winner = S. All inputs pass (largest input ~0.6 s). Exhaustive for M=8 and random stress up to M=1024 passed.
**Pitfalls**: example output not byte-identical (multiple answers allowed). The search needs the memo on failed states to avoid exponential retries.
