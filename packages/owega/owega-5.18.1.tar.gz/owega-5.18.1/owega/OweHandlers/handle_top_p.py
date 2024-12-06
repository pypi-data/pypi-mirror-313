"""Handle /top_p."""
import prompt_toolkit as pt

from ..config import baseConf
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# change top_p value
def handle_top_p(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /top_p.

    Command description:
        Sets the top_p value (0.0 - 1.0, defaults 1.0).

    Usage:
        /top_p [top_p]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    try:
        new_top_p = float(given)
    except ValueError:
        if not silent:
            info_print(f'Current top_p: {baseConf.get("top_p", 1.0)}')
            info_print('New top_p value (0.0 - 1.0, defaults 1.0)')
        try:
            if ps['float'] is not None:
                new_top_p = ps['float'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " top_p ") + ': ')).strip()
            else:
                new_top_p = input(
                    '\n' + clrtxt("magenta", " top_p ") + ': ').strip()
        except (ValueError, KeyboardInterrupt, EOFError):
            if not silent:
                info_print("Invalid top_p.")
            return messages
    baseConf["top_p"] = float(new_top_p)
    nv = baseConf.get('top_p', 1.0)
    if nv > 1.0:
        if not silent:
            info_print('top_p too high, capping to 1.0')
        baseConf["top_p"] = 1.0
    if nv < 0.0:
        if not silent:
            info_print('top_p too low, capping to 0.0')
        baseConf["top_p"] = 0.0
    if not silent:
        info_print(f'Set top_p to {baseConf.get("top_p", 1.0)}')
    return messages


item_top_p = {
    "fun": handle_top_p,
    "help": "sets the top_p value (0.0 - 1.0, defaults 1.0)",
    "commands": ["top_p"],
}
