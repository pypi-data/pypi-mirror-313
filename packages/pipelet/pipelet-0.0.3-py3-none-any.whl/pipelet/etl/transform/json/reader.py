import json
from os import PathLike
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Type,
    Union,
)

from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor
from pipelet.processors.file_system import AbstractFileSystemManager

logger = logger_factory()


class JsonParser(
    BaseProcessor[str | PathLike[str], Dict[str, Any], None, None],
):
    """
    JsonParser

    This processor reads a JSON file or string and parses its content into a Python dictionary.

    Attributes:
        file_system_manager (AbstractFileSystemManager): Manages file I/O operations.
        white_exceptions (Optional[List[type[Exception]]]): List of exceptions that will be gracefully handled.
        parse_kwargs (Dict[str, Any]): Keyword arguments passed to `json.loads` for customizing JSON parsing.
    """

    def __init__(
        self,
        file_system_manager: AbstractFileSystemManager[
            Union[str, PathLike[str]], Union[str, bytes]
        ],
        white_exceptions: Optional[List[Type[Exception]]] = None,
        parse_float: Optional[Callable[[str], Any]] = float,
        parse_int: Optional[Callable[[str], Any]] = int,
        parse_constant: Optional[
            Literal["raise_error", "ignore", "custom_handle"]
        ] = None,
        object_hook: Optional[Callable[[Dict[str, Any]], Any]] = None,
        object_pairs_hook: Optional[
            Callable[[List[tuple[str, Any]]], Any]
        ] = None,
    ) -> None:
        """
        Initializes the JsonParser.

        Args:
            file_system_manager (AbstractFileSystemManager): Manages file operations such as reading and writing files.
            white_exceptions (Optional[List[type[Exception]]]): List of exception types to be gracefully handled.
            parse_float (type, optional): Custom type for parsing floating-point numbers. Defaults to `float`.
            parse_int (type, optional): Custom type for parsing integers. Defaults to `int`.
            parse_constant (Callable[[str], Any], optional): Custom handler for special constants like `NaN`, `Infinity`. Defaults to None.
            object_hook (Callable[[Dict[str, Any]], Any], optional): Function to transform the JSON objects during decoding. Defaults to None.
            object_pairs_hook (Callable[[List[Tuple[str, Any]]], Any], optional): Function to transform key-value pairs during decoding. Defaults to None.
        """
        super().__init__(white_exceptions)
        self._file_system_manager = file_system_manager
        self._parse_float = parse_float
        self._parse_int = parse_int
        self._parse_constant = parse_constant
        self._object_hook = object_hook
        self._object_pairs_hook = object_pairs_hook
        self._parse_kwargs = {
            "parse_float": parse_float,
            "parse_int": parse_int,
            "parse_constant": parse_constant,
            "object_hook": object_hook,
            "object_pairs_hook": object_pairs_hook,
        }

    def process(
        self, input_data: str | PathLike[str]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Processes the input JSON file or string and parses it into a Python dictionary.

        Args:
            input_data (Union[str, PathLike[str]]): Path to the JSON file or a JSON string.

        Yields:
            Dict[str, Any]: The parsed JSON as a Python dictionary.
        """
        # Read content using the file system manager
        content = self._file_system_manager.read_file(input_data)

        # Parse the JSON content with custom arguments
        try:
            data = json.loads(content, **self._parse_kwargs)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON: %s", e)
            raise

        # Pass the data to the next processor if present, otherwise yield it
        if self._next is not None:
            gen = self._next.process(data)
            yield from gen
        else:
            yield data

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(parse_float={self._parse_float}, "
            f"parse_int={self._parse_int}, "
            f"parse_constant={self._parse_constant}, "
            f"object_hook={self._object_hook}, "
            f"object_pairs_hook={self._object_pairs_hook})"
        )
