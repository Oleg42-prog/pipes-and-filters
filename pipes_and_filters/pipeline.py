from typing import Iterable, Callable


class Pipeline:

    def __init__(self, source: Iterable, pipe: Callable):
        self.source = source
        self.pipe = pipe

    def __call__(self):
        for x in self.source:
            yield self.pipe(x)
