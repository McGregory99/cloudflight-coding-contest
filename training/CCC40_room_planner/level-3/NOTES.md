# Level 3
**Statement:** Rooms `x y k`, x no longer divisible by 3. Place k = maximum number of 1x3 desks (either orientation, touching allowed). Output ID matrix, 0 = empty cell, IDs 1..k.
**Approach:** guillotine DP over all sub-rectangles: f[p][q] = max(all horizontal, all vertical, best horizontal/vertical cut). Table built once up to the largest room, solutions reconstructed from stored choices. Result equals the given k for every room in all inputs (so guillotine packings are optimal here, e.g. 4x4 -> 5 desks via a 3x4 block + a 1x4 column).
**Complexity:** O(P*Q*(P+Q)) table once (~1M steps for 100x100), O(x*y) per room.
**Verification:** `check.py` (ids 1..k, each exactly 3 straight contiguous cells, zeros elsewhere) passes on all inputs.
**Pitfalls:** desks may be rotated (example has a vertical desk); k is the true optimum so a naive "floor(area/3)" is not always achievable in general, DP handles it.
