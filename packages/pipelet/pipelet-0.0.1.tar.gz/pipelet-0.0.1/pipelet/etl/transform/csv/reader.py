import csv
import io
from os import PathLike
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Type,
    Union,
)

import chardet
import numpy as np
import pandas as pd

from pipelet.exceptions.base import ProcessorStopIteration
from pipelet.exceptions.csv_processor import CsvParsingError
from pipelet.log import logger_factory
from pipelet.processors.base import BaseProcessor
from pipelet.processors.file_system import (
    AbstractFileSystemManager,
    FileEncodingEnum,
)

logger = logger_factory()


class CsvParser(
    BaseProcessor[str | PathLike[str], List[Dict[str, Any]], None, None],
):
    """
    A base CSV parser for reading and processing CSV files using the pandas library.

    Attributes:
        file_system_manager (AbstractFileSystemManager[Union[str, PathLike[str]], Union[str, bytes]]): Manages file operations.
        white_exceptions (List[Type[Exception]], optional): Exceptions to ignore and raise StopIteration on.
        separators (List[str]): Possible delimiters to try when parsing the CSV.
        header (int, optional): Specifies the row to use as header (default is 0).
        batch_size (Optional[int], optional): Size of each batch for chunked processing.
        encoding (Optional[str], optional): Encoding to use for reading the file.
        engine (Literal["python", "c"], optional): Engine to use for parsing.
        skip_blank_lines (bool, optional): If True, skips blank lines.
        on_bad_lines (Literal["error", "warn", "skip"], optional): Determines action for bad lines.
        quoting (Literal[0, 1, 2, 3], optional): CSV quoting style.
        oriends (Literal["dict", "list", "series", "records", "index", "columns"], optional): Parsed data format.
        converters (Optional[Dict[str, Callable]], optional): Maps column names to conversion functions.
        true_values (Optional[List[str]], optional): Values to interpret as True.
        false_values (Optional[List[str]], optional): Values to interpret as False.
        na_values (Optional[List[str]], optional): Additional values to interpret as NaN.
        keep_default_na (bool, optional): If True, uses default NaN values.
        na_filter (bool, optional): If True, detects missing values (NaN).
        auto_delete (bool, optional): If True, deletes the file after processing.

    Methods:
        process(self, input_data: str | PathLike[str]) -> Generator[List[Dict[str, Any]], None, None]:
            Parses the specified CSV file and yields data in the defined format.

        clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
            Removes unnamed columns, drops empty rows and columns, and replaces NaN with None.

        clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
            Trims whitespace and converts column names to lowercase.
    """

    def __init__(
        self,
        file_system_manager: AbstractFileSystemManager[
            Union[str, PathLike[str]], Union[str, bytes]
        ],
        separators: List[str],
        white_exceptions: Optional[List[Type[Exception]]] = None,
        header: int = 0,
        batch_size: Optional[int] = None,
        encoding: Optional[str] = None,
        engine: Literal["python", "c"] = "python",
        skip_blank_lines: bool = False,
        on_bad_lines: Literal["error", "warn", "skip"] = "skip",
        quoting: Literal[0, 1, 2, 3] = csv.QUOTE_NONE,
        oriends: Literal[
            "dict", "list", "series", "records", "index", "columns"
        ] = "records",
        converters: Optional[Dict[str, Callable]] = None,
        true_values: Optional[List[str]] = None,
        false_values: Optional[List[str]] = None,
        na_values: Optional[List[str]] = None,
        keep_default_na: bool = True,
        na_filter: bool = True,
        auto_delete: bool = True,
    ) -> None:
        """
        Initializes the CsvParser with settings for parsing.

        Args:
            file_system_manager (AbstractFileSystemManager[
                    Union[str, PathLike[str]], Union[str, bytes]
                ]
            ): Manages file interactions.
            separators (List[str]): Possible delimiters for the CSV.
            white_exceptions (Optional[List[Type[Exception]]], optional): Exceptions to bypass during processing.
            header (int, optional): Row number to use as headers (default is 0).
            batch_size (Optional[int], optional): Row count for chunked processing.
            encoding (Optional[str], optional): File encoding for reading.
            engine (Literal["python", "c"], optional): Parsing engine.
            skip_blank_lines (bool, optional): If True, ignores blank lines.
            on_bad_lines (Literal["error", "warn", "skip"], optional): Action on encountering bad lines.
            quoting (Literal[0, 1, 2, 3], optional): Quoting style used in the CSV.
            oriends (Literal["dict", "list", "series", "records", "index", "columns"], optional): Format for parsed data.
            converters (Optional[Dict[str, Callable]], optional): Converters for specific columns.
            true_values (Optional[List[str]], optional): Values to recognize as True.
            false_values (Optional[List[str]], optional): Values to recognize as False.
            na_values (Optional[List[str]], optional): Additional strings for NaN.
            keep_default_na (bool, optional): If True, adds default NaN values.
            na_filter (bool, optional): If True, detects NaN.
            auto_delete (bool, optional): Deletes the file after processing if True.
        """
        self._file_system_manager = file_system_manager
        self._white_exceptions = white_exceptions or []
        self._separators = separators
        self._header = header
        self._batch_size = batch_size
        self._encoding = encoding
        self._engine = engine
        self._skip_blank_lines = skip_blank_lines
        self._on_bad_lines = on_bad_lines
        self._oriends = oriends
        self._quoting = quoting
        self._converters = converters or {}
        self._true_values = true_values or []
        self._false_values = false_values or []
        self._na_values = na_values or []
        self._keep_default_na = keep_default_na
        self._na_filter = na_filter
        self._auto_delete = auto_delete

    @staticmethod
    def _get_encoding(content: bytes) -> Optional[str]:
        """
        Detects encoding of file content bytes.

        Args:
            content (bytes): Byte data to inspect.

        Returns:
            Optional[str]: Encoding if detected, else None.
        """
        result = chardet.detect(content)
        encoding = result["encoding"]
        return encoding

    def _read_csv(
        self, filename: str | PathLike[str], separator: str, **kwargs
    ) -> pd.DataFrame:
        """Reads a CSV file with a given separator.

        Args:
            filename (str): CSV file path.
            separator (str): Delimiter for fields.

        Returns:
            pd.DataFrame: Parsed data in a DataFrame.
        """
        content = self._file_system_manager.read_file(filename)
        if isinstance(content, str):
            content = content.encode(FileEncodingEnum.UTF_8)
        if bytes(separator, encoding=FileEncodingEnum.UTF_8) not in content:
            raise pd.errors.ParserError(
                f"Separator '{separator}' not found in the file content."
            )
        content_io = io.BytesIO(content)
        return pd.read_csv(
            content_io,
            sep=separator,
            encoding=self._encoding or self._get_encoding(content),  # type: ignore
            **kwargs,
        )

    @staticmethod
    def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans column names by stripping whitespace and converting to lowercase.

        Args:
            df (pd.DataFrame): DataFrame with columns to clean.

        Returns:
            pd.DataFrame: DataFrame with cleaned column names.
        """
        df.columns = df.columns.str.strip().str.lower()
        return df

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes unnamed columns, drops all-NA rows and columns, and replaces NaN with None.

        Args:
            df (pd.DataFrame): DataFrame to clean.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        df = self._clean_column_names(df)
        df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]
        df = (
            df.dropna(how="all")
            .dropna(axis=1, how="all")
            .replace({np.nan: None})
        )
        return df

    def process(
        self, input_data: str | PathLike[str]
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Parses the CSV file and yields formatted data as records.

        Args:
            input_data (str | PathLike[str]): CSV file path.

        Yields:
            Generator[List[Dict[str, Any]], None, None]: Parsed data as records.

        Raises:
            CsvParsingError: If parsing fails.
        """
        logger.debug(f"Start parsing: {input_data}")
        suffix = Path(input_data).suffix
        if suffix != ".csv":
            raise CsvParsingError(
                input_data,
                f"File has an extension '{suffix}', expected .csv",
            )
        read_csv_kwargs = {
            "header": self._header,
            "chunksize": self._batch_size,
            "engine": self._engine,
            "skip_blank_lines": self._skip_blank_lines,
            "on_bad_lines": self._on_bad_lines,
            "quoting": self._quoting,
            "converters": self._converters,
            "true_values": self._true_values,
            "false_values": self._false_values,
            "na_values": self._na_values,
            "keep_default_na": self._keep_default_na,
            "na_filter": self._na_filter,
        }

        df = None
        for sep in self._separators:
            try:
                df = self._read_csv(
                    input_data, separator=sep, **read_csv_kwargs
                )
                break
            except pd.errors.ParserError as e:
                logger.warning(
                    f"Failed to parse {input_data} with separator '{sep}': {e}"
                )
                continue

        if df is None:
            raise CsvParsingError(
                input_data,
                "Failed to parse with any of the provided separators.",
            )

        if self._batch_size is None:
            df = self._clean_dataframe(df)
            records = df.to_dict(orient=self._oriends)  # type: ignore
            if self._next is not None:
                gen = self._next.process(records)
                yield from gen
            else:
                yield records
        else:
            for chunk in df:
                chunk = self._clean_dataframe(chunk)  # type: ignore
                if chunk.empty:
                    continue
                records = chunk.to_dict(orient=self._oriends)  # type: ignore
                if self._next is not None:
                    gen = self._next.process(records)
                    try:
                        yield from gen
                    except ProcessorStopIteration:
                        ...
                else:
                    yield records
        if self._auto_delete:
            self._file_system_manager.delete_file(input_data)
        logger.debug(f"Successful parsing: {input_data}")

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(auto_delete={self._auto_delete}, "
            f"batch_size={self._batch_size}, "
            f"separators={self._separators}, "
            f"header={self._header}, "
            f"encoding={self._encoding})"
        )
