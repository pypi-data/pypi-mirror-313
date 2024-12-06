"""Handle /dir_input."""
import os

import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print
from .handle_finput import guess_language


def is_readable(filename: str) -> bool:
    try:
        open(filename, 'r').read()
    except UnicodeDecodeError:
        return False
    return True


def file_list(path: str = '.') -> list[str]:
    rval = []
    for root, _, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            if '.git' not in filename.split('/'):
                rval.append(filename)
    return rval


# send a whole directory structure as /file_input
def handle_dinput(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /dir_input.

    Command description:
        Sends text-readable files from a given directory.

    Usage:
        /dir_input [directory]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given:
        dir_path = given
    else:
        if ps['dirload'] is not None:
            dir_path = ps['dirload'].prompt(pt.ANSI(
                clrtxt("yellow", " DIR LOCATION ") + ": ")).strip()
        else:
            dir_path = input(
                clrtxt("yellow", " DIR LOCATION ") + ": ").strip()
    for file_path in file_list(dir_path):
        if (is_readable(file_path)):
            user_prompt = f'{file_path}:'
            with open(file_path, "r") as f:
                language = guess_language(file_path)
                file_contents = f.read()
                full_prompt = \
                    f"{user_prompt}\n```{language}\n{file_contents}\n```\n"
                messages.add_question(full_prompt)
                if not silent:
                    info_print(f"File added: {file_path}")
        pass
    return messages


item_dinput = {
    "fun": handle_dinput,
    "help": "sends text-readable files from a given directory",
    "commands": ["dir_input"],
}
