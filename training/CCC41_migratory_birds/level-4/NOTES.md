# Level 4 - Going Global (flock classification, F1 macro > 90%)

**Statement.** `Flock ID,BOP Path,Species`; every row of a flock shares one species; ~25% of flocks have `missing`. Output `Flock ID,Species` for each missing flock. Pass: macro F1 > 90%.
Species patterns are the same riddles as level 3 but the paths are now noisy (paths perturbed, padding with repeated start node, flocks of 3-12 birds).

**Approach.** Flock-level feature vector + random forest written from scratch (no numpy/sklearn here):
size, mean length, mean/hot-fraction temperature of BOPs (degF fixed), palindrome score (after stripping the repeated trailing base node), set-palindrome score,
start==end, duplicate-row fraction, position-wise agreement of rows in four path quarters + halves, Jaccard of row node sets, trailing repeats, unique-node ratio, short-path flag.
300 trees, depth 8, trained on all labelled flocks (main file + example).

**Verification.** 5-fold CV over labelled flocks: macro F1 ~0.975-0.98 (accuracy ~0.98) -> margin over 0.90. Example flock 17 -> Red Firefinch matches. Predicted class counts on the 72 missing flocks are balanced (10-15 per species).
Remaining CV errors are Goldhammer/Wolfthroat/Blackfinch confusions on short noisy flocks. Runtime ~30 s including CV (`CV=1`), ~10 s without.

**Pitfalls.** Flock ids are only unique per file. Trailing repeated nodes break naive palindrome tests. Temperature needs the degF fix to separate Hurracurra.
