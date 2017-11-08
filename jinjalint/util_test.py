from .util import flatten


def test():
    assert list(flatten([2, [], [3, [[4], 5]]])) == [2, 3, 4, 5]
