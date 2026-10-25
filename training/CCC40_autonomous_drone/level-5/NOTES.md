# Level 5 - buildings

**Input:** N; per flight `pad_x pad_y limit`, B, then B buildings `left right height` (rectangle [left,right] x [0,height], closed).
No building covers x = 0. The pad may sit on a building roof (pad_y = its height). **Output:** `ax,ay` vectors as level 4.
Never touch, enter or cross a building (segment between consecutive positions counts), except the final touch-down.
Many answers valid -> `check.py` (exact integer / Fraction segment-vs-closed-rectangle test per tick; landing may touch only
the pad point at the last tick). The official example output passes the checker.

**Approach:** fly straight up (x = 0 is free) to H = 1 + max height of every building whose x-range meets the corridor
[min(0,x_pad), max(0,x_pad)] (and the pad), cross at hover (ay = 10 keeps the altitude), then descend vertically onto the pad:
`descent(H - pad_y)` lands exactly on the roof/ground. All three phases are the level-3/4 profiles. Staying strictly above every
roof in the corridor makes every segment collision-free. Time: <= 71% of the limit on all inputs.

**Pitfalls:** y must be strictly above the roof (touching is a collision); descend only after stopping exactly over the pad
(vx = 0); the descent starts from hover so the vertical column above the pad is free.
