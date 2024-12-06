"""Handles the changelog."""
from .changelogEntry import ChangelogEntry
from .version import Version


class Changelog:
    """Contains the Owega Changelog."""

    def __init__(self) -> None:
        """Initialize the changelog."""
        self.logs = []
        self.log = ""
        self.version = Version(0, 0, 0)
        self.version_str = '0.0.0'
        self.initLogs()
        self.genLog()

    def initLogs(self) -> None:
        """Fill the changelog."""
        self.logs.append(
            ChangelogEntry(5, 18, 1)
            .addLine("Added fancy err message for flagged messages (OpenAI).")
        )
        self.logs.append(
            ChangelogEntry(5, 18, 0)
            .addLine("Fixed function calling for mistral.")
        )

        self.logs.append(
            ChangelogEntry(5, 17, 2)
            .addLine("Cleaned up codebase a little, thanks pycharm...")
        )
        self.logs.append(
            ChangelogEntry(5, 17, 1)
            .addLine("Fixed logger error preventing owega from opening on")
            .addLine("Windows... I am so sorry I didn't catch this earlier!")
            .addLine(">w<")
        )
        self.logs.append(
            ChangelogEntry(5, 17, 0)
            .addLine("Added xAI (grok) support!")
            .addLine("Supports everything, even function calling and vision!")
        )

        self.logs.append(
            ChangelogEntry(5, 16, 4)
            .addLine("Fix for claude: enforce non-streaming mode")
            .addLine("(fixes the 'overloaded_error' errors)")
        )
        self.logs.append(
            ChangelogEntry(5, 16, 3)
            .addLine("Added a .md prefix to the temp file with /edit")
            .addLine("(for editor syntax highlighting)")
        )
        self.logs.append(
            ChangelogEntry(5, 16, 2)
            .addLine("Fixed vision support for Anthropic's claude... Again.")
        )
        self.logs.append(
            ChangelogEntry(5, 16, 1)
            .addLine("Fixed vision support for Anthropic's claude")
        )
        self.logs.append(
            ChangelogEntry(5, 16, 0)
            .addLine("Rewrite ask.py, better handling")
        )

        self.logs.append(
            ChangelogEntry(5, 15, 2)
            .addLine("- Fixed 5.15.1, as I mistyped 4o-(preview/mini)")
            .addLine("  insead of o1-(preview/mini)")
        )
        self.logs.append(
            ChangelogEntry(5, 15, 1)
            .addLine("- Added o1-preview and o1-mini to default models list.")
        )
        self.logs.append(
            ChangelogEntry(5, 15, 0)
            .addLine("OpenAI o1 update.")
            .addLine("Adds support for OpenAI's o1 models, which are limited,")
            .addLine("as they lack support for temperature, top_p, penalties,")
            .addLine("vision, and function calling.")
        )

        self.logs.append(
            ChangelogEntry(5, 14, 0)
            .addLine("Image generation update.")
            .addLine("Allows for the AI to generate images using DALLE")
        )

        self.logs.append(
            ChangelogEntry(5, 13, 3)
            .addLine("- Fixed errors with some versions of python-editor which")
            .addLine("  don't have editor.edit but editor.editor()???")
            .addLine("  Somehow... I don't know maaaan, I'm tireeeed =w='")
        )
        self.logs.append(
            ChangelogEntry(5, 13, 2)
            .addLine("- Fixed compatibility with python <3.11 by removing")
            .addLine("  typing.Self references.")
        )
        self.logs.append(
            ChangelogEntry(5, 13, 1)
            .addLine("- Changed tiktoken dep from required to optional.")
        )
        self.logs.append(
            ChangelogEntry(5, 13, 0)
            .addLine("Dependency removal update.")
            .addLine("- Changed markdownify dep from required to optional.")
            .addLine("- Changed pygame dep from required to optional.")
        )

        self.logs.append(
            ChangelogEntry(5, 12, 0)
            .addLine("Added /fancy, for toggling fancy printing.")
        )

        self.logs.append(
            ChangelogEntry(5, 11, 0)
            .addLine("Added support for Anthropic's Claude.")
        )

        self.logs.append(
            ChangelogEntry(5, 10, 0)
            .addLine("Moved single_ask to owega.ask, moved markdown_print to")
            .addLine("owega.utils.")
        )

        self.logs.append(
            ChangelogEntry(5, 9, 4)
            .addLine("Fixed a circular import, which technically wasn't really")
            .addLine("an issue, due to an old AWFUL AF fix...")
            .addLine("Also, fixed most type hinting.")
        )
        self.logs.append(
            ChangelogEntry(5, 9, 3)
            .addLine("Added __all__ variable to __init__.py files.")
        )
        self.logs.append(
            ChangelogEntry(5, 9, 2)
            .addLine("Added a tts_to_opus function in owega.utils.")
        )
        self.logs.append(
            ChangelogEntry(5, 9, 1)
            .addLine("Changed type hinting and fixed some code style!")
        )
        self.logs.append(
            ChangelogEntry(5, 9, 0)
            .addLine("Fixed a huge issue where owega couldn't be imported if")
            .addLine("the terminal wasn't interactive.")
            .addLine("Added owega.__version__")
        )

        self.logs.append(
            ChangelogEntry(5, 8, 6)
            .addLine("Updated the README with 5.7.5 demos.")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 5)
            .addLine("Changed setup.py to package the VERSION and CHANGELOG")
            .addLine("files.")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 4)
            .addLine("Fixed an issue with time-aware mode which would create")
            .addLine("new lines with just the date when sending an empty")
            .addLine("message, instead of just prompting with same history.")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 3)
            .addLine("Fixed some error handling.")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 2)
            .addLine("Oops, I didn't completely fix it last time~ Awoo! >w<\\")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 1)
            .addLine("Oops, I broke the build system again, my bad! :P")
        )
        self.logs.append(
            ChangelogEntry(5, 8, 0)
            .addLine("Added time-aware mode...")
        )

        self.logs.append(
            ChangelogEntry(5, 7, 5)
            .addLine("Fixed the bottom toolbar being cut short when terminal")
            .addLine("doesn't have enough columns.")
            .addLine("(also, added gpt-4o and mixtral-8x22b to default list)")
        )
        self.logs.append(
            ChangelogEntry(5, 7, 4)
            .addLine("Added pretty print if the rich module is installed.")
        )
        self.logs.append(
            ChangelogEntry(5, 7, 3)
            .addLine("Better cost estimation, including input/output costs.")
            .addLine("(added support for all GPT model as of 2024-05-14)")
            .addLine("(added support for all mistral API models as of today)")
            .addLine("(all other models return a cost of 0)")
        )
        self.logs.append(
            ChangelogEntry(5, 7, 2)
            .addLine("Added vision support for GPT-4o.")
        )
        self.logs.append(
            ChangelogEntry(5, 7, 1)
            .addLine("Fixed a non-ascii character in the DGPL.")
        )
        self.logs.append(
            ChangelogEntry(5, 7, 0)
            .addLine("Changed the license to the DarkGeem Public License v1.0.")
        )

        self.logs.append(
            ChangelogEntry(5, 6, 4)
            .addLine("Fix for ask.ask() crashing if OPENAI_API_KEY isn't set.")
        )
        self.logs.append(
            ChangelogEntry(5, 6, 3)
            .addLine("Fixes config's api_key not being used.")
            .addLine("Better docstrings on handlers.")
        )
        self.logs.append(
            ChangelogEntry(5, 6, 2)
            .addLine("Added terminal title status :3")
        )
        self.logs.append(
            ChangelogEntry(5, 6, 1)
            .addLine("Added extensive logging for errors.")
        )
        self.logs.append(
            ChangelogEntry(5, 6, 0)
            .addLine("Added basic support for Chub's API")
            .addLine("(chub mars, mercury, mixtral)")
            .addLine("Also, Mi(s/x)tral support is no more in beta :D")
        )

        self.logs.append(
            ChangelogEntry(5, 5, 5)
            .addLine("Now using openai module to ask mistral API.")
            .addLine("(the code is waaaay cleaner)")
        )
        self.logs.append(
            ChangelogEntry(5, 5, 4)
            .addLine("Fixed a debug_print never showing.")
        )
        self.logs.append(
            ChangelogEntry(5, 5, 3)
            .addLine("Removed debug lines that shouldn't have been left there.")
        )
        self.logs.append(
            ChangelogEntry(5, 5, 2)
            .addLine("Added debug info on mistral's part of ask()")
            .addLine("Added matching for mixtral")
        )
        self.logs.append(
            ChangelogEntry(5, 5, 1)
            .addLine("Removed useless available_mistral and mistral_model")
            .addLine(" variables.")
        )
        self.logs.append(
            ChangelogEntry(5, 5, 0)
            .addLine("Added basic support for Mistral's API (beta feature)")
        )

        self.logs.append(
            ChangelogEntry(5, 4, 0)
            .addLine("Added default_prompt variable in configuration")
        )

        self.logs.append(
            ChangelogEntry(5, 3, 1)
            .addLine("Re-enabled get_page with better parsing")
        )
        self.logs.append(
            ChangelogEntry(5, 3, 0)
            .addLine("Added /dir_input")
        )

        self.logs.append(
            ChangelogEntry(5, 2, 2)
            .addLine("Suppressed pygame-related warnings")
            .addLine("(i.e. avx2 not enabled).")
        )
        self.logs.append(
            ChangelogEntry(5, 2, 1)
            .addLine("Fixed the create_file function, disabled get_page.")
        )
        self.logs.append(
            ChangelogEntry(5, 2, 0)
            .addLine("Changed file_input behavior to only add the prompt and")
            .addLine("not immediately request an answer.")
        )

        self.logs.append(
            ChangelogEntry(5, 1, 1)
            .addLine("Fixed handle_image")
        )
        self.logs.append(
            ChangelogEntry(5, 1, 0)
            .addLine("Added silent flag for handlers.")
        )

        self.logs.append(
            ChangelogEntry(5, 0, 4)
            .addLine("Added better given handling for handlers.")
        )
        self.logs.append(
            ChangelogEntry(5, 0, 3)
            .addLine("Added a play_tts function for using owega as a module.")
        )
        self.logs.append(
            ChangelogEntry(5, 0, 2)
            .addLine("Changed the /image given handling, now you can give it")
            .addLine("  both the image, then a space, then the pre-image prompt.")
        )
        self.logs.append(
            ChangelogEntry(5, 0, 1)
            .addLine("Added support for local images for vision")
            .addLine("Also, better crash handling...")
        )
        self.logs.append(
            ChangelogEntry(5, 0, 0)
            .addLine("ADDED VISION")
        )

        self.logs.append(
            ChangelogEntry(4, 12, 10)
            .addLine("Added docstrings")
            .addLine("Switched from tabs to spaces (PEP8)")
            .addLine("Changed default available models")
            .addLine("Changed estimation token cost values")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 9)
            .addLine("Added badges to the README :3")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 8)
            .addLine("Added a vim modeline to history files")
            .addLine("  to specify it's json5, not json.")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 7)
            .addLine('Fixed a minor bug where /file_input would insert a "\'"')
            .addLine("  after the file contents.")
            .addLine("Also, added filetype information on codeblocks with")
            .addLine("  /file_input, depending on the file extension")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 6)
            .addLine("Fixed emojis crashing the edit function because utf16")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 5)
            .addLine("Fixed emojis crashing the history because utf16")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 4)
            .addLine("Fixed requirements to use json5 instead of json-five")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 3)
            .addLine("Fixed requirements to be more lenient")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 2)
            .addLine("Fixed TUI-mode TTS")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 1)
            .addLine("Added -e/--estimate option to estimate consumption")
        )
        self.logs.append(
            ChangelogEntry(4, 12, 0)
            .addLine("Added -T/--training option to generate training line")
        )

        self.logs.append(
            ChangelogEntry(4, 11, 5)
            .addLine("Fixed requirements in setup.py not working when getting")
            .addLine("the source from PyPI")
        )
        self.logs.append(
            ChangelogEntry(4, 11, 4)
            .addLine("Fixed edit with blank message (remove message)")
        )
        self.logs.append(
            ChangelogEntry(4, 11, 3)
            .addLine("Fixed /genconf")
        )
        self.logs.append(
            ChangelogEntry(4, 11, 2)
            .addLine("Fixed -a / single_ask")
        )
        self.logs.append(
            ChangelogEntry(4, 11, 1)
            .addLine("Oops, last version broke owega, fixed here")
            .addLine("(Problem was I forgot to export submodules in setup.py)")
        )
        self.logs.append(
            ChangelogEntry(4, 11, 0)
            .addLine("Huge refactor, added TTS as config parameter")
        )

        self.logs.append(
            ChangelogEntry(4, 10, 3)
            .addLine("- changed from OpenAI to Owega in term display")
        )
        self.logs.append(
            ChangelogEntry(4, 10, 2)
            .addLine("- added cost estimation in token estimation")
        )
        self.logs.append(
            ChangelogEntry(4, 10, 1)
            .addLine("- added support server in readme and pypi")
        )
        self.logs.append(
            ChangelogEntry(4, 10, 0)
            .addLine("- added system souvenirs (add_sysmem/del_sysmem)")
        )

        self.logs.append(
            ChangelogEntry(4, 9, 0)
            .addLine("- added system command")
        )

        self.logs.append(
            ChangelogEntry(4, 8, 2)
            .addLine("- added infos to pypi page")
            .addLine("- changed to automatic script generation (setup.py)")
        )
        self.logs.append(
            ChangelogEntry(4, 8, 1)
            .addLine("Oops, forgot to add requirements to setup.py")
            .addLine("Automated the process, should be good now")
        )
        self.logs.append(
            ChangelogEntry(4, 8, 0)
            .addLine("Edit update")
            .addLine("- you can now edit the history from the TUI")
            .addLine("- on a side note, I also improved completion for files")
            .addLine("    and numeric values (temperature, top_p, penalties...)")
        )

        self.logs.append(
            ChangelogEntry(4, 7, 3)
            .addLine("Added ctrl+C handling when playing TTS to stop speaking.")
        )
        self.logs.append(
            ChangelogEntry(4, 7, 2)
            .addLine(
                "Fixed a bug where the output tts file could not be set to mp3"
            )
            .addLine("  (it was previously checking for mp4 extension, lol)")
        )
        self.logs.append(
            ChangelogEntry(4, 7, 1)
            .addLine("Now prints message before reading TTS")
            .addLine("Also, removes the pygame init message")
        )
        self.logs.append(
            ChangelogEntry(4, 7, 0)
            .addLine("Added TTS (using pygame)")
        )

        self.logs.append(
            ChangelogEntry(4, 6, 2)
            .addLine("Oops, forgot to check help, help should be fixed now")
        )
        self.logs.append(
            ChangelogEntry(4, 6, 1)
            .addLine("Added support for overwriting config file")
        )
        self.logs.append(
            ChangelogEntry(4, 6, 0)
            .addLine("Fine tweaking update")
            .addLine("- added command for changing the temperature")
            .addLine("- added top_p command and parameter")
            .addLine("- added frequency penalty command and parameter")
            .addLine("- added presence penalty command and parameter")
            .addLine("- fixed /quit and /exit not working")
            .addLine("- fixed tab completion")
        )

        self.logs.append(
            ChangelogEntry(4, 5, 3)
            .addLine("Fixed files being removed everytime")
        )
        self.logs.append(
            ChangelogEntry(4, 5, 2)
            .addLine("Now removes temp files even if ctrl+c if they are empty")
        )
        self.logs.append(
            ChangelogEntry(4, 5, 1)
            .addLine(
                "fixed owega bash script for systems that still have "
                + "PYTHON 2 AS DEFAULT"
            )
            .addLine("WTF GUYS GET OVER IT, IT'S BEEN DEPRECATED SINCE 2020")
        )
        self.logs.append(
            ChangelogEntry(4, 5, 0)
            .addLine("Added support for organization specification")
        )

        self.logs.append(
            ChangelogEntry(4, 4, 0)
            .addLine("Changed from json to json5 (json-five)")
        )

        self.logs.append(
            ChangelogEntry(4, 3, 6)
            .addLine(
                "Re-added handling of invalid request, mostly for too large "
                + "requests"
            )
        )
        self.logs.append(
            ChangelogEntry(4, 3, 5)
            .addLine("Added exception handling for token estimation")
        )
        self.logs.append(
            ChangelogEntry(4, 3, 4)
            .addLine("Re-added server unavailable error handling")
        )
        self.logs.append(
            ChangelogEntry(4, 3, 3)
            .addLine("Changed time taken to only show up to ms")
        )
        self.logs.append(
            ChangelogEntry(4, 3, 2)
            .addLine("Fixed 4.3.1 :p")
        )
        self.logs.append(
            ChangelogEntry(4, 3, 1)
            .addLine("Added time taken per request in debug output")
        )
        self.logs.append(
            ChangelogEntry(4, 3, 0)
            .addLine("Added token estimation")
        )

        self.logs.append(
            ChangelogEntry(4, 2, 0)
            .addLine("VERY IMPORTANT UPDATE: NOW COMPATIBLE WITH OPENAI 1.1.1")
        )

        self.logs.append(
            ChangelogEntry(4, 1, 1)
            .addLine("Removed a warning due to beautifulsoup4")
        )
        self.logs.append(
            ChangelogEntry(4, 1, 0)
            .addLine("Changed the getpage function to strip the text")
        )

        self.logs.append(
            ChangelogEntry(4, 0, 4)
            .addLine("Fixed context not working correctly")
        )
        self.logs.append(
            ChangelogEntry(4, 0, 3)
            .addLine("Added README to pypi page")
        )
        self.logs.append(
            ChangelogEntry(4, 0, 2)
            .addLine("Fixed a typo where owega wouldn't send the memory")
        )
        self.logs.append(
            ChangelogEntry(4, 0, 1)
            .addLine(
                "oops, forgot to change the setup.py and now I messed up my "
                + "4.0.0! >:C"
            )
        )
        self.logs.append(
            ChangelogEntry(4, 0, 0)
            .addLine("LTS: Long-Term-Souvenirs")
            .addLine("The AI now have long-term memory!!!")
            .addLine(
                "Huge update: full refactoring, the code is now readable!")
            .addLine(
                "Also, the name is now Owega (it's written with unicode "
                + "characters though)"
            )
            .addLine(
                "You can see the new code here: "
                + "https://git.pyrokinesis.fr/darkgeem/owega"
            )
            .addLine(
                "Also, the project is now available on PyPI so, just go pip "
                + "install owega!"
            )
        )

        self.logs.append(
            ChangelogEntry(3, 9, 4)
            .addLine("changed default values")
        )
        self.logs.append(
            ChangelogEntry(3, 9, 3)
            .addLine("fixed api key not saving with /genconf")
        )
        self.logs.append(
            ChangelogEntry(3, 9, 2)
            .addLine(
                "changed the temp file creation method for non-unix systems")
        )
        self.logs.append(
            ChangelogEntry(3, 9, 1)
            .addLine(
                "fixed an issue when the openai api key does not exist "
                + "anywhere"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 9, 0)
            .addLine("Windows update")
            .addLine("  - Do I really need to explain that update?")
        )
        self.logs.append(
            ChangelogEntry(3, 8, 1)
            .addLine("added a debug option for devs")
        )
        self.logs.append(
            ChangelogEntry(3, 8, 0)
            .addLine("WEB download update")
            .addLine(
                "  - added a get_page function for openchat to get pages "
                + "without the need"
            )
            .addLine("      for curl")
        )
        self.logs.append(
            ChangelogEntry(3, 7, 0)
            .addLine("DIRECT CONTEXT COMMANDS update:")
            .addLine(
                "  - now, you can use commands in one line, instead of waiting"
                + "for prompt"
            )
            .addLine("      example: /save hello.json")
            .addLine(
                "      (instead of typing /save, then enter, then typing "
                + "hello.json"
            )
            .addLine(
                "       works on all commands, the only specific case being "
                + "file_input.)"
            )
            .addLine(
                "  - file_input as a direct command takes only one argument: "
                + "the file"
            )
            .addLine(
                "      to load (e.g. /load ./src/main.c). The pre-prompt will "
                + "be asked"
            )
            .addLine(
                "      directly instead of having to do it in three steps")
            .addLine("        (/load, then filename, then pre-prompt)")
            .addLine(
                "  - also, fixed /tokens splitting the prompt instead of the "
                + "user input"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 6, 0)
            .addLine("PREFIX update:")
            .addLine(
                "  - added prefixes for command (changeable in the config)")
            .addLine(
                "  - reformatted most of the main loop code to split it in "
                + "handlers"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 5, 2)
            .addLine("added infos on bottom bar")
        )
        self.logs.append(
            ChangelogEntry(3, 5, 1)
            .addLine(
                'added "commands" command, to enable/disable command '
                + 'execution'
            )
        )
        self.logs.append(
            ChangelogEntry(3, 5, 0)
            .addLine(
                "WEB update: now added a flask app, switched repos to its own")
        )
        self.logs.append(
            ChangelogEntry(3, 4, 0)
            .addLine("CLI update:")
            .addLine(
                "  - added command-line options to change input/output files")
            .addLine(
                "  - added command-line option to ask a question from command "
                + "line"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 3, 1)
            .addLine(
                "added tokens command, to change the amount of requested "
                + "tokens"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 3, 0)
            .addLine(
                "implemented prompt_toolkit, for better prompt handling, "
                + "newlines with"
            )
            .addLine("control+n")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 11)
            .addLine(
                "now, the default gpt models implement function calling, no "
                + "need for"
            )
            .addLine("0613 anymore")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 10)
            .addLine(
                "added a command line option for specifying the config file")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 9)
            .addLine(
                "changed execute's subprocess call to shell=True, now "
                + "handling pipes..."
            )
        )
        self.logs.append(
            ChangelogEntry(3, 2, 8)
            .addLine("fixed command execution stderr handling")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 7)
            .addLine(
                "fixed json sometimes not correctly formatted when writing "
                + "multiple lines"
            )
            .addLine("files")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 6)
            .addLine(
                "reversed the changelog order, fixed function calling chains")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 5)
            .addLine(
                "now handling non-zero exit status when running a command")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 4, "fix1")
            .addLine("fixed a missing parenthesis")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 4)
            .addLine(
                "fixed variables and ~ not expanding when executing a command")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 3)
            .addLine("added create_file as a function OpenAI can call")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 2)
            .addLine(
                "fixed openchat sometimes not detecting the command has been "
                + "ran"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 2, 1)
            .addLine("fixed a space missing in openchat's function calling")
        )
        self.logs.append(
            ChangelogEntry(3, 2, 0)
            .addLine("FUNCTION CALLING UPDATE:")
            .addLine(
                "added function calling, now openchat is able to run commands")
            .addLine("on your computer, as long as you allow it to")
            .addLine(
                "(you will be prompted on each time it tries to run a "
                + "command)"
            )
            .addLine(
                "!!! only available on -0613 models (gpt-3.5-turbo-0613, "
                + "gpt-4-0613) !!!"
            )
            .addLine(
                "will be available on all gpt models from 2023-06-27, with "
                + "the latest"
            )
            .addLine("openchat 3.2.X patch")
        )
        self.logs.append(
            ChangelogEntry(3, 1, 1)
            .addLine("now handling the service unavailable error")
        )
        self.logs.append(
            ChangelogEntry(3, 1, 0)
            .addLine("BMU (Better Module Update)!")
            .addLine("modified MSGS:")
            .addLine("  - added last_question()")
            .addLine("  - changed last_answer()")
            .addLine("modified ask() to allow for blank prompt,")
            .addLine("  which will reuse the last question")
        )
        self.logs.append(
            ChangelogEntry(3, 0, 3)
            .addLine(
                "quitting with EOF will now discard the temp file (^C will "
                + "still keep it)"
            )
        )
        self.logs.append(
            ChangelogEntry(3, 0, 2)
            .addLine("added conversion script")
        )
        self.logs.append(
            ChangelogEntry(3, 0, 1)
            .addLine("added changelog")
        )
        self.logs.append(
            ChangelogEntry(3, 0, 0)
            .addLine("changed conversation save from pickle to json")
        )

        self.logs.append(
            ChangelogEntry(2, 2, 4)
            .addLine("automatic temp file save")
        )
        self.logs.append(
            ChangelogEntry(2, 2, 3)
            .addLine(
                "genconf now saves the current conf instead of a blank "
                + "template"
            )
        )
        self.logs.append(
            ChangelogEntry(2, 2, 2)
            .addLine(
                "stripped user input (remove trailing spaces/tabs/newlines)")
        )
        self.logs.append(
            ChangelogEntry(2, 2, 1)
            .addLine(
                "added license and version info in command line (-l and -v)")
        )
        self.logs.append(
            ChangelogEntry(2, 2, 0)
            .addLine("added context command to change GPT's definition")
        )
        self.logs.append(
            ChangelogEntry(2, 1, 1)
            .addLine("added file_input in help command")
        )
        self.logs.append(
            ChangelogEntry(2, 1, 0)
            .addLine("added file_input command")
        )
        self.logs.append(
            ChangelogEntry(2, 0, 1)
            .addLine("added genconf command")
        )
        self.logs.append(
            ChangelogEntry(2, 0, 0)
            .addLine("WTFPL license")
        )

    def genLog(self) -> None:
        """Generate the changelog string."""
        self.logs.sort()
        self.version = self.logs[-1].version
        self.version_str = str(self.logs[-1].version)
        self.log = f"OWEGA v{self.version_str} CHANGELOG:"
        for entry in self.logs:
            ver = entry.version
            if (not ver.status) and ver.patch == 0:
                self.log += '\n'
                if ver.minor == 0:
                    self.log += '\n'
            self.log += '\n'
            if 'rc' in ver.status:
                self.log += '\033[91m'
            self.log += str(entry)
            if 'rc' in ver.status:
                self.log += '\033[m'


OwegaChangelog = Changelog()
