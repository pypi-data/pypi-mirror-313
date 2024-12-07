from typing import Any, Callable, Generator, List

from pipelet.processors.base import BaseProcessor


class SplitterProcessor(BaseProcessor):
    """
    SplitterProcessor splits input data into parts using a provided function and yields them sequentially.

    This processor is useful for breaking down input data into smaller components,
    such as splitting a string into words, dividing a list into sublists, or
    decomposing JSON objects into their individual elements.

    Args:
        splitter (Callable[[Any], List[Any]]):
            A function that takes the input data and returns a list of parts.

    Attributes:
        splitter (Callable[[Any], List[Any]]):
            The function used to split the input data.
    """

    def __init__(self, splitter: Callable[[Any], List[Any]], *args, **kwargs):
        """
        Initializes the SplitterProcessor with a splitting function.

        Args:
            splitter (Callable[[Any], List[Any]]):
                The function to use for splitting the input data.
            *args: Additional positional arguments passed to the BaseProcessor.
            **kwargs: Additional keyword arguments passed to the BaseProcessor.
        """
        super().__init__(*args, **kwargs)
        self.splitter = splitter

    def process(self, input_data: Any) -> Generator[Any, Any, Any]:
        """
        Processes the input data by splitting it into parts.

        Args:
            input_data (Any): The input data to be split.

        Yields:
            Any: Each part of the input data as returned by the splitter function.

        Returns:
            List[Any]: The complete list of parts after processing.
        """
        parts = self.splitter(input_data)
        for part in parts:
            if self._next is not None:
                yield from self._next.process(part)
            else:
                yield part
