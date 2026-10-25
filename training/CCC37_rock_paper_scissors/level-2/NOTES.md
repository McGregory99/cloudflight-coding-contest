# Level 2 - first two rounds of a tournament

**Input**: `N M`, then N lines with M chars (first-round order, M a power of two). Adjacent fighters (0-1, 2-3, ...) fight; winners keep their order and fight again.
**Output**: N lines with the M/4 styles still alive after two rounds, in bracket order.

**Approach**: simulate two rounds with the level-1 `winner`. O(N*M).
**Pitfalls**: keep winners in bracket order; ties keep the common style. Exact match with the example. (Guard added for M < 4.)
