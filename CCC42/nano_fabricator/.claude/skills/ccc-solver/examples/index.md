# Solved challenges (code in ~/DEVELOPMENT/CCC/training/<folder>/)

Each folder has `README.md`, `explainer.html` (Spanish, animated), `run_all.py`, `level-N/{statement.pdf,input,expected,output,solution.py,check.py,NOTES.md}` and `outputs/level-N/` (files to upload). Read the level's `NOTES.md` for the full approach.

## CLASSIC

- **CCC37_rock_paper_scissors** (7 levels): L1 single fights; L2 two rounds; L3-L5 arrange round 1 from style counts (L5 adds Spock/Lizard), search over count vectors; L6 fill `X` via bracket DP; L7 adversarial `Z`. Levels 3-6 multi-answer (checker). Grader status: not reported yet.
- **CCC40_room_planner** (7 levels): L1 formula `(x/3)*y`; L2-L3 desks 1x3 (guillotine DP); L4-L7 non-touching desks via territory reduction + guillotine/pinwheel packing. **7/7 passed on the grader.**

- **CCC42_nanofabricator** (6 levels, live edition): L1 draw hex board; L2 one laser beam on a hex char grid; L3 several emitters, exactly 2 hits create matter, 3+ destroy; L4 emitter ring with F/B/T programs; L5 pattern detection and submission count; L6 optimisation (shortest programs that submit each pattern K times). L1-L5 passed; L6 final 14966 lines. Code: `challenge/level-N/` in ccc-cloud-test (L6: `solution.py` baseline, `mb/` C++ beam search + cloud shard runners, `merge.py`).

## SCHOOL

- **CCC39_magic_money** (5 levels): coin sets. L1 mex of coins; L2 two-coin sum; L3 DP 1..100; L4 amounts up to 1e9 via M^2 argument; L5 limited inventory via exchange argument + bounded knapsack. **5/5 passed on the grader.**

## DATA

- **CCC41_migratory_birds**: in progress.

## Also solved locally (grader not confirmed)

- CCC39_robotic_lawn_mower (Classic, 7): **7/7 passed on the grader.** Hamiltonian path/cycle via max-flow + 2x2 flips.
- CCC37_wasp_honeycomb (School, 5), CCC40_autonomous_drone (School, 6), CCC41_asteroid_mining (School, 5): solved locally with checkers.

## Unsolved but downloaded

CCC41_spaceship (Classic, 8), CCC39_robotic_lawn_mower (Classic, 7), CCC41_asteroid_mining (School, 5), CCC40_autonomous_drone (School, 6), CCC37_wasp_honeycomb (School, 5).
