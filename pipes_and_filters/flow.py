from typing import Iterable, Callable, Generator, Any


class Flow:
    """
    A data flow processor that combines splitting and sinking operations.

    The Flow class implements a pattern where each element from an iterable source
    is processed through a splitter (which typically returns multiple values),
    and then these values are combined through a sink function. This allows for
    complex data transformations where you need to split data into multiple
    components and then aggregate or transform those components.

    Example:
        >>> from pipes_and_filters.pipes.splitter import Splitter
        >>> from pipes_and_filters.utils import identity
        >>> # Calculate statistics and format them
        >>> stats_splitter = Splitter(
        ...     input_pipe=identity,
        ...     outputs_pipes=[
        ...         lambda scores: sum(scores) / len(scores),  # mean
        ...         max,  # maximum
        ...         min   # minimum
        ...     ]
        ... )
        >>> flow = Flow(
        ...     source=[[85, 92, 78], [75, 68, 82]],
        ...     splitter=stats_splitter,
        ...     sink=lambda avg, max_val, min_val: f"Avg: {avg:.1f}, Max: {max_val}, Min: {min_val}"
        ... )
        >>> results = list(flow())
        >>> print(results[0])
        Avg: 85.0, Max: 92, Min: 78
    """

    def __init__(
        self,
        source: Iterable[Any],
        splitter: Callable[[Any], Any],
        sink: Callable[[Any], Any] = lambda x: x
    ) -> None:
        """
        Initialize the flow with source data, splitter, and sink functions.

        Args:
            source: An iterable containing the data to process.
            splitter: A function or Splitter that processes each element from
                     source and typically returns multiple values (as a tuple,
                     list, or other iterable).
            sink: A function that takes the unpacked results from the splitter
                 and combines or transforms them into the final output.
                 Defaults to identity function if not provided.
        """
        self.source = source
        self.splitter = splitter
        self.sink = sink

    def __call__(self) -> Generator[Any, None, None]:
        """
        Process each element of the source through the splitter and sink.

        This method creates a generator that applies the splitter to each element
        of the source, then unpacks the splitter's results and passes them to
        the sink function. The results are yielded lazily (on-demand).

        Yields:
            The result of applying the sink function to the unpacked results
            from the splitter for each source element.

        Example:
            >>> from pipes_and_filters.pipes.splitter import Splitter
            >>> from pipes_and_filters.utils import identity
            >>> flow = Flow(
            ...     source=[5, 10],
            ...     splitter=Splitter(
            ...         input_pipe=identity,
            ...         outputs_pipes=[lambda x: x, lambda x: x ** 2]
            ...     ),
            ...     sink=lambda x, y: x / y
            ... )
            >>> for result in flow():
            ...     print(result)
            1.0
            0.1
        """
        for x in self.source:
            inner_result = self.splitter(x)
            yield self.sink(*inner_result)
