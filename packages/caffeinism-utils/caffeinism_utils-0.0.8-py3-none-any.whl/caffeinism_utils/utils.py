class DummyStopIteration(Exception):
    pass


def next_without_stop_iteration(iterator):
    try:
        return next(iterator)
    except StopIteration:
        raise DummyStopIteration()
