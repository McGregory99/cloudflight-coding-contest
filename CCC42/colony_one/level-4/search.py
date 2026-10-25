"""Score parameter variants vs reference opponents. usage: search.py '<json list of param dicts>' [games]"""
import json, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))
import build_model as bm
import tourney

def main():
    variants = json.loads(sys.argv[1]); games = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    tmp = Path(tempfile.mkdtemp())
    refs = [HERE / "env/play/random.onnx", HERE / "model_l3.onnx"]
    for i, kw in enumerate(variants):
        m = tmp / ("v%d.onnx" % i); bm.build(m, **kw)
        scores = [tourney.match(m, r, games)[0] for r in refs]
        print(json.dumps(kw), "-> vs random %d/%d, vs L3 %d/%d" % (scores[0], games, scores[1], games), flush=True)


if __name__ == '__main__':
    main()
