# Module 2 — Titanic EDA and Machine Learning

## Overview

This module performs exploratory data analysis and machine learning using the Titanic dataset.

The work includes:

* Exploratory data analysis
* Data cleaning and preprocessing
* Class distribution analysis
* Classification model comparison
* Decision tree visualization
* Random Forest modeling
* Hyperparameter tuning using GridSearchCV
* Feature importance analysis
* Fare prediction using regression
* Model evaluation
* Saving trained models and evaluation outputs for deployment

## Dataset

The Titanic dataset contains passenger information and survival outcomes.

The analysis focuses on predicting whether a passenger survived using available passenger attributes.

Important features include:

* Passenger class
* Sex
* Age
* Fare
* Number of siblings or spouses aboard
* Number of parents or children aboard
* Embarked port
* Survival status

## Exploratory Data Analysis

The EDA notebook examines:

* Dataset structure and data types
* Missing values
* Numerical and categorical features
* Passenger survival distribution
* Class imbalance
* Relationships between passenger characteristics and survival
* Feature distributions and visual patterns

The EDA results are documented in:

```text
01_eda.ipynb
```

## Machine Learning

The modeling notebook compares classification models and evaluates their performance.

The module includes:

* Decision Tree classification
* Random Forest classification
* Class-imbalance comparison
* Random Forest hyperparameter tuning
* Feature importance analysis
* Deployment-style prediction testing

The modeling workflow is documented in:

```text
02_modeling.ipynb
```

## Saved Models

The trained models are stored in the `models` directory:

```text
models/
├── titanic_preprocessor.joblib
└── titanic_random_forest_pipeline.joblib
```

The preprocessing object and Random Forest pipeline are saved separately so that the same preprocessing and prediction workflow can be reused during deployment.

## Saved Outputs

The `outputs` directory contains the following artifacts:

```text
outputs/
├── best_random_forest_summary.csv
├── classification_model_comparison.csv
├── class_imbalance_comparison.csv
├── decision_tree.png
├── decision_tree_feature_importance.csv
├── deployment_test_predictions.csv
├── fare_regression_metrics.csv
└── random_forest_gridsearch_results.csv
```

### Output descriptions

| File                                   | Description                                               |
| -------------------------------------- | --------------------------------------------------------- |
| `best_random_forest_summary.csv`       | Summary of the selected Random Forest model               |
| `classification_model_comparison.csv`  | Comparison of classification model performance            |
| `class_imbalance_comparison.csv`       | Comparison of results related to class imbalance          |
| `decision_tree.png`                    | Visual representation of the trained decision tree        |
| `decision_tree_feature_importance.csv` | Feature importance values from the decision tree          |
| `deployment_test_predictions.csv`      | Test predictions produced using the saved model pipeline  |
| `fare_regression_metrics.csv`          | Evaluation metrics for fare regression                    |
| `random_forest_gridsearch_results.csv` | Hyperparameter search results for the Random Forest model |

## Project Structure

```text
analytics/
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── cleaned_titanic_eda.csv
├── titanic.csv
├── models/
│   ├── titanic_preprocessor.joblib
│   └── titanic_random_forest_pipeline.joblib
└── outputs/
    ├── best_random_forest_summary.csv
    ├── classification_model_comparison.csv
    ├── class_imbalance_comparison.csv
    ├── decision_tree.png
    ├── decision_tree_feature_importance.csv
    ├── deployment_test_predictions.csv
    ├── fare_regression_metrics.csv
    └── random_forest_gridsearch_results.csv
```

## Running the Module

From the project root, activate the virtual environment and open the notebooks:

```powershell
jupyter notebook
```

Run the notebooks in this order:

1. `analytics/01_eda.ipynb`
2. `analytics/02_modeling.ipynb`

The notebooks generate the cleaned dataset, trained models, evaluation results, and visual outputs.

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook
* Joblib
