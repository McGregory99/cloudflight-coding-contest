# Level 3 - Spaceship (CCC41 Classic)

## Statement
1D. Given a station position and a time limit, output a pace sequence that starts at 0, reaches the
station exactly and ends at 0, within the time limit. Rules of the sequence:
- first and last pace are 0; non-zero paces have `1 <= |p| <= 5`;
- paces change gradually: `-1 <-> -2 <-> ... <-> -5 <-> 0 <-> 5 <-> 4 <-> ... <-> 1`
  (a pace may stay, move one step along that chain, and the only way to change direction is through 0).
The limit is "very generous" (the statement text is hidden behind a shifted font, deciphered as such).
Input: `N`, then `station limit` per line. Output: one pace sequence per line.

## Approach
Model one axis as an automaton. State after a tick = `(pace, ticks_left_in_block)`. A block of pace `p`
lasts `max(1,|p|)` ticks and moves `sign(p)` cells on its last tick. This is the core reused by all later levels.
`build_H` runs a reverse BFS on `(state, remaining distance)` and gives `H[state][d]` = exact minimum ticks to finish
(at distance 0, resting on pace 0) from any state. `greedy_axis` walks down that table, which yields a
time-optimal sequence, so the limit is always met. O(31 * R) table, O(length) per answer.

## Verification
Exact diff with the example (the optimal answers coincide with it) plus `check.py` on every input:
legal progression, first/last 0, final position, total time <= limit.

## Pitfalls
- 0 -> +-5 only; 5 -> 0 only (you cannot go 1 -> 0 directly): stopping from cruise speed 1 needs 2,3,4,5 first.
- Position only changes at the END of a block (matters from level 5 on).
