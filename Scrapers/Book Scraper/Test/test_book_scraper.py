import pytest

from typing import Any, Generator
from pytest_httpx._httpx_mock import HTTPXMock

import book_scraper

url = "https://books.toscrape.com/"


def test_get_html_as_str(httpx_mock: Generator[HTTPXMock, None, None]) -> None:
    with open("status_200.html", "r") as f:
        html_text = f.read()
    httpx_mock.add_response(
        url=url,
        text=html_text,
    )
    html = book_scraper.get_html_as_str(url)
    assert "All products | Books to Scrape - Sandbox" in html


def test_get_html_as_str_404(httpx_mock: Generator[HTTPXMock, None, None]) -> None:
    httpx_mock.add_response(url=url, status_code=404)
    with pytest.raises(ConnectionError):
        book_scraper.get_html_as_str(url)


def test_get_genres(httpx_mock: Generator[HTTPXMock, None, None]) -> None:
    with open("status_200.html", "r") as f:
        html_text = f.read()
    genres = book_scraper.get_genres(html_text)
    assert genres[0]["genre"] == "Travel"
    assert genres[0]["link"] == "catalogue/category/books/travel_2/index.html"
    assert genres[1]["genre"] == "Mystery"


def test_get_books(httpx_mock: Generator[HTTPXMock, None, None]) -> None:
    with open("travel.html", "r") as f:
        genre_html_text = f.read()
    result = {"Travel": {}}
    genre = {"genre": "Travel", "link": "category/books/travel_2/index.html"}
    book_scraper.get_books(genre_html_text, genre, result, "status_200.html")
    assert "It's Only the Himalayas" in result["Travel"]
    assert result["Travel"]["It's Only the Himalayas"]["price"] == "£45.17"
    assert (
        result["Travel"][
            "Full Moon over Noah\u2019s Ark: An Odyssey to Mount Ararat and Beyond"
        ]["stock"]
        == "In stock"
    )


def test_check_next_page(httpx_mock: Generator[HTTPXMock, None, None]) -> None:
    with open("travel.html", "r") as f:
        genre_html_text = f.read()
    httpx_mock.add_response(
        url="https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        text=genre_html_text,
    )

    with open("mystery.html", "r") as file2:
        genre_html_text = file2.read()
    httpx_mock.add_response(
        url="https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        text=genre_html_text,
    )

    html_negative = book_scraper.get_html_as_str(
        "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    )
    html_possitive = book_scraper.get_html_as_str(
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    )
    assert book_scraper.check_next_page(html_negative) == None
    assert book_scraper.check_next_page(html_possitive) == "page-2.html"


def test_save(mocker: Generator[Any, None, None]) -> None:
    file = mocker.patch("builtins.open")
    result = {
        "Travel": {
            "Book 1": {"price": "9.99", "stock": "In stock"},
            "Book 2": {"price": "5.55", "stock": "Out of stock"},
        }
    }
    book_scraper.save(result)
    file.assert_called_once_with("books.json", "w")
