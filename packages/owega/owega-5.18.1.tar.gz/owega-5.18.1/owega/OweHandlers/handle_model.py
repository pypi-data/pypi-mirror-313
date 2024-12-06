"""Handle /model."""
import prompt_toolkit as pt

from ..config import baseConf, list_models
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# changes the selected model
def handle_model(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /model.

    Command description:
        List the available models and prompt for change.

    Usage:
        /model [model name/ID]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if not silent:
        info_print(f"Current model: {baseConf.get('model', '')}")
        list_models()
        print()
    if given:
        new_model = given
    else:
        if ps['model'] is not None:
            new_model = ps['model'].prompt(pt.ANSI(
                '\n' + clrtxt("magenta", " new model ") + ': ')).strip()
        else:
            new_model = input(
                '\n' + clrtxt("magenta", " new model ") + ': ').strip()
    if (new_model.isnumeric()):
        if (int(new_model) < len(baseConf.get("available_models", []))):
            mn = int(new_model)
            baseConf["model"] = baseConf.get("available_models", [])[mn]
            if not silent:
                info_print(f"Model changed to {baseConf.get('model', '')}")
        else:
            if not silent:
                info_print(
                    f"Model not available, keeping {baseConf.get('model', '')}"
                )
    else:
        baseConf["model"] = new_model
        if not silent:
            info_print(f"Model changed to {baseConf.get('model', '')}")
    return messages


item_model = {
    "fun": handle_model,
    "help": "list the available models and prompt for change",
    "commands": ["model"],
}
