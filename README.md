# Zepto Data and AI Platform Capstone

## Overview

This repository contains the completed work for the Zepto Data and AI Platform capstone project.

The project is divided into three modules:

1. **Module 1 — Data Pipeline**
2. **Module 2 — Titanic EDA and Machine Learning**
3. **Module 3 — Offline GenAI Support Assistant**

The project demonstrates data collection, data cleaning, SQL analysis, machine learning, model evaluation, vector search, retrieval-augmented generation concepts, workflow orchestration, API development, and containerization.

## Project Structure

```text
zepto-ai-ml-capstone/
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── cleaned_titanic_eda.csv
│   ├── titanic.csv
│   ├── models/
│   │   ├── titanic_preprocessor.joblib
│   │   └── titanic_random_forest_pipeline.joblib
│   └── outputs/
│       ├── best_random_forest_summary.csv
│       ├── classification_model_comparison.csv
│       ├── class_imbalance_comparison.csv
│       ├── decision_tree.png
│       ├── decision_tree_feature_importance.csv
│       ├── deployment_test_predictions.csv
│       ├── fare_regression_metrics.csv
│       └── random_forest_gridsearch_results.csv
│
├── data_pipeline/
│   ├── database.py
│   ├── queries.py
│   ├── README.md
│   ├── run_pipeline.py
│   ├── schema.sql
│   ├── scraper.py
│   ├── books_cleaned.csv
│   ├── books.db
│   └── sql_results.txt
│
├── support_assistant/
│   ├── corpus/
│   ├── config.py
│   ├── Dockerfile
│   ├── graph.py
│   ├── knowledge_base.py
│   ├── main.py
│   ├── prompts.py
│   ├── README.md
│   ├── requirements.txt
│   └── schemas.py
│
├── .gitignore
└── README.md
```

## Module 1 — Data Pipeline

### Overview

Module 1 builds an end-to-end data pipeline using the public Books to Scrape website.

The pipeline:

1. Scrapes book information using `requests` and `BeautifulSoup`.
2. Cleans and converts scraped fields into appropriate data types.
3. Converts prices from GBP to INR using a fixed conversion rate.
4. Saves the cleaned dataset as a CSV file.
5. Loads the data into a normalized SQLite database.
6. Executes SQL queries for data analysis.
7. Demonstrates equivalent SQL `JOIN` and Pandas `merge()` operations.

### Data Source

The data is collected from:

https://books.toscrape.com/

The dataset contains 78 books from the following categories:

* Travel
* Mystery
* Romance

### Dataset Fields

* `title`
* `price_gbp`
* `price_inr`
* `rating`
* `in_stock`
* `category`

The fixed conversion rate used in the project is:

```text
1 GBP = 105.50 INR
```

### Database Design

The SQLite database contains two related tables:

* `categories`
* `books`

The `books.category_id` field references `categories.category_id`.

This establishes a normalized structure using a primary-key and foreign-key relationship.

### SQL Analysis

The SQL queries demonstrate:

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `BETWEEN`
* `JOIN`

The SQL queries and their outputs are saved in:

```text
data_pipeline/sql_results.txt
```

### Running Module 1

From the project root:

```powershell
python data_pipeline\run_pipeline.py
```

The pipeline produces:

* `books_cleaned.csv`
* `books.db`
* `sql_results.txt`

The database is recreated from the cleaned CSV to prevent duplicate records during repeated runs.

## Module 2 — Titanic EDA and Machine Learning

### Overview

Module 2 performs exploratory data analysis and machine learning using the Titanic dataset.

The module includes:

* Data exploration
* Missing-value analysis
* Feature analysis
* Survival distribution analysis
* Class-imbalance analysis
* Classification model comparison
* Decision Tree modeling
* Random Forest modeling
* Random Forest hyperparameter tuning
* Feature importance analysis
* Fare regression
* Deployment-style prediction testing

### Main Notebooks

```text
analytics/01_eda.ipynb
analytics/02_modeling.ipynb
```

The EDA notebook focuses on understanding and cleaning the dataset.

The modeling notebook trains, compares, tunes, and evaluates machine learning models.

