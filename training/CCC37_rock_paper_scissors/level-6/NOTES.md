# Level 6 - fill the X spots so Scissors wins

**Input**: `N M`, then N lines with M chars from R,P,S,Y,L (5 styles) and X (free spot) forming the first round. **Output**: N strings (X replaced by any style) such that the final winner is S. Multiple answers accepted.

**Approach**: exact bottom-up DP on the bracket. For every node keep the family of achievable "possible winner" sets; for a node with a fixed set the winner is deterministic, so this is a singleton. A leaf X offers 5 options (singletons). Combining children: `winners = union over (a in L, b in R) of beat(a, b)`. Smaller sets are never worse, so keep only inclusion-minimal sets (antichain, <= 10 masks). The root must offer exactly {S}; reconstruction walks top-down choosing back-pointers and finally the leaf styles. Preference order for X ties: S, R, P, Y, L.
Complexity: O(M * A^2) with A <= 10 (bitmask combine table 32x32); 4096-leaf tournaments run in ~10 ms.

**Verification**: `check.py` checks fixed spots unchanged, X replaced, and S wins. All inputs pass. The example output differs from ours (valid alternative).
**Pitfalls**: the statement says "any style you want" so multiple answers; an exact reference-output match is not attempted beyond the preference order.
