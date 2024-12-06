# ΦωΦ (pronounced owega)
ΦωΦ is a command-line interface for conversing with GPT models (from OpenAI)

Pypi:
[![PyPI - Status](https://img.shields.io/pypi/status/owega)](https://pypi.org/project/owega/)
[![PyPI - Version](https://img.shields.io/pypi/v/owega)](https://pypi.org/project/owega/)
[![Downloads](https://static.pepy.tech/badge/owega)](https://pepy.tech/project/owega) [![Downloads](https://static.pepy.tech/badge/owega/month)](https://pepy.tech/project/owega)
[![PyPI - License](https://img.shields.io/pypi/l/owega)](https://git.pyrokinesis.fr/darkgeem/owega/-/blob/main/LICENSE)
[![PyPI - Format](https://img.shields.io/pypi/format/owega)](https://pypi.org/project/owega/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/owega)](https://pypi.org/project/owega/)

AUR:
[![AUR Version](https://img.shields.io/aur/version/python-owega)](https://aur.archlinux.org/packages/python-owega)
[![AUR Last Modified](https://img.shields.io/aur/last-modified/python-owega?logo=archlinux&label=AUR%20update)](https://aur.archlinux.org/packages/python-owega)
[![AUR License](https://img.shields.io/aur/license/python-owega)](https://git.pyrokinesis.fr/darkgeem/owega/-/blob/main/LICENSE)
[![AUR Maintainer](https://img.shields.io/aur/maintainer/python-owega)](https://aur.archlinux.org/packages/python-owega)
[![AUR Votes](https://img.shields.io/aur/votes/python-owega)](https://aur.archlinux.org/packages/python-owega)

Gitlab:
[![GitLab Tag](https://img.shields.io/gitlab/v/tag/81?gitlab_url=https%3A%2F%2Fgit.pyrokinesis.fr)](https://git.pyrokinesis.fr/darkgeem/owega)
[![GitLab Issues](https://img.shields.io/gitlab/issues/open/81?gitlab_url=https%3A%2F%2Fgit.pyrokinesis.fr)](https://git.pyrokinesis.fr/darkgeem/owega)
[![GitLab Merge Requests](https://img.shields.io/gitlab/merge-requests/open/81?gitlab_url=https%3A%2F%2Fgit.pyrokinesis.fr)](https://git.pyrokinesis.fr/darkgeem/owega)
[![GitLab License](https://img.shields.io/gitlab/license/81?gitlab_url=https%3A%2F%2Fgit.pyrokinesis.fr)](https://git.pyrokinesis.fr/darkgeem/owega/-/blob/main/LICENSE)

[![Discord](https://img.shields.io/discord/1171384402438275162?style=social&logo=discord)](https://discord.gg/KdRmyRrA48)



## ΦωΦ's homepage
You can check on the source code [on its gitlab page](https://git.pyrokinesis.fr/darkgeem/owega)!

Also, here's the [discord support server](https://discord.gg/KdRmyRrA48), you
can even get pinged on updates, if you want!


## Features
ΦωΦ has quite a lot of features!

These include:
- Saving/loading conversation to disk as json files.
- Autocompletion for commands, file search, etc...
- History management.
- Temp files to save every message, so that you can get back the conversation
  if you ever have to force-quit ΦωΦ.
- Config file to keep settings like api key, preferred model, command execution
  status...
- Command execution: if enabled, allows ΦωΦ to execute commands on your system
  and interpret the results.
- File creation: if commands are enabled, also allows ΦωΦ to create files on
  your system and fill them with desired contents.
- GET requests: allows ΦωΦ to get informations from online pages, through
  http(s) GET requests.
- Long-term memory: allows for ΦωΦ to store memories, which will not be deleted
  as the older messages are, to keep requests under the available tokens per
  request.
- Context management: allows to set the AI context prompt (example: "you are a
  cat. cats don't talk. you can only communicate by meowing, purring, and
  actions between asterisks" will transform ΦωΦ into a cat!!)
- Meow.
- Meow meow.
- MEOW MEOW MEOW MEOW!!!!


## Installation
Just do ``pip install --upgrade owega`` to get the latest version


## Command-line arguments
Do you really need me to do ``owega --help`` for you?

```
usage: owega [-h] [-d] [-c] [-l] [-v] [-f CONFIG_FILE] [-i HISTORY] [-a ASK]
             [-o OUTPUT] [-t] [-s TTSFILE] [-T] [-e]

Owega main application

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug output
  -c, --changelog       Display changelog and exit
  -l, --license         Display license and exit
  -v, --version         Display version and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Specify path to config file
  -i HISTORY, --history HISTORY
                        Specify the history file to import
  -a ASK, --ask ASK     Asks a question directly from the command line
  -o OUTPUT, --output OUTPUT
                        Saves the history to the specified file
  -t, --tts             Enables TTS generation when asking
  -s TTSFILE, --ttsfile TTSFILE
                        Outputs a generated TTS file single-ask mode
  -T, --training        outputs training data from -i file
  -e, --estimate        shows estimate token usage / cost from a request from
                        -i file
```


## Markdown formatting and syntax highlighting
To allow ΦωΦ to print its output nicely, you can just install the rich python
module: ``pip install rich``


## Showcase
See ΦωΦ in action!

### Demos made with ΦωΦ 5.7.5
[![asciicast](https://asciinema.org/a/659607.png)](https://asciinema.org/a/659607)
[Youtube demo](https://youtu.be/_LGSc6mj-EM)
