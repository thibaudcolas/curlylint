import collections


def flatten(_list):
    """
    Deeply flattens an iterable.
    """
    for el in _list:
        if isinstance(el, collections.Iterable) and not isinstance(
            el, (str, bytes)
        ):
            yield from flatten(el)
        else:
            yield el
