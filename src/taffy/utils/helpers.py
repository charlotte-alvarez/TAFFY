def handle_input(output_text: str, number_of_options: int) -> int:
    """
    Handles input from the user for selecting options

    Args:
        output_text (str): The text to print
        number_of_options (int): The number of options the user can select

    Returns:
        int: The users selection
    """

    while True:
        user_input = input(output_text)
        try:
            user_input = int(user_input)
            if 0 <= user_input < number_of_options + 1:
                return user_input
        except TypeError, ValueError:
            pass
