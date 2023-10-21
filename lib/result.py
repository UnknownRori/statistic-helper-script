from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E')


class Result(Generic[T, E]):
    def __init__(self, value: T = None, error: E = None):
        self.value = value
        self.error = error

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(value=value)

    @classmethod
    def err(cls, error: E) -> 'Result[T, E]':
        return cls(error=error)

    def is_ok(self) -> bool:
        return self.value is not None

    def is_err(self) -> bool:
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_ok():
            return self.value
        else:
            if hasattr(self.error, '__str__'):
                raise ValueError(self.error.__str__())
            else:
                raise ValueError("Result contains an error")

    def expect(self, message: str) -> T:
        if self.is_ok():
            return self.value
        else:
            raise ValueError(message)

    def map(self, func) -> 'Result[T, E]':
        if self.is_ok():
            return Result.ok(func(self.value))
        else:
            return self

    def map_err(self, func) -> 'Result[T, E]':
        if self.is_err():
            return Result.err(func(self.error))
        else:
            return self

    def __str__(self) -> str:
        if self.is_ok():
            return f"Ok({self.value})"
        else:
            return f"Err({self.error})"
