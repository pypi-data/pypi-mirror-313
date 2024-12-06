"""Handle /file_input."""
import os

import prompt_toolkit as pt

from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import clrtxt, info_print


def guess_language(file_path: str) -> str:
    """
    Try to guess the file's [programming] language.

    Args:
        file_path: The path to the file to guess.

    Returns:
        A string corresponding to the guessed programming language.
    """
    filename = file_path.split('/')[-1].lower()
    if 'iptables' in filename:
        return 'iptables'
    if 'makefile' in filename:
        return 'makefile'

    ext = filename.split('.')[-1]

    known_exts = {}

    def add_exts(i_lang: str, exts) -> None:
        if isinstance(exts, str):
            known_exts[exts] = i_lang.lower()
        else:
            for i_ext in exts:
                known_exts[i_ext] = i_lang.lower()

    def add_sexts(langs) -> None:
        if isinstance(langs, str):
            known_exts[langs] = langs.lower()
        else:
            for i_lang in langs:
                known_exts[i_lang] = i_lang.lower()

    add_exts('brainfuck', ['brainfuck', 'bf'])
    add_exts('c', ['c', 'h'])
    add_exts(
        'cpp',
        ['cpp', 'cxx', 'c++', 'cc', 'hpp', 'hxx', 'h++', 'hh']
    )
    add_exts('csharp', 'cs')
    add_exts('clojure', ['clojure', 'clj'])
    add_exts('diff', ['diff', 'patch'])
    add_exts('dos', ['dos', 'bat', 'cmd'])
    add_exts('elixir', ['elixir', 'ex', 'exs'])
    add_exts('erlang', ['erlang', 'erl'])
    add_exts('fortran', ['fortran', 'f90', 'f95'])
    add_exts('golang', 'go')
    add_exts(
        'xml',
        ['xml', 'rss', 'atom', 'xjb', 'xsd', 'xsl', 'plist', 'svg'])
    add_exts('haskell', ['haskell', 'hs'])
    add_exts('haxe', ['haxe', 'hx'])
    add_exts('julia', ['julia', 'jl'])
    add_exts('kotlin', ['kotlin', 'kt'])
    add_exts('makefile', ['mk', 'mak', 'make', 'makefile'])
    add_exts('markdown', ['markdown', 'md', 'mkdown', 'mkd'])
    add_exts('mirc', ['mirc', 'mrc'])
    add_exts('nim', ['nim', 'nimrod'])
    add_exts('ocaml', ['ocaml', 'ml'])
    add_exts(
        'objc',
        ['objectivec', 'mm', 'objc', 'obj-c', 'obj-c++', 'objective-c++'])
    add_exts('openscad', ['openscad', 'scad'])
    add_exts('perl', ['perl', 'pl', 'pm'])
    add_exts('pgsql', ['pgsql', 'postgres', 'postgresql'])
    add_exts('powershell', ['powershell', 'ps', 'ps1'])
    add_exts('puppet', ['puppet', 'pp'])
    add_exts('python', ['python', 'py', 'gyp'])
    add_exts('rpm', ['rpm-specfile', 'rpm', 'spec', 'rpm-spec', 'specfile'])
    add_exts('ruby', ['ruby', 'rb', 'gemspec', 'podspec', 'thor', 'irb'])
    add_exts('rust', ['rust', 'rs'])
    add_exts('scilab', ['scilab', 'sci'])
    add_exts('tcl', ['tcl', 'tk'])
    add_exts('typescript', ['typescript', 'ts', 'tsx', 'mts', 'cts'])
    add_exts('verilog', ['verilog', 'v'])
    add_exts('yaml', ['yaml', 'yml'])
    add_sexts([
        'ada', 'ino', 'awk', 'sh', 'bash', 'zsh', 'basic', 'bbcode', 'blade',
        'bnf', 'bqn', 'cmake', 'cobol', 'coq', 'csp', 'css', 'd', 'dart',
        'fix', 'gcode', 'gdscript', 'gradle', 'graphql', 'gsql', 'html',
        'xhtml', 'haml', 'hlsl', 'ini', 'toml', 'json', 'java', 'js', 'jsx',
        'tex', 'leaf', 'less', 'lisp', 'lua', 'matlab', 'nix', 'oak', 'ocl',
        'glsl', 'pf', 'php', 'parser3', 'processing', 'prolog', 'properties',
        'qml', 'r', 'sas', 'scss', 'sql', 'scala', 'scheme', 'sfz', 'smali',
        'spl', 'svelte', 'swift', 'thrift', 'toit', 'tp', 'tsql', 'vbnet',
        'vb', 'vba', 'vbscript', 'vbs', 'vhdl', 'vala'
    ])

    lang = known_exts.get(ext.lower(), '')

    if not lang:
        if 'vim' in filename:
            return 'vim'

    return lang


# get input from a file instead of the terminal
def handle_finput(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    """Handle /file_input.

    Command description:
        Sends a prompt and a file from the system.

    Usage:
        /file_input [file] [pre-file prompt]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    if given.split(' ')[0]:
        file_path = given.split(' ')[0]
        given = ' '.join(given.split(' ')[1:])
    else:
        if ps['load'] is not None:
            file_path = ps['load'].prompt(pt.ANSI(
                clrtxt("yellow", " FILE LOCATION ") + ": ")).strip()
        else:
            file_path = input(
                clrtxt("yellow", " FILE LOCATION ") + ": ").strip()
    if (os.path.exists(file_path)):
        if not given:
            if ps['main'] is not None:
                user_prompt = ps['main'].prompt(pt.ANSI(
                    clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
            else:
                user_prompt = input(
                    clrtxt("yellow", " PRE-FILE PROMPT ") + ": ").strip()
        else:
            user_prompt = given
        with open(file_path, "r") as f:
            language = guess_language(file_path)
            file_contents = f.read()
            full_prompt = \
                f"{user_prompt}\n```{language}\n{file_contents}\n```\n"
            messages.add_question(full_prompt)
            if not silent:
                info_print("File added!")
    else:
        if not silent:
            info_print(f"Can't access {file_path}")
    return messages


item_finput = {
    "fun": handle_finput,
    "help": "sends a prompt and a file from the system",
    "commands": ["file_input"],
}
