# Level 3 - Magic Money

## Statement
- Input: like level 1 (`N`, `C`, then `N` coin lines). Every currency contains coin 1.
- Output: for each currency and each amount 1..100, a line `QxV QxV ...` with the fewest coins that sum to the amount (`Q` coins of value `V`). Order within a line is free; several optimal answers exist.

## Approach
Coin-change DP per currency over amounts 1..100 (`dp[a] = min dp[a-c] + 1`), storing one coin per amount and walking back to build the multiset. O(100*C) per currency. Coins are tried ascending with a strict `<`, and lines are printed with the largest coin first; this reproduces the example output byte for byte.

## Pitfalls
- Greedy is wrong for non-canonical coin systems (e.g. 6 with {1,3,4}: greedy 4+1+1 = 3 coins, optimal 3+3 = 2); use DP.
- Exactly `N*100` output lines.
- `check.py` verifies sums and minimality with an independent DP.
