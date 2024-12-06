"""Handle /system."""
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# adds a system message
def handle_system(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /system.

    Command description:
        Adds a system prompt in the chat.

    Usage:
        /system [message]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if not given:
        try:
            if ps['main'] is not None:
                given = ps['main'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " System message ") + ": "
                )).strip()
            else:
                given = input(
                    '\n' + clrtxt("magenta", " System message ") + ": "
                ).strip()
        except (KeyboardInterrupt, EOFError):
            return messages
    if given:
        messages.add_system(given)
    else:
        if not silent:
            info_print("System message empty, not adding.")
    return messages


item_system = {
    "fun": handle_system,
    "help": "adds a system prompt in the chat",
    "commands": ["system"],
}
