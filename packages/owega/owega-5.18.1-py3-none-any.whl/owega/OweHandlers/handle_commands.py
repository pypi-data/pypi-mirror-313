"""Handle /commands."""
from ..config import baseConf
from ..conversation import Conversation
from ..OwegaFun import existingFunctions
from ..utils import info_print


# enables/disables command execution
def handle_commands(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /commands.

    Command description:
        Toggles command execution / file creation.

    Usage:
        /commands [on/true/enable/enabled/off/false/disable/disabled]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["commands"] = True
        existingFunctions.enableGroup("utility.system")
        if not silent:
            info_print("Command execution enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["commands"] = False
        existingFunctions.disableGroup("utility.system")
        if not silent:
            info_print("Command execution disabled.")
        return messages

    baseConf["commands"] = (not baseConf.get("commands", False))
    if baseConf.get("commands", False):
        existingFunctions.enableGroup("utility.system")
        if not silent:
            info_print("Command execution enabled.")
    else:
        existingFunctions.disableGroup("utility.system")
        if not silent:
            info_print("Command execution disabled.")
    return messages


item_commands = {
    "fun": handle_commands,
    "help": "toggles command execution / file creation",
    "commands": ["commands"],
}
