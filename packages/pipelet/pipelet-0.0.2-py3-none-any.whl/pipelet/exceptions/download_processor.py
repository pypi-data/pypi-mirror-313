from pipelet.exceptions.base import BaseDownloadProcessorException


class DownloadProcessorException(BaseDownloadProcessorException):
    """Base exception for download processor-related errors."""


class DownloadError(DownloadProcessorException):
    """Exception raised for errors occurring during file download."""

    def __init__(self, url: str, message: str):
        """
        Initialize DownloadError.

        Args:
            url (str): The URL of the file that caused the error.
            message (str): A message describing the error.
        """
        self.url = url
        self.message = message
        super().__init__(f"Failed to download file from '{url}': {message}")
