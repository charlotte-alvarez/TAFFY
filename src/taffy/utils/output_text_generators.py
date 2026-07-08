def wikipedia_page_suggestions(page_list: list[tuple]):
    """
    Generate output text for wikipedia page suggestions

    Args:
        page_list (list[tuple]): list of page tuples (page number, page title, short desc)
    """

    output_text = ""
    for page in page_list:
        output_text += f"{page[0]} {page[1]}  ---  {page[2]}\n"
    output_text = f"Search for what? (1-{len(page_list)}; 0 quits)\n\n{output_text}"

    return output_text
