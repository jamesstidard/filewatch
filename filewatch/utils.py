def split_iterable(predicate: callable, iterable):
    """
    Like a mix of str.split and itertools.takewhile.

    Takes a predicate and a iterable, and returns chunks of the
    list split around where predicate returns True.

    >>> list(split_iterable(lambda c: c == "e", "abesdfkjees"))
    [['a', 'b'], ['s', 'd', 'f', 'k', 'j'], [], ['s']]
    """
    group = []
    for i in iterable:
        if predicate(i):
            yield group
            group = []
            continue

        group.append(i)

    yield group
