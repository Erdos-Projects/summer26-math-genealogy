# Keyword Trends


## Question

Within each subject, which thesis-title keywords are rising over time, and can we
predict which will keep trending?

## Idea

New terminology tends to show up in thesis titles before a topic grows large. By
tracking each word's yearly usage share within a subject, we want to flag words
with a low historical base and a steep recent rise.

## Data

Starting from 307,399 theses with a recorded title, we narrow to a usable set in
two steps:

- **Language:** 84.7% of titles are English. The remaining 15.3% (mostly French,
 German, Dutch) are excluded to avoid splitting the same concept across languages  (for example modeling / modélisation / Modellierung). Language: titles are filtered to English using fastText lid.176, keeping 208,150 of 234,743 titles (88.7%). A langdetect cross-check agreed within ~2.5 points; manual inspection of the disagreement set showed the gap was almost entirely langdetect misreading short English titles (for example single-token titles like "Topological Means" or "Fuzzy Geometry") as other languages. fastText was correct
 in these cases, so it was chosen as the filter.


## Planned approach

- Filter theses to a target subject
- Tokenize titles and compute each word's share of titles per year
- Detect rising words from their recent trend (positive slope on a low base)
- Plot top rising words per subject to confirm the trend is real and not a one-year spike

## Method notes

- Strip accents before tokenizing using `unicodedata.normalize("NFD")` to avoid
  splitting accented words (for example "modélisation" wrongly becoming "mod" + "lisation")
- Run the analysis per subject so results are not dominated by the largest subjects

## Modeling and evaluation (not started yet)

Planned as a temporal forecasting problem: predict a word's next-year usage share
from its past years. Because this is a time series, the main risk is temporal
leakage, so the plan is a time-based split (train on earlier years, test on later
years) rather than a random split. Baseline model will be linear regression on
lag features, evaluated with RMSE/MAE plus a shuffled-target leakage check.

## Status

- [ ] Tokenization and per-year word counts
- [ ] Rising-word detection
- [ ] Per-subject trend plots
- [ ] Modeling and evaluation
