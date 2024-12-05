import random
from collections.abc import Sequence
from decimal import Decimal


def random_choice[T](source: Sequence[T] | T | None) -> T | None:
    """Deprecated, don't use it"""
    if source is None:
        return None
    if isinstance(source, str):
        return source  # type: ignore[return-value]
    if isinstance(source, Sequence):
        if source:
            return random.choice(source)  # type:ignore[no-any-return]
        return None
    return source


def random_str_choice(source: Sequence[str] | str | None) -> str | None:
    if source is None:
        return None
    if isinstance(source, str):
        return source
    if isinstance(source, Sequence):
        if source:
            return random.choice(source)
        return None
    return source


def random_decimal(from_: Decimal, to: Decimal) -> Decimal:
    from_ndigits = abs(from_.as_tuple().exponent)  # type:ignore[arg-type]
    to_ndigits = abs(to.as_tuple().exponent)  # type:ignore[arg-type]
    ndigits = max(from_ndigits, to_ndigits)
    return Decimal(str(round(random.uniform(float(from_), float(to)), ndigits)))
