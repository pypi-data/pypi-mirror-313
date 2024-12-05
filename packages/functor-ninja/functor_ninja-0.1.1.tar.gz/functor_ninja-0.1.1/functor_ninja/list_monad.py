from functor_ninja.monad import (
    A,
    B,
    Callable,
    Monad,
)

from typing import List as BaseList


class List(Monad[A]):
    def __init__(self, values: BaseList[A]):
        self.values = values

    @staticmethod
    def of(init: Callable[[], BaseList[A]]) -> "List[A]":
        values = init()
        return List(values)

    def len(self) -> int:
        return len(self.values)

    def map(self, f: Callable[[A], B]) -> "List[B]":
        result = [f(value) for value in self.values]
        return List(result)

    def flat_map(self, f: Callable[[A], "List[B]"]) -> "List[B]":
        result = [
            child
            for value in self.values
            for child in f(value).values
        ]
        return List(result)
