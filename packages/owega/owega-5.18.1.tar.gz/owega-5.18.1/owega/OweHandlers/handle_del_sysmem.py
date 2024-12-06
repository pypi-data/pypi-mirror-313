"""Handle /del_sysmem."""
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# adds a system message
def handle_del_sysmem(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /del_sysmem.

    Command description:
        Deletes a system souvenir.

    Usage:
        /del_sysmem
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    for index, sysmem in enumerate(messages.systemsouv):
        if not silent:
            print("[\033[0;95mSystem souvenir\033[0m] "
                  + f"[\033[0;92m{index}\033[0m]:")
            print('\033[0;37m', end='')
            print(sysmem)
            print('\033[0m', end='')
            print()
    try:
        if not given:
            if ps['integer'] is not None:
                msg_id = ps['integer'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " message ID ") + ': ')).strip()
            else:
                msg_id = input(
                    '\n' + clrtxt("magenta", " message ID ") + ': ').strip()
        else:
            msg_id = given
    except (ValueError, KeyboardInterrupt, EOFError):
        if not silent:
            info_print("Invalid message ID, cancelling edit")
        return messages

    try:
        msg_id = int(msg_id)
    except ValueError:
        info_print("Invalid message ID, cancelling edit")
        return messages

    if (msg_id < 0) or (msg_id >= len(messages.systemsouv)):
        if not silent:
            info_print("Invalid message ID, cancelling edit")
        return messages

    messages.systemsouv.pop(msg_id)

    return messages


item_del_sysmem = {
    "fun": handle_del_sysmem,
    "help": "deletes a system souvenir",
    "commands": ["del_sysmem"],
}
