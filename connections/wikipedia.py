import requests
from utils.enums import WikipediaEnum
from utils.errors import ConnectionError
from bs4 import BeautifulSoup


class Wikipedia:
    def search_page(search_term: str, limit: int) -> list:
        """
        Hit the search_page Wikipedia endpoint.

        Args:
            search_term (str): The term to search for
            limit (int): The number of results to show

        Raises:
            ConnectionError: If request fails

        Returns:
            list: List of pages
        """
        url = WikipediaEnum.URL_SEARCH_PAGE.value
        headers = WikipediaEnum.HEADERS.value
        params = {"q": search_term, "limit": limit}

        try:
            response = requests.get(url=url, headers=headers, params=params)
            response.raise_for_status()
        except Exception:
            raise ConnectionError("Could not search for wikipedia page")
        return response.json()

    def get_page(title: str) -> BeautifulSoup:
        """
        Hit the get_page Wikipedia endpoint.

        Args:
            title (str): Title of page to search for

        Raises:
            ConnectionError: If connection fails

        Returns:
            BeautifuSoup: HTML parser of response
        """
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
