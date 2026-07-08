# Subject Trend Analysis and Forecasting

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas has changed over time. The analysis has two stages:

1. exploratory analysis of historical subject trends;
2. rolling-window cross-validation and forecasting for all pure- and applied-mathematics subjects.

## Notebooks

| Notebook                                           | Description                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------- |
| [`subject_EDA.ipynb`](subject_EDA.ipynb)           | Visualizes historical changes in subject counts and percentage shares.    |
| [`cross_validation.ipynb`](cross_validation.ipynb) | Selects forecasting models and produces coherent forecasts for 2025–2027. |

## Data

The notebooks use:

```text
data/processed/version2_new_dataset_fitted.csv
```

The dataset contains 338,532 mathematicians. The cross-validation notebook retains the 202,492 records with originally observed subject codes and excludes predicted subject assignments. 

Subjects are divided into two baskets:

```text
Pure mathematics:    subject_code <= 60
Applied mathematics: subject_code >= 62
```

For each subject and year, the analysis calculates:

* the number of PhD graduates;
* the subject’s percentage share within its pure- or applied-mathematics basket.

Counts measure the absolute size of a subject, while shares measure its relative size within the corresponding basket.

---

## 1. Exploratory Data Analysis

The EDA notebook constructs subject-by-year count and percentage matrices. A centered five-year rolling average is used to reduce short-term fluctuations.

The main visualizations include:

* heatmaps of historical subject shares;
* trend plots for the largest recent subjects;
* stacked area charts showing changes in the overall subject distribution.

The recent pure-mathematics distribution is led by subjects such as Probability, Partial Differential Equations, Number Theory, Combinatorics, Algebraic Geometry, and Differential Geometry.

The applied-mathematics distribution has increasingly shifted toward Computer Science, Statistics, Numerical Analysis, Operations Research, and related modern fields.

Early-year percentages are unstable because relatively few graduates are recorded. Apparent declines near the end of the dataset should also be interpreted cautiously because recent Mathematics Genealogy Project records may be incomplete.

---

## 2. Rolling-Window Cross-Validation

The cross-validation analysis uses annual observations from **1960 through 2024**. We chose this range because the data are more complete and stable during this period.

The main validation design uses:

```text
Training window:   20 years
Forecast horizon:   3 years
Step size:          3 years
```

Every fold trains on the preceding 20 years and predicts the following three years. One-year and five-year horizons are also examined for Algebraic Geometry.

Seven forecasting specifications are compared:

1. simple exponential smoothing with fixed alpha = 0.5;
2. optimized simple exponential smoothing;
3. optimized Holt linear trend;
4. damped Holt trend;
5. linear regression on year;
6. ARIMA(0,1,1);
7. Auto ARIMA.

Note that ARIMA(0,1,1) is mathematically equivalent to simple exponential smoothing, and the latter one is performs well in preliminary tests.

Performance is evaluated using MSE, RMSE, MAE, and MASE. Mean MSE is used for final model selection.

### Model Selection Across Subjects

The cross-validation pipeline is applied separately to:

* 44 pure-mathematics subjects;
* 19 applied-mathematics subjects;
* annual pure-mathematics basket totals;
* annual applied-mathematics basket totals.

For each subject, the model with the lowest mean MSE receives one vote. A tied subject divides its vote equally among the tied models.

The selected models are:

| Forecast component          | Selected model |
| --------------------------- | -------------- |
| Pure-math subject shares    | Damped Holt    |
| Applied-math subject shares | ARIMA(0,1,1)   |
| Pure-math basket total      | Auto ARIMA     |
| Applied-math basket total   | ARIMA(0,1,1)   |

Direct count forecasts are also evaluated as benchmarks. Fixed-alpha simple exponential smoothing wins the largest number of direct-count series in both baskets. However, direct count models are not used for the final forecasts because independently forecasted subject counts would not necessarily add up to the total number of graduates.

---

## 3. Coherent Forecasts for 2025–2027

The final models are fitted using the most recent 20 years, **2005–2024**, matching the rolling cross-validation window.

The forecasting procedure is:

1. Forecast every subject’s percentage share.
2. Replace negative share forecasts with zero.
3. Normalize the shares so that they sum to 100% within each basket.
4. Forecast the total number of pure- and applied-mathematics graduates.
5. Derive subject counts using

```text
subject count = subject share × basket total / 100
```

This guarantees that:

* both pure-mathematics and shares sum to 100%;
* derived subject counts sum exactly to their forecasted basket total.

(Note that we still added separate count series prediction in the notebook as a comparison.)

The forecasted pure-mathematics total increases from approximately **1,638 graduates in 2025** to **1,707 in 2027**. The applied-mathematics total remains approximately **1,535 graduates per year** under the selected model.

The five largest forecasted pure-mathematics subjects are:

```text
35 — Partial differential equations
11 — Number theory
14 — Algebraic geometry
60 — Probability theory and stochastic processes
05 — Combinatorics
```
Their percentages among pure math subjects are shown below:

<img width="1491" height="790" alt="pure_math_share_predict" src="https://github.com/user-attachments/assets/97d10fbd-03a7-411b-ab09-d9ef611b844b" />
We predict in 2027, subject 35 has share 10.56%, subject 11 has share 9.18%, subject 14 has share 8.83%, subject 60 has share 8.30%, subject 05 has share 8.29%.

The five largest forecasted applied-mathematics subjects are:

```text
68 — Computer science
62 — Statistics
65 — Numerical analysis
90 — Operations research and mathematical programming
91 — Game theory, economics, and social sciences
```
Their percentages among applied math subjects are shown below:
<img width="1491" height="790" alt="applied_math_counts_predict" src="https://github.com/user-attachments/assets/ce9393e9-e673-4e4a-8315-3226cca22b2c" />
We predict in 2027, subject 68 has share 32.28%, subject 62 has share 21.76%, subject 65 has share 9.95%, subject 90 has share 6.27%, subject 91 has share 5.36%.

The total number of graduated students forecasts are shown below:
<img width="1491" height="790" alt="pure_math_counts_predict" src="https://github.com/user-attachments/assets/4d862e08-4b80-4be2-a57d-ba4530ac00b0" />
<img width="1491" height="790" alt="applied_math_share_predict" src="https://github.com/user-attachments/assets/43d69263-a845-4f9e-95cf-2cc5d348ab7f" />

The complete forecast table is exported as:

```text
all_subject_share_and_derived_count_forecasts_2025_2027.csv
```
<!--
## 4. Overall conclusions

Taken together, these four figures suggest that the short-term forecasts are driven more by **continuation of recent structure** than by large changes in ranking.

- In **pure mathematics**, the top subjects remain relatively close to one another, with Subject 35-Partial Differential Equations leading and Subjects 11-Number Theory and 14-Algebraic Geometry gradually strengthening.
- In **applied mathematics**, Subject 68-Computer Science remains dominant, followed by Subject 62-Statistics, while the remaining top subjects stay much smaller.
- The forecast horizon is short (2025–2027), so these plots should be interpreted as **near-term extrapolations** rather than long-run predictions.
- Because the final workflow forecasts shares and totals separately, the resulting count forecasts are internally consistent and easier to interpret than independently forecasted subject counts.

These figures therefore provide a compact visual summary of the final forecasting pipeline and its main substantive conclusions.
-->
