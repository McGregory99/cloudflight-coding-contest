"""Merge per-pattern programs from several JSON sources (shortest wins), verify, write outputs."""
import json, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import solution as base  # noqa: E402
import importlib.util
_sp = importlib.util.spec_from_file_location('l5sol', HERE.parent / 'level-5' / 'solution.py')
l5 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(l5)

SCRATCH = Path("/tmp/claude-0/-home-user-ccc-cloud-test/dcc51239-9132-56b4-8241-b06f380db307/scratchpad")
SOURCES = sorted(p for p in SCRATCH.glob("l6_*") if p.is_dir())
NAMES = ["1-small", "2-medium", "3-large", "4-enormous"]


def main():
    base.OUT.mkdir(parents=True, exist_ok=True)
    grand = 0
    for name in NAMES:
        text = (HERE / f"in_level-6_{name}.txt").read_text()
        t = text.split(); n = int(t[0]); p = 1; pats = []
        for _ in range(n):
            R, rows, cols, K = map(int, t[p:p + 4]); p += 4
            pats.append((R, K, t[p:p + rows])); p += rows
        cands = {i: [] for i in range(n)}
        for src in SOURCES:
            for f in list(src.glob(f"out_{name}.json")) + list(src.glob(f"out_v*_{name}.json")):
                for k, prog in json.loads(f.read_text()).items():
                    cands[int(k)].append((len(prog), src.name, prog))
        out = []; used = {}; total = 0
        for i, (R, K, pat) in enumerate(pats):
            best = None
            for ln, sname, prog in sorted(cands[i], key=lambda c: c[0]):
                pr = [l.split() if isinstance(l, str) else l for l in prog]
                if all(len(l) == 6 for l in pr) and l5.run(R, pat, pr) == K:
                    best = (ln, sname, pr); break
            if best is None:
                pr = base.build_program(R, pat, K); best = (len(pr), "baseline", pr)
            used[best[1]] = used.get(best[1], 0) + 1
            total += best[0]
            out.append("".join(" ".join(l) + "\n" for l in best[2]) + "\n")
        (base.OUT / f"level-6_{name}.out").write_text("".join(out))
        print(name, total, used); grand += total
    print("TOTAL", grand)


main()
