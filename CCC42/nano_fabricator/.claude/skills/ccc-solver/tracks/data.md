# DATA / AI track

Challenge so far: Migratory Birds (CCC41, "predict and classify migrating birds with machine learning", 6 levels). Solving in progress at the time of writing; fill the sections below with what is actually observed.

## What is different from Classic/School

- Levels likely involve **training/fitting on provided data and predicting** for held-out rows, so the grader may score accuracy/error rather than exact output.
- Hidden labels cannot be verified locally: hold out part of the labeled data (cross-validation) and report that score; be explicit about what is unverified.
- Libraries: check what is installed (`python3 -c "import numpy, sklearn, pandas"`) before planning; the live contest environment is Goyo's own machine.

## To record after the first run (TODO)

- Data format per level and what is predicted.
- Scoring rule / pass threshold as shown by the grader.
- Models that worked, validation score vs grader score.
- Time spent per level and which levels were deterministic parsing/feature work.
