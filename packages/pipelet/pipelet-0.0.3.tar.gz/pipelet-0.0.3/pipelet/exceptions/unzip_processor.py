from os import PathLike
from typing import Union

from pipelet.exceptions.base import BaseUnzipException


class UnzipProcessorException(BaseUnzipException):
    """Base exception for unzip processor-related errors."""


class UnzipError(UnzipProcessorException):
    """Exception raised for errors occurring during the unzip process."""

    def __init__(self, filename: Union[PathLike[str], str], message: str):
        """
        Initialize UnzipError.

        Args:
            filename (str): The name of the file that caused the error.
            message (str): A message describing the error.
        """
        self.filename = filename
        self.message = message
        super().__init__(f"Failed to unzip file '{filename}': {message}")
