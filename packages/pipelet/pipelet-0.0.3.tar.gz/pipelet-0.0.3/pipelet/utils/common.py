from typing import Any, Callable, Generator

from pipelet.exceptions.base import ProcessorStopIteration


class SafeGenerator:
    """
    A generator wrapper that safely handles ProcessorStopIteration exceptions that may be raised
    during iteration. It ensures that the generator continues to operate correctly despite
    such errors.

    Attributes:
        gen (Generator[Any, Any, None]): The underlying generator
            that is being wrapped by this SafeGenerator.
    """

    def __init__(self, gen: Generator[Any, Any, None]) -> None:
        """
        Initializes the SafeGenerator with a given generator.

        Args:
            gen (Generator[Any, Any, None]): The generator to
                be wrapped.
        """
        self.gen = gen

    def __iter__(
        self,
    ) -> "SafeGenerator":
        """
        Returns the iterator object itself. This allows SafeGenerator to be used in iteration
        contexts like for-loops.

        Returns:
            SafeGenerator: The iterator object itself.
        """
        return self

    def __next__(self) -> Any:
        """
        Retrieves the next value from the generator. If a ProcessorStopIteration occurs, it is caught
        and ignored, allowing the generator to continue operating. If the generator raises
        StopIteration, it is propagated to signal the end of iteration.

        Returns:
            Any: The next value yielded by the generator.

        Raises:
            StopIteration: If the generator is exhausted.
        """
        try:
            return next(self.gen)
        except ProcessorStopIteration:
            return
        except StopIteration:
            raise


def auto_launch_coroutine(
    func: Callable[..., Generator[Any, Any, None]]
) -> Callable[..., Generator[Any, Any, None]]:
    """
    A decorator that automatically starts a coroutine upon its creation.

    Args:
        func: A function that returns a generator (coroutine).

    Returns:
        A function that creates and starts the coroutine automatically.
    """

    def start(*args: Any, **kwargs: Any) -> Generator[Any, Any, None]:
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


def save_launch_generator(gen: Generator[Any, Any, None], n: int = 1) -> Any:
    """
    Initializes a SafeGenerator with the given generator and retrieves  n-nexted values.

    Args:
        gen (Generator[Any, Any, None]): The generator to be wrapped.
        n - numbers of iterations

    Returns:
        Any: The next value yielded by the SafeGenerator.

    """
    safe_gen = SafeGenerator(gen=gen)
    try:
        result = [next(safe_gen) for _ in range(n)]
    except StopIteration:
        result = None
    return result
