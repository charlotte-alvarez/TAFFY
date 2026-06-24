import typer
from typing import Annotated
from connections.wikipedia import Wikipedia

app = typer.Typer(help="TAFFY: The Answer Finder for You!")


@app.command()
def search(
    search_term: str,
    wikipedia: Annotated[
        bool, typer.Option(help="Search only wikipedia for page")
    ] = False,
    page_limit: Annotated[int, typer.Option(help="The number of pages to suggest")] = 3,
):
    pages = Wikipedia.search_page(search_term, page_limit)
    page_list = []
    number_of_pages = len(pages)
    page_num = 1
    for page in pages:
        title = page.get("title")
        description = page.get("description")
        page_list.append((page_num, title, description))
        page_num += 1

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

    r = Wikipedia.get_page(page_list[user_input - 1][1])
    print(r)
    if wikipedia:
        print("Only searching in wikipedia")
    else:
        print("Searching all sources")


if __name__ == "__main__":
    app()
