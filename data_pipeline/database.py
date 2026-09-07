import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "books_cleaned.csv"
DB_PATH = BASE_DIR / "books.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def create_database():
    """Create a fresh SQLite database and its tables."""

    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    return connection


def insert_data(connection, df):
    """Insert categories and books into the normalized database."""

    # Insert unique categories first.
    categories = (df[["category"]].drop_duplicates().rename(columns={"category": "category_name"}))

    categories.to_sql(
        "categories",
        connection,
        if_exists="append",
        index=False,
    )

    # Read category IDs back from SQLite.
    category_lookup = pd.read_sql(
        "SELECT category_id, category_name FROM categories",
        connection,
    )

    # Connect each book to its category ID.
    books = df.merge(
        category_lookup,
        left_on="category",
        right_on="category_name",
        how="left",
    )

    books = books[
        [
            "title",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock",
            "category_id",
        ]
    ]

    books.to_sql(
        "books",
        connection,
        if_exists="append",
        index=False,
    )


def main():
    df = pd.read_csv(CSV_PATH)

    connection = create_database()

    try:
        insert_data(connection, df)
        connection.commit()

        print("Database created successfully.")
        print(f"Database location: {DB_PATH}")

        categories_count = pd.read_sql(
            "SELECT COUNT(*) AS count FROM categories",
            connection,
        ).iloc[0]["count"]

        books_count = pd.read_sql(
            "SELECT COUNT(*) AS count FROM books",
            connection,
        ).iloc[0]["count"]

        print(f"Categories inserted: {categories_count}")
        print(f"Books inserted: {books_count}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()