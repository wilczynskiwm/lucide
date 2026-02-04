from __future__ import annotations

import sys
from typing import IO

if sys.version_info < (3, 9):

    def str_removeprefix(self: str, prefix: str) -> str:
        if self.startswith(prefix):
            return self[len(prefix) :]
        else:  # pragma: no cover
            return self[:]

else:
    str_removeprefix = str.removeprefix


if sys.version_info >= (3, 9):
    from importlib.resources import files

    def open_binary(pkg: str, filename: str) -> IO[bytes]:
        return (files(pkg) / filename).open("rb")

    def open_text(pkg: str, filename: str) -> IO[str]:
        return (files(pkg) / filename).open("r", encoding="utf-8")

else:
    from importlib.resources import open_binary  # noqa: F401
    from importlib.resources import open_text  # noqa: F401
