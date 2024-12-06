from io import TextIOWrapper
from typing import Any, Callable, Literal, TypeAlias, overload

import pandas as pd
from fsspec import AbstractFileSystem
from fsspec.spec import AbstractBufferedFile

GlobPath: TypeAlias = str

class Storage(AbstractFileSystem):
    def __init__(
        self, logging_function: Callable | None = None, *args, **storage_options
    ): ...
    @overload
    def get(
        self,
        remote_path: str | list[str] | GlobPath | list[GlobPath],
        local_path: str,
        recursive: bool = False,
    ): ...
    @overload
    def get(
        self,
        remote_path: list[str],
        local_path: list[str],
        recursive: bool = False,
    ): ...
    def put(self, local_path: str | list[str], remote_path: str | list[str]): ...
    def open_for_writing(
        self, path: str, text: bool = False, *, log: bool = True
    ) -> TextIOWrapper | AbstractBufferedFile: ...
    def open_for_reading(
        self, path: str, text: bool = False, *, log: bool = True
    ) -> TextIOWrapper | AbstractBufferedFile: ...
    def move(self, source_path: str, destination_path: str): ...
    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    def remove_files(self, paths: str | list[str], recursive: bool = False): ...
    def read_dataset_from_parquet(self, path: str) -> pd.DataFrame: ...
    def write_dataframe_to_parquet(self, path: str, df: pd.DataFrame): ...
    def loader(self, path: str, load_method: Callable, text: bool = False): ...
    def write_to_file(self, path: str, content: str | bytes): ...

def filesystem(
    protocol: str, logging_function: Callable | None = None, **storage_options
) -> Storage: ...
