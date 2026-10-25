"""Independent validator for CCC40 Autonomous Drone (level LEVEL).
Simulates every rule of the statement's "Valid Flight Checklist" on each flight of each output file."""
import sys
from fractions import Fraction
from pathlib import Path

LEVEL = 3
HERE = Path(__file__).parent


def parse_input(text):
    t = text.split()
    p = 0
    cases = []
    if LEVEL == 3:
        n, limit = int(t[0]), int(t[1])
        for h in t[2:2 + n]:
            cases.append(dict(px=0, py=0, hmin=int(h), limit=limit, B=[], Z=[]))
        return cases
    n = int(t[0]); p = 1
    for _ in range(n):
        c = dict(B=[], Z=[], hmin=0)
        if LEVEL == 4:
            c["px"], c["hmin"], c["limit"] = int(t[p]), int(t[p + 1]), int(t[p + 2]); p += 3
            c["py"] = 0
        else:
            c["px"], c["py"], c["limit"] = int(t[p]), int(t[p + 1]), int(t[p + 2]); p += 3
            b = int(t[p]); p += 1
            for _ in range(b):
                c["B"].append((int(t[p]), int(t[p + 1]), int(t[p + 2]))); p += 3
            if LEVEL == 6:
                s = int(t[p]); p += 1
                for _ in range(s):
                    c["Z"].append((int(t[p]), int(t[p + 1]))); p += 2
        cases.append(c)
    assert p == len(t), "unparsed input"
    return cases


def seg_rect(p0, p1, l, r, h):
    """Parameter interval [t0,t1] (Fractions) where segment p0->p1 lies in closed rect [l,r]x[0,h], or None."""
    t0, t1 = Fraction(0), Fraction(1)
    for a, d, lo, hi in ((p0[0], p1[0] - p0[0], l, r), (p0[1], p1[1] - p0[1], 0, h)):
        if d == 0:
            if a < lo or a > hi:
                return None
        else:
            ta, tb = Fraction(lo - a, d), Fraction(hi - a, d)
            if ta > tb:
                ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
            if t0 > t1:
                return None
    return t0, t1


def check_flight(c, accs):
    if not accs:
        return "empty flight"
    if len(accs) > c["limit"]:
        return f"too long {len(accs)} > {c['limit']}"
    x = y = vx = vy = 0
    maxy = 0
    n = len(accs)
    for i, (ax, ay) in enumerate(accs):
        last = i == n - 1
        if ay < 0:
            return f"tick {i+1}: negative ay"
        if LEVEL == 3:
            if ax != 0 or ay > 20:
                return f"tick {i+1}: bad acceleration"
        elif abs(ax) + ay > 20:
            return f"tick {i+1}: |ax|+ay > 20"
        vx += ax
        vy += ay - 10
        nx, ny = x + vx, y + vy
        if LEVEL == 6 and (ax, ay) != (0, 0):
            # rule confirmed by the official example output: only the position where the tick STARTS counts
            for zl, zr in c["Z"]:
                if zl <= x <= zr:
                    return f"tick {i+1}: accelerates inside silent zone {zl},{zr} (x={x})"
        if i == 0 and ny <= 0:
            return "no take-off at first tick"
        if ny < 0:
            return f"tick {i+1}: below ground"
        landing = (nx == c["px"] and ny == c["py"])
        if ny == 0 and not landing:
            return f"tick {i+1}: touches ground away from pad (x={nx})"
        for l, r, h in c["B"]:
            iv = seg_rect((x, y), (nx, ny), l, r, h)
            if iv is not None and not (landing and last and iv == (1, 1)):
                return f"tick {i+1}: hits building {l},{r},{h}"
        if landing and not last:
            return f"tick {i+1}: reaches pad but sequence continues"
        if last:
            if not landing:
                return f"ends at ({nx},{ny}) not on pad ({c['px']},{c['py']})"
            if vy not in (-1, 0):
                return f"landing vy={vy}"
            if LEVEL >= 4 and vx != 0:
                return f"landing vx={vx}"
        x, y = nx, ny
        maxy = max(maxy, y)
        if LEVEL <= 4 and not last and False:
            pass
    if LEVEL <= 4 and maxy < c["hmin"]:
        return f"max height {maxy} < {c['hmin']}"
    return None


def parse_output(text, level):
    flights = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        if level == 3:
            flights.append([(0, int(v)) for v in line.split()])
        else:
            flights.append([tuple(map(int, tok.split(","))) for tok in line.split()])
    return flights


def main():
    ok_all = True
    for fin in sorted(HERE.glob(f"in_level-{LEVEL}_*.txt")):
        fout = HERE / fin.name.replace("in_", "").replace(".txt", ".out")
        if not fout.exists():
            print("MISSING", fout.name); ok_all = False; continue
        cases = parse_input(fin.read_text())
        text = fout.read_text()
        if text.endswith(" \n") or " \n" in text or text.startswith(" "):
            print("trailing/leading space in", fout.name); ok_all = False
        flights = parse_output(text, LEVEL)
        if len(flights) != len(cases):
            print(f"{fout.name}: {len(flights)} flights, expected {len(cases)}"); ok_all = False; continue
        bad = 0
        for k, (c, f) in enumerate(zip(cases, flights)):
            err = check_flight(c, f)
            if err:
                bad += 1
                if bad <= 3:
                    print(f"  {fout.name} flight {k}: {err}")
        print(f"{fout.name}: {'OK' if not bad else 'FAIL'} ({len(cases) - bad}/{len(cases)})")
        ok_all &= not bad
    sys.exit(0 if ok_all else 1)


main()
