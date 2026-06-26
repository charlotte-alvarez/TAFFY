from enum import Enum


class WikipediaEnum(Enum):
    HEADERS = {
        "User-Agent": "MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)"
    }
    URL_SEARCH_PAGE = "https://en.wikipedia.org/w/rest.php/v1/search/page"
    URL_GET_PAGE = "https://en.wikipedia.org/w/rest.php/v1/page/{}/html"
