# Level 4 - Asteroid Mining

**Statement.** Same I/O as level 3. Width or height divisible by 3, other in 3..199; the limit is optimum + 1 (optimal or 1 worse accepted).

**Approach.** Same solver as level 3 (comb DP over lines with one interval per line + outpost extra cell, both orientations).
It is at or below the limit on every asteroid. See level-3/NOTES.md for details.

**Verification.** `check.py` (same independent validator) passes every input; large file runs in ~3 s.

**Pitfalls.** Nothing new in the format; the slack only makes the task easier, no need for exact optimality.
