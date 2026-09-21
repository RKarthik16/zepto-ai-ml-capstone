# Module 1 — Data Pipeline

## Overview

This module builds an end-to-end data pipeline using the public Books to Scrape website.

The pipeline:

1. Scrapes book information using `requests` and `BeautifulSoup`.
2. Cleans and converts the scraped fields into appropriate data types.
3. Calculates INR prices using the fixed conversion rate of 1 GBP = 105.50 INR.
4. Saves the cleaned dataset as CSV.
5. Loads the data into a normalized SQLite database.
6. Executes SQL queries demonstrating filtering, sorting, limiting, distinct values, range filtering, and table joins.
7. Demonstrates equivalent SQL JOIN and Pandas `merge()` operations.

## Data Source

Books to Scrape:

https://books.toscrape.com/

The dataset contains books from three categories:

- Travel
- Mystery
- Romance

The final dataset contains 78 books.

## Dataset Fields

| Field | Description |
|---|---|
| title | Book title |
| price_gbp | Original listed price in GBP |
| price_inr | Price converted using fixed GBP → INR rate |
| rating | Star rating from 1 to 5 |
| in_stock | Whether the book is currently in stock |
| category | Book category |

## Cleaning

The following transformations are applied:

- GBP price is converted to `float`.
- Star ratings are converted from text to integers from 1 to 5.
- Availability is converted into a Boolean `in_stock` field.
- INR price is calculated using the fixed conversion rate:
  `1 GBP = 105.50 INR`.
- Parsing failures are caught so that one malformed book does not terminate the entire scraping process.

## Database Design

The SQLite database contains two related tables:

### categories

- `category_id` — primary key
- `category_name` — unique category name

### books

- `book_id` — primary key
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id` — foreign key referencing `categories.category_id`

This separates category information from book records and establishes a primary-key/foreign-key relationship.

## SQL Analysis

The SQL queries demonstrate:

- SELECT and WHERE
- ORDER BY
- LIMIT
- DISTINCT
- BETWEEN
- JOIN

Query strings and outputs are saved in `sql_results.txt`.

At least two query results are also loaded using `pandas.read_sql()`.

The SQL JOIN is reproduced using `pandas.merge()` on the corresponding `category_id`.

## Running the Pipeline

From the project root with the virtual environment activated:

```powershell
python data_pipeline\run_pipeline.py
## Reproducibility

The database is recreated from scratch whenever `database.py` runs. This prevents duplicate records when rebuilding the project from the cleaned CSV.

## Pipeline Output

The pipeline produces three main artifacts:

- `books_cleaned.csv` — cleaned scraped data
- `books.db` — normalized SQLite database
- `sql_results.txt` — SQL queries and their outputs
### SQL JOIN and Pandas JOIN Equivalence

The JOIN query combines the `books` and `categories` tables using the shared `category_id` foreign key.

The SQL implementation orders the joined records by `price_gbp` in descending order and returns the top 10 records.

The same operation is reproduced in Pandas using `pd.merge()`, followed by `sort_values()` and `head(10)`.

The resulting DataFrames are normalized to the same column order and compared using `DataFrame.equals()`. The comparison returns `True`, confirming that the SQL JOIN and Pandas implementation produce equivalent results.