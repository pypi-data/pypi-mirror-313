"""Handle /estimation."""
from ..config import baseConf
from ..conversation import Conversation
from ..utils import info_print


def handle_estimation(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /estimation.

    Command description:
        Toggles displaying the token estimation.

    Usage:
        /estimation [on/true/enable/enabled/off/false/disable/disabled]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["estimation"] = True
        if not silent:
            info_print("Token estimation enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["estimation"] = False
        if not silent:
            info_print("Token estimation disabled.")
        return messages

    baseConf["estimation"] = (not baseConf.get("estimation", False))
    if baseConf.get("estimation", False):
        if not silent:
            info_print("Token estimation enabled.")
    else:
        if not silent:
            info_print("Token estimation disabled.")
    return messages


item_estimation = {
    "fun": handle_estimation,
    "help": "toggles displaying the token estimation",
    "commands": ["estimation"],
}
