# SCHOOL track

5 levels (Wasp in the Honeycomb, Asteroid Mining, Autonomous Drone, Magic Money). Solved so far: Magic Money (CCC39, 5/5 passed on the grader). Asteroid Mining (CCC41), Autonomous Drone (CCC40), Wasp in the Honeycomb (CCC37) downloaded, unsolved.

## Shape

Same ladder idea as Classic but shorter and numeric/discrete; the last level is where the real algorithm hides (Magic Money L4-L5: amounts up to 1e9 / 3e8).

## What Magic Money taught (transferable)

- L1-L2: set/two-sum style lookups.
- L3: coin-change DP over a small range. Greedy is wrong for non-canonical systems; DP.
- L4 (huge amounts): never iterate over the amount. Find the structural reason (for x >= M^2 an optimal solution contains the largest coin M) and reduce to a small table + arithmetic.
- L5 (limited inventory): exchange argument shrinks the search space to a bounded knapsack; validate against an exact brute force on ~1e5 small random instances.
- Output tie-breaking differs from the example but the grader validates optimality.

## Habits

- When constraints explode (1e8+), look for periodicity/exchange arguments before coding.
- Check input layout changes between levels (global C/A, `QxV` count-first).
