"""usage: a_cmp.py '<json params>' tag -> random 100@9000 and vs best.onnx 200@9000, Pool(6)"""
import json, sys
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H))
import a_build, a_tourney as T
def main():
    kw = json.loads(sys.argv[1]); m = H / ("a_%s.onnx" % sys.argv[2]); a_build.build(m, **kw)
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    print(sys.argv[2], json.dumps(kw), flush=True)
    print(T.fmt("vs random", T.match(m, H.parent / "env/play/random.onnx", 100, 9000, 6)), flush=True)
    print(T.fmt("vs best", T.match(m, H / "best.onnx", n, 9000, 6)), flush=True)
if __name__ == "__main__": main()
