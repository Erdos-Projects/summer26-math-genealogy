# Subject Trend Analysis and Forecasting

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas has changed over time. The analysis has three stages:

1. exploratory analysis of historical subject trends;
2. initial time-series modeling using Algebraic Geometry as a case study;
3. rolling-window cross-validation and forecasting for all pure- and applied-mathematics subjects.

## Notebooks

| Notebook                                           | Description                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------- |
| [`subject_EDA.ipynb`](subject_EDA.ipynb)           | Visualizes historical changes in subject counts and percentage shares.    |
| [`subject_predict.ipynb`](subject_predict.ipynb)   | Tests several forecasting models on MSC 14, Algebraic Geometry.           |
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

## 2. Initial Forecasting Models

The initial modeling notebook uses MSC 14, Algebraic Geometry, as a case study. It models both:

* annual graduate counts;
* annual percentage shares within pure mathematics.

The candidate methods include exponential smoothing, a linear trend, a fixed ARIMA model, and Auto ARIMA.

A chronological train-test split shows that counts and percentage shares may favor different models. However, conclusions from one holdout period can depend strongly on the selected test years. The cross-validation notebook therefore evaluates models over multiple historical forecasting periods.

---

## 3. Rolling-Window Cross-Validation

The cross-validation analysis uses annual observations from **1960 through 2024**.

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

## 4. Coherent Forecasts for 2025–2027

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

* pure-mathematics shares sum to 100%;
* applied-mathematics shares sum to 100%;
* derived subject counts sum exactly to their forecasted basket total.

The forecasted pure-mathematics total increases from approximately **1,638 graduates in 2025** to **1,707 in 2027**. The applied-mathematics total remains approximately **1,535 graduates per year** under the selected model.

The five largest forecasted pure-mathematics subjects are:

```text
35 — Partial differential equations
11 — Number theory
14 — Algebraic geometry
60 — Probability theory and stochastic processes
05 — Combinatorics
```

The five largest forecasted applied-mathematics subjects are:

```text
68 — Computer science
62 — Statistics
65 — Numerical analysis
90 — Operations research and mathematical programming
91 — Game theory, economics, and social sciences
```

The complete forecast table is exported as:

```text
all_subject_share_and_derived_count_forecasts_2025_2027.csv
```

## Forecast Figures and Interpretation

The following figures summarize the final forecasting results for the top five pure-mathematics and applied-mathematics subjects. In each plot, the vertical dotted line marks the start of the forecast period, and the dashed extensions show the forecasts for 2025–2027.

The count forecasts are **coherent derived forecasts**: subject shares are forecast first, basket totals are forecast separately, and subject counts are then obtained by

\[
\text{subject count} = \frac{\text{subject share} \times \text{basket total}}{100}.
\]

This guarantees that the forecasted subject counts add up exactly to the forecasted total number of graduates in each basket.

### Top five pure mathematics subjects: counts

![Top five pure mathematics subjects: historical counts and coherent derived forecasts](top5_pure_counts_forecast.png)

This figure shows the historical counts and forecasted counts for the five largest pure-mathematics subjects: 35, 11, 14, 60, and 5.  
Several patterns are visible:

- **Subject 35 (Partial Differential Equations)** remains the largest pure subject in forecasted counts.
- **Subject 11 (Number Theory)** and **Subject 14 (Algebraic Geometry)** both show modest upward forecasts.
- **Subject 60 (Probability Theory and Stochastic Processes)** declines from its earlier peak and remains below Subject 35 in the forecast period.
- **Subject 5 (Combinatorics)** appears relatively stable, with only a slight upward movement.

Overall, the pure-mathematics forecasts suggest moderate growth or stability rather than dramatic structural change over 2025–2027.

### Top five pure mathematics subjects: shares

![Top five pure mathematics subjects: historical shares and forecasts](top5_pure_shares_forecast.png)

This figure shows the same five pure subjects in terms of their percentage share within pure mathematics.

- **Subject 35** keeps the largest forecasted share, at roughly around 10%.
- **Subjects 11 and 14** both continue a gradual upward trend.
- **Subject 60** shows a noticeable long-term decline in share relative to its earlier dominance.
- **Subject 5** remains fairly stable near the 8% range.

The share plot helps separate **relative importance** from raw counts. For example, a subject may rise in counts simply because the total number of pure-math graduates rises, but the share plot shows whether the subject is actually gaining or losing ground within pure mathematics.

### Top five applied mathematics subjects: counts

![Top five applied mathematics subjects: historical counts and coherent derived forecasts](top5_applied_counts_forecast.png)

This figure shows the historical and forecasted counts for the five largest applied-mathematics subjects: 68, 62, 65, 90, and 91.

- **Subject 68 (Computer Science)** remains by far the largest applied subject, although its forecasted counts are lower than its historical peak.
- **Subject 62 (Statistics)** remains the second-largest applied subject.
- **Subject 65 (Numerical Analysis)** stays clearly below 68 and 62 but remains well above 90 and 91.
- **Subjects 90 (Operations Research and Mathematical Programming)** and **91 (Game Theory, Economics, and Social Sciences)** are forecast to remain comparatively small and fairly stable.

The applied count forecasts suggest that the largest fields remain dominant, but recent declines in some subjects are projected to persist into the near future.

### Top five applied mathematics subjects: shares

![Top five applied mathematics subjects: historical shares and forecasts](top5_applied_shares_forecast.png)

This figure shows the top five applied subjects as shares within applied mathematics.

- **Subject 68** continues to dominate, with a forecasted share around the low 30% range.
- **Subject 62** remains second, with a share around the low 20% range.
- **Subject 65** stays near 10%.
- **Subjects 90 and 91** remain much smaller, around the 5–6% range.

Compared with the count plot, the share plot shows that the ranking of the largest applied subjects is quite stable. In particular, Computer Science and Statistics remain the two central applied areas in both absolute size and relative share.

### Overall interpretation

Taken together, these four figures suggest that the short-term forecasts are driven more by **continuation of recent structure** than by large changes in ranking.

- In **pure mathematics**, the top subjects remain relatively close to one another, with Subject 35 leading and Subjects 11 and 14 gradually strengthening.
- In **applied mathematics**, Subject 68 remains dominant, followed by Subject 62, while the remaining top subjects stay much smaller.
- The forecast horizon is short (2025–2027), so these plots should be interpreted as **near-term extrapolations** rather than long-run predictions.
- Because the final workflow forecasts shares and totals separately, the resulting count forecasts are internally consistent and easier to interpret than independently forecasted subject counts.

These figures therefore provide a compact visual summary of the final forecasting pipeline and its main substantive conclusions.
