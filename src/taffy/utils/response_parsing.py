from bs4 import BeautifulSoup as bs


class WikipediaParsers:
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

            if h2:  # This is for sections not part of the basic description
                h2 = h2.text
                content[h2] = section_text

            else:  # This is for the basic description
                if not content:  # If the start of the basic description
                    content["Description"] = section_text

                else:
                    existing_desc = content["Description"]
                    content["Description"] = existing_desc + "\n" + section_text

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
