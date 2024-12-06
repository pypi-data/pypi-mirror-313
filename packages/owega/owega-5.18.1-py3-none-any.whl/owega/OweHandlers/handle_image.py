"""Handle /image."""
import base64
import binascii
import mimetypes
import os

import prompt_toolkit as pt

from ..config import baseConf
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


def encode_image(filename: str) -> str:
    """
    Return the local image as a base64 url.

    Args:
        filename: The path to the image file to encode.

    Returns:
        The base64url-encoded image.
    """
    if "http" in filename:
        return filename
    out = {
        'str': filename
    }
    try:
        with open(filename, "rb") as image_data:
            mt = mimetypes.guess_type(filename)[0]
            if not isinstance(mt, str):
                mt = 'data'
            out['str'] = f"data:{mt};base64,"
            out['str'] += base64.b64encode(image_data.read()).decode('utf-8')
    except (
            FileNotFoundError,
            IsADirectoryError,
            PermissionError,
            OSError,
            binascii.Error,
            UnicodeDecodeError
    ):
        return ''
    return out['str']


def handle_image(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /image.

    Command description:
        Sends a prompt and an image from an url.

    Usage:
        /image [image path/url] [prompt]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    user_prompt = ''
    if given.split(' ')[0]:
        image_url = given.split(' ')[0]
        user_prompt = ' '.join(given.split(' ')[1:])
    else:
        if ps['main'] is not None:
            image_url = ps['main'].prompt(pt.ANSI(
                clrtxt("yellow", " IMAGE URL ") + ": ")).strip()
        else:
            image_url = input(
                clrtxt("yellow", " IMAGE URL ") + ": ").strip()
    image_url_encoded = encode_image(image_url)
    if not image_url_encoded:
        if not silent:
            info_print(f"Can't access {image_url}")
            if baseConf.get('debug', True):
                info_print(f"we are in {os.getcwd()}")
        return messages
    image_urls = [image_url_encoded]
    if not user_prompt:
        if ps['main'] is not None:
            user_prompt = ps['main'].prompt(pt.ANSI(
                clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
        else:
            user_prompt = input(
                clrtxt("yellow", " PRE-FILE PROMPT ") + ": ").strip()
    messages.add_image(user_prompt, image_urls)
    if not silent:
        info_print("Image added!")
    return messages


item_image = {
    "fun": handle_image,
    "help": "sends a prompt and an image from an url",
    "commands": ["image"],
}
