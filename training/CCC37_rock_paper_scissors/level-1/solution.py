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


def solve(text):
    lines = text.split()
    n = int(lines[0])
    return [winner(s[0], s[1]) for s in lines[1:1 + n]]


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for path in sorted(glob.glob(str(INPUT_DIR / "in_level-1_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-1_"):-len(".txt")]
        with open(path) as f:
            out = solve(f.read())
        with open(OUTPUT_DIR / ("level-1_%s.out" % suffix), "w") as f:
            f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
