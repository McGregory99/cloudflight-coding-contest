"""Validator for levels 4-7 (X/. grids). Usage: python3 check.py [level]
Level 4: desks 1x3, 5: 1x2, 6: per-room length (4th input int), 7: free lengths 1..7,
the 3rd input int is the desk count (4-6) or the covered-cell count (7).
Rules: each 8-connected component of 'X' must be a straight line of exactly the desk
length (levels 4-6) or length 1..7 (level 7) -> this enforces "no touching, incl. diagonal"."""
import glob, os, sys

def components(grid, x, y):
    seen = [[False] * x for _ in range(y)]
    comps = []
    for r in range(y):
        for c in range(x):
            if grid[r][c] == "X" and not seen[r][c]:
                st = [(r, c)]; seen[r][c] = True; cells = []
                while st:
                    a, b = st.pop(); cells.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < y and 0 <= nb < x and grid[na][nb] == "X" and not seen[na][nb]:
                                seen[na][nb] = True; st.append((na, nb))
                comps.append(cells)
    return comps

def check(level, inp, outp):
    toks = open(inp).read().split()
    n = int(toks[0])
    w = 4 if level == 6 else 3
    rooms = [tuple(int(t) for t in toks[1 + w * i: 1 + w * (i + 1)]) for i in range(n)]
    lines = [l for l in open(outp).read().split("\n") if l.strip() != ""]
    pos = 0
    for idx, room in enumerate(rooms):
        x, y, k = room[:3]
        L = {4: 3, 5: 2, 6: room[3] if level == 6 else 0, 7: 0}[level]
        grid = lines[pos:pos + y]; pos += y
        assert len(grid) == y and all(len(r) == x and set(r) <= {"X", "."} for r in grid), f"room {idx}: bad shape/chars"
        comps = components(grid, x, y)
        total = 0
        for cells in comps:
            rs = sorted({a for a, _ in cells}); cs = sorted({b for _, b in cells})
            if len(rs) == 1:
                straight = cs[-1] - cs[0] + 1 == len(cells)
            elif len(cs) == 1:
                straight = rs[-1] - rs[0] + 1 == len(cells)
            else:
                straight = False
            assert straight, f"room {idx}: component {cells[:3]}.. not a straight line"
            if level == 7:
                assert 1 <= len(cells) <= 7, f"room {idx}: desk length {len(cells)}"
            else:
                assert len(cells) == L, f"room {idx}: desk length {len(cells)} != {L}"
            total += len(cells)
        got = total if level == 7 else len(comps)
        assert got == k, f"room {idx} ({x}x{y}): got {got}, expected {k}"
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
