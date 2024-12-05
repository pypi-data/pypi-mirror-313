from functor_ninja.monad import (
    A,
    B,
    Callable,
    Monad,
)


class Try(Monad[A]):
    def __init__(self, value: A):
        self.value = value

    @staticmethod
    def of(init: Callable[[], A]) -> "Try[A]":
        result = Try(None).map(lambda _: init())
        return result

    def map(self, f: Callable[[A], B]) -> "Try[B]":
        try:
            result = f(self.value)
            return Success(result)
        except Exception as e:
            return Fail(e)

    def flat_map(self, f: Callable[[A], "Try[B]"]) -> "Try[B]":
        try:
            result = f(self.value)
            return result
        except Exception as e:
            return Fail(e)


class Success(Try[A]):
    pass


class Fail(Try[Exception]):
    def map(self, f: Callable[[A], B]) -> "Fail[B]":
        return self

    def flat_map(self, f: Callable[[A], "Monad[B]"]) -> "Fail[B]":
        return self
