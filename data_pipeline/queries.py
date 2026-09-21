import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "books.db"
OUTPUT_PATH = BASE_DIR / "sql_results.txt"


def run_query(connection, query, description):
    """Run a SQL query, display its result, and return the result DataFrame."""
    print("\n" + "=" * 70)
    print(description)
    print("=" * 70)

    print("\nSQL:")
    print(query.strip())

    result = pd.read_sql(query, connection)

    print("\nResult:")
    print(result.to_string(index=False))

    return result


def main():
    connection = sqlite3.connect(DB_PATH)

    try:
        # ---------------------------------------------------------
        # REQUIRED SQL QUERIES
        # ---------------------------------------------------------
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
                    books.book_id,
                    books.title,
                    books.price_gbp,
                    books.price_inr,
                    books.rating,
                    books.in_stock,
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

        # ---------------------------------------------------------
        # RUN ALL SQL QUERIES
        # ---------------------------------------------------------
        for query, description in queries:

            result = run_query(
                connection,
                query,
                description,
            )

            all_output.append("=" * 70)
            all_output.append(description)
            all_output.append("=" * 70)
            all_output.append("\nSQL:")
            all_output.append(query.strip())
            all_output.append("\nResult:")
            all_output.append(result.to_string(index=False))
            all_output.append("")

        # ---------------------------------------------------------
        # PANDAS read_sql() DEMONSTRATION
        # ---------------------------------------------------------
        print("\n" + "=" * 70)
        print("Pandas read_sql() demonstration")
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

        result_1 = pd.read_sql(
            read_sql_query_1,
            connection,
        )

        result_2 = pd.read_sql(
            read_sql_query_2,
            connection,
        )

        print("\nFirst read_sql() result:")
        print(result_1.to_string(index=False))

        print("\nSecond read_sql() result:")
        print(result_2.to_string(index=False))

        all_output.append("=" * 70)
        all_output.append("Pandas read_sql() demonstration")
        all_output.append("=" * 70)

        all_output.append("\nFirst read_sql() result:")
        all_output.append(
            result_1.to_string(index=False)
        )

        all_output.append("\nSecond read_sql() result:")
        all_output.append(
            result_2.to_string(index=False)
        )

        # ---------------------------------------------------------
        # SQL JOIN
        # ---------------------------------------------------------
        join_query = """
            SELECT
                books.book_id,
                books.title,
                books.price_gbp,
                books.price_inr,
                books.rating,
                books.in_stock,
                categories.category_name
            FROM books
            JOIN categories
                ON books.category_id = categories.category_id
            ORDER BY books.price_gbp DESC
            LIMIT 10
        """

        sql_join_result = pd.read_sql(
            join_query,
            connection,
        )

        print("\n" + "=" * 70)
        print("SQL JOIN result")
        print("=" * 70)

        print(
            sql_join_result.to_string(index=False)
        )

        all_output.append("\n" + "=" * 70)
        all_output.append("SQL JOIN result")
        all_output.append("=" * 70)
        all_output.append(
            sql_join_result.to_string(index=False)
        )

        # ---------------------------------------------------------
        # LOAD TABLES INTO PANDAS
        # ---------------------------------------------------------
        books_df = pd.read_sql(
            """
            SELECT
                book_id,
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
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

        # ---------------------------------------------------------
        # REPRODUCE SQL JOIN USING pandas.merge()
        # ---------------------------------------------------------
        merged_df = pd.merge(
            books_df,
            categories_df,
            on="category_id",
            how="inner",
        )

        # Reproduce the SAME ORDER BY and LIMIT used by SQL.
        pandas_join_result = (
            merged_df
            .sort_values(
                "price_gbp",
                ascending=False,
            )
            .head(10)
        )

        # Select the exact same columns as the SQL query.
        pandas_join_result = pandas_join_result[
            [
                "book_id",
                "title",
                "price_gbp",
                "price_inr",
                "rating",
                "in_stock",
                "category_name",
            ]
        ]

        # ---------------------------------------------------------
        # DISPLAY PANDAS JOIN RESULT
        # ---------------------------------------------------------
        print("\n" + "=" * 70)
        print("Pandas merge() equivalent of SQL JOIN")
        print("=" * 70)

        print(
            pandas_join_result.to_string(index=False)
        )

        all_output.append("\n" + "=" * 70)
        all_output.append(
            "Pandas merge() equivalent of SQL JOIN"
        )
        all_output.append("=" * 70)
        all_output.append(
            pandas_join_result.to_string(index=False)
        )

        # ---------------------------------------------------------
        # COMPARE SQL JOIN AND PANDAS JOIN
        # ---------------------------------------------------------
        sql_compare = (
            sql_join_result
            .reset_index(drop=True)
        )

        pandas_compare = (
            pandas_join_result
            .reset_index(drop=True)
        )

        # Ensure both DataFrames have exactly the same
        # column order before comparison.
        pandas_compare = pandas_compare[
            sql_compare.columns
        ]

        joins_are_equivalent = (
            sql_compare.equals(pandas_compare)
        )

        print("\n" + "=" * 70)
        print("SQL JOIN vs Pandas merge() equivalence")
        print("=" * 70)

        print(
            "\nDo SQL JOIN and Pandas JOIN "
            "produce equivalent results?"
        )

        print(joins_are_equivalent)

        all_output.append("\n" + "=" * 70)
        all_output.append(
            "SQL JOIN vs Pandas merge() equivalence"
        )
        all_output.append("=" * 70)

        all_output.append(
            "\nDo SQL JOIN and Pandas JOIN "
            "produce equivalent results?"
        )

        all_output.append(
            str(joins_are_equivalent)
        )

        # ---------------------------------------------------------
        # SAVE QUERY STRINGS AND OUTPUTS
        # ---------------------------------------------------------
        OUTPUT_PATH.write_text(
            "\n".join(all_output),
            encoding="utf-8",
        )

        print(
            f"\nSQL results saved to: {OUTPUT_PATH}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()