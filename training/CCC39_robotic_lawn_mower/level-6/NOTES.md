# Level 6 - Hamiltonian cycle, one tree

**I/O**: same as L5, but the end cell must be a (4-neighbour; diagonals do not count - hidden shifted text on the slide) neighbour of the start cell, i.e. the path closes into a Hamiltonian cycle (closing move not written). One tree, anywhere; start free.

**Approach**: same `lawn.py`, mode "cycle": every vertex degree 2 -> 2-factor by max-flow (needs |black|=|white|, guaranteed by solvability), merge cycles via 2x2 flips until one cycle, then cut it at any cell and walk it. Output the N-1 moves.

**Verification**: `check.py` checks coverage/no repeats/stays inside lawn/tree-free AND |start-end| = 1 Manhattan; all inputs OK, ~2 s total (large 97x77 included).

**Pitfalls**: slide text partly garbled (shifted-ASCII overlay says diagonals don't count); path has N-1 moves for N free cells.
