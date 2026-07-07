# Mathematics Genealogy Data Cleaning and Subject Imputation

This notebook cleans a Mathematics Genealogy-style dataset and fills missing mathematical subject areas using a combination of thesis-title text classification and academic genealogy information.

## Overview

The notebook starts from a JSON dataset of mathematician nodes and converts it into a pandas DataFrame. Each row represents a mathematician and includes fields such as `id`, `name`, `thesis`, `school`, `country`, `year`, `subject`, `advisors`, and `students`.

The main goal is to produce a cleaned dataset in which missing subject codes and subject names are filled when the prediction confidence is sufficiently high.

## Input Data

The notebook reads:

```text
../../data/processed/data-new.json
```

The JSON file is expected to contain a `nodes` field, which is converted into the main DataFrame:

```python
tree = pd.DataFrame(data["nodes"])
```

The loaded dataset contains:

- **338,532 rows**
- **202,492 rows with original subject information**
- **136,040 rows with missing subject information**

## Main Workflow

### 1. Load and inspect the dataset

The notebook imports the required packages, loads the JSON file, converts the node data into a DataFrame, and inspects the first few rows.

Important columns include:

- `id`
- `name`
- `thesis`
- `school`
- `country`
- `year`
- `subject`
- `advisors`
- `students`

### 2. Build a subject lookup table

The notebook extracts all non-missing subject entries from the `subject` column. Each subject is split into:

- `subject_Code`
- `subject_Name`

For example:

```text
34—Ordinary differential equations
```

is split into:

```text
subject_Code = 34
subject_Name = Ordinary differential equations
```

The resulting subject table contains **63 subject areas**.

### 3. Check for duplicate or nearly duplicate subject names

The notebook normalizes subject names by:

- lowercasing
- replacing `&` with `and`
- removing punctuation
- standardizing whitespace

It then checks for exact duplicates after normalization. No exact duplicates are found.

The notebook also uses `rapidfuzz` to find highly similar subject names. Some similar pairs are detected, such as:

| Code 1 | Subject 1 | Code 2 | Subject 2 | Similarity |
|---|---|---|---|---:|
| 16 | Associative rings and algebras | 17 | Nonassociative rings and algebras | 95.24 |
| 34 | Ordinary differential equations | 35 | Partial differential equations | 85.25 |
| 26 | Real functions | 33 | Special functions | 83.87 |
| 13 | Commutative rings and algebras | 16 | Associative rings and algebras | 83.33 |

These appear to be mathematically distinct subject areas rather than simple duplicates.

### 4. Add subject code and subject name columns

The original `subject` column is split into two new columns:

```python
tree["subject_code"]
tree["subject_name"]
```

Rows with missing subject information have missing values in both of these new columns.

### 5. Prepare advisor and student relationships

The notebook prepares `advisors` and `students` as list-like columns and creates dictionaries for fast lookup:

```python
id_to_subject
id_to_advisors
id_to_students
```

These dictionaries are used to collect subject evidence from a mathematician's academic neighbors.

### 6. Collect subject evidence from academic neighbors

The function `collect_subjects_from_neighbors` traverses either advisors or students up to a chosen depth and gathers subject-code votes.

Closer academic relatives receive larger weights:

```python
weight = 1 / (depth + 1)
```

This means direct neighbors count more than more distant academic ancestors or descendants.

### 7. Train thesis-title classifiers

The notebook trains supervised models using rows where both `thesis` and `subject_code` are known.

The thesis titles are vectorized using TF-IDF with:

- English stop words removed
- unigrams and bigrams
- `min_df=2`

The following models are compared:

- Logistic Regression
- Random Forest
- Decision Tree
- Linear SVM with probability calibration

The data is split into training and testing sets with stratification by subject code.

### 8. Compare model performance

Using 3-fold stratified cross-validation, the SVM gives the best mean test accuracy and macro F1 score among the tested models.

| Model | Mean Test Accuracy | Mean Test Macro F1 |
|---|---:|---:|
| SVM | 0.6454 | 0.4615 |
| Logistic Regression | 0.5686 | 0.4329 |
| Random Forest | 0.5601 | 0.3889 |
| Decision Tree | 0.4225 | 0.2937 |

The initial SVM model achieves:

```text
Training Accuracy: 0.9257
Testing Accuracy: 0.6574
```

