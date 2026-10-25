# Level 3 - vertical flight with soft landing

**Input:** N, time limit T (shared by all flights), then N minimum heights H. **Output:** per flight one line of accelerations
(0..20) from take-off until landing. Dynamics as level 2. Landing = height reaches exactly 0 with velocity -1 or 0, drone must
reach H first, must not touch ground after the first tick, sequence ends at landing, <= T ticks. Many answers are valid, so
`check.py` simulates all rules on every flight (the official example output also passes it).

**Key reformulation:** with `dv = a - 10` in [-10, 10] the vertical flight is a velocity profile with |dv| <= 10 per tick.
 * Ascent: speeds s_1..s_n >= 0 (s_0 = 0), sum = H, then a final 0 (apex, hover state vy = 0).
 * Descent from hover: speeds u_i (vy = -u_i) with sum = R and last speed exactly 1 (landing at height 1 -> 0 with vy = -1).
   Built as `rt(R-1)` followed by a final tick with speed 1 (|s_n - 1| <= 9 always holds).
 * `rt(S)`: greedy "accelerate as fast as possible, but keep a feasible braking tail": next speed is the largest u' in
   [u-10, u+10] with `R - u' >= smin(u')`, where `smin(u)` is the sum of the braking ramp u-10, u-20, ... (closed form).
   Binary search on u' (monotone). Tested exhaustively for S < 3000 and randomly up to 1e6: always exact.
 * Result is near time-optimal (triangular profile): ~ 4*sqrt(H/10) ticks, far below the limit (worst 16% of it).

**Complexity:** O(ticks * log) per flight. **Pitfalls:** exact (not >=) sum for the descent; the apex must have vy = 0 so that
the second phase can start from a clean hover; the first tick must already take off.
