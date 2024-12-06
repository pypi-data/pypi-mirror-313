"""Prompt sessions."""
import os
import re
from typing import Generator

import prompt_toolkit as pt
from prompt_toolkit import (auto_suggest, completion, history, key_binding,
                            validation)

from ..handlerBase import handlers
from ..utils import get_home_dir
from .main_bottom_toolbar import main_bottom_toolbar


def set_ps(i_ps) -> None:
    """Set the prompt sessions."""
    # generate completion from command list (handlers)
    command_list = ['/' + command for command in handlers.keys()]

    # CTRL+N makes a new line
    main_kb = key_binding.KeyBindings()

    @main_kb.add('c-n')
    def _(event) -> None:
        event.current_buffer.insert_text('\n')

    # this defines how newlines are shown
    def main_prompt_continuation(width, line_number, is_soft_wrap) -> str:
        cont = '...'
        try:
            if (line_number > 9999):
                cont = '!!!'
        except (TypeError, ValueError):
            pass
        if is_soft_wrap:
            cont = '   '
        if (width >= 4):
            return (' ' * (width - 4)) + cont + ' '
        else:
            return ' ' * width

    # get main style
    main_style = main_bottom_toolbar("style")

    class SlashCommandCompleter(completion.WordCompleter):
        def __init__(self, words, ignore_case=False) -> None:
            super().__init__(words, ignore_case=ignore_case)
            # Define a regex pattern that includes the slash as a word char
            self.pattern = re.compile(r'[^ \t\n\r\f\v]+')

        def get_completions(self, document, complete_event) -> Generator:
            if complete_event:
                pass  # removes a linting warning
            # Use the custom pattern to find the word before the cursor
            word_before_cursor = document.get_word_before_cursor(
                pattern=self.pattern)
            if isinstance(self.words, list):
                for word in self.words:
                    if word.startswith(word_before_cursor):
                        yield completion.Completion(
                            word, -len(word_before_cursor))

    # keyword autocompletion
    main_completer = SlashCommandCompleter(
        words=command_list,
        ignore_case=True
    )

    try:
        # main session, for general context
        i_ps['main'] = pt.PromptSession(
            history=history.FileHistory(
                '' + get_home_dir() + '/.owega.history'
            ),
            completer=main_completer,
            complete_while_typing=True,
            complete_in_thread=True,
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            bottom_toolbar=main_bottom_toolbar,
            style=main_style,
            key_bindings=main_kb,
            prompt_continuation=main_prompt_continuation,
        )

        # context session, when editing owega's system prompt
        i_ps['context'] = pt.PromptSession()

        class SaveValidator(validation.Validator):
            def validate(self, document) -> None:
                text = document.text

                if os.path.isdir(text):
                    raise validation.ValidationError(
                        message='you specified a directory, not a file',
                        cursor_position=len(text)
                    )
                elif not os.path.isdir(os.path.dirname(text)):
                    raise validation.ValidationError(
                        message='parent dir does not exist, cannot create file',
                        cursor_position=len(text)
                    )

        i_ps['save'] = pt.PromptSession(
            completer=completion.PathCompleter(),
            validator=SaveValidator()
        )

        class LoadValidator(validation.Validator):
            def validate(self, document) -> None:
                text = document.text

                if os.path.isdir(text):
                    raise validation.ValidationError(
                        message='this is a directory, not a file',
                        cursor_position=len(text)
                    )

                if not os.path.isfile(text):
                    raise validation.ValidationError(
                        message='file does not exist',
                        cursor_position=len(text)
                    )

        class DirValidator(validation.Validator):
            def validate(self, document) -> None:
                text = document.text

                if not os.path.isdir(text):
                    raise validation.ValidationError(
                        message='this is not a directory',
                        cursor_position=len(text)
                    )

        i_ps['load'] = pt.PromptSession(
            completer=completion.PathCompleter(),
            validator=LoadValidator()
        )

        i_ps['dirload'] = pt.PromptSession(
            completer=completion.PathCompleter(),
            validator=DirValidator()
        )

        # file session, with file completion
        i_ps['file'] = pt.PromptSession(
            completer=completion.PathCompleter()
        )

        # file session with file completion for file_input directive
        i_ps['file_input'] = pt.PromptSession(
            completer=completion.PathCompleter()
        )

        # model session, for model selection
        # TODO: add model completion
        i_ps['model'] = pt.PromptSession()

        class IntegerValidator(validation.Validator):
            def validate(self, document) -> None:
                text = document.text

                try:
                    int(text)
                except ValueError:
                    raise validation.ValidationError(
                        message='This input contains non-numeric characters',
                        cursor_position=len(text)
                    )

        class FloatValidator(validation.Validator):
            def validate(self, document) -> None:
                text = document.text

                try:
                    float(text)
                except ValueError:
                    raise validation.ValidationError(
                        message='This input is not a valid floating-point'
                        ' number',
                        cursor_position=len(text)
                    )

        i_ps['integer'] = pt.PromptSession(validator=IntegerValidator())
        i_ps['float'] = pt.PromptSession(validator=FloatValidator())
    except AttributeError:
        i_ps['main'] = None
        i_ps['context'] = None
        i_ps['save'] = None
        i_ps['load'] = None
        i_ps['dirload'] = None
        i_ps['file'] = None
        i_ps['file_input'] = None
        i_ps['model'] = None
        i_ps['integer'] = None
        i_ps['float'] = None


ps = {}
