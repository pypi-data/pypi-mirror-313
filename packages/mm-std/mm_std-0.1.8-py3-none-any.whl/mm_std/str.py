import re
from collections.abc import Iterable
from decimal import Decimal

import pydash


def str_to_list(
    data: str | Iterable[object] | None,
    lower: bool = False,
    remove_comments: bool = False,
    unique: bool = False,
    split_line: bool = False,
) -> list[str]:
    match data:
        case None | "" | []:
            return []
        case str():
            if lower:
                data = data.lower()
            result = [line.strip() for line in data.split("\n") if line.strip()]
            if remove_comments:
                result = [line.split("#")[0].strip() for line in result]
                result = [line for line in result if line]
            if unique:
                result = pydash.uniq(result)

            if split_line:
                new_result = []
                for line in result:
                    new_result.extend(line.split())
                return new_result

            return result
        case Iterable():
            return [str(x) for x in data]
        case _:
            raise ValueError("data has a wrong type")


def number_with_separator(
    value: float | str | Decimal | None,
    prefix: str = "",
    suffix: str = "",
    separator: str = "_",
    hide_zero: bool = False,
    round_digits: int = 2,
) -> str:
    if value is None or value == "":
        return ""
    if float(value) == 0:
        return "" if hide_zero else f"{prefix}0{suffix}"
    if float(value) > 1000:
        value = "".join(
            reversed([x + (separator if i and not i % 3 else "") for i, x in enumerate(reversed(str(int(value))))]),
        )
    else:
        value = round(value, round_digits)  # type:ignore[arg-type,assignment]

    return f"{prefix}{value}{suffix}"


def str_starts_with_any(value: str, prefixes: list[str]) -> bool:
    """check if str starts with any of prefixes"""
    for prefix in prefixes:
        if value.startswith(prefix):
            return True
    return False


def str_ends_with_any(value: str, prefixes: list[str]) -> bool:
    """check if str ends with any of prefixes"""
    for prefix in prefixes:
        if value.endswith(prefix):
            return True
    return False


def split_on_plus_minus_tokens(value: str) -> list[str]:
    value = "".join(value.split())
    if not value:
        raise ValueError("value is empty")
    if "++" in value:
        raise ValueError("++ in value")
    if "--" in value:
        raise ValueError("-- in value")
    if value.endswith("-"):
        raise ValueError("ends with -")
    if value.endswith("+"):
        raise ValueError("ends with +")

    if not value.startswith("+") and not value.startswith("-"):
        value = "+" + value

    result: list[str] = []
    rest_value = value
    while True:
        if not rest_value:
            return result
        items = re.split(r"[+\-]", rest_value)
        if rest_value.startswith("+"):
            result.append("+" + items[1])
            rest_value = rest_value.removeprefix("+" + items[1])
        elif rest_value.startswith("-"):
            result.append("-" + items[1])
            rest_value = rest_value.removeprefix("-" + items[1])
