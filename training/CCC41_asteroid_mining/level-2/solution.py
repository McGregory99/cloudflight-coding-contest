from pathlib import Path

HERE = Path(__file__).parent


def parse(text):
    lines = text.split("\n")
    n = int(lines[0])
    i, res = 1, []
    for _ in range(n):
        while not lines[i].strip():
            i += 1
        w, h = map(int, lines[i].split()[:2])
        res.append((w, h, lines[i + 1:i + h + 3]))
        i += h + 3
    return res


def solve(text):
    out = []
    for w, h, g in parse(text):
        s = g[0].index("S")
        rows = [g[0]]
        for r in range(1, h + 1):  # tunnel: straight down from below the outpost to the last minable row
            rows.append(g[r][:s] + "X" + g[r][s + 1:])
        rows.append(g[h + 1])
        out += rows + [""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for f in sorted(HERE.glob("in_level-2_*.txt")):
        (HERE / f.name.replace("in_", "").replace(".txt", ".out")).write_text(solve(f.read_text()))
