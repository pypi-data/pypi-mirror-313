"""
Processor Metaclass for Exception Handling and Attribute Validation

This module defines a metaclass, `ProcessorMeta`, used to automate exception handling
and validate attributes for processor classes in an ETL pipeline.

The metaclass wraps the `process` method of processor classes with a decorator to
handle exceptions that might occur during the generator execution. This ensures that
exception handling logic is consistently applied across different processor implementations.

Classes:
- `ProcessorMeta`: Metaclass for processors that provides exception handling and validation.

Key Features:
- The `process_decorator` method wraps the `process` method to handle exceptions
  gracefully during generator execution.
- Exceptions can be selectively handled by a white-list of exceptions that will
  not terminate the processing but instead raise a `ProcessorStopIteration`.
- Ensures that any processor class that uses this metaclass automatically inherits
  robust exception handling logic.
"""

from abc import ABCMeta
from functools import wraps
from typing import Any, Callable, Generator, List, Optional, Type, Union

from pipelet.exceptions.base import (
    BaseProcessorException,
    ProcessorStopIteration,
)
from pipelet.processors.abc import AbstractProcessor


class ProcessorMeta(ABCMeta):
    """
    Metaclass for processors that automates exception handling and validates attributes.

    This metaclass:
    - Wraps the `process` method of processor classes with a decorator to handle exceptions.
    Attributes:
        process (Callable): The generator function to be decorated for error handling.
    """

    @staticmethod
    def process_decorator(
        func: Callable[
            ...,
            Generator[
                Any,
                Any,
                Optional[Any],
            ],
        ]
    ) -> Callable[
        ...,
        Generator[
            Any,
            Any,
            Optional[Any],
        ],
    ]:
        """
        Decorator for the `process` method to handle exceptions during generator execution.

        Args:
            func (Callable): The `process` generator method.

        Returns:
            Callable: A wrapped generator function with added exception handling.
        """

        @wraps(func)
        def wrapper(
            obj: AbstractProcessor,
            *args,
            **kwargs,
        ) -> Generator[
            Any,
            Any,
            Union[Any, None],
        ]:
            white_exceptions: List[Type[BaseProcessorException]] = (
                getattr(obj, "_white_exceptions") or []
            )
            generator = func(obj, *args, **kwargs)
            while True:
                try:
                    value = next(generator)
                    yield value
                except StopIteration:
                    return
                except Exception as e:
                    if any(
                        issubclass(e.__class__, exc) for exc in white_exceptions
                    ):
                        raise ProcessorStopIteration(str(e))
                    raise e

        return wrapper

    def __new__(cls: Type, name: str, bases: tuple, dct: dict) -> Type:
        """
        Creates a new class and applies validations and enhancements.

        Args:
            name (str): The name of the new class.
            bases (tuple): The base classes of the new class.
            dct (dict): The class attributes.

        Returns:
            Type: The newly created class with applied enhancements.
        """
        # Automatically decorate the `process` method.
        if "process" in dct and callable(dct["process"]):
            original_process = dct["process"]
            dct["process"] = cls.process_decorator(original_process)
        return super().__new__(cls, name, bases, dct)  # type: ignore
