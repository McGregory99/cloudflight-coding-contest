import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))
from colony_one.env import ColonyOneEnv
from model_vs_model import SearchAgent
a_path, b_path = sys.argv[1], sys.argv[2]
for g in range(int(sys.argv[3])):
    aa, bb = SearchAgent(Path(a_path), 100, seed=2 * g), SearchAgent(Path(b_path), 100, seed=2 * g + 1)
    swap = g % 2 == 1
    cyan, mag = (bb, aa) if swap else (aa, bb)
    env = ColonyOneEnv(); hist = []
    while not env.terminated:
        ag = cyan if env.current_team == "CYAN" else mag
        if env.actions_left == 2:
            hist.append((env.round_number, env.current_team, env.render()))
        env.step(ag.select(env.board, env.current_team, env.actions_left, env.round_number))
    a_won = (env.winner == "MAGENTA") if swap else (env.winner == "CYAN")
    if not a_won and env.round_number >= 9:
        print("game", g, "A is", "MAGENTA" if swap else "CYAN", "winner", env.winner, "end round", env.round_number)
        for r, t, s in hist[-4:]:
            print("round", r, t, "to move"); print(s.split("\n\n")[0] if False else "\n".join(s.splitlines()[:9]))
        print(env.render()); break
