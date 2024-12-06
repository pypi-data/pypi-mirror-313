import zipfile
from os import PathLike
from pathlib import Path
from typing import Generator, List, Optional, Type, Union

from pipefy.exceptions.base import ProcessorStopIteration
from pipefy.exceptions.unzip_processor import UnzipError
from pipefy.log import logger_factory
from pipefy.processors.base import BaseProcessor
from pipefy.processors.file_system import AbstractFileSystemManager, FileModeEnum

logger = logger_factory()


class BaseUnzipProcessor(
    BaseProcessor[
        Union[str, PathLike[str]], Union[str, PathLike[str]], None, None
    ],
):
    """
    A processor that handles unzipping of `.zip` files.

    This processor takes a `.zip` file as input, extracts its contents,
    and yields the paths of the extracted files. Optionally, the processor
    can delete the `.zip` file after extraction and can handle large files
    in batches.

    Attributes:
        _file_system_manager (AbstractFileSystemManager): The file system manager for file operations.
        _white_exceptions (List[Type[Exception]]): List of exceptions to bypass.
        _auto_delete (bool): Flag to delete the zip file after processing.
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
        """
        Initializes the BaseUnzipProcessor.

        Args:
            file_system_manager (AbstractFileSystemManager): The file system manager for file operations.
            white_exceptions (Optional[List[Type[Exception]]]): List of exceptions to bypass. Defaults to None.
            auto_delete (bool): Flag to delete the zip file after processing. Defaults to True.
            batch_size (Optional[int]): The batch size in megabytes for extracting large files. Defaults to None.
        """
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
        Processes the given zip file and extracts its contents.

        Args:
            input_data (Union[str, PathLike[str]]): The path to the zip file to extract.

        Yields:
            Union[str, PathLike[str]]: The path to each extracted file.

        Raises:
            UnzipError: If the file is not a `.zip` file or cannot be processed.
        """
        suffix = Path(input_data).suffix
        if suffix != ".zip":
            raise UnzipError(
                input_data,
                f"File has an extension '{suffix}', expected .zip",
            )

        file_path = self._file_system_manager.get_path(input_data)
        logger.debug(f"Starting to unzip {input_data}")

        unzip_files: List[Union[str, PathLike[str]]] = []
        with zipfile.ZipFile(file_path, FileModeEnum.READ) as zip_ref:
            for file_info in zip_ref.infolist():
                extracted_file_path = self._file_system_manager.get_path(
                    file_info.filename
                )

                with zip_ref.open(
                    file_info, FileModeEnum.READ
                ) as source_file, open(
                    extracted_file_path,
                    FileModeEnum.WRITE_BINARY,
                ) as target_file:
                    if self._batch_size is not None:
                        while chunk := source_file.read(self._batch_size):
                            target_file.write(chunk)
                    else:
                        target_file.write(source_file.read())

                unzip_files.append(extracted_file_path)

        logger.debug("Unzipping was successful")

        if self._next is not None:
            for item in unzip_files:
                gen = self._next.process(item)
                try:
                    yield from gen
                except ProcessorStopIteration:
                    # Continue processing other files in the list even if one fails
                    pass
        else:
            yield from iter(unzip_files)

        # Optionally delete the zip file after extraction
        if self._auto_delete:
            self._file_system_manager.delete_file(input_data)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(auto_delete={self._auto_delete}, "
            f"batch_size={self._batch_size})"
        )
