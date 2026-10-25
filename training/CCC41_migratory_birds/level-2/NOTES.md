# Level 2 - Bird Love Score (regression)

**Statement.** Per BOP: vegetation, insects, urban light and a `Bird Love Score` that is `missing` for some rows. Predict the missing scores
(`BOP,Bird Love Score [<3]`, 2 decimals). Pass: RMSE < 6 (a), < 3 (b), < 3 (c). The degF bug in the level-1 temperatures must be fixed.

**Data.** Files a (1000 rows, 200 missing), b (1400, 200), c (100, all missing), example (4). BOP ids are disjoint across files, so the labelled rows of a+b(+example) = 2000 rows
are the training set for all files (c has no labels at all). Level-1 temperature and humidity (`all_data_from_level_1.in`) are joined by BOP id.

**Approach.** Linear regression (normal equations, tiny ridge) on `[1, vegetation, insects, light, temperature(degF-fixed), humidity]`.
Temperature is the dominant feature (+1.70 score per degC); vegetation/insects/light have almost no linear weight once temperature is included.
Quadratic terms and interactions did not help (CV 2.59 vs 2.59). Residuals look Gaussian with sd ~2.55, so ~2.6 is the noise floor.
If a missing BOP is labelled in another input file (only the example/a overlap), that value is used.

**Verification.** 5-fold CV RMSE = 2.59 (`CV=1 python3 solution.py`) -> passes a (<6) comfortably; b/c need <3 (margin ~0.4; c has only 100 rows, so its sampling noise is ~+-0.2).
Example: BOP 4 exact (leaked label from file a), BOP 3 predicted 25.26 vs expected 28.20 (within noise). `check.py`: format, ids, range 0..100.

**Pitfalls.** Without the degF fix RMSE is ~20. Number-word temperature `seventeen` must be parsed (value 17). Pure Python (no numpy installed here).
