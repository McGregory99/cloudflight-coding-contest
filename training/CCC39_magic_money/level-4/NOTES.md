# Level 4 - Magic Money

## Statement
- Input: `N`, `C`, `A` (global), then per currency a line of `C` coins and a line of `A` amounts (amounts up to ~1e9, coins <= 20, coin 1 present).
- Output: per amount, a line `QxV ...` using the fewest coins (unlimited supply). Any optimal answer is accepted.

## Approach
Let `M` be the largest coin. Any multiset of `M` or more smaller coins contains a subset whose sum is a multiple of `M`, which can be replaced by no more large coins. Hence an optimal solution for `x >= M*M` always contains an `M` coin, so `f(x) = f(x-M) + 1`.
- Build a DP table up to `M*M + M` once per currency (with a parent coin).
- For a big amount subtract `k` copies of `M` so the rest lands in `[M*M, M*M+M)`, read the rest from the table, add `k` to the `M` count.
Complexity: O(C*M^2) per currency + O(M^2) per amount (reconstruction), independent of the amount size.

## Pitfalls
- Never loop over the amount (1e9) or build a table that large.
- Use ints only; counts reach tens of millions.
- `check.py` verifies optimality independently with Dijkstra over residues mod `M` (edge weight `M-c`).
