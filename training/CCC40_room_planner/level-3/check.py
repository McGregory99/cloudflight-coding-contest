"""Validator for levels 2 and 3 (ID matrices). Usage: python3 check.py [level]"""
import glob, os, sys

def check(level, inp, outp):
    toks = open(inp).read().split()
    n = int(toks[0])
    rooms = [tuple(int(t) for t in toks[1 + 3 * i: 4 + 3 * i]) for i in range(n)]
    lines = [l for l in open(outp).read().split("\n") if l.strip() != ""]
    pos = 0
    for idx, (x, y, k) in enumerate(rooms):
        rows = [list(map(int, l.split())) for l in lines[pos:pos + y]]
        pos += y
        assert len(rows) == y, f"room {idx}: missing rows"
        assert all(len(r) == x for r in rows), f"room {idx}: bad width"
        cells = {}
        for r in range(y):
            for c in range(x):
                v = rows[r][c]
                if v:
                    cells.setdefault(v, []).append((r, c))
                elif level == 2:
                    raise AssertionError(f"room {idx}: empty cell in level 2")
        assert sorted(cells) == list(range(1, k + 1)), f"room {idx}: ids != 1..{k}"
        for v, cs in cells.items():
            assert len(cs) == 3, f"room {idx}: desk {v} has {len(cs)} cells"
            rs = {a for a, _ in cs}; cols = {b for _, b in cs}
            if len(rs) == 1:
                assert max(cols) - min(cols) == 2, f"room {idx}: desk {v} not contiguous"
            else:
                assert len(cols) == 1 and max(rs) - min(rs) == 2, f"room {idx}: desk {v} not straight"
    assert pos == len(lines), "extra lines"

def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.path.basename(os.getcwd()).split("-")[1])
    ok = True
    for inp in sorted(glob.glob(f"in_level-{level}_*.txt")):
        outp = os.path.basename(inp)[3:-4] + ".out"
        try:
            check(level, inp, outp)
            print("PASS", outp)
        except Exception as e:
            ok = False
            print("FAIL", outp, repr(e))
    sys.exit(0 if ok else 1)

main()
