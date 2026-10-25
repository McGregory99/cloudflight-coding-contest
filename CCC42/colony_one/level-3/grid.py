import itertools, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))
import build_model as bm
from colony_one.baselines import GreedyAgent
from model_vs_model import SearchAgent, play_game

N = int(sys.argv[1]) if len(sys.argv) > 1 else 80
tmp = Path(tempfile.mkdtemp())
for kr, er in itertools.product([1.5, 2.0, 3.0, 5.0], [0.0, 1.0]):
    bm.KERNEL_RING, bm.ENEMY_RING = kr, er
    p = tmp / "m.onnx"; bm.build(p)
    w = sum(play_game(SearchAgent(p, 60, seed=g), GreedyAgent(seed=1000 + g))[0] == "CYAN" for g in range(N))
    print("kernel_ring=%s enemy_ring=%s  wins %d/%d" % (kr, er, w, N), flush=True)
