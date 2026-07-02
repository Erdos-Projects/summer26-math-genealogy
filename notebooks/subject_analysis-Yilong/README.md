# Subject Trend Analysis and Forecasting

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas has changed over time. The analysis consists of three parts:

1. exploratory analysis of historical subject trends;
2. initial time-series modeling for Algebraic Geometry;
3. time-series cross-validation for evaluating forecast stability.

## Notebooks

| Notebook                                           | Purpose                                                                                                  |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`subject_EDA.ipynb`](subject_EDA.ipynb)           | Examines long-term changes in the counts and percentage shares of pure and applied mathematics subjects. |
| [`subject_predict.ipynb`](subject_predict.ipynb)   | Fits several forecasting models to MSC subject 14, Algebraic Geometry.                                   |
| [`cross_validation.ipynb`](cross_validation.ipynb) | Compares the models using rolling- and expanding-window time-series cross-validation.                    |

## Data

The notebooks use:

```text
data/processed/version2_new_dataset_fitted.csv
```

The dataset contains 338,532 records, of which 280,203 have a non-null subject code after incorporating high-confidence predicted subject codes.

For this preliminary analysis, subjects are divided into:

```text
Pure mathematics:    subject_code <= 60
Applied mathematics: subject_code >= 62
```

For each subject and year, the notebooks calculate both:

* the number of PhD graduates;
* the percentage of graduates within pure or applied mathematics.

Counts measure the absolute size of a subject, whereas percentages measure its relative position within the corresponding group.

---

## 1. Exploratory Data Analysis

The EDA notebook constructs subject-by-year count tables with `pd.crosstab` and normalizes them by yearly totals to obtain percentage shares. A centered five-year rolling average is used to reduce short-term variation.

The main visualizations are:

* heatmaps of subject percentages from 1900 to 2026;
* trend plots for the ten largest recent subjects;
* stacked area charts showing changes in the overall subject distribution.

The leading recent pure-mathematics subjects are:

```text
60, 35, 11, 05, 14, 53, 37, 20, 03, 46
```

These include Probability, PDE, Number Theory, Combinatorics, Algebraic Geometry, Differential Geometry, Dynamical Systems, Group Theory, Mathematical Logic, and Functional Analysis.

The pure-mathematics plots suggest later growth in subjects such as Probability, PDE, Logic, and Combinatorics, together with declining relative shares for some historically large subjects such as Group Theory and Algebraic Geometry.

The applied-mathematics distribution is increasingly dominated by:

```text
68 — Computer Science
62 — Statistics
```

Overall, the applied distribution shifts toward computer science, statistics, numerical analysis, operations research, and related modern fields.

Percentages fluctuate strongly before approximately 1960, partly because relatively few graduates are recorded in the early years. Changes near the end of the series should also be interpreted cautiously because recent MGP records may be incomplete.

---

## 2. Initial Forecasting Models

The modeling notebook uses MSC subject 14, Algebraic Geometry, as a case study. It separately models:

* annual graduate counts;
* annual percentage shares within pure mathematics.

Five models are fitted using a chronological training and testing split:

1. simple exponential smoothing;
2. double exponential smoothing;
3. linear trend;
4. ARIMA(0,0,2);
5. Auto ARIMA.

For the single holdout period, Auto ARIMA gives the lowest count MSE:

| Best count model |    MSE |
| ---------------- | -----: |
| Auto ARIMA       | 558.55 |

Double exponential smoothing gives the lowest percentage-share MSE:

| Best share model             |   MSE |
| ---------------------------- | ----: |
| Double exponential smoothing | 0.934 |

These results show that counts and percentages may favor different models. However, one holdout period is not sufficient for reliable model selection, since the ranking may depend strongly on the selected test years.

---

## 3. Time-Series Cross-Validation

The cross-validation notebook evaluates the models over multiple historical forecasting periods while preserving chronological order. The model set is expanded to six specifications:

```text
Simple exponential smoothing
Holt optimized
Holt damped
Linear trend
ARIMA(0,0,2)
Auto ARIMA
```

Performance is measured using MSE, RMSE, MAE, and MASE.

### Five-Year Forecasts

Two validation designs are compared:

* a **40-year rolling window**, which discards older observations;
* an **expanding window beginning with 80 years**, which retains all previous observations.

For subject 14, the best models vary by validation design:

| Validation design      | Counts      | Percentage shares            |
| ---------------------- | ----------- | ---------------------------- |
| 40-year rolling window | Auto ARIMA  | Simple exponential smoothing |
| Expanding window       | Holt damped | Simple exponential smoothing |

For counts, all models have mean MASE above 1 in the five-year analyses, meaning that they do not consistently outperform a naive benchmark. Percentage-share forecasts perform better relative to the benchmark, with simple exponential smoothing producing the strongest and most stable overall results.

### One-Year Forecasts

The notebook also tests one-year-ahead forecasting. For the expanding-window percentage analysis, simple exponential smoothing again performs best, with mean MASE well below 1.

### All Pure-Mathematics Subjects

The same cross-validation pipeline is applied to all 44 pure-mathematics subject-share series. The best model differs across subjects, but the Simple exponential smoothing outperforms overall.

---

## Next Step

The next stage is to study advisor-student subject transitions using decade-indexed matrices:

```text
M(t)[i,j] = number of advisor-student relationships in decade t
            where the advisor has subject i
            and the student has subject j
```

This will allow the project to examine subject retention, migration between fields, inflows and outflows, and changes in the structure of mathematics across generations.