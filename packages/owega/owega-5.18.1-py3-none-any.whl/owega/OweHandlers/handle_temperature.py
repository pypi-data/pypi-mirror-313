"""Handle /temperature."""
import prompt_toolkit as pt

from ..config import baseConf
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


# change temperature
def handle_temperature(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /temperature.

    Command description:
        Sets the temperature (0.0 - 1.0, defaults 0.8).

    Usage:
        /temperature [temperature]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    try:
        new_temperature = float(given)
    except ValueError:
        if not silent:
            info_print(
                'Current temperature: '
                + f'{baseConf.get("temperature", 1.0)}')
            info_print('New temperature value (0.0 - 2.0, defaults 0.8)')
        try:
            if ps['float'] is not None:
                new_temperature = ps['float'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " temperature ") + ': ')).strip()
            else:
                new_temperature = input(
                    '\n' + clrtxt("magenta", " temperature ") + ': ').strip()
        except (ValueError, KeyboardInterrupt, EOFError):
            if not silent:
                info_print("Invalid temperature.")
            return messages
    baseConf["temperature"] = float(new_temperature)
    nv = baseConf.get('temperature', 0.0)
    if nv > 2.0:
        if not silent:
            info_print('Temperature too high, capping to 2.0')
        baseConf["temperature"] = 2.0
    if nv < 0.0:
        if not silent:
            info_print('Temperature negative, capping to 0.0')
        baseConf["temperature"] = 0.0
    if not silent:
        info_print(
            'Set temperature to '
            + f'{baseConf.get("temperature", 0.0)}')
    return messages


item_temperature = {
    "fun": handle_temperature,
    "help": "sets the temperature (0.0 - 1.0, defaults 0.8)",
    "commands": ["temperature"],
}
