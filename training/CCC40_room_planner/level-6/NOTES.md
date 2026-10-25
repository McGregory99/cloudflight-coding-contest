# Level 6
**Statement:** Rooms `x y k L` with L in 1..7: place k = maximum number of non-touching 1xL desks. Output X/. grid.
**Approach:** same territory reduction (2x(L+1) rectangles in the (x+1)x(y+1) box), guillotine + pinwheel DP, one table per distinct L (cached). L=1 is single cells (2x2 territories).
**Complexity:** a few tables of ~1M steps; ~0.4 s for the whole level.
**Verification:** `check.py` (components straight with length L, count = k) passes on all inputs.
**Pitfalls:** large L (6,7) needs pinwheel blocks with centres up to 5x1 / 3x3 / 4x2 for the optimum; pinwheel search is restricted to boxes <= 22 (larger boxes decompose via guillotine cuts into such blocks) - validated against all given maxima, but not proven for arbitrary inputs.
