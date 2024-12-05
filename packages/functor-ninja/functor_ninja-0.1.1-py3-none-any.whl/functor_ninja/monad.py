from abc import abstractmethod
from typing import Callable, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")


class Functor(Generic[A]):
    @abstractmethod
    def map(self, f: Callable[[A], B]) -> "Functor[B]":
        pass


class Monad(Functor[A]):
    @staticmethod
    @abstractmethod
    def of(init: Callable[[], A]) -> "Monad[A]":
        pass

    @abstractmethod
    def flat_map(self, f: Callable[[A], "Monad[B]"]) -> "Monad[B]":
        pass

