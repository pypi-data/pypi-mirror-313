"""Handle /tts."""
from ..config import baseConf
from ..conversation import Conversation
from ..utils import info_print


# enables/disables the TTS
def handle_tts(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /tts.

    Command description:
        Toggles the TTS output.

    Usage:
        /tts [on/true/enable/enabled/off/false/disable/disabled]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.lower() in ["on", "true", "enable", "enabled"]:
        baseConf["tts_enabled"] = True
        if not silent:
            info_print("Text-to-speech enabled.")
        return messages

    if given.lower() in ["off", "false", "disable", "disabled"]:
        baseConf["tts_enabled"] = False
        if not silent:
            info_print("Text-to-speech disabled.")
        return messages

    baseConf["tts_enabled"] = (not baseConf.get("tts_enabled", False))
    if baseConf.get("tts_enabled", False):
        if not silent:
            info_print("Text-to-speech enabled.")
    else:
        if not silent:
            info_print("Text-to-speech disabled.")
    return messages


item_tts = {
    "fun": handle_tts,
    "help": "enables/disables the TTS",
    "commands": ["tts"],
}
