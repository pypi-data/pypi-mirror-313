"""Handles a changelog entry."""
import functools
from typing import Any

from .version import Version


@functools.total_ordering
class ChangelogEntry:
    """Handles a changelog entry."""

    def __init__(
        self,
        major: int = 0,
        minor: int = 0,
        patch: int = 0,
        status: str = "",
        entry: str = ""
    ) -> None:
        """Initialize the changelog entry."""
        self.version = Version(major, minor, patch, status)
        self.entry = entry
        if entry:
            self.entry += "\n"

    # Here, Any should be Self, but using Any allows for compatibility with
    # python <3.11
    def addLine(self, line: str = "") -> Any:
        """Add a line to the changelog entry and return itself."""
        self.entry += line
        self.entry += '\n'
        return self

    def __eq__(self, other) -> bool:
        """Version equality check."""
        return self.version.__eq__(other.version)

    def __lt__(self, other) -> bool:
        """Version lessthan check."""
        return self.version.__lt__(other.version)

    def __repr__(self) -> str:
        """Representation when shown."""
        return f"ChangelogEntry(version='{self.version}', ...)"

    def __str__(self) -> str:
        """Representation as str."""
        # se = stripped entry
        se = self.entry.strip().split('\n')
        ver = str(self.version)
        verlen = len(ver)
        verpad = verlen * ' '
        ret = ""
        first_put = False
        for line in se:
            if not first_put:
                ret += f"{ver}: {line}\n"
                first_put = True
            else:
                ret += f"{verpad}  {line}\n"
        return ret.strip()