### Saved Models

```text
analytics/models/titanic_preprocessor.joblib
analytics/models/titanic_random_forest_pipeline.joblib
```

The saved preprocessing object and Random Forest pipeline support reuse during deployment and prediction.

### Saved Outputs

The module saves model comparisons, hyperparameter search results, feature importance values, regression metrics, decision-tree visualizations, and deployment test predictions in:

```text
analytics/outputs/
```

## Module 3 — Offline GenAI Support Assistant

### Overview

Module 3 implements an offline Zepto customer-support assistant using local policy documents.

The assistant uses:

* Sentence Transformer embeddings
* ChromaDB vector search
* Structured prompts
* LangGraph
* Pydantic response validation
* FastAPI
* Docker

The knowledge base contains eight local policy documents covering:

1. Delivery
2. Returns
3. Refunds
4. Membership
5. Order tracking
6. Cancellation
7. Gift cards
8. Support hours

### Architecture

The LangGraph workflow contains three main nodes:

1. `classify_intent`
2. `retrieve_and_answer`
3. `direct_answer`

Policy-related questions are routed through retrieval and answer generation.

General questions receive a direct fallback response.

### Retrieval

The assistant uses the local:

```text
all-MiniLM-L6-v2
```

Sentence Transformer model to generate embeddings.

The embeddings are stored in a persistent ChromaDB collection and queried using cosine similarity.

### Mock Mode

The default configuration is fully offline:

```text
MOCK_LLM=1
```

Mock mode does not require:

* An API key
* An external LLM
* An internet connection for answer generation

The assistant produces deterministic responses from the retrieved policy context.

### API Endpoints

The FastAPI service exposes:

| Method | Endpoint  | Purpose                |
| ------ | --------- | ---------------------- |
| `GET`  | `/`       | Service information    |
| `GET`  | `/health` | Health check           |
| `POST` | `/ask`    | Ask a support question |

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

### Running Module 3 Locally

From the project root, activate the virtual environment and run:

```powershell
python -m uvicorn support_assistant.main:app --reload
```

Then open:

```text
http://localhost:8000/docs
```

Example request:

```json
{
  "query": "How can I track my delivery?"
}
```

Example response structure:

```json
{
  "answer": "According to the relevant policy...",
  "sources": [
    "doc_05_order_tracking.md"
  ],
  "confidence": 0.8
}
```

### Running the Knowledge Base

From the project root:

```powershell
python -m support_assistant.knowledge_base
```

This creates or updates the ChromaDB collection using the local policy corpus.

### Docker

To build the support assistant image:

```powershell
docker build -t zepto-support-assistant .\support_assistant
```

To run the container:

```powershell
docker run --rm -p 8000:8000 zepto-support-assistant
```

The API is then available at:

```text
http://localhost:8000
```

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

## Installation

Create and activate a virtual environment from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies required for Module 3:

```powershell
pip install -r support_assistant\requirements.txt
```

For Modules 1 and 2, install the libraries used by the notebooks and data pipeline, including:

* Pandas
* NumPy
* Requests
* BeautifulSoup
* Matplotlib
* Scikit-learn
* Joblib
* Jupyter

## Reproducibility

The project stores generated datasets, model outputs, and deployment artifacts in their respective module directories.

The data pipeline recreates its SQLite database from the cleaned CSV.

The GenAI assistant uses a local policy corpus and deterministic mock mode by default.

The machine learning notebooks can be rerun to regenerate the saved models and evaluation outputs.

## Technologies Used

* Python
* Pandas
* NumPy
* Requests
* BeautifulSoup
* SQLite
* SQL
* Matplotlib
* Scikit-learn
* Joblib
* Jupyter Notebook
* Sentence Transformers
* ChromaDB
* LangGraph
* Pydantic
* FastAPI
* Uvicorn
* Docker

## Notes

Generated environments, caches, databases, model files, and secrets should not be committed to version control unless explicitly required.

The repository should be checked before pushing to GitHub to ensure that:

* `.venv` is excluded
* `.env` files are excluded
* ChromaDB data is excluded
* Python cache files are excluded
* Secrets and API keys are not included
