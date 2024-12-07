def lazy(initializer):
    value = [None]

    def function():
        if value[0] is None:
            value[0] = initializer()
            if value[0] is None:
                raise ValueError("Lazy property initializer returned None")
        return value[0]

    return function


def take(count, iterable):
    iterable = iter(iterable)
    lst = []

    for i in range(count):
        try:
            lst.append(next(iterable))
        except StopIteration:
            break

    return lst
