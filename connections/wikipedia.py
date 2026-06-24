import requests
from utils.enums import WikipediaEnum
from utils.errors import ConnectionError
from bs4 import BeautifulSoup


class Wikipedia:
    def search_page(search_term: str, limit: int) -> list:
        url = WikipediaEnum.URL_SEARCH_PAGE.value
        headers = WikipediaEnum.HEADERS.value
        params = {"q": search_term, "limit": limit}

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
        except Exception:
            raise ConnectionError("Could not search for wikipedia page")
        data = response.json()
        pages = data.get("pages")

        return pages

    def get_page(title: str):
        url = WikipediaEnum.URL_GET_PAGE.value
        url = url.format(title)
        headers = WikipediaEnum.HEADERS.value

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
        except Exception:
            raise ConnectionError("Could not get wikipedia page")

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.prettify()
