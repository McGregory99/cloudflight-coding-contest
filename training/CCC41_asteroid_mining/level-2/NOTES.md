# Level 2 - Asteroid Mining

**Statement.** Input: N, then per asteroid `W H` (W is always 3) and its character grid (bedrock `#`, minable `:`, outpost `S`
in the middle of the first row), blank line between asteroids. Output: the same grid with a tunnel `X` dug straight down
from the cell below `S` to the last minable row (before the bottom bedrock). Unique answer.

**Approach.** Find column of `S`, replace that column by `X` in rows 1..H. O(cells).

**Pitfalls.** Input grids now contain the outpost row, header `W H` is glued to the grid, blank line after each grid (output too, including the last).
Verified: exact diff with the example, `check.py` rebuilds the expected grid for every input.
