from enum import Enum


class BaseExceptionsEnum(str, Enum):
    csv_exception = "pipelet.exceptions.csv_processor.CsvProcessorException"
    csv_parsing_error = "pipelet.exceptions.csv_processor.CsvParsingError"
    unzip_exception = (
        "pipelet.exceptions.unzip_processor.UnzipProcessorException"
    )
    unzip_error = "pipelet.exceptions.unzip_processor.UnzipError"
    download_exception = (
        "pipelet.exceptions.download_processor.DownloadProcessorException"
    )
    download_error = "pipelet.exceptions.download_processor.DownloadError"

    file_system_exception = "pipelet.exceptions.base.BaseFileSystemException"
    local_file_system_exception = (
        "pipelet.exceptions.file_system.LocalFileSystemException"
    )
    local_file_system_create_file_error = (
        "pipelet.exceptions.file_system.LocalFileCreationError"
    )
    local_file_system_read_file_error = (
        "pipelet.exceptions.file_system.LocalFileReadError"
    )
    local_file_system_delete_file_error = (
        "pipelet.exceptions.file_system.LocalFileDeleteError"
    )
    local_file_system_too_large_error = (
        "pipelet.exceptions.file_system.LocalFileTooLargeError"
    )
