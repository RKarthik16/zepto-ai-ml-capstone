import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "books.db"
OUTPUT_PATH = BASE_DIR / "sql_results.txt"


def run_query(connection, query, description):
    """Run a SQL query and print its result."""
    print("\n" + "=" * 70)
    print(description)
    print("=" * 70)

    print("\nSQL:")
    print(query)

    result = pd.read_sql(query, connection)

    print("\nResult:")
    print(result.to_string(index=False))

    return result


def main():
    connection = sqlite3.connect(DB_PATH)

    queries = [
        (
            """
            SELECT title, price_gbp, rating
            FROM books
            WHERE rating >= 4
            """,
            "Query 1 - SELECT and WHERE",
        ),
        (
            """
            SELECT title, price_gbp
            FROM books
            ORDER BY price_gbp DESC
            """,
            "Query 2 - ORDER BY",
        ),
        (
            """
            SELECT title, price_gbp
            FROM books
            ORDER BY price_gbp DESC
            LIMIT 5
            """,
            "Query 3 - LIMIT",
        ),
        (
            """
            SELECT DISTINCT category_name
            FROM categories
            ORDER BY category_name
            """,
            "Query 4 - DISTINCT",
        ),
        (
            """
            SELECT title, price_gbp, category_id
            FROM books
            WHERE price_gbp BETWEEN 20 AND 40
            ORDER BY price_gbp
            """,
            "Query 5 - BETWEEN",
        ),
        (
            """
            SELECT
                books.title,
                books.price_gbp,
                categories.category_name
            FROM books
            JOIN categories
                ON books.category_id = categories.category_id
            ORDER BY books.price_gbp DESC
            LIMIT 10
            """,
            "Query 6 - JOIN",
        ),
    ]

    all_output = []

    for query, description in queries:
        result = run_query(connection, query, description)

        all_output.append("=" * 70)
        all_output.append(description)
        all_output.append("=" * 70)
        all_output.append("\nSQL:")
        all_output.append(query.strip())
        all_output.append("\nResult:")
        all_output.append(result.to_string(index=False))
        all_output.append("")

    # Demonstrate that at least two query results
    # can be read with pandas.read_sql.
    print("\n" + "=" * 70)
    print("Pandas read_sql demonstration")
    print("=" * 70)

    read_sql_query_1 = """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 5
    """

    read_sql_query_2 = """
        SELECT
            books.title,
            books.rating,
            categories.category_name
        FROM books
        JOIN categories
            ON books.category_id = categories.category_id
        WHERE books.rating = 5
    """

    result_1 = pd.read_sql(read_sql_query_1, connection)
    result_2 = pd.read_sql(read_sql_query_2, connection)

    print("\nFirst read_sql result:")
    print(result_1.to_string(index=False))

    print("\nSecond read_sql result:")
    print(result_2.to_string(index=False))

    all_output.append("=" * 70)
    all_output.append("Pandas read_sql demonstration")
    all_output.append("=" * 70)
    all_output.append("\nFirst read_sql result:")
    all_output.append(result_1.to_string(index=False))
    all_output.append("\nSecond read_sql result:")
    all_output.append(result_2.to_string(index=False))

        # Reproduce the SQL JOIN using pandas.merge().
    books_df = pd.read_sql(
        """
        SELECT
            title,
            price_gbp,
            rating,
            category_id
        FROM books
        """,
        connection,
    )

    categories_df = pd.read_sql(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        """,
        connection,
    )

    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner",
    )

    print("\n" + "=" * 70)
    print("Pandas merge() equivalent of SQL JOIN")
    print("=" * 70)
    print(merged_df.head(10).to_string(index=False))

    all_output.append("\n" + "=" * 70)
    all_output.append("Pandas merge() equivalent of SQL JOIN")
    all_output.append("=" * 70)
    all_output.append(merged_df.head(10).to_string(index=False))

    # Save query strings and outputs.
    OUTPUT_PATH.write_text(
        "\n".join(all_output),
        encoding="utf-8",
    )

    connection.close()

    print(f"\nSQL results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()