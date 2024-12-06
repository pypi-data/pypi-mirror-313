from typing import Generic, TypeVar, Union, Callable

T = TypeVar("T")
E = TypeVar("E")


class OK(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value


class Err(Generic[E]):
    def __init__(self, err: E) -> None:
        self.err = err


class Result(Generic[T, E]):

    def __init__(self, _value: Union[OK[T], Err[E]]) -> None:
        self._value = _value

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return Result(OK(value))

    @classmethod
    def err(cls, err: E) -> 'Result[T, E]':
        return Result(Err(err))

    def is_ok(self) -> bool:
        return isinstance(self._value, OK)

    def is_err(self) -> bool:
        return isinstance(self._value, Err)

    def bind(self, f: Callable[[T], 'Result']) -> 'Result':
        if isinstance(self._value, Err):
            return self
        return f(self._value.value)
