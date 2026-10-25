# Level 6 - Spaceship (CCC41 Classic)

## Statement
Level 5 with a much shorter time limit (no optimal solution required). Same input/output format.
Used/limit in our answers: at most 0.90.

## Approach
Same solver as level 5 (`solve_case`): weighted best-first search (weight 2) over `(x, y, state_x, state_y)` with the
exact lower bound `max(H_x, H_y, GD)` and the prune `g + 1 + h > limit`. Because of that prune the search only returns
plans that fit in the limit; the weight just decides how greedy the exploration is. With one asteroid the free
straight plan is almost always possible with a small side step, so the search finishes in a few hundred nodes.
Runtime about 8 s for the 1000 + 20 cases (single process).

## Verification
`check.py` (rules of the official sandbox ported to Python) on every input: OK. Examples of the statement pass too.

## Pitfalls
- A detour costs ramp time: changing the direction of an axis needs a stop (pace 0), so the cheap detour is to move
  the other axis away early and come back late (the example outputs do exactly that).
- Equality `time == limit` is valid.
