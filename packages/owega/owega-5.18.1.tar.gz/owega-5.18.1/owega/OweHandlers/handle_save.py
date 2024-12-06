"""Handle /save."""
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt


# saves the messages and prompt to a json file
def handle_save(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /save.

    Command description:
        Saves the conversation history to a file.

    Usage:
        /save [history file]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    file_path = ""
    try:
        if given:
            file_path = given
        else:
            if ps['save'] is not None:
                file_path = ps['save'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " file output ") + ': ')).strip()
            else:
                file_path = input(
                    '\n' + clrtxt("magenta", " file output ") + ': ').strip()
        messages.save(file_path)
    except (Exception, KeyboardInterrupt, EOFError):
        if not silent:
            print(
                clrtxt("red", " ERROR ")
                + f": could not write to \"{file_path}\""
            )
    else:
        if not silent:
            print(clrtxt("green", " SUCCESS ") + ": conversation saved!")
    return messages


item_save = {
    "fun": handle_save,
    "help": "saves the conversation history to a file",
    "commands": ["save"],
}
