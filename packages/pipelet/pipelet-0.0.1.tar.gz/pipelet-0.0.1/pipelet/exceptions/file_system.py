from os import PathLike
from typing import Union

from pipelet.exceptions.base import BaseFileSystemException


class LocalFileSystemException(BaseFileSystemException):
    """Base exception for local file system-related errors."""


class LocalFileCreationError(LocalFileSystemException):
    """Exception raised for errors occurring during file creation."""

    def __init__(self, filename: Union[PathLike[str], str], message: str):
        """
        Initialize LocalFileCreationError.

        Args:
            filename (str): The name of the file that caused the error.
            message (str): A message describing the error.
        """
        self.filename = filename
        self.message = message
        super().__init__(f"Failed to create file '{filename}': {message}")


class LocalFileReadError(LocalFileSystemException):
    """Exception raised for errors occurring during file reading."""

    def __init__(self, filename: Union[PathLike[str], str], message: str):
        """
        Initialize LocalFileReadError.

        Args:
            filename (str): The name of the file that caused the error.
            message (str): A message describing the error.
        """
        self.filename = filename
        self.message = message
        super().__init__(f"Failed to read file '{filename}': {message}")


class LocalFileDeleteError(LocalFileSystemException):
    """Exception raised for errors occurring during file deletion."""

    def __init__(self, filename: Union[PathLike[str], str], message: str):
        """
        Initialize LocalFileDeleteError.

        Args:
            filename (str): The name of the file that caused the error.
            message (str): A message describing the error.
        """
        self.filename = filename
        self.message = message
        super().__init__(f"Failed to delete file '{filename}': {message}")


class LocalFileTooLargeError(LocalFileSystemException):
    """Exception raised when a file is too large to be read."""

    def __init__(
        self, filename: Union[PathLike[str], str], size: int, max_size: int
    ):
        """
        Initialize LocalFileTooLargeError.

        Args:
            filename (str): The name of the file that caused the error.
            size (int): The size of the file.
            max_size (int): The maximum allowed size of the file.
        """
        self.filename = filename
        self.size = size
        self.max_size = max_size
        super().__init__(
            f"File '{filename}' is too large to read: {size} bytes (max allowed: {max_size} bytes)"
        )
