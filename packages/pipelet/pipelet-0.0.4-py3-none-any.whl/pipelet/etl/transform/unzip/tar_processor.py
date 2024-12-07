import tarfile
from os import PathLike
from pathlib import Path
from typing import Generator, List, Optional, Type, Union

from pipelet.exceptions.base import ProcessorStopIteration
from pipelet.exceptions.unzip_processor import UnzipError
from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor
from pipelet.processors.file_system import (
    AbstractFileSystemManager,
    FileModeEnum,
)

logger = logger_factory()


class TarExtractProcessor(
    BaseProcessor[
        Union[str, PathLike[str]], Union[str, PathLike[str]], None, None
    ],
):
    """
    A processor that handles extracting `.tar` archives (including compressed formats).

    This processor takes a `.tar` file (or compressed `.tar` variants like `.tar.gz`, `.tgz`),
    extracts its contents, and yields the paths of the extracted files and directories.

    Attributes:
        _file_system_manager (AbstractFileSystemManager): File system manager for file operations.
        _white_exceptions (List[Type[Exception]]): List of exceptions to bypass.
        _auto_delete (bool): Flag to delete the tar file after processing.
        _batch_size (Optional[int]): The batch size in bytes for extracting large files.
    """

    def __init__(
        self,
        file_system_manager: AbstractFileSystemManager[
            Union[str, PathLike[str]], Union[str, bytes]
        ],
        white_exceptions: Optional[List[Type[Exception]]] = None,
        auto_delete: bool = True,
        batch_size: Optional[int] = None,
    ) -> None:
        self._file_system_manager = file_system_manager
        self._white_exceptions = white_exceptions or []
        self._auto_delete = auto_delete
        self._batch_size = (
            batch_size * 1024 * 1024 if batch_size is not None else None
        )

    def process(
        self,
        input_data: Union[str, PathLike[str]],
    ) -> Generator[Union[str, PathLike[str]], None, None]:
        """
        Processes the given tar file and extracts its contents.

        Args:
            input_data (Union[str, PathLike[str]]): The path to the tar file to extract.

        Yields:
            Union[str, PathLike[str]]: The path to each extracted file or directory.

        Raises:
            UnzipError: If the file is not a `.tar` file or cannot be processed.
        """
        suffix = Path(input_data).suffix
        if suffix not in [".tar", ".gz", ".bz2", ".xz", ".tgz", ".tbz2"]:
            raise UnzipError(
                input_data,
                f"File has an extension '{suffix}', expected a supported .tar format",
            )

        file_path = self._file_system_manager.get_path(input_data)
        extracted_paths: List[Union[str, PathLike[str]]] = []

        try:
            with tarfile.open(file_path, mode="r:*") as tar:
                for member in tar.getmembers():
                    extracted_path = self._file_system_manager.get_path(
                        member.name
                    )
                    if member.isdir():
                        # Create the directory if it does not exist
                        Path(extracted_path).mkdir(parents=True, exist_ok=True)
                        logger.info(f"Created directory: {member.name}")
                        extracted_paths.append(extracted_path)
                    elif member.isfile():
                        # Extract file and handle large files with batching
                        source_file = tar.extractfile(member)
                        if source_file is not None:
                            with source_file, open(
                                extracted_path, FileModeEnum.WRITE_BINARY
                            ) as target_file:
                                if self._batch_size is not None:
                                    while chunk := source_file.read(
                                        self._batch_size
                                    ):
                                        target_file.write(chunk)
                                else:
                                    target_file.write(source_file.read())
                            extracted_paths.append(extracted_path)
                        else:
                            logger.warning(
                                f"Could not extract file: {member.name}"
                            )
                    else:
                        logger.info(
                            f"Skipping unsupported member type: {member.name}"
                        )

        except Exception as e:
            raise UnzipError(file_path, f"Failed to extract tar file: {e}")

        # Pass extracted paths to the next processor, if defined
        if self._next is not None:
            for item in extracted_paths:
                try:
                    yield from self._next.process(item)
                except ProcessorStopIteration:
                    pass
        else:
            yield from iter(extracted_paths)

        # Optionally delete the tar file after processing
        if self._auto_delete:
            self._file_system_manager.delete_file(input_data)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(auto_delete={self._auto_delete}, "
            f"batch_size={self._batch_size})"
        )
