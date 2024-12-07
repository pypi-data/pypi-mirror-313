from functools import wraps
from typing import Any, Callable, Generator, Optional, Union

from pipelet.decarators.option_decorator import prepare_gen_processor
from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor

default_logger = logger_factory()


def logging_decorator(
    func: Callable[
        ...,
        Generator[Any, Any, Optional[Any]],
    ],
    custom_logger: Optional[Any] = None,
) -> Callable[
    ...,
    Generator[Any, Any, Optional[Any]],
]:
    """
    A decorator that adds logging functionality to a processor's `process` method.

    Logs the processor's class name, arguments, and keyword arguments each time
    the `process` method is invoked. Supports generator functions and normalizes
    calls to ensure compatibility with bound and unbound methods.

    Args:
        func (Callable): The generator function (`process` method) to wrap.
        custom_logger (Optional[Any]): Custom logger to use. Defaults to the global logger.

    Returns:
        Callable: A wrapped generator function with logging functionality.

    Example:
        ```
        @logging_decorator
        def process(self, *args, **kwargs):
            yield ...
        ```
    """
    logger_to_use = custom_logger or default_logger

    @wraps(func)
    def wrapper(
        obj: BaseProcessor[Any, Any, Any, Any],
        *args,
        **kwargs,
    ) -> Generator[
        Any,
        Any,
        Union[Any, None],
    ]:
        logger_to_use.info(
            f"Processor: {obj.__class__.__name__}, args: {args}, kwargs: {kwargs}"
        )
        generator = prepare_gen_processor(
            func, obj, *args, **kwargs
        )  # Normalized call
        try:
            while True:
                yield next(generator)
        except StopIteration:
            return

    return wrapper
