# Level 4
**Statement:** Rooms `x y k` (x,y >= 4). Place exactly k = maximum number of 1x3 desks, no two desks touching (diagonals count), walls may be touched. Output grid of `X` / `.`.
**Key idea (territory):** give each desk a 2x(L+1) "territory" (desk + a gap cell at its end + a gap row/col beside it). Two desks do not touch iff their territories are disjoint inside the box of size (x+1) x (y+1) (territories may overhang the right/bottom wall by the gap). So the problem becomes packing 2x(L+1) rectangles (both orientations) into an (x+1)x(y+1) box; each rectangle contributes a desk on its top row (horizontal) or left column (vertical).
**Algorithm:** guillotine DP with homogeneous-block base cases, plus pinwheel (five-block) splits for boxes <= 22 with a small centre (<= 6) only when the area bound is not met (needed for L>=4, e.g. 5x5 box with 2x3 / 7x7). Table built once per L; reconstruction by stored choices.
**Complexity:** ~O(P*Q*(P+Q)) table; whole level runs in ~0.1 s.
**Verification:** `check.py` (every 8-connected X component is a straight line of length exactly L, component count = k, grid shape) passes on all inputs. Example not byte-identical (answer not unique).
**Pitfalls:** diagonal touching; counting must use the (x+1)x(y+1) box, not x*y.
