# Level 1 - Spaceship (CCC41 Classic)

## Statement
A movement sequence is a list of paces. A pace `p > 0` takes `p` time units and moves 1 unit of space.
Input: `N`, then `N` lines, each a space separated list of paces.
Output: one line per sequence, the total time.

## Approach
Time of a sequence = sum of its paces. One pass over the numbers, O(total numbers).

## Verification
Exact diff with `out_level-1_0-example.txt` (answer is unique).

## Pitfalls
None really. Just make sure to write one number per line with no trailing spaces.
