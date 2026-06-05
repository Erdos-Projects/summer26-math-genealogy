# Summer 2026 Math Genealogy Project

This repository contains the data and analysis for the Summer 2026 Mathematics Genealogy Project team project.

## Problem Statement



## Data Scraping

We scraped records from the [Mathematics Genealogy Project](https://www.mathgenealogy.org/) and saved the results in `data/raw/data-new.json`.

* Original scraped records: **338,530**
* Approximate JSON file size: **129.9 MB**
* Fetching errors: **2 records**

The two records that initially produced fetching errors were later manually retrieved and added to the dataset.

For scrapping we used a slightly modified version of the script given in https://github.com/j2kun/math-genealogy-scraper.git. The modified code can be found in `src/data/scraper`.

## Initial Data Cleaning

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

* manually added the two records that produced fetching errors;
* removed six records with missing names; and
* identified seven records with clearly incorrect years:

  * four caused by scraping or parsing errors;
  * three appearing to originate from the MGP database.

After this initial cleaning, the dataset contains **338,526 records**.

## Dataset Summary

| Column     | Data type | Non-null entries | Missing entries | Completeness |
| ---------- | --------: | ---------------: | --------------: | -----------: |
| `id`       |   integer |          338,526 |               0 |       100.0% |
| `name`     |    string |          338,526 |               0 |       100.0% |
| `thesis`   |    string |          307,399 |          31,127 |        90.8% |
| `school`   |    string |          281,805 |          56,721 |        83.2% |
| `country`  |    string |          322,986 |          15,540 |        95.4% |
| `year`     |     float |          277,236 |          61,290 |        81.9% |
| `subject`  |    string |          202,492 |         136,034 |        59.8% |
| `advisors` |      list |          338,526 |               0 |       100.0% |
| `students` |      list |          338,526 |               0 |       100.0% |

The `advisors` and `students` columns are always present, although their values may be empty lists.

## Missing-Data Analysis

<img width="2085" height="901" alt="image" src="https://github.com/user-attachments/assets/953eac7f-7930-4871-9ffe-83d8c78e2068" />

Initial observations include:

1. Missing `year` values are strongly associated with missing `school` values.
2. Records from earlier periods are more likely to have missing `subject` values.
3. Records with missing `year` values are also more likely to have missing `country` and `thesis` values.

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
