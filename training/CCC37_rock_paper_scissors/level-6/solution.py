import glob
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "input"
OUTPUT_DIR = HERE / "output"

LEVEL = 6

STYLES = "RPSYL"
# BEATS[a] = styles that a beats (Rock-Paper-Scissors-Spock-Lizard)
BEATS = {"S": "PL", "P": "RY", "R": "LS", "L": "YP", "Y": "SR"}
IDX = {c: i for i, c in enumerate(STYLES)}
K = len(STYLES)
FULL = (1 << K) - 1
S_MASK = 1 << IDX["S"]

WIN = [[0] * K for _ in range(K)]
for a in STYLES:
    for b in STYLES:
        WIN[IDX[a]][IDX[b]] = IDX[a] if (a == b or b in BEATS[a]) else IDX[b]

# COMB[ma][mb]: set of possible winners when the left subtree can produce any
# winner in ma and the right subtree any winner in mb (worst case = union).
COMB = [[0] * (FULL + 1) for _ in range(FULL + 1)]
for ma in range(1, FULL + 1):
    for mb in range(1, FULL + 1):
        r = 0
        for i in range(K):
            if ma >> i & 1:
                for j in range(K):
                    if mb >> j & 1:
                        r |= 1 << WIN[i][j]
        COMB[ma][mb] = r


def prune(options):
    """Keep only the inclusion-minimal masks (smaller winner set is never worse)."""
    masks = sorted(options, key=lambda m: bin(m).count("1"))
    kept = []
    for m in masks:
        if not any((k & m) == k for k in kept):
            kept.append(m)
    return {m: options[m] for m in kept}


def leaf_options(c):
    if c == "X":  # we choose: any of the 5 styles (tie-break preference: S first)
        return {1 << IDX[ch]: ch for ch in "SRPYL"}
    if c == "Z":  # adversary chooses: any style, winner-set is everything
        return {FULL: "Z"}
    return {1 << IDX[c]: c}


def solve_one(s):
    m = len(s)
    # level[j] = list of nodes; node = {mask: back-pointer}
    level = [leaf_options(c) for c in s]
    history = [level]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left, right = level[i], level[i + 1]
            opts = {}
            for ma in left:
                for mb in right:
                    r = COMB[ma][mb]
                    if r not in opts:
                        opts[r] = (ma, mb)
            nxt.append(prune(opts))
        level = nxt
        history.append(level)
    root = level[0]
    if S_MASK not in root:
        raise RuntimeError("no way to make scissors win")
    out = [None] * m
    # top-down reconstruction (iterative, level by level)
    want = [S_MASK]
    for depth in range(len(history) - 1, 0, -1):
        nodes = history[depth]
        new_want = []
        for i, mask in enumerate(want):
            ma, mb = nodes[i][mask]
            new_want.append(ma)
            new_want.append(mb)
        want = new_want
    for i, mask in enumerate(want):
        ch = history[0][i][mask]
        out[i] = ch if ch != "Z" else "Z"
    return "".join(out)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for path in sorted(glob.glob(str(INPUT_DIR / ("in_level-%d_*.txt" % LEVEL)))):
        suffix = os.path.basename(path)[len("in_level-%d_" % LEVEL):-len(".txt")]
        with open(path) as f:
            lines = f.read().split("\n")
        n, m = map(int, lines[0].split())
        res = [solve_one(lines[1 + i].strip()) for i in range(n)]
        with open(OUTPUT_DIR / ("level-%d_%s.out" % (LEVEL, suffix)), "w") as f:
            f.write("\n".join(res) + "\n")


if __name__ == "__main__":
    main()
