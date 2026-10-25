# Level 6 - silent zones

**Input:** as level 5 plus, per flight, S zones `left right` (closed x-intervals, unlimited height). In a zone the drone must not
accelerate, i.e. the acceleration vector must be (0,0) (free fall, constant vx). Start and pad are never inside a zone.
The official example output shows the rule is evaluated on the position where the tick STARTS (a tick that starts outside and ends
inside may still accelerate); my planner is stricter (no thrust on any tick whose segment touches a zone), `check.py` uses the
official rule. Many answers valid -> checker on all inputs (official example passes it).

**Approach**
* Flights with no zone in the corridor: level-5 baseline (fly above, cross, land).
* Otherwise (mirror so that x_pad > 0, negate ax at the end):
  1. *Horizontal schedule*: ramp up to a constant cruise speed V (+10 per tick), cruise, brake after the last zone, stop at P
     (may overshoot the pad as long as P stays before the next zone beyond the pad), then a rest-to-rest correction `rt(|X-P|)`.
     Conditions: ramp-up ends before the first zone, braking starts after the last zone. All V are enumerated (analytic checks only),
     the 6 cheapest candidates are tried. Zones near the pad (windows of ~2000 units) simply force a smaller V.
  2. *Vertical plan given the schedule* (the key step). Each tick gives a budget: forced free fall (dvy = -10) while touching a
     zone, otherwise dvy in [-10, 10-|ax|]; barrier: y >= 1 + highest building overlapped by the tick's segment (+ margin). Goal:
     end the horizontal part at vy = 0 (hover), then land with the level-3 descent. The set of viable (vy, y) states is convex,
     so the backward value `L_t(vy)` = minimal altitude that keeps the future feasible is a convex piecewise-linear function;
     one backward sweep (shift left/right parts by dmax/dmin, subtract v, clip with the barrier) gives all L_t in
     O(ticks * breakpoints). The same sweep, extended over extra idle ticks at the start, finds the smallest number of
     take-off ticks. Forward pass: at each tick take the lowest integer vy' with `y + vy' >= L_{t+1}(vy')`;
     the barrier gets a margin (3, then 40, 400) to absorb integer rounding.
  This automatically produces the "boost up, free-fall arc over the zone, brake" manoeuvres.
* Result: all flights within the limit (worst 86% of it), whole input set runs in ~5 s (pure stdlib).

**Pitfalls:** zero acceleration in a zone means free fall (ay = 0), not hover; speed is constant while crossing, so zones close to the
pad cap the cruise speed (braking distance ~V^2/20); stopping after the pad and returning is allowed; ground-landing pad and
roof pad are both handled by `descent(y_T - pad_y)`; never trust a single interpretation of the zone rule (verified with the example).
