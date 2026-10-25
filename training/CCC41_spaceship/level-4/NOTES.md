# Level 4 - Spaceship (CCC41 Classic)

## Statement
2D. Station `x,y`, time limit that requires an OPTIMAL solution. Output one pace sequence for X and one for Y
(both obey the level 3 rules; they may have different durations, the shorter one is padded with 0 at the end).
Input: `N`, then `x,y limit` per line. Output: X line, Y line, blank line (blank line optional), per case.

## Approach
The axes are independent, so the optimum is the maximum of the two 1D optima. Reuse the level 3 automaton and
the exact table `H` (reverse BFS), walk it greedily for each axis. The limit equals `1 + max(H)` in every case.
O(31 * R) preprocessing, O(answer) per case.

## Verification
Exact diff with the example output (matches byte for byte) and `check.py` (a port of the rules of the official
sandbox/visualizer, written as a tick simulator) on every input: all OK. Runtime 0.15 s.

## Pitfalls
- Total time of an axis = sum of `max(1,|p|)` including the leading and trailing 0 blocks (1 tick each).
- The axis with distance 0 is just `0`.
- The X and Y lines may differ in length; do not pad them yourself (the checker pads with trailing 0s).
