# Keyword Trends

## Question

Within each subject, which thesis-title keywords are rising over time, and can we
predict which will keep trending?

## Idea

New terminology tends to show up in thesis titles before a topic grows large. By
tracking each word's yearly usage share within a subject, we want to flag words
with a low historical base and a steep recent rise.
## Folder Structure

```
keyword_trends-Aaroodd/
├── README.md
├── 01_build_parquets.ipynb
├── 02_keyword_trends_eda.ipynb
├── 03_model_v2.ipynb
├── images/                     # figures used in README
├── archive/
│   ├── model_v1.ipynb          # superseded, kept for reference
│   └── fasttextvlangdetect.ipynb  # not needed, kept for reference
├── lid.176.bin
└── data/
    ├── global_counts.parquet
    ├── bigram_model.pkl
    ├── subject_counts/
    ├── word_year_subject.parquet
    ├── subject_meta.parquet
    └── watchlist_2024.csv
```
## Data

Starting from 338,532 rows in the full dataset, we narrow to a usable set in
four steps:

- **Subject code origin:** keep only rows with an original (from the MGP website)
  subject code, not a model-predicted one (by Osanda). This drops 77,711 predicted-code
  rows, leaving 202,492 rows (59.8% of the total).
- **Completeness:** keep only rows with a title and year present, leaving
  160,548 rows across 63 subjects.
- **Language:** titles are filtered to English using fastText lid.176, keeping
  144,594 of 160,548 titles (90.1%). fastText was chosen over langdetect after
  manual inspection showed langdetect misread short English titles.
- **Year window:** derived dynamically, not fixed. START_YEAR is the first year
  with at least 200 titles (a stable-share floor). TREND_END is the last year
  before title volume drops below 75% of the peak, which catches data-entry
  lag in recent years. Subject-years with fewer than 50 total title words are
  excluded on top of this (see Method section for the derived window and plot).


![Derived analysis year window](images/year_window_derivation.png)
*Title volume by year, shaded regions excluded. START_YEAR and TREND_END are
derived from volume thresholds, not fixed by hand.*


## Method

**Tokenizer** (`01_keyword_trends_eda.ipynb`, shared with `02_build_parquets.ipynb`):
- Strip accents via `unicodedata.normalize("NFD")` before tokenizing
- spaCy `en_core_web_sm` with parser and NER disabled (tagger only)
- Keep NOUN, ADJ, VERB, PROPN; drop spaCy stopwords; min lemma length 4
- Drop a custom list of generic academic filler words (e.g. study, method,
  model, research, theory, application, case) that pass spaCy's stopword
  filter but carry no topical signal in thesis titles
- Bigram detection via gensim Phrases (trained once in build_parquets, applied
  here) to capture phrases like `machine_learning`, `neural_network`

**Subject volume check:** each subject's title volume is checked per decade
before trusting its word shares. Subjects with thin decades are treated with
caution in the rising-word ranking.

![Subject volume by decade](images/subject_volume_by_decade.png)
*Computer science, titles per decade against a thin-data floor.*

**Rising-word detection:**
- Per-subject word share = word token count / total title tokens per year
- Specificity filter: subject share / global share >= 1.5 (removes generic terms)
- Rising score: linear slope over a recent 10-year window
- Enriched score: rising score weighted by specificity and penalized by
  global frequency, so words that are both generic and non-specific rank low.
  Not a bounded or normalized metric, only meaningful for ranking words
  within the same subject, not for comparing magnitudes across subjects.
- Deduplication: merges lemma/bigram variants of the same word (e.g.
  learn/learning, machine_learn/machine_learning) using underscore-aware
  token-prefix matching

The plots below use Computer science as a worked example, one of the
highest-volume subjects. The same method runs across all subjects.

![Rising words in Computer science](images/rising_words_barh_subject68.png)
*Top rising words in Computer science, ranked by recent slope.*

![Rising words over time](images/rising_words_timeseries_subject68.png)
*Yearly share (10-yr smoothed) for Computer science's top rising words.
Deep_learning, reinforcement_learning, and explainable show clear post-2015
inflections; algorithm peaks in the 1980s-90s and gradually declines as a
share of titles, showing the method also catches fading terms, not just
rising ones.*


