from functor_ninja import List


def test_empty():
    empty = List([]).map(lambda v: v)

    assert empty.len() == 0


def test_multi():
    result = List([1, 2, 3]).map(lambda v: v + 1)

    assert result.values == [2, 3, 4]


def test_flatten():
    result = List([1, 2, 3]).flat_map(lambda v: List([v]))

    assert result.len() == 3

def test_flat_expend():
    result = List([1, 2, 3]).flat_map(lambda v: List([v]*v))

    assert result.len() == 6

def test_flat_compose():
    a = List(["a1", "a2", "a3"])
    b = List(["b1", "b2", "b3"])
    result = a.flat_map(
        lambda a:
        b.map(lambda b: (a, b))
    )

    assert result.len() == 9
