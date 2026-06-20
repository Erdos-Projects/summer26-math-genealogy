# Summer 2026 Math Genealogy Project

This repository contains the data and analysis for the Summer 2026 Mathematics Genealogy Project team project.

## Problem Statement

1. Study the trend of mathematics in a given field
2. Predict the research subject (MSC code) of a mathematician depending on their descendants/relatives.

## Data Scraping (see folder src)

We scraped records from the [Mathematics Genealogy Project](https://www.mathgenealogy.org/) and saved the results in `data/raw/data-new.json`.

* Original scraped records: **338,530**
* Approximate JSON file size: **129.9 MB**
* Fetching errors: **2 records**

The two records that initially produced fetching errors were later manually retrieved and added to the dataset.

For scrapping we used a slightly modified version of the script given in https://github.com/j2kun/math-genealogy-scraper.git. The modified code can be found in `src/data/scraper`.

## Initial Data Cleaning (see folder notebooks)

Each record contains the following fields:

* `id`
* `name`
* `thesis`
* `school`
* `country`
* `year`
* `subject`
* `advisors`
* `students`

During the initial cleaning process, we:

* manually added the two records missed from fetching errors;
* fixed 1,456 entries with student/advisor mismatches;
* identified seven records with incorrect years and six records with missing names.

After this initial cleaning, the dataset contains **338,532 records**.

For records missing a `subject` field (136,040 entries, 40.2% of the dataset), we assigned subjects using a classifier, adding two new fields: `predicted_subject_code` and `subject_prediction_confidence`. This expanded subject coverage from 59.8% to 89.2% of all records.

## Dataset Summary

| Column                          | Data type | Non-null entries | Missing entries | Completeness |
| ------------------------------- | --------: | ---------------: | --------------: | -----------: |
| `id`                            |   integer |          338,532 |               0 |       100.0% |
| `name`                          |    string |          338,526 |               6 |       100.0% |
| `thesis`                        |    string |          307,399 |          31,133 |        90.8% |
| `school`                        |    string |          276,167 |          62,365 |        81.6% |
| `country`                       |    string |          322,986 |          15,546 |        95.4% |
| `year`                          |     float |          277,237 |          61,295 |        81.9% |
| `subject_code`                  |    string |          302,106 |          36,426 |        89.2% |
| `subject_name`                  |    string |          302,106 |          36,426 |        89.2% |
| `predicted_subject_code`        |    string |          133,502 |         205,030 |        39.4% |
| `subject_prediction_confidence` |     float |          136,040 |         202,492 |        40.2% |
| `advisors`                      |      list |          312,066 |          26,466 |        92.2% |
| `students`                      |      list |           82,914 |         255,618 |        24.5% |

The `advisors` and `students` columns are always present, although their values may be empty lists (see below).

## Missing-Data Analysis

<img width="1417" height="1180" alt="image" src="https://github.com/user-attachments/assets/e8300458-64a9-4d95-8ad7-648598da0f36" />


Initial observations include:

1. Missing `year` values are strongly associated with missing `school` values.
2. Records from earlier periods are more likely to have missing `subject` values.
3. Records with missing `year` values are also more likely to have missing `country` and `thesis` values.

Also, many `students` entries are empty, but that is probably due to the fact that most mathematicians have no students.

## Basic Analysis of Student Counts

The number of listed students per mathematician has the following summary:

| Statistic                               | Value |
| --------------------------------------- | ----: |
| Mean number of students                 |  1.13 |
| Standard deviation                      |  4.00 |
| Maximum number of students              |   181 |
| Mathematicians with no listed students  | 75.5% |
| Mathematicians with one listed student  | 10.3% |
| Mathematicians with two listed students |  3.8% |

The distribution is highly right-skewed: most mathematicians have no listed students, while a small number have very large numbers of students.

(may add a few more analysis here if needed)

## Project Proposal
Based on the analysis above, we propose the following four problems/questions:
1. How to fill in the missing subject code? - Osanda

2. What is the trend of key words in each subject for the next year/decade? - Aaroodd 

3. Which subject will be the next “dominating” subject? - Yilong

4. How are the subject topics discributed in US states? - Jon

### 1. Missing code 
The dataset had 136,040 entries with subject missing. The following missing value imputation procedure has been taken to decrease the number of entries with missing subjects. Every subject comes with a subject code (varying between 0 and 97) and subject name. 

First, every ID in the dataset either have ancestors or descendants. The subject code/name can be connected upto some extend based on these connections. For some IDs this doesn't work as the subject codes of ancestors or descendants are missing. Therefore, a subject code prediction based on the key words in thesis title was carried out. 

Following models were selected for the initial evaluation. 
   - LogisticRegression
   - DecisionTreeClassifier
   - RandomForestClassifier
   - LinearSVC

Pipelines were created using TfidVectorizer and these models. Used StratifiedKFold for a 3-fold cross validation of all the models and F1 Macro for model selection (this metric is used as the subjects (codes/names) are imbalanced). 

<img width="1301" height="177" alt="image" src="https://github.com/user-attachments/assets/aef65fb6-d718-4969-9331-f37a56c1989a" />

Hyperparameter tuning for LinearSVC was done using GrideSearchCV and found that c=0.1 gives the best fit (train accuracy = 76.07% test accuracy = 63.34%). Only the subject codes with predication confidence score greater than or equal to 0.55 were kept. For the calculation of confidence score a weight was given for subject codes based on the ones of descendants and ancestors and prediction probabilities coming from the model fit.  

Repeated the same process for the new dataset to fill in more missing values. The best model with best accuracy and f1 macro after hyperparameter tuning was LogisticRegression. (More details about this 


### 2. Keyword Trends - 

**Question:**
Within each subject, which thesis-title keywords are rising, and can we predict which will keep trending?

**Idea:** 
New terminology tends to appear in thesis titles before a topic grows large. By tracking each word's yearly usage share within a subject, we can flag words with a low historical base and a steep recent rise, then forecast their near-future share.

**Approach:**
- Tokenize thesis titles per subject and compute each word's share of titles per year
- Detect rising words from their recent trend (slope on a low base)
- Frame forecasting as predicting next-year share from lagged usage features

**Modeling and evaluation:**
Baseline is linear regression on lag features. Because this is a time series, the main risk is temporal leakage, so we use a custom time-based split (train on past years, test on future years) rather than a random split.

More details and notrbooks in [notebooks/keyword_trends](notebooks/keyword_trends)
 
### 3. Subject trend 

### 4. Geography analysis 
