# Level 5
**Statement:** Same as level 4 but desks are 1x2.
**Approach:** identical territory reduction with L=2 (2x3 territories in the (x+1)x(y+1) box). Here the pinwheel step is essential: e.g. 6x6 -> 7x7 box needs 8 desks, pure guillotine only finds 7. All maxima equal floor((x+1)(y+1)/6) in the inputs and are reached.
**Verification:** `check.py` passes on all inputs (components straight, length 2, count = k). Runtime ~0.05 s.
**Pitfalls:** guillotine-only packing is off by one on many rooms; need the five-block split for small boxes.
