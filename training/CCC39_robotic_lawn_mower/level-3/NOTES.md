# Level 3 - path validity

**I/O**: N lawns: 'W H', H rows of '.' (free) / 'X' (tree), then a path string. Output VALID/INVALID per lawn.

**Rules**: visit every free cell, no cell twice, never the tree, never leave the lawn.

**Approach**: the path gives NO start cell (the dot in the pictures is just its start). Since cells visited = free count and no repeats, validity means: exists an offset where the whole relative walk lies on free cells. Check count == free cells and distinct, then try all offsets in the bounding-box slack (few when the count equals the free cells). O(len * offsets).

**Pitfalls**: start position is unknown (must be inferred); example output matches exactly (VALID only for the last lawn).