![Rising words specificity vs slope](images/bubble_subject68.png)
*Recent slope vs subject-specificity for Computer science's rising words,
bubble size is total word count, color is enriched score. deep_learning has
both a high slope and high enriched score; explainable is more specific
(higher specificity ratio) but lower volume.*

**Multi-subject scan:** the same detection runs across all subjects with
enough data, using precomputed per-subject counts from build_parquets.

![Top rising words across highest-volume subjects](images/top15_subjects_rising_words.png)
*Top 5 rising words in the 15 subjects with the most titles, ranked by
enriched score. Not directly comparable across subjects with very different
total title counts.*
## Pipeline outputs

`01_build_parquets.ipynb` runs once and produces everything the EDA and
modeling notebooks need. Outputs are versioned (`_v5_final` suffix) so
changing the tokenizer, filters, or dataset never silently reuses stale
cached files:

- `data/global_counts_v5_final.parquet` — global lemma counts across all
  titles. 27,804 unique lemmas.
- `data/bigram_model_v5_final.pkl` — trained gensim Phraser. 447 bigrams
  learned (e.g. `differential_equation`, `machine_learning`,
  `neural_network`, `monte_carlo`).
- `data/subject_counts/XX_v5_final.pkl` — per-subject (year_word, year_total)
  cache, one file per subject, 63 subjects total.
- `data/word_year_subject_v5_final.parquet` — flat modeling table
  (word x subject x year). 445,666 rows, 27,804 unique words, 63 subjects.
- `data/subject_meta_v5_final.parquet` — subject code to name + title count
  lookup. Largest subjects by title count: Computer science (23,692),
  Game theory/economics/social sciences (17,700), Statistics (14,502).

**Filtering applied before tokenizing:**
- Only original (human-assigned) subject codes are kept, not model-predicted ones
- A custom academic-stopword list is dropped in addition to spaCy's default
  stopwords (e.g. study, method, model, research, theory, application, case),
  since these pass spaCy's filter but carry no topical signal in thesis titles
- Tokens: NOUN, ADJ, VERB, or PROPN (proper nouns only kept when they end up
  inside a bigram), min lemma length 4

**Sanity checks run on the saved output:**
- Words expected to survive filtering (e.g. `network`, `stochastic`, `markov`)
  are confirmed present with nonzero counts
- Top bigrams by total count: `differential_equation` (1,002),
  `time_series` (758), `high_dimensional` (751), `machine_learning` (602),
  `neural_network` (447)

**Modeling** (`model.ipynb`):
- Features: share_lag1, share_lag2, share_lag3, slope_3yr, slope_5yr, specificity
- Target: share at t+1
- Split: train < 2013, test 2013-2022 (time-based, no random split, try with different splits)
- Baseline: naive lag-1 (predict next year = this year)
- Preliminary models: Ridge regression (better), GradientBoostingRegressor (marginal loss)
- Leakage check: shuffled-target RMSE >> model RMSE -- clean
- Later will try better models or improved features
## Results (check notebook for up to date results)

| Metric | Baseline (lag-1) | Ridge | GBR |
|---|---|---|---|
| RMSE (test) | 0.007634 | 0.006281 | 0.006348 |
| MAE (test) | 0.004355 | 0.003623 | 0.003692 |

- Direction accuracy (test): 69.0%
- NDCG@all (test, per year): 0.958 mean
- NDCG@5 (2024 holdout, 60 subjects): 0.858 mean
- Direction accuracy (2024 holdout): 70.7%
- 3 subjects excluded from 2024 evaluation: insufficient 2024 titles (different for different years)

Key finding: Ridge beats GBR -- relationship is approximately linear. Lag features
dominate (lag2 highest coefficient). slope_3yr adds signal; specificity does not
predict share level but is useful for candidate filtering.

Model undershoots accelerating trends (deep learning surge post-2015) and misses
inflection points on declining words (privacy in CS).
