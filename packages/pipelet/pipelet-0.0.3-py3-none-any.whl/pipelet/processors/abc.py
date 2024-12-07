"""
AbstractProcessor

This abstract base class represents a processing unit in a chain-of-responsibility pattern.
It provides an interface for managing the connection between processors and supports subprocessors for parallel or 
branched execution. Classes that extend this must implement methods for setting the next processor and associating 
subprocessors.

Features:
- Chain-of-responsibility: Allows linking processors in a sequential chain.
- Subprocessor management: Supports parallel or branched processing by associating multiple subprocessors.

Attributes:
    _next (Optional[PROCESSOR]): Reference to the next processor in the chain, or None if this is the last processor.
    _sub_processors (Optional[List[PROCESSOR]]): List of subprocessors for parallel or branched execution, or None if no subprocessors are defined.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

PROCESSOR = TypeVar("PROCESSOR", bound="AbstractProcessor")


class AbstractProcessor(
    ABC,
    Generic[PROCESSOR],
):
    """
    Abstract base class for a processing unit in a chain-of-responsibility pattern.

    This class defines the interface for processors, which can:
    - Connect to a next processor in the chain.
    - Manage subprocessors for parallel or conditional execution.
    - Serve as a base for custom processing workflows.

    Attributes:
        _next (Optional[PROCESSOR]): Reference to the next processor in the chain.
        _sub_processors (Optional[List[PROCESSOR]]): List of associated subprocessors.
    """

    _next: Optional[PROCESSOR] = None
    """Reference to the next processor in the chain, if any."""

    _sub_processors: Optional[List[PROCESSOR]] = None
    """List of subprocessors, used for parallel or branched processing."""

    @abstractmethod
    def set_next(self, next_: PROCESSOR) -> PROCESSOR:
        """
        Set the next processor in the chain.

        Args:
            next_ (PROCESSOR): The next processor to connect to.

        Returns:
            PROCESSOR: The current processor instance for method chaining.
        """
        pass

    @abstractmethod
    def set_subprocessors(self, sub_processors: List[PROCESSOR]) -> PROCESSOR:
        """
        Set a list of possible subprocessors.

        Args:
            sub_processors (List[PROCESSOR]): A list of subprocessors to associate with this processor.

        Returns:
            PROCESSOR: The current processor instance for method chaining.
        """
        pass
