# Level 1 - count cells
**I/O:** input is one paragraph of characters (`O` = hex cell, `-` = stagger filler); output the number of cells.
**Approach:** count `'O'` in the whole file. O(size).
**Pitfalls:** the `-` are padding only; one honeycomb per file, no N header at this level.
