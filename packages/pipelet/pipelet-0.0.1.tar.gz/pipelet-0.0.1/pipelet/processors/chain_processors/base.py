"""
Processor Classes for ETL Chain Operations

This module contains two key processor classes used in the ETL chain-of-responsibility pattern:
`ChainAnyProcessor` and `ChainAllProcessor`.

1. **ChainAnyProcessor**:
   - A processor that processes data through a chain of sub-processors, attempting each in order.
   - The first sub-processor that successfully processes the data is moved to the front of the chain, ensuring it is prioritized in future attempts.
   - If no processor in the chain can handle the data, an error is logged.

2. **ChainAllProcessor**:
   - A processor that executes multiple sub-processors in parallel, either using threads or processes.
   - Results from sub-processors are yielded as soon as they become available.
   - If any exception occurs during processing, it is logged.

Classes:
- `ChainAnyProcessor`: A processor that attempts to process data through each sub-processor in sequence.
- `ChainAllProcessor`: A processor that executes all sub-processors in parallel.

Both processors are designed to be part of a larger ETL pipeline, facilitating flexible data processing strategies.
"""

import concurrent.futures
from typing import Any, Generator, List, Optional

from pipelet.exceptions.base import ProcessorStopIteration
from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor

logger = logger_factory()


class ChainAnyProcessor(BaseProcessor[Any, Any, None, None]):
    _last_success_processor: Optional[BaseProcessor[Any, Any, None, None]] = (
        None
    )

    """
    A processor that processes data through a chain of sub-processors.

    The processor attempts to process the input data using each of the 
    sub-processors in the order they appear. The first processor that successfully
    handles the data will pass the result to the next processor in the chain (if 
    any). If no processor is able to process the data, an error is logged. 
    Processors that successfully handle the data are moved to the front of the chain.

    Attributes:
        _last_success_processor (Optional[Type[BaseProcessor]]): The processor 
        that last successfully handled the data.
        _sub_processors (List[BaseProcessor]): A list of sub-processors to attempt processing.
        _next (Optional[BaseProcessor]): The next processor to handle data after this one.
    """

    def _move_processor_to_front(self, index: int):
        """
        Moves the processor at the specified index to the front of the sub-processor list.

        This method is called when a processor successfully handles data, ensuring
        that it is prioritized in future processing attempts.

        Args:
            index (int): The index of the processor to be moved to the front.
        """
        if self._sub_processors is not None:
            self._sub_processors.insert(0, self._sub_processors.pop(index))

    def process(self, input_data: Any) -> Generator[Any, None, None]:
        """
        Processes the input data through a series of sub-processors.

        The method attempts to process the input data with each processor in the chain.
        If a processor successfully handles the data, it is passed along to the next
        processor (if there is one). If no processor can handle the data, an error
        is logged. If the data is processed successfully, the result is yielded.

        Args:
            input_data (Any): The data to be processed.

        Yields:
            Any: The processed data, passed along to the next processor or returned
            as the final result.

        Logs:
            Warning: If a processor in the chain cannot handle the data.
            Error: If all processors in the chain fail to handle the data.
        """
        if self._sub_processors is not None:
            for index, processor in enumerate(self._sub_processors):
                try:
                    # Try processing the input data with the current processor
                    gen = processor.process(input_data)
                    for record in gen:
                        if self._next is not None:
                            # If there is a next processor, pass the result to it
                            next_gen = self._next.process(record)  # type: ignore
                            yield from next_gen
                        else:
                            # Otherwise, yield the final result
                            yield record
                        if index > 0:
                            self._move_processor_to_front(index)
                    break  # Exit the loop once the data is successfully processed
                except ProcessorStopIteration:
                    # Log a warning if a processor cannot handle the data
                    logger.warning(
                        f"Processor '{processor}' could not handle data"
                    )
            else:
                # Log an error if no processor in the chain handled the data
                logger.error(
                    "All processors in the chain failed to handle the data."
                )
        else:
            raise ValueError(
                f"{self.__class__.__name__} must have at least one subprocessor."
            )


class ChainAllProcessor(BaseProcessor[Any, Any, None, None]):
    """
    A processor that executes multiple sub-processors in parallel.
    """

    def __init__(
        self,
        white_exceptions: List[type[Exception]] | None = None,
        use_threads: bool = False,
        result_timeout: int | None = None,
    ) -> None:
        super().__init__(white_exceptions)
        self._executor = (
            concurrent.futures.ThreadPoolExecutor
            if use_threads
            else concurrent.futures.ProcessPoolExecutor
        )
        self._result_timeout = result_timeout

    def process(self, input_data: Any) -> Generator[Any, None, None]:
        """
        Processes the input data using all sub-processors in parallel.
        Yields partial results as soon as they become available.
        """
        if not self._sub_processors:
            raise ValueError(
                f"{self.__class__.__name__} must have at least one subprocessor."
            )

        with self._executor() as executor:
            # Submit tasks for all sub-processors
            futures = {
                executor.submit(
                    (
                        processor.process
                        if isinstance(
                            self._executor,
                            concurrent.futures.ProcessPoolExecutor,
                        )
                        else processor.read_full_result
                    ),
                    input_data,
                ): processor
                for processor in self._sub_processors
            }

            for future in concurrent.futures.as_completed(
                futures, self._result_timeout
            ):
                try:
                    # Retrieve and yield results as they become available
                    result = future.result()
                    for partial in result:
                        yield partial  # Yielding results immediately
                except Exception as e:
                    logger.error(f"Error in sub-processor: {e}")
