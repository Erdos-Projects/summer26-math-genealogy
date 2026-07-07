# KPIs

Target: `dshare = share(t+1) - share(t)`, the change in a word's share of
subject title-words from one year to the next, for words already flagged as
rising by the EDA method.

## Primary KPI

**RMSE (root mean squared error) on `dshare`, test window only.**

```
RMSE = sqrt( mean( (y_true - y_pred)^2 ) )
```

- Direction: lower is better.
- Why primary: directly measures how close predicted share-change is to
  actual share-change, the core forecasting task. Squaring penalizes large
  misses more, which matters here since a few subjects have large swings
  (e.g. deep_learning post-2015) that a useful model should not miss badly.

## Secondary KPIs

**MAE (mean absolute error) on `dshare`.**

```
MAE = mean( |y_true - y_pred| )
```

- Direction: lower is better.
- Why: RMSE alone can be dominated by a handful of outlier subject-years.
  MAE gives a more robust, less outlier-sensitive read on typical error size.

**Direction accuracy.**

```
dir_acc = mean( sign(y_pred) == sign(y_true) ), over rows where y_true != 0
```

- Direction: higher is better (ceiling 100%).
- Why: for a watchlist use case, getting the direction right (word is
  rising vs falling) is often more actionable than the exact magnitude.

**NDCG on change, per subject-year.**

```
NDCG@k = DCG@k / IDCG@k
DCG@k  = sum_i ( rel_i / log2(i + 1) )   for the top-k ranked items
```
where `rel_i` is the (shifted to non-negative) true `dshare` of the word
ranked `i`-th by the model's predicted `dshare`, within one subject-year.

- Direction: higher is better (ceiling 1.0).
- Why: the practical output of this project is a ranked watchlist per
  subject, not a single global number. NDCG measures whether the model
  puts the right words near the top, which RMSE/MAE do not directly capture.

## Baseline definitions

All models below are evaluated on the identical leak-free feature panel and
test window, so comparisons are apples to apples.

| Model | Type | Description |
|---|---|---|
| `DummyRegressor` (mean) | Trivial | Predicts the training-set mean `dshare` for every row |
| Zero-change | Trivial (domain) | Predicts `dshare = 0` (persistence: next year = this year) |
| Momentum | Domain baseline | Predicts `dshare = slope_3yr` |
| Ridge (weighted) | Linear | Ridge regression, standardized features, sample-weighted by next-year volume |
| HistGBR (weighted) | Tree-based | Histogram gradient boosting, sample-weighted by next-year volume |

## Improvement direction summary

| KPI | Direction | Beats trivial means |
|---|---|---|
| RMSE | lower is better | model RMSE < zero-change RMSE |
| MAE | lower is better | model MAE < zero-change MAE |
| Direction accuracy | higher is better | model dir_acc > 50% (coin flip) and > momentum's dir_acc |
| NDCG on change | higher is better | model NDCG > momentum's NDCG |

A model that cannot beat both zero-change (trivial) and momentum (domain
baseline) on RMSE and direction accuracy is not adding value over simpler
rules, regardless of how it looks in isolation.
