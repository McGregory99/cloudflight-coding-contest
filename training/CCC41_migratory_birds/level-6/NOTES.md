# Level 6 - Final Reckoning (predict top-50 arrivals for day 791, required accuracy 100%)

**Statement.** Same table as level 5 plus 30 more days with arrivals (761-790). Predict the 50 BOPs with the highest Arrivals on day 791.

**Key finding.** The new 30 days are an *exact time reversal* of the last 30 known days with the wind negated:
`arrivals(761+k) == arrivals(760-k)` and `occupancy(761+k) == occupancy(760-k)` for every BOP, k = 0..29 (e.g. 761<->760, 790<->731; wind x/y have opposite signs).
That is the "wind blows the other way and the worms move backwards" story. The reflection continues, so day 791 mirrors day 730: the prediction is the top 50 by Arrivals of day 730
(rank 50 = 490, rank 51 = 488: no tie at the cut). Output ordered by arrivals descending.

**Approach.** `solution.py` loads the level-5 table + the new file, verifies the mirror property on all 30 days, and if it holds maps day 791 -> 730. Fallback if the mirror is not detected: persistence of the last day (not used here).

**Verification.** Mirror property verified exactly for all 30 days (the duplicate-array search finds only these 30 pairs in all 790 days). `check.py` recomputes the top-50 from the raw level-5 table independently.
This cannot be confirmed against a hidden label.

**Doubt.** If the generator stops mirroring exactly at day 791 (e.g. a fresh regime), the answer is wrong; a data-driven predictor gets at most ~0.9 one-step overlap, which would not reach 100%, so mirroring is the only route to a 100% answer.
