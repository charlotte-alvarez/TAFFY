class WikipediaTextGeneration:
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

    def description_of_page(page_content: dict) -> str:
        """
        Output text for the basic description from a wikipedia page

        Args:
            page_content (dict): The dictionary of page content and sections

        Returns:
            str: The output text
        """

        output_text = "\n\n---------------\n\n"
        output_text += page_content.pop("Description")
        output_text += "\n\n"

        return output_text

    def references_list(references: list) -> str:
        """
        Output text for the reference list

        Args:
            refrences (list): List of references

        Returns:
            str: generated text
        """
        output_text = "References:\n"
        index = 0
        for reference in references:
            output_text += f"{index + 1} - {reference}\n"
            index += 1

        return output_text

    def additional_sections(page_content: dict) -> str:
        """
        Output text for additional wikipedia page sections

        Args:
            sections (list): dict of all sections and their content

        Returns:
            str: generated text
        """
        output_text = "Additional Sections\n"
        index = 0
        for section in page_content:
            output_text += f"{index + 1} - {list(page_content.keys())[index]}\n"
            index += 1
        output_text = f"---\nSee additional section? (1-{len(page_content)}; 0 quits)\n\n{output_text}"

        return output_text

class StackExchangeTextGeneration:
    def site_choice(sites: list):
        """
        Output text for the SE site choice

        Args:
            sites (list): List of sites

        Returns:
            str: generated text
        """
        output_text = "Choose site:\n"
        index = 0
        for site in sites:
            output_text += f"{index + 1} - {site}\n"
            index += 1

        return output_text
