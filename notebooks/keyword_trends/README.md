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

- **Language:** titles are filtered to English using fastText lid.176, keeping
  208,150 of 234,743 titles (88.7%). fastText was chosen over langdetect after
  manual inspection showed langdetect misread short English titles.
- **Year window:** 1950-2023. Pre-1950 is too sparse; 2024+ has data-entry lag
  (confirmed by drop in title counts). Subject-years with fewer than 50 total
  title words are excluded.

## Method

**Tokenizer** (`build_parquets.ipynb`, `eda.ipynb`):
- Strip accents via `unicodedata.normalize("NFD")` before tokenizing
- spacy `en_core_web_sm` with parser and NER disabled (tagger only)
- Keep NOUN, ADJ, VERB, PROPN; drop spacy stopwords; min lemma length 4
- Bigram detection via gensim Phrases (min_count=30, threshold=15) to capture
  phrases like `hilbert_scheme`, `machine_learning`

**Rising-word detection** (`eda.ipynb`):
- Per-subject word share = word token count / total title tokens per year
- Specificity filter: subject share / global share >= 1.5 (removes generic terms)
- Rising score: linear slope over recent 10-year window, weighted by specificity
  and penalized by global frequency (enriched score)
- Deduplication: prefix-based lemma dedup to remove learn/learning collisions
- Output: top 10 rising words per subject, 592 words across 63 subjects

**Pipeline outputs** (`build_parquets.ipynb`):
- `data/global_counts.parquet` — global lemma counts
- `data/bigram_model.pkl` — trained gensim Phraser
- `data/subject_counts/XX.pkl` — per-subject (year_word, year_total) cache
- `data/word_year_subject.parquet` — flat modeling table (word x subject x year)
- `data/subject_meta.parquet` — subject code to name lookup

**Modeling** (`model.ipynb`):
- Features: share_lag1, share_lag2, share_lag3, slope_3yr, slope_5yr, specificity
- Target: share at t+1
- Split: train < 2013, test 2013-2022 (time-based, no random split)
- Baseline: naive lag-1 (predict next year = this year)
- Models: Ridge regression (winner), GradientBoostingRegressor (marginal loss)
- Leakage check: shuffled-target RMSE >> model RMSE -- clean

## Results

| Metric | Baseline (lag-1) | Ridge | GBR |
|---|---|---|---|
| RMSE (test) | 0.007634 | 0.006281 | 0.006348 |
| MAE (test) | 0.004355 | 0.003623 | 0.003692 |

- Direction accuracy (test): 69.0%
- NDCG@all (test, per year): 0.958 mean
- NDCG@5 (2024 holdout, 60 subjects): 0.858 mean
- Direction accuracy (2024 holdout): 70.7%
- 3 subjects excluded from 2024 evaluation: insufficient 2024 titles

Key finding: Ridge beats GBR -- relationship is approximately linear. Lag features
dominate (lag2 highest coefficient). slope_3yr adds signal; specificity does not
predict share level but is useful for candidate filtering.

Model undershoots accelerating trends (deep learning surge post-2015) and misses
inflection points on declining words (privacy in CS).

## Status

- [x] Tokenization with accent stripping, POS filter, bigrams
- [x] Per-subject rising-word detection with specificity and enriched score
- [x] Per-subject trend plots and cross-subject heatmap
- [x] Feature engineering (lag + slope features)
- [x] Ridge and GBR modeling with leakage check
- [x] 2024 holdout evaluation (NDCG, direction accuracy, biggest misses)
- [x] Watchlist saved to `data/watchlist_2024.csv`
- [ ] Rerun build_parquets with bigrams (in progress -- deleted old pkl files)
- [ ] Rerun EDA and modeling with bigram vocabulary
- [ ] VAR model for correlated word clusters
- [ ] ARIMA baseline comparison

## Resuming later

1. Check `build_parquets.ipynb` finished (sanity check cell shows bigram tokens)
2. Rerun `eda.ipynb` from the multi-subject loop cell onwards
3. Rerun `model.ipynb` from scratch with new vocabulary
4. Compare NDCG with and without bigrams