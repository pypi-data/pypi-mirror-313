import importlib
from typing import Any, List, Type

from pipelet.processors.base import BaseProcessor


def processors_to_chain(
    processors: List[BaseProcessor[Any, Any, Any, Any]],
) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Chains together a list of processors into a single linked chain.

    Args:
        processors (List[BaseProcessor]): A list of processor instances
            to be chained together. The processors will be linked in reverse order.

    Returns:
        BaseProcessor: The head of the chain, which is an instance of BaseProcessor.

    Raises:
        ValueError: If no processors are provided.
    """
    chain = processors[-1]
    for processor in reversed(processors[:-1]):
        chain = processor.set_next(chain)

    return chain


def get_processor(
    path_to_processor: str,
) -> Type[BaseProcessor[Any, Any, Any, Any]]:
    """
    Dynamically imports and returns a processor class from a given module path.

    Args:
        path_to_processor (str): The dotted path to the processor class, e.g., "module.submodule.ProcessorClass".

    Returns:
        Type[BaseProcessor]: The processor class identified by the given path.

    Raises:
        ValueError: If the specified path is invalid, the module cannot be imported,
        or the class is not a subclass of BaseProcessor.
    """
    try:
        processor_path, processor_name = path_to_processor.rsplit(".", 1)
        processor_module = importlib.import_module(processor_path)
        processor = getattr(processor_module, processor_name)
        if not issubclass(processor, BaseProcessor):
            raise ValueError(
                f"{processor_name} is not a subclass of BaseProcessor."
            )
    except (ImportError, AttributeError, ValueError) as e:
        raise ValueError(f"Invalid path: '{path_to_processor}'. Error: {e}")
    else:
        return processor
