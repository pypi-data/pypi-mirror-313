"""Gather all the handlers."""
from ..conversation import Conversation
from ..handlerBase import handler_helps, handlers, items
from ..utils import print_help
from .handle_add_sysmem import item_add_sysmem
from .handle_commands import item_commands
from .handle_context import item_context
from .handle_del_sysmem import item_del_sysmem
from .handle_dinput import item_dinput
from .handle_edit import item_edit
from .handle_estimation import item_estimation
from .handle_fancy import item_fancy
from .handle_finput import item_finput
from .handle_frequency import item_frequency
from .handle_genconf import item_genconf
from .handle_history import item_history
from .handle_image import item_image
from .handle_load import item_load
from .handle_model import item_model
from .handle_presence import item_presence
from .handle_quit import item_quit
from .handle_save import item_save
from .handle_system import item_system
from .handle_temperature import item_temperature
from .handle_time import item_time
from .handle_tokens import item_tokens
from .handle_top_p import item_top_p
from .handle_tts import item_tts


# prints help
def handle_help(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /help."""
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if given:
        pass
    if temp_is_temp:
        pass
    if silent:
        pass
    print_help(handler_helps)
    return messages


item_help = {
    "fun": handle_help,
    "help": "Shows this help",
    "commands": ["help"],
}


def void_func(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Void function."""
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if given:
        pass
    if temp_is_temp:
        pass
    if silent:
        pass
    return messages


def populate() -> None:
    """Gather all the handlers."""
    for item in [
        item_help,
        item_quit,
        item_genconf,
        item_history,
        item_commands,
        item_estimation,
        item_tokens,
        item_context,
        item_save,
        item_load,
        item_model,
        item_finput,
        item_dinput,
        item_temperature,
        item_top_p,
        item_frequency,
        item_presence,
        item_edit,
        item_system,
        item_add_sysmem,
        item_del_sysmem,
        item_tts,
        item_image,
        item_time,
        item_fancy,
    ]:
        items.append(item)

    for item in items:
        for command in item.get('commands', []):
            handler_helps[command] = item.get('help', '')
            handlers[command] = item.get('fun', void_func)


populate()
