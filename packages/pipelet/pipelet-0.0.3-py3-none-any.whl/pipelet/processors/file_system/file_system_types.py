from os import PathLike
from pathlib import Path
from typing import TypeVar, Union

TContent = TypeVar("TContent", bound=Union[str, bytes])
TPath = TypeVar("TPath", bound=Union[str, PathLike[str], Path])
