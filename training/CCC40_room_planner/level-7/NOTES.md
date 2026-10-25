# Level 7
**Statement:** Rooms `x y k`: desks of any length 1..7 (mixed, 1 cell wide, non-touching). Cover exactly k cells (the maximum possible). Output X/. grid.
**Approach:** territory reduction: a desk of length l owns a 2x(l+1) block, worth l cells. Maximise the total value of disjoint 2xm (m=2..8, any orientation) blocks in the (x+1)x(y+1) box: guillotine DP (empty strips allowed, value 0) with leaf blocks 2xm worth m-1, plus pinwheel splits for boxes <= 22 when below an area-based upper bound (area/2 - ceil(area/16)).
**Complexity:** O(P*Q*(P+Q)) once; ~0.1 s total.
**Verification:** `check.py` (components straight, length 1..7, total X cells = k) passes on all inputs.
**Pitfalls:** statement says "matrix of integers" but the example uses X/.; adjacent collinear desks would merge into one longer desk (must stay <= 7), the territory construction never produces touching desks. Pinwheel bounds validated empirically against the given maxima only.
