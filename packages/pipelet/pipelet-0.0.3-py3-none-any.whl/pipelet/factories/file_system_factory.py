import importlib
from typing import Any, Dict

from pipelet.processors.file_system import AbstractFileSystemManager


def file_system_factory(
    path: str, kwargs: Dict[str, Any] | None = None
) -> AbstractFileSystemManager[Any, Any]:
    """
    Factory function to create an instance of a file system manager.

    Args:
        path (str): Path to the file system manager class in the format "module.submodule.ClassName".
        kwargs (Dict[str, Any]): Keyword arguments to pass to the file system manager constructor.

    Returns:
        AbstractFileSystemManager[Any, Any]: An instance of the file system manager class.

    Raises:
        ValueError: If the path is invalid or the class is not a subclass of AbstractFileSystemManager[Any, Any].
    """
    try:
        file_system_path, file_system_name = path.rsplit(".", 1)
        file_system_module = importlib.import_module(file_system_path)
        file_system_manager = getattr(file_system_module, file_system_name)
        if not issubclass(file_system_manager, AbstractFileSystemManager):
            raise ValueError(
                f"{file_system_name} is not a subclass of AbstractFileSystemManager."
            )
    except (ImportError, AttributeError, ValueError) as e:
        raise ValueError(f"Invalid path: {path}. Error: {e}")
    else:
        return (
            file_system_manager(**kwargs) if kwargs else file_system_manager()
        )
