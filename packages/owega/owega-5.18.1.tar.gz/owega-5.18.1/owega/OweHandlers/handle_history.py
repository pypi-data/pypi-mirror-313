"""Handle /history."""
from ..conversation import Conversation


# shows chat history
def handle_history(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /history.

    Command description:
        Prints the conversation history.

    Usage:
        /history
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if given:
        pass
    if temp_is_temp:
        pass
    if not silent:
        messages.print_history()
    return messages


item_history = {
    "fun": handle_history,
    "help": "prints the conversation history",
    "commands": ["history"],
}
