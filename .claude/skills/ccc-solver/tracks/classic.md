# CLASSIC track

7-8 levels, the hardest ladder. Solved so far: Rock Paper Scissors (CCC37, 7), Room Planner (CCC40, 7, outputs not yet confirmed on the grader). Spaceship (CCC41, 8) and Robotic Lawn Mower (CCC39, 7) downloaded, unsolved.

## Shape of a Classic challenge

- L1-L2: compute/simulate (one formula, one round of rules). Often unique answer: exact match with the example.
- L3+: **construct** an arrangement that satisfies constraints. The statement says "there may be multiple correct solutions": grader validates, so write a checker and do not chase the example.
- Last levels: optimisation or adversarial twist (maximum packing, adversary-chosen cells, limited inventory).

## Recurring patterns and how to spot them

- **Grid/sequence simulation** (Pacman, Lawnmower, Spaceship): U/D/L/R or step lists; later add obstacles, route generation (BFS/coverage). Pitfall: x = column, y = row.
- **Tournament/bracket** (RPS): only the multiset per round matters when you control ordering -> search over count vectors; with fixed leaves + unknown cells -> bottom-up DP keeping the set of possible winners per node (bitmask combine table).
- **Packing** (Room Planner): "no touching, diagonals count" -> give each item a territory (item + gap cell + gap row) so non-touching becomes disjoint packing in a (x+1)x(y+1) box; guillotine DP plus pinwheel splits for small boxes.
- **Geometry/physics-like stepping** (Spaceship): simulate exactly with integers, check collisions each step.

## Workflow notes

- Always write `check.py` that re-simulates the rules independently of the solver.
- Heuristic search is acceptable if it finds a solution on every input; also stress it on random feasible instances (and say it is not proven).
- Statement vs example mismatches happen (Room Planner L7 says "matrix of integers", example shows X/.): follow the example.
