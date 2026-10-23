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

## Optimisation last level (lessons from Nano Fabricator, CCC42 classic, L6)

Score = total lines of the program you output, lower is better. Final 14966 vs 66031 first valid upload; world top was ~14400. What moved the score, in order of payoff:

1. **Get a valid baseline uploaded in minutes** (simple constructive planner), then iterate. The grader keeps the best upload.
2. **Tick-level beam search in C++** over all actors at once (bitset state, potential = distance to cells still missing, heavy penalty on forbidden matter). Took 66k -> 17k. Python was too slow for this.
3. **Variance is huge between runs** (one pattern: 117-152 lines by seed). Many randomized restarts per instance beat a wider beam. Spread them over many cloud sessions (4 processes each), each on a slice of instances, budget proportional to current length.
4. **Exact CP-SAT** (OR-Tools installs with pip) on small instances / single copies: per-copy re-solve with free end state, tail re-solve, cycles of copies for high-K repeats. Good for the last 2-5%.
5. **Per-instance merge**: keep a `merge.py` that takes the shortest *verified* program per instance from every source dir, and always include the previously uploaded outputs as a source (an agent that empties its JSON must never make the merge worse).

Did not pay: line sweeps with blocker beams, instruction-level SA/compaction, symmetry transfer, rule-loophole hunting. The gap to the top was emitter travel between high-yield configurations: next time try configuration-level planning (pick high-yield setups, order them by travel cost) seeded into the beam search early, not in the last hour.

Process lessons: push every improvement immediately and tell Goyo to re-upload; schedule merges before the deadline; cloud sessions take ~3 min to start and must push by a hard time; compute-only sessions should run on a cheap model.
