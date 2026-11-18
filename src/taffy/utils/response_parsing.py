from bs4 import BeautifulSoup as bs
from taffy.utils.enums import StackExchangeEnum as see


class WikipediaSection:
    def __init__(
        self,
        name: str,
        text: str,
        parent: WikipediaSection = None,
        children: list | None = None,
    ):
        self.name = name
        self.text = text
        self.parent = parent
        self.children = [] if children is None else children

    def add_child(self, section: WikipediaSection):
        self.children.append(section)

    def has_parent(self):
        return self.parent != None


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

    def parse_wiki_page_for_content(soup: bs) -> WikipediaSection:
        """
        Parse a wikipedia page for its relevant content.

        Args:
            soup (bs): The soupy object (html parser BeautifulSoup object)

        Returns:
            WikipediaSection: The root section, usually the description
        """
        sections = soup.find_all("section")
        desc = sections.pop(0)
        desc_text = desc.get_text()

        root = WikipediaSection("Description", desc_text)

        for section in sections:
            h2 = section.find("h2")

            if h2:
                text = []

                for element in h2.find_all_next():
                    if element.name == "h3":
                        break

                    if element.name == "p":
                        text.append(f"{element.get_text()}\n\n")

                text = " ".join(text)

                s = WikipediaSection(h2.get_text(), text, root)
                last_parent = s
                root.add_child(s)

            else:
                h3 = section.find("h3")
                if h3:
                    s = WikipediaSection(h3.get_text(), section.get_text(), last_parent)
                    last_parent.add_child(s)

        return root

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


class StackExchangeParsers:
    def parse_site_dict_for_api_site_param(sites_response: dict) -> list:
        """
        Get a list of API site parameters from a dictionary of site objects

        Args:
            sites_response(dict): A dictionary of site objects

        Returns:
            list: List of api site parameters of each site
        """

        sites_list = []
        for site_object in sites_response:
            sites_list.append(site_object.get("api_site_parameter"))

        return sites_list

    def parse_search_response_for_relevant_fields(search_response: list) -> list:
        """
        Get a list of dictionaries with only the relevant information in them

        Args:
            search_response (list): List of dictionaries with all
        information returned from SE

        Returns:
            list: List of dictionaries with only relevant information
        """
        title = see.SEARCH_RESULT_FIELD_TITLE.value
        owner = see.SEARCH_RESULT_FIELD_OWNER.value
        creation_date = see.SEARCH_RESULT_FIELD_CREATION_DATE.value
        is_answered = see.SEARCH_RESULT_FIELD_IS_ANSWERED.value
        score = see.SEARCH_RESULT_FIELD_SCORE.value
        link = see.SEARCH_RESULT_FIELD_LINK.value

        parsed_list = []
        for result in search_response:
            d = {
                title: result.get(title),
                owner: result.get(owner),
                creation_date: result.get(creation_date),
                is_answered: result.get(is_answered),
                score: result.get(score),
                link: result.get(link),
            }
            parsed_list.append(d)

        return parsed_list
