# Level 1 - path direction counts

**I/O**: N, then N path strings over W(north) D(east) S(south) A(west). Output per path: counts of W D S A, space separated.

**Approach**: str.count for each letter in order W D S A. O(total length).

**Pitfalls**: output order is W D S A (not alphabetical, not WASD-reading order of the compass). Verified by exact diff with the example.
