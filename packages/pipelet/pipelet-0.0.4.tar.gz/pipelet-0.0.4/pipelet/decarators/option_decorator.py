import types
from typing import Any, Callable, Generator

from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor

logger = logger_factory()


def prepare_gen_processor(
    func: Callable[..., Generator[Any, Any, Any]],
    obj: BaseProcessor[Any, Any, Any, Any],
    *args,
    **kwargs
) -> Generator[Any, Any, Any]:
    """
    A utility function to prepare and execute generator-based processors.

    This function normalizes the invocation of generator functions or methods.
    If the provided callable `func` is a bound method, it is invoked directly
    with `*args` and `**kwargs`. If `func` is an unbound function, it is
    invoked with `obj` passed as the first argument along with `*args` and `**kwargs`.

    Args:
        func (Callable): The generator function or method to be executed.
        obj (BaseProcessor): The processor object, passed explicitly for unbound functions.
        *args: Positional arguments to pass to the generator.
        **kwargs: Keyword arguments to pass to the generator.

    Returns:
        Generator: The generator object produced by executing `func`.

    """
    if isinstance(func, types.MethodType):
        return func(*args, **kwargs)
    return func(obj, *args, **kwargs)
