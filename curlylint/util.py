from collections.abc import Iterable


def flatten(_list):
    """
    Deeply flattens an iterable.
    """
    for el in _list:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
