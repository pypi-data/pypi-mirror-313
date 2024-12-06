"""
Data classes and helpful for assembling/disassembling an AX.25 frame at large.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self, Type

from pax25.ax25.address import Ax25RoutePath
from pax25.ax25.constants import AX25_ENDIAN
from pax25.ax25.control_field import derive_control_class
from pax25.ax25.exceptions import DisassemblyError
from pax25.ax25.protocols import Assembler, ControlField


@dataclass(frozen=True, kw_only=True)
class Ax25Frame:
    """
    Represents an AX.25 frame for transmission or reception
    """

    pid: int
    route: Ax25RoutePath
    control: ControlField
    info: bytes

    def __len__(self) -> int:
        return sum(
            (
                len(item or "")
                for item in (
                    self.route,
                    self.control,
                    self.control and self.pid.to_bytes(1, AX25_ENDIAN),
                    self.info,
                )
            )
        )

    def __str__(self) -> str:
        """
        String representation of an AX25 frame. Emulates (mostly) how a TNC displays a
        frame, with the main exception being that we display binary data as its hex
        representation rather than sending it literally.
        """
        segments = [
            str(self.route),
            ": ",
        ]
        control_segment = str(self.control)
        if self.route.src.command_or_repeated:
            control_segment = f"<{control_segment}>"
        segments.append(control_segment)
        if self.info:
            segments.extend(
                [
                    ":",
                    os.linesep,
                    self.info.decode(encoding="utf-8", errors="backslashreplace"),
                ]
            )
        return "".join(segments)

    def assemble(self) -> bytes:
        """
        Assemble this frame into a bytearray suitable for transmission.
        """
        data = bytearray()
        data.extend(self.route.assemble())
        if self.control:
            data.extend(self.control.assemble())
            # PID could only be set if the control byte is set, per disassembly.
            data.extend(bytearray(self.pid.to_bytes(1, AX25_ENDIAN)))
        data.extend(self.info)
        return bytes(data)

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Given a bytestream frame pulled from the wire, create an Ax25Frame instance.
        """
        data, route = consume_assembler(data, Ax25RoutePath)
        control_class = derive_control_class(data)
        data, control = consume_assembler(data, control_class)
        try:
            pid = data[0]
        except IndexError as err:
            raise DisassemblyError("Protocol ID byte is missing.") from err
        data = data[1:]
        info = bytes(data)
        return cls(route=route, control=control, pid=pid, info=info)


@dataclass
class AxFrameTracker:
    """
    Metadata about a frame, unrelated to its protocol contents.
    """

    frame: Optional[Ax25Frame] = None
    tx_time: Optional[datetime] = None
    tx_count: int = 0
    # phy: PhysicalInterface, or similar, when ready.
    fault: bool = False


def consume_assembler[T: Assembler](data: bytes, cls: Type[T]) -> tuple[bytes, T]:
    """
    Given a bytearray, pull what's necessary from the array to form a given disassembled
    dataclass, and return it with the remainder.
    """
    instance = cls.disassemble(data)
    return data[len(instance) :], instance
