# CCC37 - Rock Paper Scissors (Classic track)

Fighters in a knockout tournament each know one style; every bout is decided by
Rock-Paper-Scissors (later Rock-Paper-Scissors-Spock-Lizard). Over seven levels the
task grows from "who wins this bout?" to "rig the bracket so Scissors is champion,
even against an adversary".

Open `explainer.html` in a browser for an animated, step-by-step walkthrough of every
level (each animation runs a JavaScript port of the level's `solution.py` on the
example input; the port reproduces all 42 generated `.out` files byte for byte).

## Levels

| Level | Problem | Approach | Complexity | Verification |
|---|---|---|---|---|
| 1 | Winner of single R/P/S bouts | Lookup table `BEATS = {R:S, S:P, P:R}` | O(N) | Example matches exactly |
| 2 | Survivors after the first two bracket rounds | Simulate `play_round` twice | O(N*M) | Example matches exactly |
| 3 | Arrange given R/P/S counts so no Rock survives 2 rounds (and some S does) | DFS over rounds on count vectors; a round = a matching of pair types (heuristic first, then seeded random perturbations), memo of dead states; materialise the plan by nesting pairs into blocks | Tiny search + O(M) | `check.py` (many valid answers; example differs by design) |
| 4 | Arrange R/P/S counts so Scissors wins the full tournament | Same engine over all log2(M) rounds, goal "one S left"; budget doubling restarts | O(rounds*tries) + O(M log M) | `check.py` (example differs by design) |
| 5 | Same with Spock (Y) and Lizard (L) | Engine generalised to 5 styles / 15 pair types | Up to ~3-4 s for the level | `check.py` (example differs by design) |
| 6 | Fill free `X` spots so Scissors wins | Bottom-up DP on the bracket: each node keeps inclusion-minimal possible-winner sets (bitmasks); reconstruct from root `{S}`; X tie-break S,R,P,Y,L | O(M*A^2), A <= 10 | `check.py` (example differs by design) |
| 7 | Fill `X` so Scissors wins for every filling of adversarial `Z` spots | Same DP with Z leaves = full set {R,P,S,Y,L} (exists X, for all Z) | Same as level 6 | `check.py` + example matches exactly |

Per-level details and pitfalls are in each `level-N/NOTES.md`.

## Layout

```
level-N/
  statement.pdf   original statement
  input/          in_level-N_*.txt
  expected/       official example output
  output/         generated level-N_*.out (including the example)
  solution.py     reads ./input, writes ./output (paths relative to the script)
  check.py        levels 3-7: validates ./output against ./input
  NOTES.md
outputs/level-N/  submittable .out files (no example), ready for upload
explainer.html    animated explainer
run_all.py        runs everything and prints a pass/fail table
```

## How to run

```
python3 run_all.py              # all levels: solution + example/check, non-zero exit on failure
python3 level-4/solution.py     # one level (works from any cwd)
python3 level-4/check.py
```

Levels 1, 2 and 7 have a unique answer for the example and are diffed against
`expected/`; levels 3-6 accept many valid answers and are validated by `check.py`.
