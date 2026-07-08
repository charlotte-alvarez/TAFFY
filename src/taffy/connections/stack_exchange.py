import requests
from requests.exceptions import HTTPError
from taffy.utils.enums import StackExchangeEnum
from taffy.utils.errors import ConnectionError


class StackExchange:
    def sites_list() -> list:
        """
        Hit the sites endpoint for stack exchange

        Returns:
            list: List of pages

        Raises:
            ConnectionError: If request fails

        """
        url = StackExchangeEnum.URL_SITES.value

        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except HTTPError:
            raise ConnectionError("Could not search for stack exchange sites")
        return response.json().get("items")

    def advanced_search(query: str) -> dict:
        """
        Hit the advanced search endpoint of the wikipedia api

        Args:
            query (str): Phrase to search for

        Returns:
            dict: Dictionary containing items found
        """

        url = StackExchangeEnum.URL_ADVANCED_SEARCH.value.format(
            VERSION=StackExchangeEnum.VERSION.value, QUERY=query
        )

        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except HTTPError:
            raise ConnectionError("Could not search for query")

        return response.json().get("items")
