# CCC39 - Magic Money (School track)

The goblin bank of the wizard world mints its own coin sets. Each level asks a harder
question about paying amounts with those coins: from "what is the first amount a single coin
cannot pay" up to "pay a huge amount with the fewest coins from a limited vault".

All 5 levels passed on the official grader. `explainer.html` is a self-contained animated
walkthrough of every level (open it by double-click).

## Levels

| Level | Problem | Approach | Complexity | Verification |
|---|---|---|---|---|
| 1 | Smallest positive integer that is not a coin value | Coin set, count up from 1 until missing | O(N*C) | Example matches exactly (unique answer) |
| 2 | Two coins (repeats allowed) summing to each amount | Two-sum: scan coins ascending, look up `amount - x` in a set | O(A*C) per currency | `check.py` (pair valid); example matches |
| 3 | Fewest coins for every amount 1..100 (coin 1 present) | Coin-change DP with a parent coin, walk back to build `QxV` lines | O(100*C) per currency | `check.py` (independent DP for minimality); example matches |
| 4 | Fewest coins for amounts up to ~1e9 (coins <= 20) | Above `M*M` an optimum always uses the largest coin `M`: peel `k` copies of `M`, finish from a DP table of size `M*M+M` | O(C*M^2) per currency + O(M^2) per amount | `check.py` (Dijkstra over residues mod `M`); example matches |
| 5 | Fewest coins with a limited inventory per coin type, amounts up to ~3e8 | Exchange argument: at most one "free" type; others are near-full or bounded. Per free-type choice, one small bounded knapsack per currency, then a residue-class lookup per amount | ~7 knapsacks of ~2k states per currency + O(C) per amount | `check.py` (sums, inventory, exact DP for amounts <= 3000); example differs only in tie-breaking (same coin counts) |

Details and pitfalls per level are in `level-N/NOTES.md`.

## Layout

```
level-N/
  statement.pdf   official statement
  input/          in_level-N_*.txt
  expected/       official example output
  output/         generated level-N_*.out (including the example)
  solution.py     reads ./input, writes ./output (works from any cwd)
  check.py        validates ./output against ./input (levels 2-5)
  NOTES.md
outputs/level-N/  submittable .out files (no example), for drag-and-drop upload
run_all.py        runs every solution + checker and prints a pass/fail table
explainer.html    animated explainer
```

## How to run

```bash
python3 run_all.py                 # everything; exits non-zero on any failure
python3 level-4/solution.py        # one level
python3 level-4/check.py           # its checker
```

`run_all.py` requires the example output to match exactly only for level 1 (unique answer);
levels 2-5 accept any valid/optimal answer, so `check.py` decides there. Level 5's example
output intentionally differs from the official one in which equally small coin mix is printed.
After running, refresh `outputs/` with the non-example files from each `level-N/output/`.
