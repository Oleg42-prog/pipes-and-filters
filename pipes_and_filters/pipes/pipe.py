from typing import Any, Callable


class Pipe:
    """
    A sequential filter processor that applies multiple functions in order.

    The Pipe class implements the pipes and filters architectural pattern by
    allowing you to chain multiple functions together. Each function receives
    the output of the previous function as input.

    Example:
        >>> pipe = Pipe(
        ...     lambda x: x * 2,
        ...     lambda x: x + 1,
        ...     lambda x: x ** 2
        ... )
        >>> result = pipe(5)  # ((5 * 2) + 1) ** 2 = 121
        >>> print(result)
        121
    """

    def __init__(self, *filters: Callable[[Any], Any]) -> None:
        """
        Initialize the pipe with a sequence of filter functions.

        Args:
            *filters: Variable number of functions to apply sequentially.
                     Each function should accept one argument and return one value.

        Raises:
            ValueError: If no filters are provided.
        """
        if not filters:
            raise ValueError("Pipe must contain at least one filter")
        self.filters = filters

    def __call__(self, arg: Any) -> Any:
        """
        Apply all filters sequentially to the input argument.

        Args:
            arg: The input data to process through all filters.

        Returns:
            The result after applying all filters in sequence.
        """
        result = arg
        for f in self.filters:
            result = f(result)
        return result
