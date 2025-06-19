from typing import Any, Callable, List


class Splitter:
    """
    A data splitter that processes input through one pipe and then splits
    the result through multiple output pipes.

    The Splitter class allows you to take the output of one processing pipeline
    and apply multiple different transformations to it, returning a list of results.
    This is useful for parallel processing paths or when you need to compute
    multiple values from the same intermediate result.

    Example:
        >>> from pipes_and_filters.pipes.pipe import Pipe
        >>> input_pipe = Pipe(lambda x: x * 2)
        >>> output_pipes = [
        ...     lambda x: x + 1,
        ...     lambda x: x - 1
        ... ]
        >>> splitter = Splitter(input_pipe, output_pipes)
        >>> result = splitter(5)  # input: 5*2=10, outputs: [11, 9]
        >>> print(result)
        [11, 9]
    """

    def __init__(self, input_pipe: Callable, outputs_pipes: List[Callable]) -> None:
        """
        Initialize the splitter with input and output processing pipes.

        Args:
            input_pipe: A function or Pipe that preprocesses the input data.
            outputs_pipes: A list of functions or Pipes that will each process
                          the result of input_pipe independently.

        Raises:
            ValueError: If outputs_pipes is empty.
        """
        if not outputs_pipes:
            raise ValueError("Splitter must have at least one output pipe")
        self.input_pipe = input_pipe
        self.outputs_pipes = outputs_pipes

    def __call__(self, *args: Any) -> List[Any]:
        """
        Process input through the input pipe, then apply each output pipe to the result.

        Args:
            *args: Arguments to pass to the input_pipe.

        Returns:
            A list containing the results from each output pipe applied to
            the input_pipe result.
        """
        result = self.input_pipe(*args)
        split_results = []
        for output_pipe in self.outputs_pipes:
            split_results.append(output_pipe(result))
        return split_results
