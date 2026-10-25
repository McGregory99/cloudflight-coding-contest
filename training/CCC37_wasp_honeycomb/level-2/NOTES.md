# Level 2 - empty neighbours of the wasp
**I/O:** `N`, blank line, then N honeycombs (rows, blank-line separated). `O` empty, `X` barrier, `W` wasp (never on the edge). Output one count per honeycomb: empty (`O`) cells adjacent to `W`.
**Approach:** keep the string grid as is; a cell at (row r, string index c) has the 6 neighbours (r, c+-2) and (r+-1, c+-1). Count those equal to `O`. O(cells).
**Pitfalls:** the stagger is encoded by the `-` characters, so neighbours are +-2 horizontally and +-1 on adjacent rows (no offset-parity logic needed). Split blocks on blank lines, tolerate trailing blanks.
