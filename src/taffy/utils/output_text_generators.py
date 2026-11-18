from taffy.utils.enums import StackExchangeEnum
from taffy.utils.response_parsing import WikipediaSection


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

    def additional_sections(section: WikipediaSection) -> str:
        """
        Output text for additional wikipedia page sections

        Args:
            section (WikipediaSection): The current section to parse

        Returns:
            str: generated text
        """
        output_text = "Additional Sections\n"
        index = 0
        for child in section.children:
            output_text += f"{index + 1} - {child.name}\n"
            index += 1
        parent = section.parent.name if section.parent else "Description"
        num_children = len(section.children)
        children = f"See additional section? (1-{num_children});" if num_children > 0 else ""
        output_text = f"-----------\n{children} [Enter] goes up ({parent}); 0 quits)\n\n{output_text}"
        output_text += "\n"

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

    def response(relevant_field_list: list, details: bool):
        """
        Output text for the field list

        Args:
            relevant_field_list (list): List of relevant fields from SE output
            details (bool): Whether to show extra details

        Returns:
            str: generated text
        """
        output_text = "Results:\n"
        index = 0
        for result in relevant_field_list:
            title = result.get(StackExchangeEnum.SEARCH_RESULT_FIELD_TITLE.value)
            creation_date = result.get(
                StackExchangeEnum.SEARCH_RESULT_FIELD_CREATION_DATE.value
            )
            url = result.get(StackExchangeEnum.SEARCH_RESULT_FIELD_LINK.value)
            output_text += (
                f"{index + 1} - {title}\n\tcreated: {creation_date}\n\tlink: {url}"
            )
            if details:
                answered = result.get(
                    StackExchangeEnum.SEARCH_RESULT_FIELD_IS_ANSWERED.value
                )
                owner = result.get(StackExchangeEnum.SEARCH_RESULT_FIELD_OWNER.value)
                score = result.get(StackExchangeEnum.SEARCH_RESULT_FIELD_SCORE.value)
                output_text += f"\n\t\tanswered: {answered}\n\t\towner: {owner}\n\t\tscore: {score}"

            output_text += "\n"
            index += 1

        output_text = f"{output_text}\n\nOpen link? (1 - {index}... 0 exits)  "

        return output_text
