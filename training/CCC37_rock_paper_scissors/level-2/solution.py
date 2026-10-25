import glob
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "input"
OUTPUT_DIR = HERE / "output"

BEATS = {"R": "S", "S": "P", "P": "R"}  # key beats value


def winner(a, b):
    if a == b or BEATS[a] == b:
        return a
    return b


def play_round(s):
    return "".join(winner(s[i], s[i + 1]) for i in range(0, len(s), 2))


def solve(text):
    tokens = text.split()
    n = int(tokens[0])
    return [play_round(play_round(s)) if len(s) >= 4 else play_round(s) for s in tokens[2:2 + n]]


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for path in sorted(glob.glob(str(INPUT_DIR / "in_level-2_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-2_"):-len(".txt")]
        with open(path) as f:
            out = solve(f.read())
        with open(OUTPUT_DIR / ("level-2_%s.out" % suffix), "w") as f:
            f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
