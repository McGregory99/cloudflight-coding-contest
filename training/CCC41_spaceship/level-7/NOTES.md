# Level 7 - Spaceship (CCC41 Classic)

## Statement
Level 6 with several stationary asteroids (up to 5000 per case, coordinates up to +-400, goals up to 331 away).
Input per case: `x,y limit`, `A`, then a line with `A` asteroids `ax,ay`. Output as in level 4.
The limit is short but not optimal.

## What the data looks like
The large file is a dense maze: ~50% of the bounding box between start and goal is blocked (each asteroid
forbids a 5x5 square of ship positions) and the king-move shortest path is often 1.5 - 2x the Chebyshev distance.
The limits are about 1.2 - 1.8x the true optimum (measured with an exact search on small cases), so the plan must be
near-optimal in time, not just collision free.

## Approach
Same weighted best-first search as levels 5/6 (nodes = `(x, y, state_x, state_y)`, one step = one tick,
heuristic `max(H_x, H_y, GD)`, prune `g+1+h > limit`, per-axis pace automaton), with two changes:
- a window margin of 120 around the start/goal box (mazes need detours; margin 250/400 as fallbacks),
- the search is written in C (embedded in `solution.py`, compiled at start with `cc -O2 -shared`, called via
  `ctypes`) because the hardest cases need 1 - 10 million node expansions (pure Python does ~0.25 M/s, C ~4 M/s).
  Weight 2.0 first with an expansion budget, then other weights/margins (a big weight can explode: 100 M+ expansions).
- cases are solved in parallel with `multiprocessing` (biggest limits first).
If `cc` is missing, the identical Python search is used (about 2 s per large case, 500 cases: minutes).
Cost: 65 s of CPU for the large file (about 10 - 20 s wall on 8 cores; the machine was heavily loaded while measuring).

## Verification
`check.py` (sandbox rules ported, set-based collision test) on every input: OK. Pure Python fallback verified
on the small file.

## Pitfalls
- A limit-sized solution is accepted (used/limit reaches exactly 1.0 on a few cases).
- Large weights make A* faster on average but with catastrophic tails (up to 200 M expansions): use weight ~2 and
  an expansion budget per rung.
- The window must be big enough for the maze; the geometric BFS distance changes a lot between margin 30 and 120.
- Memory: 12 M nodes cap per process (about 200 MB).
