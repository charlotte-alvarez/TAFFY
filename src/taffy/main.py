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
from rich import print as richprint

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

    curr_section = content

    while True:
        print("\n\n")
        richprint(f"[red]{curr_section.text}[/red]")
        print("\n\n")
        output_text = WikipediaTextGeneration.additional_sections(curr_section)

        user_input = handle_input(output_text)

        if user_input == 0:
            print("Quitting")
            return
        if not user_input:
            if curr_section.has_parent():
                curr_section = curr_section.parent
        else:
            try:
                i = int(user_input)
            except Exception:
                continue

            if i - 1 in range(len(curr_section.children)):
                curr_section = curr_section.children[i - 1]

        if show_references:
            references = WikipediaParsers.parse_wiki_page_for_references(response)
            print(WikipediaTextGeneration.references_list(references))
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
    details: Annotated[
        bool,
        typer.Option(
            help="Whether to show extra details in results like score and owner"
        ),
    ] = False,
    num_results: Annotated[int, typer.Option(help="Number of results (1-30)")] = 6,
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
    response = response[: num_results + 1]

    relevant_field_list = (
        StackExchangeParsers.parse_search_response_for_relevant_fields(response)
    )

    output_text = StackExchangeTextGeneration.response(relevant_field_list, details)
    while True:
        user_input = handle_input(output_text, len(relevant_field_list))

        try:
            user_input = int(user_input)
        except Exception:
            continue

        if user_input > num_results + 1 or user_input < 0:
            continue

        if user_input == 0:
            print("Quitting")
            return

        else:
            import webbrowser

            link = relevant_field_list[user_input - 1].get(
                StackExchangeEnum.SEARCH_RESULT_FIELD_LINK.value
            )
            opened = webbrowser.open(link)

            if not opened:
                print("\nCould not open browser, try copy/pasting link instead!\n\n")


if __name__ == "__main__":
    app()
