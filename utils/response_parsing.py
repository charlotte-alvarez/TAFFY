from bs4 import BeautifulSoup as bs


def parse_wiki_pages_for_title_and_description(pages: list) -> list[tuple]:
    """
    Get the title and descriptions from a list of pages, pack it together with the page number.

    Page number begins at 1.

    Args:
        pages (list): List of pages to parse

    Returns:
        list[tuple]: A list of the tuple [(page number, title, description)]
    """

    page_list = []
    page_num = 1
    for page in pages:
        title = page.get("title")
        description = page.get("description")
        page_list.append((page_num, title, description))
        page_num += 1

    return page_list


def parse_wiki_page_for_content(soup: bs) -> dict:
    """
    Parse a wikipedia page for its relevant content.

    Args:
        soup (bs): The soupy object (html parser BeautifulSoup object)

    Returns:
        dict: Dictionary containing all sections and their content
    """
    pars = soup.find_all("p")
    content = {}

    for par in pars:
        section = par.parent
        section_text = section.get_text()
        h2 = section.find("h2")
        if h2:
            h2 = h2.text

        if h2:
            if h2 in content:  # If part of the same heading2 section
                existing_text = content[h2]
                content[h2] = existing_text + section_text

            else:
                content[h2] = section_text

        else:  # This is for the basic description
            if not content:  # If the start of this section
                content["Description"] = section_text

            else:
                existing_desc = content["Description"]
                content["Description"] = existing_desc + "\n" + "\t" + section_text

    return content


def parse_wiki_page_for_references(soup: bs) -> list:
    """
    Parses through a wikipedia page, returning the references section.

    Args:
        soup (BeautifulSoup): Soupy response

    Returns:
        list: List of references
    """
    refs = soup.find_all("cite")
    text_refs = []
    for r in refs:
        text_refs.append(r.text)

    return text_refs
