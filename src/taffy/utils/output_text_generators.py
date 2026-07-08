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
            output_text += f"{index + 1} - {reference}"
            index += 1
