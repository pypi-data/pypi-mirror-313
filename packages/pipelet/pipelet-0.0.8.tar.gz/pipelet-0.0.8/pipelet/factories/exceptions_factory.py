import importlib
from os import PathLike
from typing import List, Type, Union


def get_custom_exception(
    path_to_exception: Union[PathLike, str, Type[Exception]],
) -> Type[Exception]:
    """
    Retrieves a custom exception class by its string path or directly returns the exception class.

    Args:
        path_to_exception (Union[PathLike, str, Type[Exception]]):
            Path to the exception class in the format "module.submodule.ClassName"
            or the class itself.

    Returns:
        Type[Exception]: The exception class.

    Raises:
        ValueError: If the path is invalid or the class is not a subclass of Exception.
    """
    # If we are passed a class directly, return it if it's valid.
    if isinstance(path_to_exception, type) and issubclass(
        path_to_exception, Exception
    ):
        return path_to_exception

    # Otherwise, handle the case where a string path is provided.
    if isinstance(path_to_exception, str):
        try:
            exception_path, exception_name = path_to_exception.rsplit(".", 1)
            exception_module = importlib.import_module(exception_path)
            exception = getattr(exception_module, exception_name)
            if not isinstance(exception, type) or not issubclass(
                exception, Exception
            ):
                raise ValueError(
                    f"{exception_name} is not a subclass of Exception."
                )
        except (ImportError, AttributeError, ValueError) as e:
            raise ValueError(f"Invalid path: {path_to_exception}. Error: {e}")
        else:
            return exception
    else:
        raise ValueError(
            f"Invalid type for path_to_exception: {type(path_to_exception)}"
        )


def custom_exceptions_factory(
    paths: List[Union[PathLike, str, Type[Exception]]],
) -> List[Type[Exception]]:
    """
    Creates a list of custom exception classes from a list of string paths or directly from exception classes.

    Args:
        paths (List[Union[PathLike, str, Type[Exception]]]):
            List of paths to exception classes in the format "module.submodule.ClassName"
            or exception classes themselves.

    Returns:
        List[Type[Exception]]: List of exception classes.
    """
    exceptions = []
    for path in paths:
        exception = get_custom_exception(path)
        exceptions.append(exception)
    return exceptions
