import httpx
from bs4 import BeautifulSoup
import re
import json


def get_html_as_str(url: str) -> str:
    response = httpx.get(url)
    if response.status_code != 200:
        raise ConnectionError("Couldn't access the site")
    return response.text


def get_genres(html: str) -> list:
    genres_list = []
    soup = BeautifulSoup(html, "html.parser")
    html_genre_list = soup.find(class_="side_categories")
    genres = html_genre_list.find_all("li")[1:]

    for genre in genres:
        link = genre.find("a")["href"]
        genre_text = genre.find("a").text.strip()
        genres_list.append({"genre": genre_text, "link": link})
    return genres_list


def get_books(html: str, genre: dict, main_dict: dict, url: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    all_books = soup.find_all(class_="product_pod")

    for book in all_books:
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text.strip()
        stock = book.find("p", class_="instock availability").text.strip()
        main_dict[genre["genre"]][title] = {"price": price, "stock": stock}

    try:
        next_page = check_next_page(html)
        if next_page:
            genre_url = re.sub(r"/[^/]+\.html$", "/", genre["link"])
            get_books(get_html_as_str(url + genre_url + next_page), genre, main_dict, url)
    except AttributeError:
        return
    
    

def check_next_page(html: str) -> str| None:
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.find("li", class_="next")
    if next_page:
        try:
            next_page_url = next_page.find("a")["href"]
            return next_page_url
        except AttributeError:
            return None


def save(main_dict: dict) -> None:
    with open("books.json", 'a') as file:
            json.dump(main_dict, file, indent=4)


if __name__ == "__main__":
    main_dict = {}
    url = "https://books.toscrape.com/"
    genres_list = get_genres(get_html_as_str(url))

    for genre in genres_list:
        main_dict[genre["genre"]] = {}
        genre_html = get_html_as_str(url + genre["link"])
        get_books(genre_html, genre, main_dict, url)
    save(main_dict)
