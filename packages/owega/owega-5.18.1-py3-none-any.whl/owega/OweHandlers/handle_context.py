"""Handle /context."""
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# change owega's system prompt
def handle_context(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /context.

    Command description:
        Changes the AI's behaviour.

    Usage:
        /context [new context]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given:
        messages.set_context(given)
        if not silent:
            info_print(f"New context: {messages.get_context()}")
        return messages
    if not silent:
        info_print("Old context: " + messages.get_context())
    if ps['context'] is not None:
        new_context = ps['context'].prompt(pt.ANSI(
            '\n' + clrtxt("magenta", " new context ") + ': ')).strip()
    else:
        new_context = input(
            '\n' + clrtxt("magenta", " new context ") + ': ').strip()
    if new_context:
        messages.set_context(new_context)
        if not silent:
            info_print(f"New context: {messages.get_context()}")
    else:
        if not silent:
            info_print("New context empty, keeping old context!")
    return messages


item_context = {
    "fun": handle_context,
    "help": "changes the AI's behaviour",
    "commands": ["context"],
}
