from abc import ABC, abstractmethod
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import Generic, Optional, Union

from pipelet.exceptions.file_system import (
    LocalFileCreationError,
    LocalFileDeleteError,
    LocalFileReadError,
    LocalFileTooLargeError,
)
from pipelet.log import logger_factory
from pipelet.processors.file_system import file_system_types as f_types

logger = logger_factory()


class FileModeEnum(str, Enum):
    """Enum for file modes."""

    READ = "r"
    WRITE = "w"
    APPEND = "a"
    READ_BINARY = "rb"
    WRITE_BINARY = "wb"
    APPEND_BINARY = "ab"
    READ_WRITE = "r+"
    READ_WRITE_BINARY = "rb+"
    WRITE_READ = "w+"
    WRITE_READ_BINARY = "wb+"
    APPEND_READ = "a+"
    APPEND_READ_BINARY = "ab+"


class FileEncodingEnum(str, Enum):
    """Enum for file encoding formats."""

    UTF_8 = "utf-8"
    UTF_16 = "utf-16"
    UTF_32 = "utf-32"
    ASCII = "ascii"
    LATIN_1 = "latin-1"
    CP1252 = "cp1252"
    ISO_8859_1 = "iso-8859-1"
    WINDOWS_1251 = "Windows-1251"
    MAC_CYRILLIC = "mac_cyrillic"


class AbstractFileSystemManager(ABC, Generic[f_types.TPath, f_types.TContent]):
    """Abstract base class for file system operations."""

    @abstractmethod
    def get_path(self, filename: f_types.TPath) -> f_types.TPath:
        """
        Get the full path for the given filename.

        Args:
            filename: Relative path of the file.

        Returns:
            Full path to the file.
        """
        pass

    @abstractmethod
    def create_file(
        self,
        filename: f_types.TPath,
        content: Optional[f_types.TContent] = None,
    ) -> str:
        """
        Create a file with the given content.

        Args:
            filename: Name of the file to create.
            content: Content to write to the file.

        Returns:
            Path to the created file as a string.
        """
        pass

    @abstractmethod
    def read_file(
        self, filename: Union[PathLike[str], str]
    ) -> Union[bytes, str]:
        """
        Read the content of a file.

        Args:
            filename: Path to the file to read.

        Returns:
            The content of the file as bytes or string.
        """
        pass

    @abstractmethod
    def delete_file(self, filename: Union[PathLike[str], str]) -> None:
        """
        Delete the specified file.

        Args:
            filename: Path to the file to delete.
        """
        pass

    @abstractmethod
    def append_to_file(
        self, filename: Union[PathLike[str], str], content: Union[bytes, str]
    ) -> None:
        """
        Append content to an existing file.

        Args:
            filename: Path to the file.
            content: Content to append to the file.
        """
        pass