A grid search over the SVM regularization parameter selects:

```text
Best C: 0.1
Best macro F1: 0.4634
```

The tuned SVM gives:

```text
Training Accuracy: 0.7607
Testing Accuracy: 0.6334
```

The tuned SVM is used to generate thesis-title subject predictions.

### 9. Predict subject codes for missing rows

The notebook defines a combined inference function:

```python
infer_subject_for_id(...)
```

This function combines three sources of evidence:

1. **Descendant subject votes**
2. **Ancestor subject votes**
3. **Thesis-title classifier probabilities**

The default evidence weights are:

| Evidence source | Weight |
|---|---:|
| Descendants | 0.40 |
| Ancestors | 0.20 |
| Thesis title | 0.40 |

Each source is normalized separately before combination. The notebook also uses reliability factors so that weak evidence from a small number of relatives contributes less than stronger evidence from many relatives.

The final prediction returns:

- `predicted_subject_code`
- `subject_prediction_confidence`
- `subject_prediction_votes`

### 10. Fill missing subject values above a confidence threshold

The notebook fills missing subject values only when:

```python
subject_prediction_confidence > 0.55
```

Using this threshold, the notebook fills:

```text
Rows filled: 77,711
```

After filling, the cleaned dataset has:

- **280,203 non-null `subject_code` values**
- **280,203 non-null `subject_name` values**
- **58,329 rows still missing `subject_code`**
- **11,455 rows from year 2000 onward still missing `subject_code`**

### 11. Save the cleaned dataset

The notebook creates a final export DataFrame with the following columns:

- `id`
- `name`
- `thesis`
- `school`
- `country`
- `year`
- `advisors`
- `students`
- `subject_code`
- `subject_name`
- `predicted_subject_code`
- `subject_prediction_confidence`
- `subject_prediction_vector`

The final CSV is saved to:

```text
../../data/processed/version2_new_dataset_fitted.csv
```

## Output

The main output of the notebook is:

```text
version2_new_dataset_fitted.csv
```

This file contains the original mathematician data together with filled subject information and prediction metadata.

## Important Results

- The dataset contains **338,532 mathematician records**.
- The notebook identifies **63 mathematical subject areas**.
- Initially, **136,040 rows** have missing subject information.
- The best-performing classifier is the calibrated Linear SVM.
- The final filling strategy combines:
  - thesis-title classification,
  - advisor subject evidence,
  - student/descendant subject evidence.
- With a confidence threshold of `0.55`, the notebook fills **77,711 missing subject rows**.
- The final exported dataset has **280,203 rows with subject codes and names**.

## Dependencies

The notebook uses the following Python packages:

```text
pandas
numpy
matplotlib
seaborn
json
re
rapidfuzz
scikit-learn
collections
```

The main scikit-learn components used are:

- `TfidfVectorizer`
- `LogisticRegression`
- `RandomForestClassifier`
- `DecisionTreeClassifier`
- `LinearSVC`
- `CalibratedClassifierCV`
- `train_test_split`
- `StratifiedKFold`
- `cross_validate`
- `GridSearchCV`
- `accuracy_score`
- `f1_score`

## Notes and Possible Improvements

1. **Subject imbalance is significant.**  
   Some subject codes, such as `68`, `91`, and `62`, occur much more frequently than others. Macro F1 is therefore more informative than accuracy alone.

2. **The confidence threshold can be tuned.**  
   The current threshold is `0.55`. A higher threshold would produce fewer but safer fills; a lower threshold would fill more rows but may introduce more errors.

3. **Graph-based evidence is useful but should be validated.**  
   Academic descendants and ancestors often provide meaningful subject clues, but interdisciplinary lineages can make this noisy.

4. **Avoid data leakage in future validation.**  
   Since academic relatives may have related thesis topics, future validation could use group-based splits by genealogy components or time periods.

5. **Inspect remaining missing rows.**  
   There are still missing subject values after thresholded filling, including **11,455 rows from year 2000 onward**. These may require better thesis text features, additional metadata, or manual inspection.

## Reproduction

To reproduce the notebook workflow:

1. Place the input JSON file at:

   ```text
   ../../data/processed/data-new.json
   ```

2. Install the required dependencies.

3. Run the notebook from top to bottom.

4. The cleaned output will be written to:

   ```text
   ../../data/processed/version2_new_dataset_fitted.csv
   ```
