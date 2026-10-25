"""Independent validator for levels 3-5: python3 check.py  (checks every level-N_*.out against its input)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
LEVEL = HERE.name.split("-")[1]


def read_blocks(text):
    """split into paragraphs of consecutive non-blank lines"""
    blocks, cur = [], []
    for ln in text.split("\n"):
        if ln.strip():
            cur.append(ln.rstrip("\r"))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def check(in_text, out_text):
    first, *rest = in_text.split("\n")
    n = int(first)
    # input: header line + grid paragraph, per asteroid
    ib = read_blocks("\n".join(rest))
    # header lines are glued to their grid (no blank between) -> split manually
    cases = []
    for blk in ib:
        w, h, lim = map(int, blk[0].split())
        cases.append((w, h, lim, blk[1:]))
    ob = read_blocks(out_text)
    if len(cases) != n or len(ob) != n:
        return [f"asteroid count: input {len(cases)} / expected {n} / output {len(ob)}"]
    errs = []
    for k, ((w, h, lim, g), o) in enumerate(zip(cases, ob)):
        e = lambda m: errs.append(f"asteroid {k} ({w}x{h}, limit {lim}): {m}")
        if len(o) != h + 2 or any(len(r) != w + 2 for r in o):
            e("wrong output shape"); continue
        if len(g) != h + 2:
            e("bad input shape"); continue
        dug = set()
        bad = False
        for r in range(h + 2):
            for c in range(w + 2):
                gi, oc = g[r][c], o[r][c]
                if gi == "X" or oc not in "#:SX":
                    bad = True
                if gi == "#" and oc != "#": bad = True      # bedrock cannot be dug / changed
                if gi == "S" and oc != "S": bad = True
                if gi == ":" and oc not in ":X": bad = True
                if oc == "X": dug.add((r, c))
        if bad:
            e("bedrock/outpost altered or illegal character"); continue
        s = (0, g[0].index("S"))
        if len(dug) > lim:
            e(f"too many dug cells {len(dug)}"); continue
        # outpost: tunnel must be directly below it; connectivity from the outpost through dug cells
        seen, st = {s}, [s]
        while st:
            r, c = st.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (r + dr, c + dc)
                if nb in dug and nb not in seen:
                    seen.add(nb); st.append(nb)
        if len(seen) - 1 != len(dug):
            e("tunnels not connected to the outpost / each other"); continue
        for r in range(1, h + 1):
            for c in range(1, w + 1):
                if (r, c) in dug: continue
                if not any((r + dr, c + dc) in dug for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    e(f"cell ({r-1},{c-1}) not discovered"); break
            else:
                continue
            break
    return errs


if __name__ == "__main__":
    ok = True
    for f in sorted(HERE.glob(f"in_level-{LEVEL}_*.txt")):
        o = HERE / f.name.replace("in_", "").replace(".txt", ".out")
        errs = check(f.read_text(), o.read_text()) if o.exists() else ["missing output"]
        print(("OK  " if not errs else "FAIL"), f.name, errs[:3])
        ok &= not errs
    sys.exit(0 if ok else 1)