class FileSystemManager(AbstractFileSystemManager[Path, Union[bytes, str]]):
    """File system manager for handling file operations in a local directory."""

    def __init__(
        self,
        root_dir: Union[PathLike[str], str],
        max_file_size_mb: int = 512,
        write_mode: FileModeEnum = FileModeEnum.WRITE_BINARY,
        read_mode: FileModeEnum = FileModeEnum.READ,
        encoding: Optional[str] = None,
    ):
        """
        Initialize the file system manager.

        Args:
            root_dir: The root directory for file operations.
            max_file_size_mb: Maximum allowable file size in megabytes.
            write_mode: Default mode for writing files.
            read_mode: Default mode for reading files.
            encoding: Default file encoding (optional).
        """
        self._root_dir: Path = Path(root_dir)
        self._max_file_size_mb: int = max_file_size_mb
        self._max_file_size_bytes: int = self._max_file_size_mb * 1024 * 1024
        self._write_mode: FileModeEnum = write_mode
        self._read_mode: FileModeEnum = read_mode
        self._encoding: Optional[str] = encoding

    def get_path(self, filename: Union[PathLike[str], str]) -> Path:
        """
        Get the full path for a file within the root directory.

        Args:
            filename: Relative filename.

        Returns:
            Full path as a Path object.
        """
        return self._root_dir / filename

    def create_dir(self, dir_: Union[PathLike[str], str]) -> Path:
        """
        Create a directory if it doesn't exist.

        Args:
            dir_: Directory path to create.

        Returns:
            Path object of the created directory.
        """
        dir_path: Path = self.get_path(filename=dir_)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def create_file(
        self,
        filename: Union[PathLike[str], str],
        content: Optional[Union[bytes, str]] = None,
    ) -> str:
        """
        Create a file with optional content.

        Args:
            filename: File name to create.
            content: Content to write to the file (optional).

        Returns:
            Path to the created file as a string.
        """
        filepath: Path = self.get_path(filename=filename)
        try:
            with open(
                file=filepath,
                mode=self._write_mode.value,
                encoding=(
                    self._encoding
                    if "b" not in self._write_mode.value
                    else None
                ),
            ) as f:
                if content is not None:
                    f.write(content)  # type: ignore[arg-type]
        except OSError as e:
            logger.error(f"Failed to create file: {filepath}, error: {e}")
            raise LocalFileCreationError(filename=filepath, message=str(e))
        return str(filepath)

    def read_file(
        self, filename: Union[PathLike[str], str]
    ) -> Union[bytes, str]:
        """
        Read the content of a file.

        Args:
            filename: File name to read.

        Returns:
            The content of the file.
        """
        self._check_file_size(filename=filename)
        filepath: Path = self.get_path(filename=filename)
        try:
            with open(
                file=filepath,
                mode=self._read_mode.value,
                encoding=(
                    self._encoding if "b" not in self._read_mode.value else None
                ),
            ) as f:
                return f.read()
        except (OSError, UnicodeDecodeError) as e:
            logger.error(f"Failed to read file: {filepath}, error: {e}")
            raise LocalFileReadError(filename=filepath, message=str(e))

    def delete_file(self, filename: Union[PathLike[str], str]) -> None:
        """
        Delete a file from the filesystem.

        Args:
            filename: File name to delete.
        """
        filepath: Path = self.get_path(filename=filename)
        try:
            if filepath.exists():
                filepath.unlink()
            else:
                logger.warning(f"File does not exist: {filepath}")
        except OSError as e:
            logger.error(f"Failed to delete file: {filepath}, error: {e}")
            raise LocalFileDeleteError(filename=filepath, message=str(e))

    def append_to_file(
        self, filename: Union[PathLike[str], str], content: Union[bytes, str]
    ) -> None:
        """
        Append content to a file.

        Args:
            filename: File name to append to.
            content: Content to append to the file.
        """
        filepath: Path = self.get_path(filename=filename)
        try:
            with open(
                filepath,
                mode=(
                    FileModeEnum.APPEND_BINARY.value
                    if isinstance(content, bytes)
                    else FileModeEnum.APPEND.value
                ),
                encoding=self._encoding if isinstance(content, str) else None,
            ) as f:
                f.write(content)  # type: ignore[arg-type]
        except OSError as e:
            logger.error(f"Failed to append to file: {filepath}, error: {e}")
            raise LocalFileCreationError(filename=filepath, message=str(e))

    def _check_file_size(self, filename: Union[PathLike[str], str]) -> None:
        """
        Check if the file size exceeds the allowed limit.

        Args:
            filename: File name to check.

        Raises:
            LocalFileTooLargeError: If the file size exceeds the limit.
        """
        filepath: Path = self.get_path(filename=filename)
        file_size: int = filepath.stat().st_size
        if file_size > self._max_file_size_bytes:
            logger.error(f"File size too large: {filepath}")
            raise LocalFileTooLargeError(
                filename=filepath,
                size=file_size,
                max_size=self._max_file_size_bytes,
            )
