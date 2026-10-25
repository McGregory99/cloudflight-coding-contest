# Level 2 - bounding box

**I/O**: same input as L1. Output per path: width and height of the smallest rectangle containing the walk (start included).

**Approach**: simulate with x/y (W=y-1, S=y+1, D=x+1, A=x-1), track min/max, size = max-min+1 (cells, not steps). O(length).

**Pitfalls**: +1 (cells vs. moves); width first, then height. Exact diff with the example.
