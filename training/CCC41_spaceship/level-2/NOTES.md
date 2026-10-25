# Level 2 - Spaceship (CCC41 Classic)

## Statement
Paces can now be 0 (stand still, costs 1 time unit) or negative (move 1 unit backwards, costs `|p|`).
Input: `N`, then `N` sequences. Output: `final_position time` per sequence (start position 0).

## Approach
`position = sum(sign(p))`, `time = sum(max(1, |p|))`. Linear in the input size.

## Verification
Exact diff with `out_level-2_0-example.txt` (unique answer).

## Pitfalls
- A pace of 0 is NOT free: it takes 1 tick. `max(1, |p|)` is the unit of time of a block, used in every later level.
- The sign of the pace gives the direction, its magnitude the duration.
