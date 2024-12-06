"""
ETL Operation Processing Framework

This module provides the foundational components and functions for handling ETL operations
using a chain-of-responsibility pattern. The main features include:

1. **Operation Processing (`Op`, `OpAny`, `OpAll`):** 
   - Classes to represent individual and composite operations in ETL workflows.
   - Support for retry logic, processor chains, and flexible configurations.

2. **Processor Management:**
   - Mapping between operations and their respective processor classes.
   - Functions to process individual and composite operations (`process_op`, `process_op_composite`).

3. **Customizability:**
   - Retry processors with customizable configurations.
   - Dynamic processor instantiation using `get_processor`.

4. **Core Enums and Utilities:**
   - `BaseOpEnum`: Predefined enumeration for common processor paths.
   - `PROCESSOR_DISPATCH_MAP`: Dispatch table for mapping operation types to processing functions.

Classes and Functions:
- `BaseOpEnum`: Enum defining paths to processor classes for common operations.
- `Op`: Represents a single operation configuration.
- `OpAny`, `OpAll`: Define composite operations requiring any or all conditions.
- `prepare_retry_processor`: Wraps a processor with retry logic.
- `process_op`, `process_op_composite`: Handle individual and composite operation processing.
- `get_processor_for_operation`: Dispatch function for retrieving the appropriate processor.

Dependencies:
- `factories`: Contains `KEYWORD_FACTORY_MAP` for keyword-based processor initialization.
- `log`: Logger factory for logging processor execution.
- `processors`: Includes base and custom processors.

This framework enables modular, reusable, and extensible ETL workflows by abstracting the 
processing logic into well-defined processors and operations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar, Union

from pipelet.factories import KEYWORD_FACTORY_MAP
from pipelet.log import logger_factory
from pipelet.processors import get_processor
from pipelet.processors.base import BaseProcessor
from pipelet.processors.chain_processors import (
    ChainAllProcessor,
    ChainAnyProcessor,
)
from pipelet.processors.retry_processor import RetryProcessor

logger = logger_factory()


class BaseOpEnum(str, Enum):
    """Enumeration defining base operations and their corresponding processor paths."""

    downloading = "pipelet.etl.extract.http.HttpDataExtractProcessor"
    stream_downloading = "pipelet.etl.extract.http.HttpxStreamDownloadProcessor"
    unzip = "pipelet.etl.transform.unzip.BaseUnzipProcessor"
    csv_parsing = "pipelet.etl.transform.csv.CsvParser"
    json_parsing = "pipelet.etl.transform.json.JsonParser"
    retrying = "pipelet.processors.retry_processor.RetryProcessor"
    splitting = "pipelet.processors.splitter_processor.SplitterProcessor"


T = TypeVar("T", bound="BaseOpComposite")


@dataclass(slots=True)
class Op:
    """
    Represents an operation configuration.

    Attributes:
        operation (str): Path to the processor class in "module.ClassName" format.
    """

    operation: str
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BaseOpComposite(Generic[T]):
    """
    Base class for a configuration of multiple operations.

    Attributes:
        operations (List[Op | T]): List of operations.
    """

    operations: List[Union[Op, T]]
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OpAny(BaseOpComposite[Union["OpAny", "OpAll"]]):
    """
    Represents a configuration for multiple operations (any of).

    Attributes:
        operations (List[Op | OpAny | OpAll]): List of operations.
    """


@dataclass(slots=True)
class OpAll(BaseOpComposite[Union["OpAny", "OpAll"]]):
    """
    Represents a configuration for multiple operations (all of).

    Attributes:
        operations (List[Op | OpAny | OpAll]): List of operations.
    """


def prepare_retry_processor(
    processor: BaseProcessor[Any, Any, Any, Any], kwargs: Dict[str, Any]
) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Wraps a given processor with a retry processor if retry parameters are provided.

    This function allows optional customization of the retry processor by passing
    a "retry_processor" key in the kwargs dictionary. If no custom processor is
    specified, the default `RetryProcessor` is used. Any remaining arguments in
    `kwargs` are passed to the retry processor as initialization parameters.

    Args:
        processor (BaseProcessor[Any, Any, Any, Any]): The processor to wrap with a retry mechanism.
        kwargs (Dict[str, Any]): A dictionary of parameters, including optional retry-specific settings.
            - "retry_processor" (Optional): The name of a custom retry processor class to use.
            - Any additional keys are treated as arguments for the retry processor.

    Returns:
        BaseProcessor[Any, Any, Any, Any]: The original processor wrapped with a retry processor, if applicable.

    """
    custom_retry_processor = kwargs.pop("retry_processor", None)

    if kwargs:
        retry_processor = (
            get_processor(custom_retry_processor)(**kwargs)
            if custom_retry_processor
            else RetryProcessor(**kwargs)
        )
        processor = retry_processor.set_next(processor)

    return processor


