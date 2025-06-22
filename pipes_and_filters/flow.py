from typing import Iterable, Callable, Generator, Any


class Flow:

    def __init__(
        self,
        source: Iterable[Any],
        splitter: Callable[[Any], Any],
        sink: Callable[[Any], Any] = lambda x: x
    ) -> None:
        self.source = source
        self.splitter = splitter
        self.sink = sink

    def __call__(self) -> Generator[Any, None, None]:
        for x in self.source:
            inner_result = self.splitter(x)
            yield self.sink(*inner_result)
