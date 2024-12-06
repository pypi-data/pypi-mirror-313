from typing import Any, Callable, Dict

from pipelet.factories.exceptions_factory import custom_exceptions_factory
from pipelet.factories.file_system_factory import file_system_factory

KEYWORD_FACTORY_MAP: Dict[str, Callable[..., Any]] = {
    "file_system_manager": file_system_factory,
    "white_exceptions": custom_exceptions_factory,
}
