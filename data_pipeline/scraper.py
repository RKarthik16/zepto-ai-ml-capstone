import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


BASE_URL = "https://books.toscrape.com/"
GBP_TO_INR = 105.50

CATEGORIES = {
    "Travel": "catalogue/category/books/travel_2/index.html",
    "Mystery": "catalogue/category/books/mystery_3/index.html",
    "Romance": "catalogue/category/books/romance_8/index.html",
}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def get_soup(url):
    """Download a webpage and return its parsed HTML."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Ensure the pound symbol is decoded correctly.
    response.encoding = "utf-8"

    return BeautifulSoup(response.text, "html.parser")


def parse_book(book, category):
    """Extract and clean information from one book."""

    title = book.select_one("h3 a")["title"]

    price_text = book.select_one(".price_color").get_text(strip=True)

    price_gbp = float(
        price_text.replace("£", "").replace("Â", "").strip()
    )

    rating_text = book.select_one(".star-rating")["class"][1]
    rating = RATING_MAP[rating_text]

    availability_text = book.select_one(".availability").get_text(
        " ", strip=True
    )

    in_stock = "In stock" in availability_text

    price_inr = round(price_gbp * GBP_TO_INR, 2)

    return {
        "title": title,
        "price_gbp": price_gbp,
        "price_inr": price_inr,
        "rating": rating,
        "in_stock": in_stock,
        "category": category,
    }


def scrape_category(category_name, category_url):
    """Scrape all books from one category."""

    url = urljoin(BASE_URL, category_url)
    books = []

    while url:

        soup = get_soup(url)

        for book in soup.select("article.product_pod"):
            try:
                books.append(parse_book(book, category_name))
            except (AttributeError, KeyError, TypeError, ValueError) as error:
                print(
                    f"Skipping a book in {category_name} "
                    f"because of parsing error: {error}"
                )

        next_button = soup.select_one("li.next a")

        if next_button:
            next_url = next_button.get("href")
            url = urljoin(url, next_url)
        else:
            url = None

    return books


def main():
    all_books = []

    for category_name, category_url in CATEGORIES.items():
        print(f"Scraping {category_name}...")

        books = scrape_category(category_name, category_url)

        print(f"  Books found: {len(books)}")

        all_books.extend(books)

    df = pd.DataFrame(all_books)

    print("\nDataset shape:", df.shape)

    print("\nBooks per category:")
    print(df["category"].value_counts())

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())

    # Save cleaned dataset
    OUTPUT_PATH = BASE_DIR / "books_cleaned.csv"
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCleaned dataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()