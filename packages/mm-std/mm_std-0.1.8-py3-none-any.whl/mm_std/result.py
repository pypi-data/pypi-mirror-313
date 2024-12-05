from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, Literal, NoReturn

from pydantic_core import core_schema


class Ok[T]:
    __match_args__ = ("ok",)

    def __init__(self, ok: T, data: Any = None) -> None:
        self.ok = ok
        self.data = data

    def __repr__(self) -> str:
        if self.data is None:
            return f"Ok({self.ok!r})"
        else:
            return f"Ok({self.ok!r}, data={self.data!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self.ok == other.ok and self.data == other.data

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self.ok, self.data))

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    @property
    def err(self) -> None:
        return None

    def expect(self, _message: str) -> T:
        return self.ok

    def expect_err(self, message: str) -> NoReturn:
        raise UnwrapError(self, message)

    def unwrap(self) -> T:
        return self.ok

    def unwrap_err(self) -> NoReturn:
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or[U](self, _default: U) -> T:
        return self.ok

    def unwrap_or_else(self, op: object) -> T:
        return self.ok

    def unwrap_or_raise(self, e: object) -> T:
        return self.ok

    def map[U](self, op: Callable[[T], U]) -> Ok[U]:
        return Ok(op(self.ok), data=self.data)

    def map_or[U](self, default: object, op: Callable[[T], U]) -> U:
        return op(self.ok)

    def map_or_else[U](self, err_op: object, ok_op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return ok_op(self.ok)

    def map_err(self, op: object) -> Ok[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def and_then[U](self, op: Callable[[T], U | Result[U]]) -> Result[U]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in. If return of `op` function is not Result, it will be a Ok value.
        """
        try:
            res = op(self.ok)
            if not isinstance(res, Ok | Err):
                res = Ok(res)
        except Exception as e:
            res = Err(e)
        res.data = self.data
        return res

    def or_else(self, op: object) -> Ok[T]:
        return self

    def ok_or_err(self) -> T | str:
        return self.ok

    def ok_or_none(self) -> T | None:
        return self.ok

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.model_schema(
            cls,
            core_schema.model_fields_schema(
                {
                    "ok": core_schema.model_field(core_schema.any_schema()),
                    "data": core_schema.model_field(core_schema.any_schema()),
                },
            ),
        )


class Err:
    __match_args__ = ("err",)

    def __init__(self, err: str | Exception, data: Any = None) -> None:
        self.err = f"exception: {err}" if isinstance(err, Exception) else err
        self.data = data

    def __repr__(self) -> str:
        if self.data is None:
            return f"Err({self.err!r})"
        else:
            return f"Err({self.err!r}, data={self.data!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self.err == other.err and self.data == other.data

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self.err, self.data))

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    @property
    def ok(self) -> None:
        """
        Return `None`.
        """
        return None

    def expect(self, message: str) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(self, f"{message}: {self.err!r}")
        if isinstance(self.err, BaseException):
            raise exc from self.err
        raise exc

    def expect_err(self, _message: str) -> str:
        """
        Return the inner value
        """
        return self.err

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(self, f"Called `Result.unwrap()` on an `Err` value: {self.err!r}")
        if isinstance(self.err, BaseException):
            raise exc from self.err
        raise exc

    def unwrap_err(self) -> str:
        """
        Return the inner value
        """
        return self.err

    def unwrap_or[U](self, default: U) -> U:
        """
        Return `default`.
        """
        return default

    def unwrap_or_else[T](self, op: Callable[[str], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self.err)

    def unwrap_or_raise[TBE: BaseException](self, e: type[TBE]) -> NoReturn:
        """
        The contained result is ``Err``, so raise the exception with the value.
        """
        raise e(self.err)

    def map(self, op: object) -> Err:
        """
        Return `Err` with the same value
        """
        return self

    def map_or[U](self, default: U, op: object) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else[U](self, err_op: Callable[[str], U], ok_op: object) -> U:
        """
        Return the result of the default operation
        """
        return err_op(self.err)

    def and_then(self, op: object) -> Err:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    def ok_or_err[T](self) -> T | str:
        return self.err

    def ok_or_none[T](self) -> T | None:
        return None

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.model_schema(
            cls,
            core_schema.model_fields_schema(
                {
                    "err": core_schema.model_field(core_schema.any_schema()),
                    "data": core_schema.model_field(core_schema.any_schema()),
                },
            ),
        )


type Result[T] = Ok[T] | Err


class UnwrapError(Exception):
    _result: Result[Any]

    def __init__(self, result: Result[Any], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any]:
        return self._result


def try_ok[T](fn: Callable[..., Result[T]], *, args: tuple[object], attempts: int, delay: int | float = 0) -> Result[T]:
    if attempts <= 0:
        raise ValueError("attempts must be more than zero")
    res: Result[T] = Err("not started")
    for _ in range(attempts):
        res = fn(*args)
        if res.is_ok():
            return res
        if delay:
            time.sleep(delay)
    return res
