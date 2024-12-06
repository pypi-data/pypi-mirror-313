"""Utility functions."""
import json
import subprocess

import bs4
import prompt_toolkit as pt
import requests

try:
    from markdownify import MarkdownConverter as Mc
except ModuleNotFoundError:
    Mc = None
    markdownify_found = False
else:
    markdownify_found = True

from owega.utils import command_text, debug_print

from .functions import Functions

Utility = Functions()


# executes a given string, if bypass is true, do not ask for confirmation
# def __execute(command: str, bypass: bool = False):
def __execute(*args, **kwargs) -> str:
    command = ""
    bypass = False
    if len(args) > 0:
        command = args[0]
        if len(args) > 1:
            command = args[1]
    command = kwargs.get("command", command)
    bypass = kwargs.get("bypass", bypass)
    rdict = {}
    if not bypass:
        print()
        print(command_text("Owega wants to execute the following command:"))
        print(command_text(command))
        user_input = pt.prompt(pt.ANSI(
            command_text("Do you want to run it? (y/N): ")))
        user_input = user_input.lower().strip()
        if (user_input) == "y":
            bypass = True
    if bypass:
        pipes = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        std_out, std_err = pipes.communicate()
        rdict["command_stdout"] = std_out.decode('utf8')
        rdict["command_stderr"] = std_err.decode('utf8')
        rdict["command_status"] = "EXECUTED"
        rdict["return_code"] = pipes.returncode
    else:
        rdict["command_stdout"] = "FAIL: User denied running this command.\n"
        rdict["command_stderr"] = "FAIL: User denied running this command.\n"
        rdict["command_status"] = "FAILED"
        rdict["return_code"] = -1
    return json.dumps(rdict)


__execute_desc = {
    "name": "execute",
    "description": "executes a command on the user's linux computer and "
    + "returns its output",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "the command to run, as a string"
            }
        },
        "required": ["command"],
    },
}


Utility.addFunction(__execute, __execute_desc)


def __html_to_markdown(html):
    soup = bs4.BeautifulSoup(html, features='html.parser')

    if markdownify_found:
        try:
            assert Mc is not None
            debug_print("__html_to_markdown with markdownify", True)
            return Mc().convert_soup(soup)
        except AssertionError:
            pass

    debug_print("__html_to_markdown without markdownify", True)

    # Handle headings
    for i in range(1, 7):
        for tag in soup.find_all(f'h{i}'):
            tag.insert_before('#' * i + ' ')
            tag.unwrap()

    # Handle paragraphs
    for tag in soup.find_all('p'):
        tag.insert_after('\n\n')
        tag.unwrap()

    # Handle bold
    for tag in soup.find_all(['strong', 'b']):
        tag.insert_before('**')
        tag.insert_after('**')
        tag.unwrap()

    # Handle italic
    for tag in soup.find_all(['em', 'i']):
        tag.insert_before('*')
        tag.insert_after('*')
        tag.unwrap()

    # Handle links
    for tag in soup.find_all('a'):
        href = tag.get('href', '')
        text = tag.text
        md_link = f'[{text}]({href})'
        tag.replace_with(md_link)

    # Handle unordered lists
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            li.insert_before('- ')
            li.insert_after('\n')
            li.unwrap()
        ul.unwrap()

    # Handle ordered lists
    for ol in soup.find_all('ol'):
        count = 1
        for li in ol.find_all('li'):
            li.insert_before(f'{count}. ')
            li.insert_after('\n')
            li.unwrap()
            count += 1
        ol.unwrap()

    # Remove all other tags (unwrap -> keep the content)
    for tag in soup.find_all(True):
        # Ensure it's a Tag, not a NavigaleString
        if not isinstance(tag, str):
            tag.unwrap()

    return str(soup)


# gets page
def __get_page(*args, **kwargs) -> str:
    url = "https://example.com"
    if len(args) > 0:
        url = args[0]
    url = kwargs.get("url", url)
    print()
    print(command_text(f"getting page: {url}"))
    rdict = {"status": "error", "page": ""}
    # get request
    req = requests.get(url)
    try:
        # get raw page
        contents = req.text
        # get soup from raw page
        soup = bs4.BeautifulSoup(contents, features='html.parser')
        # strip script and style elements
        for elem in soup.findAll(['script', 'style']):
            elem.extract()
        rdict["status"] = req.reason
        rdict["page"] = __html_to_markdown(str(soup))
    except Exception as e:
        rdict = {}
        if req.ok:
            rdict["status"] = f"{e}"
        else:
            rdict["status"] = req.reason
        rdict["page"] = ""
        pass
    return json.dumps(rdict)


__get_page_desc = {
    "name": "get_page",
    "description": "gets the requested URL, converted to markdown",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "the url to get"
            }
        },
        "required": ["url"],
    },
}


Utility.addFunction(__get_page, __get_page_desc)


# creates a file and fill it with contents
# def __create_file(filename: str, content: str, bypass: bool = False):
def __create_file(*args, **kwargs) -> str:
    filename = ""
    content = ""
    bypass = False
    if len(args) > 0:
        filename = args[0]
        if len(args) > 1:
            content = args[1]
            if len(args) > 2:
                bypass = args[2]
    filename = kwargs.get("filename", filename)
    content = kwargs.get("content", content)
    bypass = kwargs.get("bypass", bypass)
    rdict = {}
    if not filename:
        rdict["status"] = "FAILURE"
        rdict["exception"] = "FAIL: No filename provided.\n"
        return json.dumps(rdict)
    if not bypass:
        print()
        print(command_text(
            f"Owega wants to create {filename} with the following content:"
        ))
        print(content)
        user_input = pt.prompt(pt.ANSI(
            command_text("Do you want to allow it? (y/N): ")))
        user_input = user_input.lower().strip()
        if (user_input) == "y":
            bypass = True
    if bypass:
        try:
            with open(filename, "w") as f:
                f.write(content)
            rdict["status"] = "SUCCESS"
        except Exception as e:
            rdict["status"] = "FAILURE"
            rdict["exception"] = str(e)
    else:
        rdict["status"] = "FAILURE"
        rdict["exception"] = "FAIL: User denied creating this file.\n"
    return json.dumps(rdict)


# add create_file(filename, content) to owega's available functions
__create_file_desc = {
    "name": "create_file",
    "description": "creates a file and writes the given content in it",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "the name of the file to create"
            },
            "content": {
                "type": "string",
                "description": "the content to put in the file, as a string"
            },
        },
        "required": ["filename", "content"],
    },
}


Utility.addFunction(__create_file, __create_file_desc)


Utility.addGroup("utility.user", ["get_page"])
Utility.addGroup("utility.system", ["execute", "create_file"])
Utility.enableGroup("utility.user")
Utility.disableGroup("utility.system")
