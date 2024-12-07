"""
Retry Processor for Retryable Exceptions in Data Processing Pipelines

This module defines a `RetryProcessor` class, which is responsible for retrying the
processing of data if an exception occurs. The processor works exclusively with the
`_next` processor in a chain, attempting to process data multiple times if allowed by
the configured parameters. It offers flexible handling of exceptions and retries.

Key Features:
- Retries processing up to a maximum number of attempts (`max_retries`).
- Supports configurable delays between retries, with an optional increment (`delay_step`).
- Provides the ability to retry only for specific exceptions, configurable via `white_exceptions`.
- Logs warnings for each retry attempt and errors if all retries fail.

Class:
- `RetryProcessor`: A processor that retries the processing of data if an exception occurs.

Attributes:
- `white_exceptions`: A list of exceptions to allow retries for.
- `max_retries`: Maximum number of retry attempts.
- `delay`: Delay in seconds between retry attempts.
- `delay_step`: Step delay for next retry.
- `retry_with_white_exc`: If True, retries only for white-listed exceptions.

Methods:
- `_log_error`: Logs retries and final failure.
- `_is_exception_retryable`: Determines if an exception is retryable based on the white exceptions list.
- `_process_with_next`: Processes the input data with the next processor in the chain.
- `process`: Attempts to process the data using the `_next` processor, retrying if an exception occurs.

Example Usage:
```python
retry_processor = RetryProcessor(
    max_retries=5, delay=3, delay_step=2, retry_with_white_exc=True
)
"""

import time
from typing import Any, Generator, List, Optional, Type

from pipelet.exceptions.base import ProcessorStopIteration
from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor

logger = logger_factory()


class RetryProcessor(BaseProcessor[Any, Any, None, None]):
    """
    A processor that retries the processing of data if an exception occurs.
    Works exclusively with the `_next` processor.
    """

    def __init__(
        self,
        white_exceptions: Optional[List[Type[Exception]]] = None,
        max_retries: int = 3,
        delay: int = 5,
        delay_step: int = 0,
        retry_with_white_exc: bool = True,
    ) -> None:
        """
        Args:
            white_exceptions: A list of exceptions to allow retries for.
            max_retries: Maximum number of retry attempts.
            delay: Delay in seconds between retry attempts.
            delay_step: Step delay for next retry.
            retry_with_white_exc: If True, retries only for white-listed exceptions.
        """
        super().__init__(white_exceptions)
        self._max_retries = max_retries
        self._delay = delay
        self._delay_step = delay_step
        self._retry_with_white_exc = retry_with_white_exc

    def _log_error(self, attempt: int, exception: Exception) -> None:
        """
        Helper function to log errors and warnings for retries.
        """
        logger.warning(
            f"Attempt {attempt} failed for processor {self._next}. Error: {exception}"
        )
        if attempt == self._max_retries:
            logger.error(
                f"All {self._max_retries} attempts failed for processor {self._next}."
            )

    def _is_exception_retryable(self, exception: Exception) -> bool:
        """
        Determines if the exception is retryable based on the white exceptions list.
        Handles `ProcessorStopIteration` as a special case.
        """
        # If the exception is ProcessorStopIteration, treat it as white-listed
        if isinstance(exception, ProcessorStopIteration):
            return (
                self._retry_with_white_exc
            )  # Only retry if _retry_with_white_exc is True

        # Retry only if white_exceptions is set and the exception is in the list
        if self._retry_with_white_exc and self._white_exceptions:
            return isinstance(exception, tuple(self._white_exceptions))

        # Retry all other exceptions by default
        return True

    def _process_with_next(self, input_data: Any) -> Generator[Any, None, None]:
        """
        Processes the input data with the next processor in the chain.
        """
        if self._next is None:
            raise ValueError("No `_next` processor is set for RetryProcessor.")
        return self._next.process(input_data)

    def process(self, input_data: Any) -> Generator[Any, None, None]:
        """
        Attempts to process the data using the `_next` processor, retrying if an exception occurs.
        """
        next_processor_after_retry = None
        # Attempt processing with the next processor
        if self._next is None:
            raise ValueError("No `_next` processor is set for RetryProcessor.")
        if self._next._next is not None:
            next_processor_after_retry = self._next._next
            self._next._next = None

        for attempt in range(1, self._max_retries + 1):
            try:
                r_processor_to_retry = next(self._next.process(input_data))
            except Exception as e:
                if not self._is_exception_retryable(e):
                    raise e  # If exception is not retryable, raise immediately

                # Log error and retry if necessary
                self._log_error(attempt, e)

                if attempt < self._max_retries:
                    time.sleep(self._delay)
                    self._delay += self._delay_step  # Wait before retrying
                else:
                    raise ProcessorStopIteration(
                        str(e)
                    )  # Exit if processing isn't successful
            else:
                if next_processor_after_retry is not None:
                    self._next._next = next_processor_after_retry
                    next_processor_after_retry_gen = self._next._next.process(
                        r_processor_to_retry
                    )
                    yield from next_processor_after_retry_gen
                else:
                    yield r_processor_to_retry
                break

    def __str__(self) -> str:
        return (
            (f"{self.__class__.__name__}({self._next.__class__.__name__}")
            + (
                f"(max_retries={self._max_retries}, "
                f"delay={self._delay}, "
                f"delay_step={self._delay_step}, "
                f"retry_with_white_exc={self._retry_with_white_exc}))"
            )
            if self._next is not None
            else ""
        )
