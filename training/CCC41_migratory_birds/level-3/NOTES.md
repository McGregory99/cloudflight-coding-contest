# Level 3 - The Hurracurra Bird (flock -> species)

**Statement.** Per dataset exactly 6 flocks, one per species. Rows are bird paths (BOP id sequences) of a flock. Output `Flock ID,Species`.
The species are described in riddles: Hurracurra (hot regions), Bluetit (flies back along same route), Blackfinch (flock orbits one land together),
Goldhammer (travel out together, split on way back), Firefinch (nest at a base, each goes on its own adventure), Wolfthroat (lies in wait along segments of Bluetit routes).

**Approach.** Flock-level features, then a greedy ordered assignment (each species is taken once):
1. Hurracurra = highest mean temperature of the BOPs on its paths (degF fixed; ~43 degC vs ~15-22 for the rest).
2. Bluetit = highest palindrome fraction (path == reversed path), ties by length.
3. Wolfthroat = flock whose BOPs are a subset of the Bluetit flock's BOPs (highest overlap).
4. Blackfinch = highest fraction of duplicated rows (identical orbit), non-palindromic.
5. Goldhammer = longest common prefix of the paths (relative to length).
6. Firefinch = the remaining one.
The 2-flock example only assigns species whose cue clearly fires.

**Verification.** Example matches (line endings only: expected file has CRLF/no trailing newline). a/b/c verified by hand against the riddles: each flock matches exactly one species
(palindromes, identical loops, shared outbound prefix with diverging return, base-anchored short trips, hot BOPs). No hidden labels are available locally.
`check.py` validates ids, that all 6 species appear once.

**Doubt.** Low: the cues are clean in a/b/c; only risk is a dataset where Wolfthroat and Bluetit are both non-palindromic.
