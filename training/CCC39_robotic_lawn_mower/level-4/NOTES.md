# Level 4 - Hamiltonian path, one interior tree

**I/O**: N lawns (W H, H rows of ./X), lawn >= 4x4, one tree not on the edge. Output a move string (W/D/S/A) that visits every free cell exactly once; start/end free. Multiple answers accepted (grader validates). Start cell is not output: it is implied because the walk covers all free cells.

**Approach** (shared `lawn.py`, same code for L4-L7):
1. Colour cells like a chessboard. A path with free endpoints: degree 2 everywhere except two endpoints of degree 1. Endpoint colours follow from the colour counts (majority colour twice if |B|=|W|+1, one each if equal). Random endpoints are tried.
2. Find a "2-factor-like" edge set with those degrees as a max-flow (S -> black cells -> white neighbours (cap 1) -> T, vertex capacity = wanted degree), Dinic. Result: one path plus disjoint cycles.
3. Merge components with 2x2 flips: if edges a-b and c-d are parallel in one unit square and in different components, replace them by a-c, b-d (degrees unchanged, components fuse). When no merge is possible, apply a few random flips (may split) and retry. Restart with new endpoints/flow if stuck.
Complexity about O(n * sqrt n) for flow + near-linear merge passes; all inputs in 1-2 s.

**Verification**: `check.py` re-simulates every path (offset search for the start) - all inputs OK. Not an exact diff (multiple answers).

**Pitfalls**: path gives no start; bipartite colour parity decides which endpoints are possible; heuristic is not a proof (restarts with different seeds).
