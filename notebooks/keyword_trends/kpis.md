# KPIs

Target: `dshare = share(t+1) - share(t)` on the 2-year bin axis, the change in a
word's share of subject title-words from one bin to the next, for words already
flagged as rising by the EDA method.

All metrics are on the bin axis, so they are not directly comparable to a
single-calendar-year setup: a 2-year change is smoother, which lowers absolute
error. Compare against the binned baselines, not against yearly numbers.

## Primary KPI

**RMSE (root mean squared error) on `dshare`, test window only.**

```
RMSE = sqrt( mean( (y_true - y_pred)^2 ) )
```

- Direction: lower is better.
- Why primary: directly measures how close predicted share-change is to actual
  share-change, the core forecasting task. Squaring penalizes large misses more,
  which matters since a few subjects have large swings a useful model should not
  miss badly.

## Secondary KPIs

**MAE (mean absolute error) on `dshare`.**

```
MAE = mean( |y_true - y_pred| )
```

- Direction: lower is better.
- Why: RMSE can be dominated by a handful of outlier subject-bins. MAE gives a
  more robust, less outlier-sensitive read on typical error size.

**Direction accuracy.**

```
dir_acc = mean( sign(y_pred) == sign(y_true) ), over rows where y_true != 0
```

- Direction: higher is better (ceiling 100%).
- Why: for a watchlist, getting the direction right (word rising vs falling) is
  often more actionable than the exact magnitude.
- Note: zero-change predicts exactly 0, and `sign(0)` matches neither `+1` nor
  `-1`, so it scores 0% by construction, not by failure. Its RMSE/MAE are the
  real bar.

**NDCG on change, per subject-bin.**

```
NDCG@k = DCG@k / IDCG@k
DCG@k  = sum_i ( rel_i / log2(i + 1) )   for the top-k ranked items
```
where `rel_i` is the (shifted to non-negative) true `dshare` of the word ranked
`i`-th by the model's predicted `dshare`, within one subject-bin.

- Direction: higher is better (ceiling 1.0).
- Why: the practical output is a ranked watchlist per subject, not a single
  global number. NDCG measures whether the model puts the right words near the
  top, which RMSE/MAE do not directly capture. It rewards correct ranking even
  when magnitudes are off, so read it as ranking quality, not accuracy.

## Baseline definitions

All models are evaluated on the identical leak-free feature panel and test
window, so comparisons are apples to apples.

| Model | Type | Description |
|---|---|---|
| DummyRegressor (mean) | Trivial | Predicts the training-set mean `dshare` for every row |
| Zero-change | Trivial (domain) | Predicts `dshare = 0` (persistence: next bin = this bin) |
| Momentum | Domain baseline | Predicts `dshare = slope_3yr` (3-bin slope) |
| Ridge (weighted) | Linear | Ridge regression, standardized features, sample-weighted by next-bin volume |
| HistGBR (weighted) | Tree-based | Histogram gradient boosting, sample-weighted by next-bin volume |

## Measured values (final test window)

| KPI | Dummy (mean) | Zero-change | Momentum | Ridge (weighted) | HistGBR (weighted) |
|---|---|---|---|---|---|
| RMSE | 0.008161 | 0.008158 | 0.010534 | **0.006698** | 0.006894 |
| MAE | 0.004741 | 0.004718 | 0.006330 | **0.004298** | 0.004316 |
| Direction acc | 48.0% | 0.0% | 34.3% | 64.1% | **64.8%** |
| NDCG on change | 0.808 | 0.808 | 0.719 | **0.900** | 0.894 |

Ridge and HistGBR are effectively tied; Ridge leads on RMSE/MAE/NDCG, HistGBR on
direction accuracy. Ridge is the primary model for simplicity and interpretable
coefficients.

Additional leakage checks on the final split:
- Shuffled-target RMSE = 0.008176 (>= zero-change RMSE 0.008158, as required).
- Clean vs full-window candidate overlap = 112/460 (24%).

## Improvement direction summary

| KPI | Direction | Beats trivial means |
|---|---|---|
| RMSE | lower is better | model RMSE < zero-change RMSE |
| MAE | lower is better | model MAE < zero-change MAE |
| Direction accuracy | higher is better | model dir_acc > 50% (coin flip) and > momentum's dir_acc |
| NDCG on change | higher is better | model NDCG > momentum's NDCG |

A model that cannot beat both zero-change (trivial) and momentum (domain
baseline) on RMSE and direction accuracy is not adding value over simpler rules,
regardless of how it looks in isolation. Ridge clears both on the binned data.