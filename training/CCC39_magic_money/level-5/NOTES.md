# Level 5 - Magic Money

## Statement
- Input: `N`, `C`, `A` (global), then per currency an inventory line of `C` items `QxV` (Q coins of value V, e.g. `100x1`) and a line of `A` amounts (up to ~3e8).
- Output: per amount, a line `QxV ...` with the fewest coins not exceeding the inventory. Amounts do not consume inventory for each other. Any optimal answer is accepted; all amounts are assumed buildable.

## Approach
Plain DP over the amount is too big. Key exchange argument (types sorted by value, `Vmax` = largest value): if `a < b`, `x_a >= v_b` and `x_b + v_a <= u_b`, swapping `v_b` coins of `a` for `v_a` coins of `b` saves coins. So in an optimum, for every type `b` that is not nearly saturated (`u_b - x_b >= Vmax`), all smaller types are used `< v_b` times. Take `j` = largest value type that is not nearly saturated (or none). Then:
- types above `j`: `x = u - d` with `d < Vmax`;
- types below `j`: `x < v_j`;
- type `j` takes whatever remains (determined by the amount).
For each choice of `j` (plus "none") build once per currency a small bounded-knapsack `g[s]` = fewest extra coins for extra sum `s` (sizes ~ 1-2k). For an amount, only `s` with `(R-s) % v_j == 0` and `0 <= (R-s)/v_j <= u_j` is valid; minimizing `v_j*g[s] - s` per residue class (pre-sorted) gives the answer by scanning the first feasible entry. Backtrack through the stored DP layers to reconstruct the coin counts.
Complexity: about 7 knapsacks of ~2k states x ~20 choices per type per currency, then ~O(C) lookups per amount. Runtime ~2 s for the large files (both large inputs ~3.7 s total).

## Pitfalls
- Format `QxV` is count first, value second in both input and output.
- The free type can be anything, so all `j` have to be tried; keep `j` count within `[0, u_j]`.
- Verified against an exact bounded-knapsack brute force on ~800k small random instances (0 mismatches). `check.py` validates sums, inventory limits, and optimality for small amounts; for big amounts it validates feasibility only.
- Example output differs from ours but has equal coin counts (multiple optima are allowed).
