# Level 4 - escape along any path
**I/O:** same as level 3.
**Approach:** flood fill (DFS/BFS) from `W` through `O` cells; `FREE` as soon as a visited cell has one of its 6 neighbour positions outside the grid. O(cells).
**Pitfalls:** "outside" is any out-of-range neighbour position (including the trailing `-` column handled by the +-2 / +-1 geometry). Checker uses union-find with a virtual OUTSIDE node as an independent method.
