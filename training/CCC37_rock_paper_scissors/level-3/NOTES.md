# Level 3 - arrange first round so no Rock survives 2 rounds

**Input**: `N M`, then N lines `aR bP cS` (counts per style, sum = M, M a power of two).
**Output**: N lines, a first-round arrangement (string of M chars with exactly those counts) such that after two rounds there are no R fighters and at least one S. Multiple answers are accepted; a solution is guaranteed to exist.

**Approach**: only the multiset of styles matters per round, because we can choose the order of every pair and of the winners. Search round by round on count vectors `(r,p,s)`: a round is a matching described by how many pairs of each type (RR, RP, ..., PS) are formed; the next count vector follows from who wins. The search tries a heuristic matching first (let P kill R, pair enemies together, keep S alive) and then randomised perturbations (random pair-type priority order and random fractions), with DFS over rounds and a memo of failed states. After a plan is found, the string is materialised by popping fighters from per-style buckets round by round and concatenating the pair sequences (winner of each pair becomes a node whose sequence is `left+right`).
Complexity: search is tiny (2 rounds); materialisation O(M) per tournament.

**Verification**: `check.py` simulates two rounds and checks counts, no R, at least one S. All inputs pass; exhaustive check of all feasible count vectors for M=8 and random stress for M up to 4096 passed.
**Pitfalls**: the example output differs from ours (any valid answer is accepted by the statement); output lines must contain exactly the given counts.
