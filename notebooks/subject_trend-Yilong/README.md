# Subject Trend Analysis

This folder studies how the distribution of mathematics PhD graduates across MSC subject areas changes over time in the Mathematics Genealogy Project data.

There are 63 distinct MSC subjects, ranging from 00 to 97 nonconsecutively, according to according to the [2020 Mathematics Subject Classification](https://mathscinet.ams.org/msc/pdfs/classifications2020.pdf)

The analysis focuses on **subject shares**, rather than raw counts, because the number of recorded graduates varies substantially across years. Shares are computed within two broad baskets:

```text
Pure mathematics:    subject_code <= 60
Applied mathematics: subject_code >= 62
```

The workflow separates model fitting from interpretation:

1. exploratory analysis of historical subject shares;
2. model selection and short-term prediction;
3. plotting and trend interpretation using the saved prediction file.

We use data from **1960–2024**, and forecasts are produced for **2025–2027**. The year 2025 is treated as a provisional comparison point in the plotting notebook. The year 2026 is excluded from provisional plots because the available sample is too small.

---

## Notebooks

| Notebook | Purpose |
|---|---|
| `subject_EDA.ipynb` | Exploratory analysis of historical MSC subject counts and shares. |
| `model_selection_and_predict.ipynb` | Rolling-window cross-validation, model selection, and forecasts. |
| `subject_prediction_plots.ipynb` | Plots forecast results and ranks recent subject risers/decliners. |


---

## Data processing

For each year and subject, the notebooks compute:

```text
subject share within pure/applied mathematics
pure/applied basket ratio among all classified mathematics records
```

These produce 44 pure-subject share series, 19 applied-subject share series, and 1 pure/applied basket-ratio series. Our goal is to predict the short-term behavior of these time series. 

Initial tests on selected time series showed that Simple Exponential Smoothing (SES) performs reasonably well, so we treat it as a baseline model. In addition, we include Double Exponential Smoothing (Holt), Auto ARIMA, and ARIMA(0,1,1). Note that the last one is closely related to SES, but it is formulated as a statistical time-series model.

## Model-selection notebook

`model_selection_and_predict.ipynb` performs rolling-window cross-validation on annual subject-share series from 1960 through 2024.

The validation design is:

```text
Training window: 20 years
Forecast horizon: 3 years
Step size:        3 years
```

For each subject, the model with the lowest mean cross-validation MSE receives one vote. The model with the largest total vote is selected separately.

The selected models are:

| Forecast component          | Selected model |
| --------------------------- | -------------- |
| Pure-math subject shares    | Damped Holt    |
| Applied-math subject shares | ARIMA(0,1,1)   |
| Pure/applied basket ratio   | ARIMA(0,1,1)   |


Final forecasts are fitted using the most recent 20 completed years, 2005–2024.
<img width="1288" height="690" alt="image" src="https://github.com/user-attachments/assets/92a99e6f-352b-442b-a09c-d2379b8b40bf" />

<img width="1285" height="690" alt="image-1" src="https://github.com/user-attachments/assets/2598812c-4b58-4060-8f98-2df4ce36e733" />

<img width="1283" height="690" alt="image-2" src="https://github.com/user-attachments/assets/6e5b4fc0-89f4-4854-bc2f-13b0c179ff0c" />

The complete forecast table is exported as:

```text
outputs/subject_trend_predictions/subject_prediction_forecasts.csv
```

## Fast-rising and fast-declining subjects

In the `subject_prediction_plots.ipynb` notebook, we compute the slope of each share series over 2010-2024, and use the weighted least-square method to fit the trend, where the weights are the number of classified records in the relevant basket.

We select top 5 risers and decliners within each pure/applied math basket:


<img width="989" height="590" alt="image-3" src="https://github.com/user-attachments/assets/4791d764-304d-40e8-b30a-a7accb3f58f6" />
<img width="989" height="590" alt="image-4" src="https://github.com/user-attachments/assets/7b47a9bf-cca1-4802-9d5c-475023803298" />

<img width="989" height="590" alt="image-5" src="https://github.com/user-attachments/assets/87e34bf3-d1fd-496d-8a8b-9cb1e0bf52f5" />
<img width="989" height="590" alt="image-6" src="https://github.com/user-attachments/assets/99f7434e-33c3-459f-8522-7af74a63d685" />


In addition, we compute each subject's share among all math subjects, and find the top 5 risers/decliners:
<img width="989" height="590" alt="image-7" src="https://github.com/user-attachments/assets/01ae7623-808a-4210-b8ae-230c94101d1b" />
<img width="989" height="590" alt="image-8" src="https://github.com/user-attachments/assets/ff8ae0dc-b764-4db4-9a23-39f51be1e49e" />



---
Among the top five all-math risers, three are pure-math subjects and two are applied-math subjects. This agrees with the within-basket riser rankings. In contrast, the top five all-math decliners all come from applied math, and this list differs from the top five decliners within the applied-math basket. This occurs because the applied math basket share declines over 2010-2024. For example, subject 68, Computer Science, is the second-largest decliner among all math subjects, even though its share within applied math is approximately flat.

