from .util import flatten


def test():
    assert list(flatten(())) == []
    assert list(flatten([])) == []
    assert list(flatten((1,))) == [1]
    assert list(flatten([2, [], (), [3, [(4, 5), (6,)]]])) == [2, 3, 4, 5, 6]
