class BaseProcessorException(Exception):
    """Base exception for processor-related errors."""


class BaseFileSystemException(BaseProcessorException):
    """Base exception for file system-related errors."""


class BaseCsvProcessorException(BaseProcessorException):
    """Base exception for CSV processor-related errors."""


class BaseUnzipException(BaseProcessorException):
    """Base exception for unzip-related errors."""


class BaseDownloadProcessorException(BaseProcessorException):
    """Base exception for download processor-related errors."""


class ProcessorStopIteration(BaseProcessorException):
    """
    Custom exception used to stop generators in the data processing system.

    This exception is used as a replacement for the standard `StopIteration` exception.
    It allows external logic to handle the termination of generators explicitly by catching
    this exception. This provides more control over generator flow management compared
    to the default behavior.

    When this exception is raised in a generator, it indicates a normal termination
    of the iteration. It should be used in scenarios where external code needs to
    manage or log the termination of the generator.

    Attributes:
        message (str): A message describing the reason for the termination.

    Example:
        def my_generator():
            yield 1
            yield 2
            raise ProcessorStopIteration("Reached end of processing")

    Args:
        message (str): A message describing the reason for the termination.
    """

    def __init__(self, message: str):
        """
        Initialize ProcessorStopIteration.

        Args:
            message (str): A message describing the reason for the termination.
        """
        self.message = message
        super().__init__(f"Processing stopped: {message}")
