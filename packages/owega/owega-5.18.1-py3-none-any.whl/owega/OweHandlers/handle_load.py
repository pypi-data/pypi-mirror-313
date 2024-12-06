"""Handle /load."""
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt


# loads the messages and prompt from a json file
def handle_load(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /load.

    Command description:
        Loads the conversation history from a file.

    Usage:
        /load [history file]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    file_path = ''
    try:
        if given:
            file_path = given
        else:
            if ps['load'] is not None:
                file_path = ps['load'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " file to load ") + ': ')).strip()
            else:
                file_path = input(
                    '\n' + clrtxt("magenta", " file to load ") + ': ').strip()
        messages.load(file_path)
    except (Exception, KeyboardInterrupt, EOFError):
        if not silent:
            print(
                clrtxt("red", " ERROR ")
                + f": could not read from \"{file_path}\""
            )
    else:
        if not silent:
            print(clrtxt("green", " SUCCESS ") + ": conversation loaded!")
    return messages


item_load = {
    "fun": handle_load,
    "help": "loads the conversation history from a file",
    "commands": ["load"],
}
