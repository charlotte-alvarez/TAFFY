import typer
from typing import Annotated
from taffy.connections.wikipedia import Wikipedia
from taffy.utils.response_parsing import WikipediaParsers
from taffy.utils.output_text_generators import WikipediaTextGeneration
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


if __name__ == "__main__":
    app()
