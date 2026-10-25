# Level 3 - Asteroid Mining

**Statement.** Input: N, per asteroid `W H LIMIT` + grid (outpost `S` anywhere in the top bedrock row). W or H is exactly 3, the other in 3..199.
Output the grid with tunnels `X`: every minable cell is a tunnel or orthogonally adjacent to one; tunnels form one
4-connected set containing the cell directly below `S`; at most LIMIT tunnel cells (the limit is the optimum).
Several answers are valid (the grader validates).

**Approach.** This is a minimum *connected dominating set* of a grid with a forced start cell. Optimal/near-optimal layouts
are combs: a spine plus teeth every 3 lines. I search the family "every column (or, in the transposed orientation, every row) holds
ONE interval of dug cells" (first/last line may be empty; one extra cell is allowed for the outpost):
a DP over lines with state (previous interval, current interval). Candidate intervals are only a handful of
boundary-anchored types ([0,L-1], [1,L-1], spine [1,1], spine [L-2,L-2], [0,L-2], [1,L-2], [0,0] + a few extras).
Transition validity = neighbouring intervals overlap (connected) and every row of the middle line is dominated by itself/neighbours.
Both orientations are tried, the cheaper is built (stops early when the first one already meets the limit).
Complexity: ~12 candidates -> ~12^3 per line, O(W) lines: milliseconds per asteroid; whole large file ~2 s.

**Verification.** `check.py` independently validates every output (shape, bedrock untouched, <= limit, connectivity from outpost, domination). All inputs pass.

**Pitfalls.** `S` column is index-1 of the bordered row. Outpost may sit far from the spine: the extra cell on the top line
that touches the neighbouring tooth line is what makes e.g. 28x15 reach the limit. Output keeps the blank line after every asteroid.
