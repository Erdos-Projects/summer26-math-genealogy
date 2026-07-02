# Subject Trend Analysis and Forecasting

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas has changed over time. The analysis contains three stages:

1. exploratory data analysis of historical subject trends;
2. initial time-series modeling for Algebraic Geometry;
3. time-series cross-validation and model selection across all pure-mathematics subjects.

## Notebooks

| Notebook                                           | Description                                                                                       |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [`subject_EDA.ipynb`](subject_EDA.ipynb)           | Examines long-term changes in subject counts and percentage shares.                               |
| [`subject_predict.ipynb`](subject_predict.ipynb)   | Fits several forecasting models to MSC subject 14, Algebraic Geometry.                            |
| [`cross_validation.ipynb`](cross_validation.ipynb) | Evaluates the models with time-series cross-validation and selects common models across subjects. |

## Data

The notebooks use:

```text
data/processed/version2_new_dataset_fitted.csv
```

The dataset contains 338,532 records, including originally observed MSC subject codes and additional high-confidence predicted codes.

For this preliminary analysis, subjects are divided into:

```text
Pure mathematics:    subject_code <= 60
Applied mathematics: subject_code >= 62
```

For each subject and year, the notebooks calculate:

* the annual number of PhD graduates;
* the percentage of graduates within pure or applied mathematics.

Counts describe the absolute size of a subject, while percentages describe its relative importance within the corresponding group.

---

## 1. Exploratory Data Analysis

The EDA notebook constructs subject-by-year count tables and normalizes them by yearly totals to obtain percentage shares. A centered five-year rolling average is used to reduce annual fluctuations.

The main visualizations include:

* heatmaps of subject percentages from 1900 to 2026;
* smoothed trends for the ten largest recent subjects;
* stacked area charts showing changes in the overall subject distribution.

The leading recent pure-mathematics subjects are:

```text
60, 35, 11, 05, 14, 53, 37, 20, 03, 46
```

These include Probability, Partial Differential Equations, Number Theory, Combinatorics, Algebraic Geometry, Differential Geometry, Dynamical Systems, Group Theory, Mathematical Logic, and Functional Analysis.

The pure-mathematics plots suggest later growth in subjects such as Probability, PDE, Logic, and Combinatorics, while the relative shares of some historically large subjects, including Group Theory and Algebraic Geometry, decline.

Recent applied mathematics is dominated by:

```text
68 — Computer Science
62 — Statistics
```

Overall, the applied distribution shifts toward computer science, statistics, numerical analysis, operations research, and related modern fields.

Early-year percentages are unstable because relatively few graduates are recorded before approximately 1960. Recent apparent declines should also be interpreted cautiously because the newest Mathematics Genealogy Project records may be incomplete.

---

## 2. Initial Time-Series Modeling

The modeling notebook uses MSC subject 14, Algebraic Geometry, as a case study. It separately models:

* annual graduate counts;
* annual percentage shares within pure mathematics.

The models are:

1. simple exponential smoothing;
2. Holt's double exponential smoothing;
3. linear trend;
4. ARIMA(0,0,2);
5. Auto ARIMA.

Using a single chronological train-test split, Auto ARIMA gives the lowest test MSE for counts, while Holt's method gives the lowest test MSE for percentage shares.

However, the result of one train-test split may depend strongly on the selected test years. Time-series cross-validation is therefore used for more reliable model comparison.

---

## 3. Time-Series Cross-Validation

The validation notebook compares six specifications:

```text
Simple exponential smoothing
Holt optimized
Holt damped
Linear trend
ARIMA(0,0,2)
Auto ARIMA
```

Simple exponential smoothing uses a fixed smoothing level of 0.5. The Holt models estimate their parameters from each training sample.

Performance is measured using:

* mean squared error;
* root mean squared error;
* mean absolute error;
* mean absolute scaled error.

Both expanding-window and fixed 40-year rolling-window validation are considered.

### Algebraic Geometry

For five-year forecasts using a 40-year rolling window:

| Target            | Lowest mean MSE              |
| ----------------- | ---------------------------- |
| Graduate counts   | Auto ARIMA                   |
| Percentage shares | Simple exponential smoothing |

For the percentage-share series, most models have a mean MASE below 1, indicating that they outperform the corresponding naive benchmark on average. The manually specified ARIMA(0,0,2) performs substantially worse.

For one-year percentage forecasts, simple exponential smoothing again has the lowest mean MSE and a mean MASE below 1.

These results differ from some of the single-split and expanding-window results, showing that model rankings depend on the forecast horizon and training-window design.

### Model Selection Across All Pure-Mathematics Subjects

The 40-year rolling-window analysis is extended to all 44 pure-mathematics subjects, using a five-year forecast horizon.

For each subject, the model with the lowest mean cross-validation MSE receives one vote. If models tie, the subject's vote is divided equally among them.

#### Count-Series Voting

| Model                        | Subjects won | Vote percentage |
| ---------------------------- | -----------: | --------------: |
| Simple exponential smoothing |           28 |           63.6% |
| Auto ARIMA                   |            9 |           20.5% |
| Holt damped                  |            3 |            6.8% |
| Holt optimized               |            2 |            4.5% |
| Linear trend                 |            2 |            4.5% |
| ARIMA(0,0,2)                 |            0 |            0.0% |

#### Percentage-Share Voting

| Model                        | Subjects won | Vote percentage |
| ---------------------------- | -----------: | --------------: |
| Simple exponential smoothing |           17 |           38.6% |
| Holt damped                  |           12 |           27.3% |
| Auto ARIMA                   |            5 |           11.4% |
| Holt optimized               |            5 |           11.4% |
| Linear trend                 |            5 |           11.4% |
| ARIMA(0,0,2)                 |            0 |            0.0% |

Based on the equal-subject voting procedure, **simple exponential smoothing is selected as the common forecasting model for both counts and percentage shares**.

This does not mean that simple exponential smoothing is the best model for every individual subject. Rather, it provides the strongest common baseline when all subjects are treated equally.