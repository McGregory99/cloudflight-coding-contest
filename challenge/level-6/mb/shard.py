"""usage: python3 shard.py NAME A B W NR TR
Runs the C++ beam-search planner on patterns [A,B) of in_level-6_NAME.txt (NAME like 3-large),
verifies every program with the level-5 simulator and writes results/shard_NAME_A_B_W.json
({global_pattern_index: [program lines]})."""
import importlib.util, json, subprocess, sys
from pathlib import Path

H = Path(__file__).parent
L6 = H.parent
name, a, b, W, NR, TR = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
spec = importlib.util.spec_from_file_location("l5", L6.parent / "level-5" / "solution.py")
l5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(l5)
subprocess.run(["g++", "-O2", "-march=native", "-o", str(H / "mb"), str(H / "mb.cpp")], check=True)
inp = L6 / f"in_level-6_{name}.txt"
raw = H / f"raw_{name}_{a}_{b}_{W}.out"
subprocess.run([str(H / "mb"), str(inp), str(a), str(b), str(raw), W, NR, TR], check=True)
t = inp.read_text().split(); n = int(t[0]); p = 1; pats = []
for _ in range(n):
    r, rows, c, k = map(int, t[p:p + 4]); pats.append((r, t[p + 4:p + 4 + rows], k)); p += 4 + rows
progs = {}; cur = None
for ln in raw.read_text().split("\n"):
    if ln.startswith("PAT"): cur = []; idx = int(ln.split()[1])
    elif ln == "END": progs[idx] = cur
    elif ln.startswith("FAIL") or not ln: pass
    elif cur is not None: cur.append(ln)
out = {}; tot = 0
for i, prog in progs.items():
    r, pat, k = pats[i]
    if l5.run(r, pat, [l.split() for l in prog]) == k:
        out[str(i)] = prog; tot += len(prog)
    else:
        print("WRONG", i)
(L6 / "results").mkdir(exist_ok=True)
(L6 / "results" / f"shard_{name}_{a}_{b}_{W}.json").write_text(json.dumps(out))
print("verified", len(out), "of", b - a, "total lines", tot)
