from functor_ninja import Try, Success, Fail


def test_success():
    result = Try(1).map(lambda v: v + 1)

    assert isinstance(result, Success)
    assert not isinstance(result, Fail)


def test_fail():
    result = Try(0).map(lambda v: 1 / v)

    assert isinstance(result, Fail)
    assert not isinstance(result, Success)


def test_of_success():
    result = Try.of(lambda: 0 / 1)

    assert isinstance(result, Success)
    assert not isinstance(result, Fail)


def test_of_fail():
    result = Try.of(lambda: 1 / 0)

    assert isinstance(result, Fail)
    assert not isinstance(result, Success)
