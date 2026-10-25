"""Colony: One game solver (CYAN = us). Worst-case search: MAGENTA may reply with any legal turn.

State: (ck, cp, mk, rnd) with squares as (col, row) 0..7 (A1 = (0, 0)); cp None = Ping dead.
Rules from the level-2 statement: guard, firewall rounds 8/16/24/26, Kernel endgame.
"""
import sys
from functools import lru_cache

DIAG = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ORTH = [(1, 0), (-1, 0), (0, 1), (0, -1)]
ADJ = DIAG + ORTH
CYAN, MAG = "C", "M"


def bounds(rnd):
    """Playable [lo, hi] after the rings removed at the end of rounds < rnd."""
    ring = sum(rnd > r for r in (8, 16, 24, 26))
    return ring, 7 - ring


def name(sq):
    return "ABCDEFGH"[sq[0]] + str(sq[1] + 1)


def inb(sq, lo, hi):
    return lo <= sq[0] <= hi and lo <= sq[1] <= hi


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def ring_of(sq):
    return min(sq[0], 7 - sq[0], sq[1], 7 - sq[1])


def actions(side, ck, cp, mk, rnd):
    """Yield (label, result) with result = 'C'/'M' (win) or new (ck, cp, mk)."""
    lo, hi = bounds(rnd)
    if side == CYAN:
        pieces = {ck: "K", cp: "P"} if cp else {ck: "K"}
        # Kernel
        for dx, dy in ADJ:
            t = (ck[0] + dx, ck[1] + dy)
            if not inb(t, lo, hi) or t == cp:
                continue
            if t == mk:
                yield "K %s x%s" % (name(ck), name(t)), CYAN  # Magenta has no guards
            else:
                yield "K %s>%s" % (name(ck), name(t)), (t, cp, mk)
        if cp:
            for dx, dy in ORTH:
                for step in (1, 2):
                    t = (cp[0] + dx * step, cp[1] + dy * step)
                    if not inb(t, lo, hi) or t in (ck, mk):
                        break
                    yield "P %s>%s" % (name(cp), name(t)), (ck, t, mk)
            for dx, dy in DIAG:
                for step in (1, 2):
                    t = (cp[0] + dx * step, cp[1] + dy * step)
                    if not inb(t, lo, hi) or t == ck:
                        break
                    if t == mk:
                        yield "P %s x%s" % (name(cp), name(t)), CYAN
                        break
    else:
        for dx, dy in ADJ:
            t = (mk[0] + dx, mk[1] + dy)
            if not inb(t, lo, hi):
                continue
            if t == ck:
                if cp and cheb(ck, cp) == 1:  # guard dies, attacker stays
                    yield "K %s x%s (guard dies)" % (name(mk), name(t)), (ck, None, mk)
                else:
                    yield "K %s x%s" % (name(mk), name(t)), MAG
            elif t == cp:
                yield "K %s x%s" % (name(mk), name(t)), (ck, None, t)
            else:
                yield "K %s>%s" % (name(mk), name(t)), (ck, cp, t)


def end_of_turn(side, ck, cp, mk, rnd):
    """Kernel endgame, then firewall after MAGENTA's turn. Returns 'C'/'M' or (ck, cp, mk)."""
    if cp is None:
        if cheb(ck, mk) <= 2:
            return MAG if side == CYAN else CYAN
        rc, rm = ring_of(ck), ring_of(mk)
        return CYAN if rc > rm else MAG
    if side == MAG and rnd in (8, 16, 24, 26):
        lo, hi = bounds(rnd + 1)
        dead_c, dead_m = not inb(ck, lo, hi), not inb(mk, lo, hi)
        if dead_m:
            return MAG if dead_c else CYAN
        if dead_c:
            return MAG
        if not inb(cp, lo, hi):
            cp = None
            return end_of_turn_fw(ck, mk)
    return (ck, cp, mk)


def end_of_turn_fw(ck, mk):
    # Ping died to the firewall; the endgame check applies at the end of the next turn.
    return (ck, None, mk)


def turn(side, ck, cp, mk, rnd):
    """All reachable outcomes of a two-action turn: dict result -> label sequence."""
    out = {}
    for l1, r1 in actions(side, ck, cp, mk, rnd):
        if r1 in (CYAN, MAG):
            out.setdefault(r1, [l1])
            continue
        for l2, r2 in actions(side, *r1, rnd):
            if r2 in (CYAN, MAG):
                out.setdefault(r2, [l1, l2])
                continue
            res = end_of_turn(side, *r2, rnd)
            out.setdefault(res, [l1, l2])
    return out


@lru_cache(maxsize=None)
def cyan_wins(ck, cp, mk, rnd, turns):
    """Cyan to move: can it force a win within `turns` own turns? Returns label list or None."""
    if turns == 0 or rnd > 26:
        return None
    for res, seq in turn(CYAN, ck, cp, mk, rnd).items():
        if res == CYAN:
            return seq
        if res == MAG:
            continue
        if forced(res, rnd, turns):
            return seq
    return None


def forced(state, rnd, turns):
    ok = True
    replies = turn(MAG, *state, rnd)
    if MAG in replies:
        return False
    for res in replies:
        if res == CYAN:
            continue
        if cyan_wins(*res, rnd + 1, turns - 1) is None:
            return False
    return ok


def solve(ck, cp, mk, rnd=1, max_turns=4):
    for t in range(1, max_turns + 1):
        seq = cyan_wins(ck, cp, mk, rnd, t)
        if seq:
            return t, seq
    return None, None


def sq(s):
    return ("ABCDEFGH".index(s[0].upper()), int(s[1]) - 1)


if __name__ == "__main__":
    # usage: colony.py <cyanK> <cyanPing|-> <magK> [round] [maxTurns]
    ck, cp, mk = sq(sys.argv[1]), (None if sys.argv[2] == "-" else sq(sys.argv[2])), sq(sys.argv[3])
    rnd = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    mt = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    t, seq = solve(ck, cp, mk, rnd, mt)
    print("forced win in %s turn(s): %s" % (t, seq) if seq else "no forced win within %d turns" % mt)
