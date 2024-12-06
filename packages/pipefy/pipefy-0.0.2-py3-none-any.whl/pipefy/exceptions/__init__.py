from enum import Enum


class BaseExceptionsEnum(str, Enum):
    csv_exception = "pipefy.exceptions.csv_processor.CsvProcessorException"
    csv_parsing_error = "pipefy.exceptions.csv_processor.CsvParsingError"
    unzip_exception = (
        "pipefy.exceptions.unzip_processor.UnzipProcessorException"
    )
    unzip_error = "pipefy.exceptions.unzip_processor.UnzipError"
    download_exception = (
        "pipefy.exceptions.download_processor.DownloadProcessorException"
    )
    download_error = "pipefy.exceptions.download_processor.DownloadError"

    file_system_exception = "pipefy.exceptions.base.BaseFileSystemException"
    local_file_system_exception = (
        "pipefy.exceptions.file_system.LocalFileSystemException"
    )
    local_file_system_create_file_error = (
        "pipefy.exceptions.file_system.LocalFileCreationError"
    )
    local_file_system_read_file_error = (
        "pipefy.exceptions.file_system.LocalFileReadError"
    )
    local_file_system_delete_file_error = (
        "pipefy.exceptions.file_system.LocalFileDeleteError"
    )
    local_file_system_too_large_error = (
        "pipefy.exceptions.file_system.LocalFileTooLargeError"
    )
