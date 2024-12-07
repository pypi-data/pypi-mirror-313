from typing import Any, Sequence, Union

from pipelet.operations.operations import (
    Op,
    OpAll,
    OpAny,
    get_processor_for_operation,
)
from pipelet.processors import processors_to_chain
from pipelet.processors.base import BaseProcessor


class PipelineConverter:
    """
    Converts a list of operations and chains into a unified processor.

    Attributes:
        _pipeline (Sequence[Op | OpAny | OpAll]): Sequence of operations and/or nested chains.
    """

    def __init__(
        self,
        pipeline: Sequence[Union[Op, OpAny, OpAll]],
    ) -> None:
        """
        Initializes the PipelineConverter with a sequence of operations.

        Args:
            pipeline (Sequence[Op | OpAny | OpAll]): Sequence of operations and/or nested chains.
        """
        self._pipeline = pipeline

    def convert(self) -> BaseProcessor[Any, Any, Any, Any]:
        """
        Converts the pipeline into a unified processor.

        This method creates processors for each operation or chain and chains
        them together.

        Returns:
            BaseProcessor[Any, Any, Any, Any]:
            A unified processor for the entire pipeline.

        Raises:
            ValueError: If any operation or chain is invalid or cannot be converted.
        """
        processors = [get_processor_for_operation(op) for op in self._pipeline]
        processor = processors_to_chain(processors)
        return processor
