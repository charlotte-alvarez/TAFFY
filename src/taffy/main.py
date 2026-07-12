import typer
from typing import Annotated
from taffy.connections.wikipedia import Wikipedia
from taffy.connections.stack_exchange import StackExchange
from taffy.utils.response_parsing import WikipediaParsers, StackExchangeParsers
from taffy.utils.output_text_generators import (
    WikipediaTextGeneration,
    StackExchangeTextGeneration,
)
from taffy.utils.enums import StackExchangeEnum
from taffy.utils.helpers import handle_input

app = typer.Typer(help="TAFFY: The Answer Finder for You!")


@app.command()
def search_wikipedia(
    search_term: str,
    page_limit: Annotated[int, typer.Option(help="The number of pages to suggest")] = 3,
    show_references: Annotated[bool, typer.Option(help="Show references")] = False,
):
    response = Wikipedia.search_page(search_term, page_limit)

    pages = response.get("pages")
    page_list = WikipediaParsers.parse_wiki_pages_for_title_and_description(pages)

    output_text = WikipediaTextGeneration.wikipedia_page_suggestions(page_list)

    user_input = handle_input(output_text, len(page_list))

    if user_input == 0:
        print("Quitting")
        return

    response = Wikipedia.get_page(page_list[user_input - 1][1])
    content = WikipediaParsers.parse_wiki_page_for_content(response)

    print(WikipediaTextGeneration.description_of_page(content))

    while True:
        print("\n\n")
        if show_references:
            references = WikipediaParsers.parse_wiki_page_for_references(response)
            print(WikipediaTextGeneration.references_list(references))

        output_text = WikipediaTextGeneration.additional_sections(content)

        user_input = handle_input(output_text, len(content))

        if user_input == 0:
            print("Quitting")
            return
        else:
            key = list(content.keys())[user_input - 1]
            print(content[key])

        print("\n\n")


@app.command()
def search_stack_exchange(
    search_term: str,
    sort_by_activity: Annotated[
        bool, typer.Option(help="Sort by activity instead of relevance")
    ] = False,
    site: Annotated[
        bool, typer.Option(help="Choose SE site to search on instead of stackoverflow")
    ] = False,
):
    if site:
        response = StackExchange.sites_list()
        sites = StackExchangeParsers.parse_site_dict_for_api_site_param(response)
        output_text = StackExchangeTextGeneration.site_choice(sites)
        user_input = handle_input(output_text, len(sites))
        site_choice = sites[user_input - 1]
    else:
        site_choice = StackExchangeEnum.STACKOVERFLOW_SITE.value

    sort = (
        StackExchangeEnum.ACTIVITY_SORT.value
        if sort_by_activity
        else StackExchangeEnum.RELEVANCE_SORT.value
    )

    response = StackExchange.advanced_search(search_term, sort, site_choice)
    print(response)


if __name__ == "__main__":
    app()
