# Level 2 - Magic Money

## Statement
- Input: `N`, `C`, `A` (global, on lines 1-3), then for each currency a line of `C` coin values and a line of `A` amounts.
- Output: per amount, two coin values (space separated) that sum to the amount. The same coin may be used twice. Every amount is solvable; any valid pair is accepted.

## Approach
Classic two-sum: coins in a set; for each amount scan coins ascending and take the first `x` with `amount - x` also a coin. O(A*C) per currency. Smaller coin is printed first, which also reproduces the example output exactly.

## Pitfalls
- `C` and `A` are given once at the top, not per currency.
- `x == amount - x` is allowed (e.g. `2 2`), which a set lookup handles naturally.
- `check.py` validates any output (pair sums to the amount, coins exist).
