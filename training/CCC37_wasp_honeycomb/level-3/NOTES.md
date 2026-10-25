# Level 3 - straight-line escape
**I/O:** same as level 2; output `FREE` / `TRAPPED` per honeycomb.
**Approach:** for each of the 6 directions walk from `W` in a straight line; if every cell passed is `O` until the walk leaves the grid -> `FREE`. O(6*size).
**Pitfalls:** reaching an edge cell is not escaping; the line must continue out of the grid (statement example 2). Stepping onto `X` stops that direction.
