from pathlib import Path

HERE = Path(__file__).parent


def solve(text):
    t = text.split()
    n = int(t[0])
    out = []
    for i in range(n):
        w, h = int(t[1 + 2 * i]), int(t[2 + 2 * i])
        out.append("#" * (w + 2))
        out += ["#" + ":" * w + "#"] * h
        out.append("#" * (w + 2))
        out.append("")  # blank line after every asteroid (the example ends with one too)
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for f in sorted(HERE.glob("in_level-1_*.txt")):
        (HERE / f.name.replace("in_", "").replace(".txt", ".out")).write_text(solve(f.read_text()))
