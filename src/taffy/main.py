import typer
from typing import Annotated
from taffy.connections.wikipedia import Wikipedia
from taffy.utils.response_parsing import (
    parse_wiki_pages_for_title_and_description,
    parse_wiki_page_for_content,
    parse_wiki_page_for_references,
)

app = typer.Typer(help="TAFFY: The Answer Finder for You!")


@app.command()
def search(
    search_term: str,
    wikipedia: Annotated[
        bool, typer.Option(help="Search only wikipedia for page")
    ] = False,
    page_limit: Annotated[int, typer.Option(help="The number of pages to suggest")] = 3,
    show_references: Annotated[bool, typer.Option(help="Show references")] = False,
):
    response = Wikipedia.search_page(search_term, page_limit)

    pages = response.get("pages")
    page_list = parse_wiki_pages_for_title_and_description(pages)
    number_of_pages = len(page_list)

    output_text = ""
    for page in page_list:
        output_text += f"{page[0]} {page[1]}  ---  {page[2]}\n"
    output_text = f"Search for what? (1-{number_of_pages}; 0 quits)\n\n{output_text}"

    user_input = -1

    while True:
        user_input = input(output_text)
        try:
            user_input = int(user_input)
            if 0 <= user_input < number_of_pages + 1:
                break
        except TypeError, ValueError:
            pass

    if user_input == 0:
        print("Quitting")
        return

    response = Wikipedia.get_page(page_list[user_input - 1][1])
    content = parse_wiki_page_for_content(response)

    if wikipedia:
        print("Only searching in wikipedia")
    else:
        print("Searching all sources")

    print("\n\n---------------\n\n")

    # Wikipedia

    print(content.pop("Description"))

    while True:
        print("\n\n")

        if show_references:
            index = 0
            print("References:\n")
            for reference in parse_wiki_page_for_references(response):
                print(f"{index + 1} - {reference}")
                index += 1

        output_text = "Additional Sections\n"
        index = 0
        for section in content:
            output_text += f"{index + 1} - {list(content.keys())[index]}\n"
            index += 1
        output_text = (
            f"---\nSee additional section? (1-{len(content)}; 0 quits)\n\n{output_text}"
        )

        user_input = -1
        number_of_extra_sections = len(content)
        while True:
            user_input = input(output_text)
            try:
                user_input = int(user_input)
                if 0 <= user_input < number_of_extra_sections + 1:
                    break
            except TypeError, ValueError:
                pass

        if user_input == 0:
            print("Quitting")
            return
        else:
            key = list(content.keys())[user_input - 1]
            print(content[key])


if __name__ == "__main__":
    app()
