# Summer 2026 Math Genealogy Project

## Problem Statement

**Can data from the Mathematics Genealogy Project reveal early signals of emerging mathematical fields?**

This project uses the Mathematics Genealogy Project to study how mathematical
research areas evolve and to build predictive models from academic lineage data.

### Goals

1. **Trend analysis.** Track how activity in a given mathematical field changes
   over time, using MSC codes and associated keywords.

2. **Emerging field detection.** Identify early signals of new or fast growing
   fields by detecting trending keywords and subject areas before they become
   mainstream.

3. **Geographic inference.** Answer inferential questions about the geographical
   distribution of mathematical research within the US, such as regional
   concentration of specific subjects.
4. **Subject prediction.** Predict a mathematician's research subject (MSC code)
   from the subjects of their advisors, students, and thesis title.

## Data   

### Data Scraping

We scraped records from the [Mathematics Genealogy Project](https://www.mathgenealogy.org/) and saved the results in `data/raw/data-original.json`.

* Original scraped records: **338,530**
* Approximate JSON file size: **129.9 MB**
* Fetching errors: **2 records**

The two records that initially produced fetching errors were later manually retrieved and added to the dataset.

For scrapping we used a slightly modified version of the script given in https://github.com/j2kun/math-genealogy-scraper.git. The modified code can be found in [src/data/scraper](src/data/scraper).

### Data Cleaning 

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

### Missing-Data Analysis
<img width="1413" height="1180" alt="missing-data-analysis" src="https://github.com/user-attachments/assets/1a40540c-ce77-435d-b884-1eb2a927c89d" />

Note that many entries has missing `students`. This should be rather interpreted as the fact that most mathematicians have no students. The largetst missing feature is `subject`.


Initial observations include:

1. Missing `year` values are strongly associated with missing `school` values.
2. Records from earlier periods are more likely to have missing `subject` values.
3. Records with missing `year` values are also more likely to have missing `country` and `thesis` values.
   
## Exploratory Data Analysis
Please refer to [notebooks/data_visualization](notebooks/data_visualization).

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

(More details : [notebooks/missing_subjects](notebooks/missing_subjects))


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

This project aims to study the long-term changes in mathematical research subjects through the Mathematics Genealogy Project. Instead of only asking which subjects have the largest raw number of students, we aim to understand how subjects emerge, become dominant, decline, and interact with one another through academic genealogy. We focus on subject shares rather than raw dissertation counts, since the total number of recorded dissertations varies substantially from year to year. Using shares makes comparisons across time more meaningful.

First, we will analyze _subject trend_. For each year, we compute the percentage share of granted disserations belonging to each `subject` in the pure or applied math baskets, and use these shares to study changes in subject rankings. We analyze them as time series during 1960-2024, and use Damped Holt and ARIMA(0,1,1) to predict their distributions in 2024-2027. In addition, we will use the advisor-student structure of the dataset to study _genealogical transmission_ between subjects. We plan to construct a $63 \times 63$ transition matrix, where each entry measures how often advisors in one subject produce students in another subject. This can also be computed over different time windows to see how field transitions change historically. From this matrix, we can compute self-retention rankings, net inflow and outflow rankings, top migration flows between subjects, and persistence of subjects across multiple generations. More details see [notebooks/subject_trends](notebooks/subject_trends)


### Project IV. Geography analysis 

Another direction for this project is to study some geographical patterns in mathematical research subjects on the Mathematics Genealogy Project. Because most of the data is focused in the United States, we restrict attention there. In particular, we aim to investigate trends at the State level - how has subject popularity varied between States (and over time). 

We consider first the question of prediction (in the near-term) how subjects will evolve and which states will increase/decrease their proportion of PhDs granted in each subject. We set up a multinomial model to address this. 

We next consider inferential questions - how the distribution of subjects within one state compares to that of other states, and to the national average. We set up a Poisson regression model to address this. 

For more details, see [notebooks/geographic_distributions](notebooks/geographic_distributions)


## Conclusions

- **Keyword trends in thesis titles.** Our models can predict which keywords are
  likely to appear in future thesis titles, capturing shifts in how mathematicians
  describe their work.
- **Short-term subject trends.** We can forecast near-term changes in subject
  activity, identifying which MSC areas are growing or declining over the next
  few years.
- **Even distribution across US states.** We find a trend toward subjects becoming
  more evenly spread across US states over time, rather than staying concentrated
  in a few regions.

## Limitations

- **Incomplete database.** Many older records lack Mathematics Subject Classification entries, which makes it difficult to draw statistical conclusions on subjects trends before 1960.
- **US-centric coverage.** The Mathematics Genealogy Project database is more complete for the United States than for many other countries. So our conclusions should not be generalized to global mathematical research without caution. 
- **Dissertation count is a proxy.** The number of granted dissertations is only one
  indicator of a subject's size and does not capture publication volume, citations,
  or research impact.

## Future work

- **Tree structure analysis.** The advisor–student relationships and lineage structures to engineer additional features, such as lineage depth, network centrality, subject-transition probabilities, and Markov-chain dynamics. These features could deepen the analysis of subject evolution and potentially improve trend prediction.
- **Inferential questions.** Extend the analysis to further inferential questions,
  for example whether specific lineages or institutions drive the emergence of new
  fields.
- **Integrating the subject-prediction pipeline.** In Project I, missing MSC subject codes were predicted using thesis titles and genealogy information. Although this substantially improves subject coverage, classification errors may affect estimated shares and trends. Our current prediction models in Project II~IV did not use these predicted results from Project I. A future extension would integrate the imputation pipeline more carefully into the subject- and keyword-trend workflows and evaluate results separately on records with observed subject labels. This would allow us to compare trends based on observed-only data with trends that also include imputed labels and quantify the effect of imputation uncertainty.
