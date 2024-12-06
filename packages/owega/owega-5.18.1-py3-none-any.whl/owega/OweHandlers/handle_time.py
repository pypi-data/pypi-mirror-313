"""Handle /time."""
from ..config import baseConf
from ..conversation import Conversation
from ..utils import info_print


def handle_time(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /time.

    Command description:
        Toggles sending the date and time with each message.
        (time-aware mode)

    Usage:
        /time [on/true/enable/enabled/off/false/disable/disabled]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["time_awareness"] = True
        if not silent:
            info_print("Time-aware mode enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["time_awareness"] = False
        if not silent:
            info_print("Time-aware mode disabled.")
        return messages

    baseConf["time_awareness"] = (not baseConf.get("time_awareness", False))
    if baseConf.get("time_awareness", False):
        if not silent:
            info_print("Time-aware mode enabled.")
    else:
        if not silent:
            info_print("Time-aware mode disabled.")
    return messages


item_time = {
    "fun": handle_time,
    "help": "toggles sending the date and time with each message (time-aware)",
    "commands": ["time"],
}
