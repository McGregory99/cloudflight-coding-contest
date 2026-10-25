# Level 4 - add horizontal motion

**Input:** N, then per flight `x_pad  min_height  time_limit`. **Output:** per flight a line of `ax,ay` vectors.
x and y evolve independently (gravity only in y), |ax| + ay <= 20, ay >= 0. Landing: height 0 exactly at x_pad with vy in {-1,0}
and vx = 0; reach min_height at least once; take off at tick 1; no ground contact except the landing; <= time limit.
Many answers valid -> `check.py` simulates every rule (official example output passes it too).

**Approach (three phases, reuse of level 3):**
1. vertical ascent to apex height H = max(min_height, 1) with vy = 0 (`ascent`);
2. horizontal move at hover: `ay = 10` keeps vy = 0 and leaves `|ax| <= 10`, so the horizontal velocity is again a profile with
   |dvx| <= 10; reuse `rt(|x_pad|)` from rest to rest, sign = direction (`horizontal`);
3. vertical descent from hover (`descent`).
Total time ~ vertical 4*sqrt(H/10) + horizontal 2*sqrt(|x|/10); worst case uses 75% of the time limit (checked on all inputs).

**Pitfalls:** acceleration budget is the SUM |ax|+ay (no Pythagoras), so hovering leaves only 10 for ax; pad never at x = 0.
