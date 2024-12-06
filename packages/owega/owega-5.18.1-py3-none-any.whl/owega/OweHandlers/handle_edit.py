"""Handle /edit."""
import editor
import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


def __edit(txt: str) -> str:
    rval = ''
    if 'edit' in editor.__all__:
        rval = editor.edit(
            contents=txt.encode(
                'utf16', 'surrogatepass'),
            suffix='.md'
        ).decode('utf16')
    elif 'editor' in editor.__all__:
        rval = editor.editor(text=txt)
    return rval


def handle_edit(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /edit.

    Command description:
        Edits the history.

    Usage:
        /edit [message id]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    ids = []
    for msg_id, msg in enumerate(messages.messages):
        if isinstance(msg.get('content', ''), str):
            ids.append(msg_id)
            role = msg.get('role', 'unknown')
            if role == 'user':
                if not silent:
                    print(
                        f"[\033[0;93mUSER\033[0m] [\033[0;92m{msg_id}\033[0m]:"
                    )
                    print('\033[0;37m', end='')
                    print(
                        msg.get('content', '')
                        .encode('utf16', 'surrogatepass')
                        .decode('utf16')
                    )
                    print('\033[0m', end='')
                    print()
            elif role == 'system':
                if not silent:
                    print(
                        "[\033[0;95mSYSTEM\033[0m] "
                        + f"[\033[0;92m{msg_id}\033[0m]:")
                    print('\033[0;37m', end='')
                    print(
                        msg.get('content', '')
                        .encode('utf16', 'surrogatepass')
                        .decode('utf16')
                    )
                    print('\033[0m', end='')
                    print()
            elif role == 'assistant':
                if not silent:
                    print(
                        "[\033[0;96mOWEGA\033[0m] "
                        + f"[\033[0;92m{msg_id}\033[0m]:")
                    print('\033[0;37m', end='')
                    print(
                        msg.get('content', '')
                        .encode('utf16', 'surrogatepass')
                        .decode('utf16')
                    )
                    print('\033[0m', end='')
                    print()
    try:
        if not given:
            if ps['integer'] is not None:
                msg_id = ps['integer'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " message ID ") + ': ')).strip()
            else:
                msg_id = input(
                    '\n' + clrtxt("magenta", " message ID ") + ': ').strip()
        else:
            msg_id = given.split(' ')[0]
            given = ' '.join(given.split(' ')[1:])
    except (ValueError, KeyboardInterrupt, EOFError):
        if not silent:
            info_print("Invalid message ID, cancelling edit")
        return messages

    try:
        msg_id = int(msg_id)
    except ValueError:
        if not silent:
            info_print("Invalid message ID, cancelling edit")
        return messages

    if msg_id not in ids:
        if not silent:
            info_print("Invalid message ID, cancelling edit")
        return messages

    try:
        if not given:
            new_msg = __edit(messages.messages[msg_id].get('content', ''))
        else:
            new_msg = given
    except UnicodeDecodeError:
        if not silent:
            info_print("Error handling given message, edit not saved")
        return messages
    if new_msg:
        messages.messages[msg_id]['content'] = new_msg
    else:
        if not silent:
            info_print("Message empty, deleting it...")
        messages.messages.pop(msg_id)

    return messages


item_edit = {
    "fun": handle_edit,
    "help": "edits the history",
    "commands": ["edit"],
}
