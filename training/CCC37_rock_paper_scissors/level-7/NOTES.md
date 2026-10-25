# Level 7 - Z spots are filled by an adversary

**Input**: same as level 6 plus `Z` = last-minute spot whose style we cannot control (any of the 5 styles). **Output**: replace every X so that the final winner is S for EVERY possible filling of the Z spots.

**Approach**: same set-DP as level 6 with Z leaves represented as the full set {R,P,S,Y,L} of possible winners. The "possible winners" set of a node is the union of beat(a,b) over its children's sets - exact for the worst case because the Z choices in different subtrees are independent. Choose X values (before Z is revealed) so that the root's set is {S}; keep only minimal sets per node (monotone: smaller set is never worse). Z characters stay `Z` in the output (as in the example).
Complexity: same as level 6, ~10 ms per 4096-leaf tournament.

**Verification**: `check.py` computes the worst-case winner set of the output (exact) and also runs random concrete Z fillings; all inputs pass and the example output is reproduced byte-for-byte (thanks to the S-first preference order).
**Pitfalls**: order of quantifiers is exists X, forall Z; Z must remain `Z` in the output.
