from enum import Enum


class WikipediaEnum(Enum):
    HEADERS = {
        "User-Agent": "MediaWiki REST API docs examples/0.1 (https://www.mediawiki.org/wiki/API_talk:REST_API)"
    }
    URL_SEARCH_PAGE = "https://en.wikipedia.org/w/rest.php/v1/search/page"
    URL_GET_PAGE = "https://en.wikipedia.org/w/rest.php/v1/page/{}/html"


class StackExchangeEnum(Enum):
    VERSION = "2.3"
    URL_SITES = f"https://api.stackexchange.com/{VERSION}/sites"
    URL_ADVANCED_SEARCH = "https://api.stackexchange.com/{VERSION}/search/advanced?order=desc&sort={SORT}&q={QUERY}&site={SITE}"
    STACKOVERFLOW_SITE = "stackoverflow"
    ACTIVITY_SORT = "activity"
    RELEVANCE_SORT = "relevance"
