from typing import Iterable, Callable, Generator, Any


class Pipeline:
    """
    A data processing pipeline that applies a transformation to each element
    of an iterable source.

    The Pipeline class implements a generator-based approach to process sequences
    of data. It takes an iterable source and applies a transformation function
    or Pipe to each element, yielding results lazily.

    Example:
        >>> pipeline = Pipeline(
        ...     source=range(5),
        ...     pipe=lambda x: x ** 2
        ... )
        >>> result = list(pipeline())
        >>> print(result)
        [0, 1, 4, 9, 16]
    """

    def __init__(self, source: Iterable[Any], pipe: Callable[[Any], Any]) -> None:
        """
        Initialize the pipeline with a data source and transformation function.

        Args:
            source: An iterable containing the data to process.
            pipe: A function or Pipe that will be applied to each element
                 of the source iterable.
        """
        self.source = source
        self.pipe = pipe

    def __call__(self) -> Generator[Any, None, None]:
        """
        Process each element of the source through the pipe.

        This method creates a generator that applies the pipe transformation
        to each element of the source iterable lazily (on-demand).

        Yields:
            The result of applying the pipe to each source element.

        Example:
            >>> pipeline = Pipeline([1, 2, 3], lambda x: x * 2)
            >>> for result in pipeline():
            ...     print(result)
            2
            4
            6
        """
        for x in self.source:
            yield self.pipe(x)
