"""
Protocols for duck typing elements of AX.25 serialization/deserialization.

Do not include any code that should actually run here, as it won't be analyzed for
test coverage.
"""

from typing import Protocol, Self

from pax25.ax25.constants import FrameType


class Assembler(Protocol):  # pragma: no cover
    """
    Protocol for logical segments of a packet. Allows for assembly/disassembly.

    Also includes __len__ for Sized compatibility because you cannot intersection
    protocols with MyPy (yet.)
    """

    def __len__(self) -> int:
        """
        The length of the data structure when assembled.
        """
        raise NotImplementedError("Subclasses must implement __len__.")

    def assemble(self) -> bytes:
        """
        Method for turning a data structure into bytes suitable for transmission.
        """

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Method for instantiating this data structure from bytes.
        """


class ControlField(Protocol):  # pragma: no cover
    """
    Base protocol for control fields.

    Also includes the methods from Assembler because you cannot intersection protocols
    with MyPy (yet.)
    """

    def __len__(self) -> int:
        """
        The length of the data structure when assembled.
        """

    @property
    def type(self) -> FrameType:
        """
        Return the type of the frame we have.
        """

    def assemble(self) -> bytes:
        """
        Method for turning a data structure into bytes suitable for transmission.
        """

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Method for instantiating this data structure from bytes.
        """