def process_op(op: Op) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Processes an Op and returns an instance of BaseProcessor.

    Args:
        op (Op): The operation object defining the operation and its args.

    Returns:
        BaseProcessor: Processor instance for the given operation.

    Raises:
        ValueError: If the processor is not a subclass of BaseProcessor.
    """
    type_processor = get_processor(op.operation)
    kwargs: Dict[str, Any] = {}
    for k, v in op.kwargs.items():
        factory = KEYWORD_FACTORY_MAP.get(k, None)
        if factory:
            kwargs[k] = factory(**v) if isinstance(v, dict) else factory(v)
        else:
            kwargs[k] = v
    retry_args: Dict[str, Any] = kwargs.pop("retry_args", {})
    processor = type_processor(**kwargs)
    processor = prepare_retry_processor(processor, kwargs=retry_args)
    return processor


OP_COMPOSITE_PROCESSOR_MAP: Dict[
    Type[BaseOpComposite[Union[OpAny, OpAll]]],
    Type[BaseProcessor[Any, Any, Any, Any]],
] = {
    OpAny: ChainAnyProcessor,
    OpAll: ChainAllProcessor,
}


def get_composite_possible_processor(
    op: BaseOpComposite[OpAny | OpAll],
    kwargs: Dict[str, Any],
) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Retrieves a chain processor based on the type of the given composite operation.

    This function looks up the appropriate chain processor class from the
    OP_COMPOSITE_PROCESSOR_MAP using the type of the provided operation.
    It then instantiates and returns an object of that class, initialized
    with the keyword arguments (`kwargs`) from the operation.

    Args:
        op (BaseOpComposite): The composite operation for which a processor is needed.

    Returns:
        BaseProcessor: An instance of the appropriate chain processor class.

    Raises:
        ValueError: If no matching chain processor class is found for the given operation.
    """
    chain_possible_processor = OP_COMPOSITE_PROCESSOR_MAP.get(
        op.__class__, None
    )
    if not chain_possible_processor:
        raise ValueError(
            f"No processor found for operation of type {op.__class__.__name__}"
        )
    return chain_possible_processor(**kwargs)


def process_op_composite(
    possible_op: BaseOpComposite[Union[OpAny, OpAll]],
) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Processes a composite operation by constructing a chain of processors.

    This function iterates over the operations within a given composite
    operation, processing each one. It constructs and returns a chain
    processor that can handle the entire sequence of operations.

    Args:
        possible_op (Op | BaseOpComposite): The composite operation containing
        individual operations or other composite operations to process.

    Returns:
        BaseProcessor: A chain processor configured to handle
        the sequence of operations specified in the composite operation.
    """
    processors = []

    for item in possible_op.operations:
        if isinstance(item, Op):
            sub_processor = process_op(item)  # Process individual Op
            processors.append(sub_processor)
        elif isinstance(item, BaseOpComposite):
            processor = process_op_composite(item)
            processors.append(processor)

    kwargs = {}
    for k, v in possible_op.kwargs.items():
        factory = KEYWORD_FACTORY_MAP.get(k, None)
        if factory:
            kwargs[k] = factory(**v) if isinstance(v, dict) else factory(v)
        else:
            kwargs[k] = v

    # Get the appropriate processor for the composite
    chain_possible_processor = get_composite_possible_processor(
        possible_op, kwargs
    )
    chain_possible_processor.set_subprocessors(processors)
    return chain_possible_processor


PROCESSOR_DISPATCH_MAP: Dict[
    Type[Union[Op, OpAny, OpAll]],
    Union[
        Callable[[Op], BaseProcessor[Any, Any, Any, Any]],
        Callable[
            [BaseOpComposite[Union[OpAny, OpAll]]],
            BaseProcessor[Any, Any, Any, Any],
        ],
    ],
] = {
    Op: process_op,
    OpAny: process_op_composite,
    OpAll: process_op_composite,
}


def get_processor_for_operation(
    op: Union[Op, OpAny, OpAll],
) -> BaseProcessor[Any, Any, Any, Any]:
    """
    Retrieves and executes the processor function for the given operation.

    Args:
        op (Op | OpAny | OpAll): Operation object to process.

    Returns:
        BaseProcessor: Instance of processor for the given operation.

    Raises:
        ValueError: If no processor function is found for the type of op.
    """
    processor_function = PROCESSOR_DISPATCH_MAP.get(type(op))
    if not processor_function:
        raise ValueError(
            f"No processor function found for type {type(op).__name__}"
        )
    # TODO: FIX type ignore
    return processor_function(op)  # type: ignore
