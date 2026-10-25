"""Validate level-4 outputs: every output must be a valid arrangement of the
given fighter counts and satisfy the level's winning condition."""
import glob
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "input"
OUTPUT_DIR = HERE / "output"

STYLES = "RPS"
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}  # BEATS[a] = styles that a beats
ROUNDS = None  # None = full tournament; int = only that many rounds
LEVEL = 4


def winner(a, b):
    if a == b or b in BEATS[a]:
        return a
    return b


def play(seq, rounds):
    for _ in range(rounds):
        seq = [winner(seq[i], seq[i + 1]) for i in range(0, len(seq), 2)]
    return seq


def check_file(inp, outp):
    lines = open(inp).read().split("\n")
    n, m = map(int, lines[0].split())
    outs = open(outp).read().split("\n")
    if outs and outs[-1] == "":
        outs.pop()
    if len(outs) != n:
        return "expected %d lines, got %d" % (n, len(outs))
    rounds = ROUNDS if ROUNDS is not None else m.bit_length() - 1
    for i in range(n):
        want = {c: 0 for c in STYLES}
        for t in lines[1 + i].split():
            want[t[-1]] = int(t[:-1])
        s = outs[i]
        if len(s) != m or s != s.strip():
            return "line %d: bad length/whitespace" % i
        got = {c: s.count(c) for c in STYLES}
        if got != want or sum(got.values()) != m:
            return "line %d: style counts differ %r vs %r" % (i, got, want)
        res = play(list(s), rounds)
        if ROUNDS is None:
            if res != ["S"]:
                return "line %d: winner %r" % (i, res)
        else:
            if "R" in res or "S" not in res:
                return "line %d: after 2 rounds %r" % (i, "".join(res))
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
