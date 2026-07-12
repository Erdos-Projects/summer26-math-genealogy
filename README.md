# Summer 2026 Math Genealogy Project

This repository contains the data and analysis for the Summer 2026 Mathematics Genealogy Project team project.

## Problem Statement

1. Study the trend of mathematics in a given field
2. Predict the research subject (MSC code) of a mathematician depending on their descendants/relatives.

## Data Scraping

We scraped records from the [Mathematics Genealogy Project](https://www.mathgenealogy.org/) and saved the results in `data/raw/data-new.json`.

* Original scraped records: **338,530**
* Approximate JSON file size: **129.9 MB**
* Fetching errors: **2 records**

The two records that initially produced fetching errors were later manually retrieved and added to the dataset.

For scrapping we used a slightly modified version of the script given in https://github.com/j2kun/math-genealogy-scraper.git. The modified code can be found in [src/data/scraper](src/data/scraper).

## Data Cleaning 

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

Note that many `students` entries are missing, but this should be interpreted as the fact that most mathematicians have no students.


## Missing-Data Analysis
<img width="1413" height="1180" alt="missing-data-analysis" src="https://github.com/user-attachments/assets/1a40540c-ce77-435d-b884-1eb2a927c89d" />

Initial observations include:

1. Missing `year` values are strongly associated with missing `school` values.
2. Records from earlier periods are more likely to have missing `subject` values.
3. Records with missing `year` values are also more likely to have missing `country` and `thesis` values.

## Project outline
### Project I. Missing Subject Codes/Names Imputation 
The dataset had 136,040 entries with subject missing. The following missing value imputation procedure has been taken to decrease the number of entries with missing subjects. Every subject comes with a subject code (varying between 0 and 97) and subject name. 

First, every ID in the dataset either have ancestors or descendants. The subject code/name can be connected upto some extend based on these connections. For some IDs this doesn't work as the subject codes of ancestors or descendants are missing. Therefore, a subject code prediction based on the key words in thesis title was carried out. 

Following models were selected for the initial evaluation. 
   - LogisticRegression
   - DecisionTreeClassifier
   - RandomForestClassifier
   - LinearSVC

Pipelines were created using TfidVectorizer and these models. Used StratifiedKFold for a 3-fold cross validation of all the models and F1 Macro for model selection (this metric is used as the subjects (codes/names) are imbalanced). 

<img width="1301" height="177" alt="image" src="https://github.com/user-attachments/assets/aef65fb6-d718-4969-9331-f37a56c1989a" />

Hyperparameter tuning for LinearSVC was done using GrideSearchCV and found that c=0.1 gives the best fit (train accuracy = 76.07% test accuracy = 63.34%). Only the subject codes with predication confidence score greater than or equal to 0.55 were kept. For the calculation of confidence score a weight was given for subject codes connected to the ones of descendants and ancestors and prediction probabilities coming from the fitted model.  

(More details : [notebook/missing_subjects](notebooks/missing_subjects))


### Project II. Keyword Trends

**Question:**
Can we predict which thesis-title keywords are about to take off in a field, before they do?

**Idea:**
New terminology shows up in thesis titles before a topic grows large, so a word climbing from a low base is an early signal. We track each word's share of titles within a subject over time, flag the ones rising fastest, and forecast where they go next.

**What we found:**
The naive guess, "words trending up keep trending up," is actually worse than a coin flip here (35% direction accuracy): sharp rises tend to revert, not continue. A Ridge model on lagged usage and trend features learns this reversion and calls the direction of change correctly 64% of the time, ranking the true movers with 0.90 NDCG. Applied forward, it produces a per-subject watchlist of rising terms for 2025-2026, which matches the titles already coming in (rank correlation up to 0.99 in the best-covered fields).

**How it's built:**
Titles are tokenized per subject and aggregated into 2-year bins to smooth data-entry lag. Candidate rising words are chosen by specificity and recent slope, then the model predicts the next period's change in share. Evaluation is a leak-free time split, with candidate selection rebuilt inside each fold so nothing peeks at the future.

More details and notebooks in [notebooks/keyword_trends](notebooks/keyword_trends).
 
### Project III. Subject Evolution

One direction of this project is to study the long-term evolution of mathematical research subjects in the Mathematics Genealogy Project. Instead of only asking which subjects have the largest raw number of students, we aim to understand how subjects emerge, become dominant, decline, and interact with one another through academic genealogy. 

First, we will analyze _subject dominance_ over time. For each year, we plan to compute the proportion of number of graduate students belonging to each `subject` in the pure or applied math baskets, and use these proportions to study changes in subject rankings. We analyze them as time series during 1960-2024, and use Exponential Smoothing and ARIMA to predict their distributions in 2024-2027. More details see [notebooks/subject_trends](notebooks/subject_trends)
<!-- Possible outputs include a subject-share heatmap, rankings of the most common subjects by decade, top-10 subject turnover across decades, and entropy-based measures of subject diversity. 

Second, we will study _subject life cycles_. For each `subject`, we plan to estimate an emergence year, peak year, recent momentum, decline ratio, and general status. Possible outputs include a life-cycle table for all MSC subjects, a birth-versus-peak-year scatterplot, and rankings of rising and declining subjects. 
-->
Second, we will use the advisor-student structure of the dataset to study _genealogical transmission_ between subjects. We plan to construct a $63 \times 63$ transition matrix, where each entry measures how often advisors in one subject produce students in another subject. This can also be computed over different time windows to see how field transitions change historically. From this matrix, we can compute self-retention rankings, net inflow and outflow rankings, top migration flows between subjects, and persistence of subjects across multiple generations.  More details see [notebooks/subject_trends/subject_transition](notebooks/subject_trends/subject_transition)

### Project IV. Geography analysis 

Another direction for this project is to study some geographical patterns in mathematical research subjects on the Mathematics Genealogy Project. Because most of the data is focused in the United States, we restrict attention there. In particular, we aim to investigate trends at the State level - how has subject popularity varied between States (and over time). 

We consider first the question of prediction (in the near-term) how subjects will evolve and which states will increase/decrease their proportion of PhDs granted in each subject. We set up a multinomial model to address this. 

We next consider inferential questions - how the distribution of subjects within one state compares to that of other states, and to the national average. We set up a Poisson regression model to address this. 

For more details, see [notebooks/geographic_distributions](notebooks/geographic_distributions)

## Conclusions
We are able to make predictions about keywords trend showing up in thesis titles, short-term of subject trend, and we find there is trend of even distribution of subjects amoung US states.

## Limitations
The database is incomplete, many missing `subject` entries in the early years, data mostly focused on the US; The number of granted dissertation is only one indicator of the subject size.

## Future work
Study the tree structures of the database, study inferential questions
