# Level 7 - Hamiltonian cycle, multiple trees

**I/O**: as L6 but any number of trees ('X'); guaranteed solvable. Output a closed-walk path (end adjacent to start).

**Approach**: unchanged `lawn.py` cycle mode: flow-based 2-factor + 2x2 flip merging + restarts with a new random flow (shuffled edge order). With many trees corridors may be 1 wide (no flips possible), so the initial 2-factor matters and restarts (up to 200 seeds) are the safety net; in practice the first tries work.

**Verification**: `check.py` on all inputs OK, <1 s total.

**Caveat**: heuristic, not exhaustive: a lawn whose only Hamiltonian cycles are unreachable by flips from random 2-factors could fail (assertion in solution.py would flag it; none seen).
