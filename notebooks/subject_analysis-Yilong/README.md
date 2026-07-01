# Subject Trend Analysis

This folder contains exploratory data analysis of subject trends in the Mathematics Genealogy Project dataset. The goal is to study how the distribution of PhD graduates across MSC subject areas changes over time, before moving to the advisor-student transition matrix analysis.

## Data

The notebook uses the processed dataset

```python
version2_new_dataset_fitted.csv
```

which contains both originally observed MSC subject codes and additional high-confidence predicted subject codes. The dataset has 338,532 total records. Among them, 280,203 records have a non-null `subject_code` after incorporating predicted subject information. The original-only subject subset has 202,492 records.

The main relevant columns are:

```text
id
name
thesis
school
country
year
advisors
students
subject_code
subject_name
predicted_subject_code
subject_prediction_confidence
subject_prediction_vector
```

The analysis focuses on records with non-missing subject code and PhD year between 1900 and 2026.

## Pure vs. Applied Classification

For this preliminary analysis, MSC subject codes are separated into two broad groups:

```text
Pure math:    subject_code <= 60
Applied math: subject_code >= 62
```

This gives:

```text
Pure math records, 1900–2026:    87,136
Applied math records, 1900–2026: 142,294
```

Within each group, the notebook computes yearly subject shares. For example, in the pure math section, the percentage for subject code 14 in a given year is:

```text
number of pure math PhD graduates with subject 14 in that year
/
total number of pure math PhD graduates in that year
```

Thus, the pure math percentages sum to 100% within pure math, and the applied math percentages sum to 100% within applied math.

## Methods

For each group, the notebook computes a subject-by-year count matrix using `pd.crosstab`, where rows are MSC subject codes and columns are years. This count matrix is then normalized column-wise to obtain yearly percentage distributions.

The notebook produces several visualizations:

1. **Heatmaps of subject percentages over time**
   These show how the full distribution of subject codes changes from 1900 to 2026.

2. **Top 10 recent subject trends**
   The top subjects are selected by average share over 2000–2025, then plotted as smoothed time series.

3. **Stacked area charts
These show the changing composition of the major subject areas, with smaller subjects grouped into “Other.”

A 5-year centered rolling average is used in several plots to smooth yearly fluctuations.

## Preliminary Findings

We find for both pure and applied math, subject precentages changed drastically before 1960, and stablizes after 1960. This may due to the low number of Ph.D. students before 1960.

### Pure Math

The top pure math subjects by recent average share, using the augmented dataset, are:

```text
60, 35, 11, 05, 14, 53, 37, 20, 03, 46
```
which are Probability, PDE, number theory, combinatorics, algebraic geometry,differential geometry, dynamical systems, group theory, mathematical logic, and functional analysis/operator theory.

The corresponding analysis using `data-new.json` gives a very similar top 10 list:

```text
60, 35, 05, 11, 14, 53, 37, 20, 03, 46
```

This suggests that the high-confidence subject imputation does not substantially change the identity of the leading recent pure math subjects.


The heatmap plot and stacked area chart show that several subjects rises in later 20th century: 60, 35, 03, 05; while the relative dominance of some early twentieth-century areas declines: 20, 51, 14, and some subjects are relatively stable: 11, 53. Some sharp behavior near the final years should be interpreted cautiously because recent MGP data may be incomplete and because some labels are model-imputed.

### Applied Math

The top applied math subjects by recent average share are:

```text
68, 62, 91, 65, 90, 94, 92, 76, 93, 81
```

The applied math distribution is dominated in recent decades by 68-computer science and 62-statistics. Code 68 rises strongly in the late twentieth century and becomes the largest applied subject by 2020. Code 62 is also a major recent category. Earlier in the twentieth century, the applied distribution is more heavily influenced by other applied categories, including code 91 and 92.

The stacked area chart suggests a broad shift in applied mathematics from older applied/natural science categories toward statistics, computer science, numerical analysis, operations research, and related modern applied fields.


## Next Steps

The next stage is to move from subject-share trends to subject mutation analysis. The planned object is a sequence of decade-indexed transition matrices:

```text
M(t)_{ij} = number of advisor-student edges in decade t
            where the advisor has subject i and the student has subject j
```

This will allow us to study:

```text
self-retention of subjects
inflows and outflows between subjects
dominant subject mutations
changes in transition structure over time
pure-to-applied and applied-to-pure movement
```

The current subject trend analysis provides the baseline marginal distributions needed before studying these advisor-student transitions.
