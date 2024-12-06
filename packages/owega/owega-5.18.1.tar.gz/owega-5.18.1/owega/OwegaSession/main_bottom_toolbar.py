"""Main bottom toolbar for TUI."""
import shutil
from typing import Any

from prompt_toolkit import styles

from ..changelog import OwegaChangelog
from ..config import baseConf


# bottom toolbar and style for prompt_toolkit
def main_bottom_toolbar(what: str = "toolbar") -> Any:
    """Return the bottom style or toolbar."""
    if what == "style":
        msd = {
            'red':     '#000000 bg:#FF0000',  # noqa: E241
            'green':   '#000000 bg:#00FF00',  # noqa: E241
            'blue':    '#000000 bg:#0000FF',  # noqa: E241
            'yellow':  '#000000 bg:#FFFF00',  # noqa: E241
            'magenta': '#000000 bg:#FF00FF',  # noqa: E241
            'cyan':    '#000000 bg:#00FFFF',  # noqa: E241
            'white':   '#000000 bg:#FFFFFF',  # noqa: E241
        }
        msd['bottom-toolbar'] = msd['white']
        msd['bottom-even'] = msd['magenta']
        msd['bottom-odd'] = msd['cyan']
        msd['bottom-on'] = msd['green']
        msd['bottom-off'] = msd['red']
        main_style = styles.Style.from_dict(msd)
        return main_style

    # noinspection PyPep8Naming
    class tr:
        def __init__(self) -> None:
            self.table = []
            self.count = 0
            self.wpos = 0

        def add(self, prefix="/", txt="", color="yellow") -> None:
            new_class = "white"
            if not isinstance(txt, str):
                txt = str(txt)
            to_add = []
            to_add_count = 0
            if self.count:
                to_add.append((
                    "class:blue",
                    " - "
                ))
                to_add_count += len(' - ')
            if prefix:
                if txt:
                    prefix = prefix + ": "
                to_add.append(tuple([
                    f"class:{new_class}",
                    prefix
                ]))
                to_add_count += len(prefix)
            if txt:
                to_add.append((
                    f"class:{color}",
                    txt
                ))
                to_add_count += len(txt)

            term_w = shutil.get_terminal_size()[0]
            if self.count:
                if (self.wpos + to_add_count) > term_w:
                    self.newline()
                    to_add = to_add[1:]
                    to_add_count -= 3

            for e in to_add:
                self.table.append(e)

            self.count += 1
            self.wpos += to_add_count

        def newline(self) -> None:
            self.table.append(("class:blue", '\n'))
            self.count = 0
            self.wpos = 0

    to_ret = tr()
    to_ret.add(f"v{OwegaChangelog.version}")
    to_ret.add("model", baseConf.get("model", "unknown"))
    to_ret.add(
        "cmds",
        "ON" if baseConf.get("commands") else "OFF",
        "bottom-on" if baseConf.get("commands") else "bottom-off"
    )
    to_ret.add("tokens", baseConf.get("max_tokens", "unknown"))
    to_ret.add(
        "time",
        "ON" if baseConf.get("time_awareness") else "OFF",
        "bottom-on" if baseConf.get("time_awareness") else "bottom-off"
    )
    to_ret.add(
        "fancy",
        "ON" if baseConf.get("fancy") else "OFF",
        "bottom-on" if baseConf.get("fancy") else "bottom-off"
    )
    to_ret.add(
        "estm",
        "ON" if baseConf.get("estimation") else "OFF",
        "bottom-on" if baseConf.get("estimation") else "bottom-off"
    )
    to_ret.add(
        "TTS",
        "ON" if baseConf.get("tts_enabled") else "OFF",
        "bottom-on" if baseConf.get("tts_enabled") else "bottom-off"
    )
    to_ret.add("temp", baseConf.get("temperature", "unknown"))
    to_ret.add("top_p", baseConf.get("top_p", "unknown"))
    to_ret.add("freq.plty", baseConf.get("frequency_penalty", "unknown"))
    to_ret.add("pr.plty", baseConf.get("presence_penalty", "unknown"))
    return to_ret.table
