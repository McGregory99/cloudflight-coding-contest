"""Validate level-7 outputs.
Checks: same length, fixed fighters unchanged, 'X' replaced by a style,
'Z' kept as 'Z' (last-minute spots) and the final winner is scissors for every
possible filling of the 'Z' spots (exact worst-case set simulation, plus a
random Monte-Carlo simulation of concrete fillings)."""
import glob
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "input"
OUTPUT_DIR = HERE / "output"

LEVEL = 7
STYLES = "RPSYL"
BEATS = {"S": "PL", "P": "RY", "R": "LS", "L": "YP", "Y": "SR"}


def winner(a, b):
    return a if (a == b or b in BEATS[a]) else b


def all_winners(seq):
    """Set of possible winners when 'Z' may be any style (independent subtrees)."""
    level = [set(STYLES) if c == "Z" else {c} for c in seq]
    while len(level) > 1:
        level = [{winner(a, b) for a in level[i] for b in level[i + 1]}
                 for i in range(0, len(level), 2)]
    return level[0]


def concrete(seq, rng):
    level = [rng.choice(STYLES) if c == "Z" else c for c in seq]
    while len(level) > 1:
        level = [winner(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def check_file(inp, outp):
    lines = open(inp).read().split("\n")
    n, m = map(int, lines[0].split())
    outs = open(outp).read().split("\n")
    if outs and outs[-1] == "":
        outs.pop()
    if len(outs) != n:
        return "expected %d lines, got %d" % (n, len(outs))
    rng = random.Random(1)
    for i in range(n):
        src, out = lines[1 + i].strip(), outs[i]
        if len(out) != m or len(src) != m:
            return "line %d: bad length" % i
        for a, b in zip(src, out):
            if a == "X":
                if b not in STYLES:
                    return "line %d: X replaced by %r" % (i, b)
            elif a != b:
                return "line %d: fixed spot changed %r -> %r" % (i, a, b)
        if all_winners(out) != {"S"}:
            return "line %d: possible winners %s" % (i, sorted(all_winners(out)))
        for _ in range(50):
            if concrete(out, rng) != "S":
                return "line %d: random filling lost" % i
    return None


def main():
    bad = 0
    for inp in sorted(glob.glob(str(INPUT_DIR / ("in_level-%d_*.txt" % LEVEL)))):
        suffix = os.path.basename(inp)[len("in_level-%d_" % LEVEL):-len(".txt")]
        outp = OUTPUT_DIR / ("level-%d_%s.out" % (LEVEL, suffix))
        err = check_file(inp, outp)
        print("%-28s %s" % (outp.name, "OK" if err is None else "FAIL: " + err))
        bad += err is not None
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
