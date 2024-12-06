import os
from itertools import count


class RequestIdGenerator:
    def __init__(self):
        self._counter = count(start=1)

    def __call__(self) -> int:
        """Calculate unique request id.

        Not thread safe, but safe to use in single threaded async context. There
        are no async operations here, so this function is unlikely to be
        preempted in the middle. This is important otherwise we may end up with
        duplicate ids.
        """
        next_id = next(self._counter)
        return int(str(os.getpid()) + str(next_id))
