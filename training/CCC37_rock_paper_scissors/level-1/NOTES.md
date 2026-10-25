# Level 1 - single fights

**Input**: `N`, then N lines with two chars (styles of the two fighters). Styles R/P/S.
**Output**: N lines, the winning style of each fight.

Rules (diagram): rock beats scissors, scissors beats paper, paper beats rock; same style -> that style.

**Approach**: direct lookup `winner(a, b)`. O(N).
**Pitfalls**: the arrows in the diagram point from winner to loser (R->S, S->P, P->R). Verified against the example (exact match).
