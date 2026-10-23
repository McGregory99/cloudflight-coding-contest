"""usage: python3 multi_run.py NAME SESSION NSESS SPL WB
Randomized-restart beam search (mb2 multi mode) on this session's share of patterns of NAME,
4 processes per session; each process gets the patterns with slot % (4*NSESS) == SESSION*4+c.
Programs are verified with the level-5 simulator and written to results/shard_NAME_mSESSION_0_0.json."""
import importlib.util, json, subprocess, sys
from pathlib import Path

H = Path(__file__).parent; L6 = H.parent
name, s, ns, spl, wb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
TO = sys.argv[6] if len(sys.argv) > 6 else "2100"
TAG = sys.argv[7] if len(sys.argv) > 7 else "m"
subprocess.run(["g++", "-O2", "-march=native", "-o", str(H / "mb2_bin"), str(H / "mb2.cpp")], check=True)
inp = L6 / f"in_level-6_{name}.txt"
procs = []
for c in range(4):
    out = H / f"raw_m_{name}_{s}_{c}.out"; out.write_text("")
    procs.append(subprocess.Popen(["timeout", TO, str(H / "mb2_bin"), "multi", str(inp), str(H / f"prev_{name}.txt"),
                                   str(out), str(s * 4 + c), str(4 * ns), spl, wb], stderr=subprocess.DEVNULL))
for p in procs:
    p.wait()
spec = importlib.util.spec_from_file_location("l5", L6.parent / "level-5" / "solution.py")
l5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(l5)
t = inp.read_text().split(); n = int(t[0]); p = 1; pats = []
for _ in range(n):
    r, rows, c, k = map(int, t[p:p + 4]); pats.append((r, t[p + 4:p + 4 + rows], k)); p += 4 + rows
best = {}
for c in range(4):
    cur = None
    for ln in (H / f"raw_m_{name}_{s}_{c}.out").read_text().split("\n"):
        if ln.startswith("PAT"): cur = []; idx = int(ln.split()[1])
        elif ln == "END":
            r, pat, k = pats[idx]
            if l5.run(r, pat, [l.split() for l in cur]) == k and (str(idx) not in best or len(cur) < len(best[str(idx)])):
                best[str(idx)] = cur
        elif cur is not None and ln: cur.append(ln)
(L6 / "results").mkdir(exist_ok=True)
(L6 / "results" / f"shard_{name}_{TAG}{s}_0_0.json").write_text(json.dumps(best))
print("verified improved patterns", len(best), "lines", sum(len(v) for v in best.values()))
