# Level 8 - Spaceship (CCC41 Classic)

## Statement
Asteroids move. Input per case: `x,y limit`, `A`, then `A` asteroids `ax,ay,vx,vy` where `vx,vy` are PACES
(`|v| <= 5`, 0 = not moving on that axis): an asteroid with pace `v` moves 1 cell every `|v|` ticks in the direction of
`sign(v)`. Asteroids start moving at tick 1, while the ship still holds the compulsory first pace 0.
Asteroids do not interact with each other. Limit short, not optimal. Output as in level 4.

## Approach
Same search as levels 5-7, with the time in the node key (the map changes every tick, so earlier is not always better).
Asteroid position after `t` ticks = `p0 + sign(v) * (t // |v|)` (the formula used by the official visualizer).
The set of blocked ship cells at tick `t` is built lazily as one bitmask per row and cached per tick. Only asteroids whose
trajectory segment over `[0, limit]` touches the search window are considered (500 asteroids, a handful matter).
Weighted best-first (weight 2) with `h = max(H_x, H_y)` and the prune `g + 1 + h > limit`. The geometric BFS heuristic of
level 7 is not used (the map is not static). Window margin 20 grows if needed (60, 150, 400): never needed on the data.
Runtime 4 s for all inputs, pure Python.

## Verification
`check.py` (official sandbox rules ported; moving asteroids by the closed formula; collision tested at every step
0..len, also while the ship rests) on all inputs: OK. The official example output passes the same checker too.
Used/limit at most 0.99.

## Pitfalls
- The ship's first pace is 0 and takes 1 tick: asteroids already moved 1 cell when the ship can first start.
- Check collision at every tick, not only when the ship moves.
- Parse asteroid lines by tokens (a line can be long; A may make the line empty in other data sets).
