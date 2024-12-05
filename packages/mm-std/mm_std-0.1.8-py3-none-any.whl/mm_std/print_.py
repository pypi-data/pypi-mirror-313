import sys
from enum import Enum, unique
from typing import Any, NoReturn

import rich
from rich.console import Console
from rich.table import Table

from mm_std.json_ import json_dumps


@unique
class PrintFormat(str, Enum):
    PLAIN = "plain"
    TABLE = "table"
    JSON = "json"


def fatal(message: str, code: int = 1) -> NoReturn:
    print(message, file=sys.stderr)  # noqa: T201
    sys.exit(code)


def print_console(*messages: object, print_json: bool = False) -> None:
    if len(messages) == 1:
        message = messages[0]
        if isinstance(message, str):
            print(message)  # noqa: T201
        else:
            if print_json:
                rich.print_json(json_dumps(message))
            else:
                rich.print(message)
    else:
        rich.print(messages)


def print_plain(messages: object, print_format: PrintFormat | None = None) -> None:
    if print_format is None or print_format == PrintFormat.PLAIN:
        print(messages)  # noqa: T201


def print_json(data: object, print_format: PrintFormat | None = None) -> None:
    if print_format is None or print_format == PrintFormat.JSON:
        rich.print_json(json_dumps(data))


def print_table(title: str, columns: list[str], rows: list[list[Any]], print_format: PrintFormat | None = None) -> None:
    if print_format is None or print_format == PrintFormat.TABLE:
        table = Table(*columns, title=title)
        for row in rows:
            table.add_row(*(str(cell) for cell in row))
        console = Console()
        console.print(table)
