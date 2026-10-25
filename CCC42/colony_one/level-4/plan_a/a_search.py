"""Coordinate search of a_build params vs model.onnx (200 games, offset 0, Pool(3)).
usage: a_search.py '<json base params>' '<json {param: [values]}>' [games] [thresh_points]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a_build, a_tourney

ref = HERE.parent / "model.onnx"
def score(kw, tag, games=200):
    m = HERE / ("a_tmp_%s.onnx" % tag); a_build.build(m, **kw)
    r = a_tourney.match(m, ref, games, 0, 3); m.unlink()
    print("  ", json.dumps(kw), a_tourney.fmt("", r), flush=True)
    return 100 * r[0] / r[3]

def main():
    base = json.loads(sys.argv[1]); grid = json.loads(sys.argv[2])
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    thr = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    best = score(base, "base", games); print("base", best, flush=True)
    for k, vals in grid.items():
        for v in vals:
            if v == base.get(k): continue
            s = score({**base, k: v}, "x", games)
            if s >= best + thr:
                best, base = s, {**base, k: v}; print("ACCEPT", k, v, "->", best, flush=True)
    print("FINAL", json.dumps(base), best)
    

if __name__ == '__main__':
    main()
