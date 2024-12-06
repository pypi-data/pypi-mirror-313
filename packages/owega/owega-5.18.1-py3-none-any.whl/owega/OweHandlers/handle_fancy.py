"""Handle /fancy."""
from ..config import baseConf
from ..conversation import Conversation
from ..utils import info_print


def handle_fancy(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /fancy.

    Command description:
        Toggles fancy printing (requires python-rich).

    Usage:
        /fancy [on/true/enable/enabled/off/false/disable/disabled]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["fancy"] = True
        if not silent:
            info_print("Fancy printing enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["fancy"] = False
        if not silent:
            info_print("Fancy printing disabled.")
        return messages

    baseConf["fancy"] = (not baseConf.get("fancy", False))
    if baseConf.get("fancy", False):
        if not silent:
            info_print("Fancy printing enabled.")
    else:
        if not silent:
            info_print("Fancy printing disabled.")
    return messages


item_fancy = {
    "fun": handle_fancy,
    "help": "toggles fancy printing (requires python-rich)",
    "commands": ["fancy"],
}
