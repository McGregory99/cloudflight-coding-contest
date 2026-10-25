# Level 5 - Asteroid Mining

**Statement.** Same I/O as level 3, now both W and H in 3..199 and the limit requires an optimal solution
(i.e. minimum connected dominating set of the grid containing the cell below the outpost).

**Approach.** Same solver as levels 3/4. Exact profile DP is impossible at 199x199, but optimal layouts are combs with the spine on a
boundary-adjacent line; searching "one interval per line" layouts (+ empty end lines + extra outpost cell) in both orientations
reproduced the given limit on all 220 asteroids of the small/large files (one case is even 1 below the limit, 7x124: an exact
profile DP gave 332 and the limit is 333, so the limits come from a comb-like reference, not a proven optimum).
How the candidate set was found: unrestricted version of the DP (every interval) -> looked at which intervals the optimal
solutions use -> kept only boundary anchored types, then pruned greedily while all limits still held.

**Complexity.** ~12 interval types, O(types^3) per line, O(W) lines: ~10 ms per big asteroid, ~3 s for the 200-asteroid file.

**Verification.** `check.py`: shape, bedrock untouched, <= limit, 4-connectivity from the outpost cell, every cell discovered. All inputs pass.

**Doubts.** The family is a heuristic: it is not proven optimal for every possible (W,H,S). If a hidden input fails, enlarge SPECS
(core candidates) or add multi-segment lines; verify against an exact profile DP for narrow rectangles.

**Pitfalls.** Don't trust "dig limit = optimum" blindly: limits can be above the true optimum. Spine near the boundary (row 1 or L-2)
saves one cell per tooth because the spine dominates the boundary row. The outpost column may need a detour cell.
