<div align="center">

# 🏁 Cloudflight Coding Contest

**Solutions, tooling and lessons from the [Cloudflight Coding Contest (CCC)](https://codingcontest.org): live editions and a full practice run of past challenges.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX-models-005CED?logo=onnx&logoColor=white)
![Tracks](https://img.shields.io/badge/tracks-Classic%20%C2%B7%20School%20%C2%B7%20Data%2FAI-2ea44f)
![Challenges](https://img.shields.io/badge/challenges-13-orange)

</div>

---

## 🧭 What is the CCC?

The CCC is a one-day, level-based programming contest. Every challenge is a ladder of 5 to 8 levels: each level ships a PDF statement plus input files, you upload your outputs, and the next level unlocks only when the grader accepts them. Difficulty rises level by level, and later levels reuse earlier ones. There are three tracks:

| Track | Shape |
|---|---|
| **Classic** | grids, simulation, search, construction, optimisation |
| **School** | shorter ladders: number theory, greedy, DP, constructive |
| **Data / AI** | fit or build a model; in 2026 a live tournament of ONNX models |

## 🗂️ Repository layout

```
.
├── CCC42/                     # Live edition, 23 Oct 2026
│   ├── colony_one/            #   Data/AI: board game → ONNX tournament (4 levels)
│   └── nano_fabricator/       #   Classic-style ladder, level 6 solved with sharded cloud runs
├── training/                  # Full practice run of past challenges (one folder each)
│   ├── CCC37_* … CCC41_*      #   level-N/{solution.py, check.py, NOTES.md}, README, explainer.html
│   ├── RESEARCH.md            #   Map of past editions and problems
│   └── patrones-classic.html  #   Visual cheat sheet of recurring Classic patterns
├── CCC24/ · CCC25/            # First contest attempts (2024), notebooks and scripts
└── README.md
```

## 🏆 Challenges

### Live: 42nd edition (23 Oct 2026)

| Challenge | Track | Levels | Highlights |
|---|---|---|---|
| **[Colony: One](CCC42/colony_one)** | Data / AI | 4 | L1-L2 board puzzles solved with an exact worst-case solver (`colony.py`). L3-L4: a hand-built ONNX policy/value network plugged into the referee's MCTS, with exact per-piece attack maps computed as `Conv` shifts inside the graph. Final model: [`final_model.onnx`](CCC42/colony_one/level-4/final_model.onnx). |
| **[Nano Fabricator](CCC42/nano_fabricator)** | Classic | 6 | Level 6 is an optimisation level (shortest output program wins). Beam search sharded over ~110 cloud runs and merged with `merge.py`: **14 966 lines**, from 66 031 on the first valid upload (world best ≈ 14 400). |

### Practice: past editions

| Challenge | Edition | Track | Levels | Result |
|---|---|---|---|---|
| [Rock Paper Scissors](training/CCC37_rock_paper_scissors) | 37 | Classic | 7 | solved, with explainer |
| [Wasp Honeycomb](training/CCC37_wasp_honeycomb) | 37 | School | 5 | solved locally, checkers |
| [Magic Money](training/CCC39_magic_money) | 39 | School | 5 | ✅ 5/5 on the grader |
| [Robotic Lawn Mower](training/CCC39_robotic_lawn_mower) | 39 | Classic | 7 | ✅ 7/7 on the grader |
| [Autonomous Drone](training/CCC40_autonomous_drone) | 40 | School | 6 | solved locally, checkers |
| [Room Planner](training/CCC40_room_planner) | 40 | Classic | 7 | ✅ 7/7 on the grader |
| [Asteroid Mining](training/CCC41_asteroid_mining) | 41 | School | 5 | solved locally, checkers |
| [Spaceship](training/CCC41_spaceship) | 41 | Classic | 8 | in progress |
| [Migratory Birds](training/CCC41_migratory_birds) | 41 | Data / AI | 6 | in progress |

## ⚙️ How each challenge is organised

```
<challenge>/
├── level-N/
│   ├── solution.py   # reads the level inputs, writes the .out files
│   ├── check.py      # independent validator (a different algorithm from the solver)
│   └── NOTES.md      # approach, pitfalls, what the grader accepted
├── run_all.py        # runs every solution + checker, prints a pass/fail table
├── README.md
└── explainer.html    # animated walkthrough of the algorithms (Spanish)
```

Run a single level:

```bash
python3 training/CCC39_magic_money/level-3/solution.py
python3 training/CCC39_magic_money/level-3/check.py
```

Large contest inputs (the two ~60 MB Migratory Birds files) are not committed: download them again from the contest page.

## 💡 Lessons learned

- **The grader validates, it does not diff.** When a statement allows several answers, any valid one passes.
- **Read every level's I/O table again.** Formats change silently between levels.
- **Independent checkers catch real bugs.** Write the checker with a different algorithm from the solver.
- **Validate against the real opponents early** (Data/AI tournaments). Beating your own previous models locally said little about the live rating; replaying the real match log was the best test.
- **Comparisons need volume.** 100-200 games carry about ±5 points of noise; confirm on fresh seeds with 300-500 games.

## 📜 Notes

Statements, inputs and the Colony: One engine belong to Cloudflight and are included only for reference alongside the solutions. Everything else is personal work, published to learn from.
