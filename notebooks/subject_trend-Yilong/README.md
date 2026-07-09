# Subject Trend Analysis

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas changes over time in the Mathematics Genealogy Project data.

The analysis focuses on **subject shares**, rather than raw counts, because the number of recorded graduates varies substantially across years. Shares are computed within two broad baskets:

```text
Pure mathematics:    subject_code < 61
Applied mathematics: subject_code > 61
```

The workflow separates model fitting from interpretation:

1. exploratory analysis of historical subject shares;
2. model selection and short-term prediction;
3. plotting and trend interpretation using the saved prediction file.

The main forecasting period is **1960–2024**, and forecasts are produced for **2025–2027**. The year 2025 is treated as a provisional comparison point in the plotting notebook. The year 2026 is excluded from provisional plots because the available sample is too small.

---

## Notebooks

| Notebook | Purpose |
|---|---|
| `subject_EDA.ipynb` | Exploratory analysis of historical MSC subject counts and shares. |
| `model_selection_and_predict.ipynb` | Rolling-window cross-validation, model selection, and compact forecast export. |
| `subject_prediction_plots.ipynb` | Plots forecast results, compares provisional 2025 data, and ranks recent subject risers/decliners. |

Run the notebooks in this order:

```text
subject_EDA.ipynb
model_selection_and_predict.ipynb
subject_prediction_plots.ipynb
```

The plotting notebook depends on the compact CSV produced by the model-selection notebook.

---

## Data

The notebooks use:

```text
data/processed/version2_new_dataset_fitted.csv
```

Only records with originally observed subject codes are used for the main analysis. Predicted/imputed subject labels are excluded when the column `predicted_subject_code` is available.

For each year and subject, the notebooks compute:

```text
subject count
subject share within pure/applied mathematics
pure/applied basket ratio among all classified mathematics records
```

Working with shares helps reduce the effect of year-to-year changes in the total number of recorded MGP entries.

---

## Model-selection notebook

`model_selection_and_predict.ipynb` performs rolling-window cross-validation on annual subject-share series from 1960 through 2024.

The validation design is:

```text
Training window: 20 years
Forecast horizon: 3 years
Step size:        3 years
```

The reduced model set compares a small number of simple forecasting methods:

```text
SES optimized
Holt damped trend
ARIMA(0,1,1)
Auto ARIMA
```

A switch in the notebook can disable Auto ARIMA for a faster three-model version:

```python
USE_AUTO_ARIMA = False
```

For each subject, the model with the lowest mean cross-validation MSE receives one vote. Ties are divided equally across tied models. The model with the largest total vote is selected separately for:

```text
pure-math subject shares
applied-math subject shares
pure/applied basket ratio
```

Final forecasts are fitted using the most recent 20 completed years, 2005–2024.

---

## Compact prediction output

The model-selection notebook exports one compact CSV:

```text
outputs/subject_trend_predictions/subject_prediction_forecasts.csv
```

This file contains only forecasted values:

| Column | Meaning |
|---|---|
| `record_type` | Either `subject_share_forecast` or `basket_ratio_forecast`. |
| `basket` | `Pure` or `Applied`. |
| `subject_code` | Two-digit MSC subject code for subject-share forecasts. |
| `year` | Forecast year. |
| `value_percent` | Forecast percentage. |
| `model` | Selected model used for the forecast. |

Historical and provisional observations are not exported. They are reconstructed directly from `version2_new_dataset_fitted.csv` in the plotting notebook. This keeps the output folder small and avoids committing large derived tables.

---

## Forecasting logic

Subject forecasts are computed within each basket. For example, a pure-math subject share is interpreted as

$$
P(\text{subject}=s \mid \text{pure mathematics}).
$$

The pure/applied basket ratio is forecast separately:

$$
P(\text{pure mathematics} \mid \text{all mathematics}),
\qquad
P(\text{applied mathematics} \mid \text{all mathematics}).
$$

This gives a hierarchical decomposition:

```text
All mathematics
├── Pure-math basket ratio
│   └── Subject shares within pure mathematics
└── Applied-math basket ratio
    └── Subject shares within applied mathematics
```

For a pure subject \(s\), its reconstructed share among all mathematics is

$$
P(s \mid \text{all mathematics})
=
P(s \mid \text{pure mathematics})
P(\text{pure mathematics} \mid \text{all mathematics}).
$$

In percentage form:

$$
\text{overall subject share}
=
\frac{
\text{within-basket subject share}
\times
\text{basket ratio}
}{100}.
$$

This makes it possible to distinguish two questions:

1. Is a subject rising within pure or applied mathematics?
2. Is the subject rising among all mathematics subjects after accounting for the changing pure/applied ratio?

---

## Plotting and trend notebook

`subject_prediction_plots.ipynb` loads:

```text
data/processed/version2_new_dataset_fitted.csv
outputs/subject_trend_predictions/subject_prediction_forecasts.csv
```

It reconstructs historical and provisional shares, then produces:

1. pure/applied basket-ratio plots;
2. top-five largest subjects within each basket;
3. fastest recent observed risers and decliners within each basket;
4. reconstructed all-math subject shares;
5. fastest recent observed risers and decliners among all mathematics;
6. trajectory plots for the all-math risers and decliners.

The riser/decliner rankings are based on observed data from 2010–2024, not on forecast slopes.

For each subject, the notebook fits a weighted linear trend:

$$
\text{share}_{s,t}=\alpha_s+\beta_s t+\varepsilon_{s,t}.
$$

The reported trend is

$$
10\beta_s,
$$

interpreted as percentage-point change per decade. Years are weighted by the number of classified records in the relevant basket, or by the total number of classified records for the all-math analysis.

Forecast curves are shown only as visual comparisons. They are not used to define the fastest risers or decliners.

---

## Interpreting the results

The analysis intentionally keeps three ideas separate.

### 1. Within-basket share

This asks:

```text
Which subjects are gaining or losing share inside pure or applied mathematics?
```

For example, a subject may be rising within applied mathematics even if applied mathematics as a whole is shrinking relative to all mathematics.

### 2. Pure/applied basket ratio

This asks:

```text
Is pure or applied mathematics becoming a larger share of all classified mathematics records?
```

This ratio is important because it affects every subject's overall-math share.

### 3. All-math subject share

This asks:

```text
Which subjects are gaining or losing share among all mathematics subjects?
```

A subject can have different within-basket and all-math trends. For instance, a large applied subject can decline among all mathematics if the applied basket itself declines, even if the subject is stable or slightly rising within applied mathematics.

---

## Notes and cautions

- The forecasts are short-term extrapolations for 2025–2027.
- The 2025 MGP data are shown only as provisional comparison points.
- The 2026 data are excluded from provisional plots because the current number of classified records is too small.
- Recent trends are descriptive and should not be interpreted causally.
- Subject-share forecasts are normalized so that pure-math shares sum to 100% within pure mathematics, and applied-math shares sum to 100% within applied mathematics.
- All-math subject shares are reconstructed by combining within-basket subject shares with the pure/applied basket ratio.

---

## Main output

The main file produced by this folder is:

```text
outputs/subject_trend_predictions/subject_prediction_forecasts.csv
```

This compact file is enough to reproduce the forecast plots when combined with the original fitted dataset.
