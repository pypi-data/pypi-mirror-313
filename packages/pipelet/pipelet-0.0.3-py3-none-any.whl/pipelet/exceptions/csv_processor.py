from os import PathLike
from typing import Union

from pipelet.exceptions.base import BaseCsvProcessorException


class CsvProcessorException(BaseCsvProcessorException):
    """Base exception for CSV processing-related errors."""


class CsvParsingError(CsvProcessorException):
    """Exception raised for errors occurring during CSV parsing."""

    def __init__(self, filename: Union[PathLike[str], str], message: str):
        """
        Initialize CsvParsingError.

        Args:
            filename (str): The name of the CSV file that caused the error.
            message (str): A message describing the error.
        """
        self.filename = filename
        self.message = message
        super().__init__(f"Failed to parse CSV file '{filename}': {message}")
