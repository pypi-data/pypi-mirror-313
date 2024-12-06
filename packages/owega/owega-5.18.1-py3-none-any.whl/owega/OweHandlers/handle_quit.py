"""Handle /quit."""
from ..conversation import Conversation
from ..utils import do_quit, success_msg


# quits the program, deleting temp_file
def handle_quit(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /quit.

    Command description:
        Exits the program.

    Usage:
        /quit
        /exit
    """
    # removes linter warning about unused arguments
    if given:
        pass
    if silent:
        pass
    do_quit(
        success_msg(),
        temp_file=temp_file,
        is_temp=temp_is_temp,
        should_del=temp_is_temp
    )
    return messages


item_quit = {
    "fun": handle_quit,
    "help": "exits the program",
    "commands": ["quit", "exit"],
}
