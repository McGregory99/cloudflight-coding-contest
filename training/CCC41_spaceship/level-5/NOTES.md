# Level 5 - Spaceship (CCC41 Classic)

## Statement
Same as level 4 plus ONE stationary asteroid. Ship and asteroid have size 1; the ship has a square safety area of
radius 2, so a collision happens iff `|dx| <= 2 and |dy| <= 2` between ship and asteroid at some tick (including
tick 0 and the final tick). The time limit is very generous. Input: `N`, then per case `x,y limit` and `ax,ay`.
Output as in level 4. Multiple answers are valid (the grader validates).

## Approach
Joint best-first search over `(x, y, state_x, state_y)` with the per-axis automaton of level 3 (one search node per tick).
- Heuristic `h = max(H_x, H_y, GD)`: `H` is the exact free-space axis table, `GD` a king-move BFS distance to the goal
  over non-blocked cells (a ship moves at most 1 cell per axis per tick, so it is a lower bound).
- Prune any node with `g + 1 + h > limit`: it can never finish in time, so the search is complete inside its window
  whatever the weight (weight 2 only changes the visiting order).
- Static map: a node dominates a later arrival at the same `(x,y,state_x,state_y)`. Blocked cells are stored as one
  big-int bitmask per row.
- Search window = bounding box of start/goal plus a margin; the margin grows (20, 60, 150, 400) if the window is too small.
Runtime 8 s for all inputs (mostly the BFS of the heuristic; the search itself is instant here).

## Verification
`check.py` (port of the sandbox rules: pace validity, padding, limit, exact final position, resting at the end,
collision at every step 0..len) on all inputs: OK. The official example outputs also pass the same checker.

## Pitfalls
- Collision is also checked while the ship stands still (asteroids move in level 8) and at step 0.
- The position changes on the LAST tick of a block, not the first.
- The ship must be at rest (pace 0) on the station.
