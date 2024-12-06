"""
Address-related data structures.
"""

from dataclasses import dataclass
from typing import Self

from pax25.ax25.constants import (
    AX25_ADDR_SIZE,
    AX25_CODEPAGE,
    AX25_ENDIAN,
    AX25_SSID_MASK_COMMAND,
    AX25_SSID_MASK_LAST_ADDRESS,
    AX25_SSID_MASK_RESERVED,
    AX25_SSID_MASK_SSID,
    AX25_SSID_SHIFT_RESERVED,
    AX25_SSID_SHIFT_SSID,
)
from pax25.ax25.exceptions import DisassemblyError


@dataclass(frozen=True, kw_only=True)
class Ax25Address:
    """
    Address information used for connections.
    """

    name: str
    ssid: int = 0

    def __init__(self, name: str, ssid: int) -> None:
        """
        Force both values to be uppercase.
        """
        # We use the raw __setattr__ on object because this
        # is a frozen class and will not support direct assignment.
        object.__setattr__(self, "name", name.upper()[:AX25_ADDR_SIZE].strip())
        object.__setattr__(self, "ssid", ssid)

    def __len__(self) -> int:
        """
        Length, in bytes, of this structure when assembled.
        """
        return AX25_ADDR_SIZE

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Instantiate an Ax25Address from bytes. Will fail if the length of
        bytes is not precisely correct. Ignores flags on the SSID byte.
        """

        if len(data) != AX25_ADDR_SIZE:
            raise DisassemblyError(
                f"Address of incorrect length. Expected {AX25_ADDR_SIZE}, "
                f"got {len(data)} ({data!r})"
            )
        ssid = int((data[-1] & AX25_SSID_MASK_SSID) >> AX25_SSID_SHIFT_SSID)
        array = bytearray(data)
        # Addresses may only be valid ASCII values for upper-case letters or numbers.
        for i in range(0, AX25_ADDR_SIZE - 1):
            array[i] >>= 1
            if not (array[i] == 32 or (48 <= array[i] <= 57) or (65 <= array[i] <= 90)):
                raise DisassemblyError(f"ERROR: Corrupt address field: {array}")
        # ...But we decode as utf-8 so we don't end up with type errors later.
        name = array[: AX25_ADDR_SIZE - 1].decode("utf-8")
        return cls(name=name, ssid=ssid)

    def assemble(self) -> bytes:
        """
        Takes the address and serializes it to a byte array.
        """
        data = bytearray()
        name = self.name.ljust(AX25_ADDR_SIZE - 1)
        data += bytes(name, AX25_CODEPAGE)
        for i in range(0, AX25_ADDR_SIZE - 1):
            data[i] <<= 1
        ssid_byte = 0
        ssid_byte = ssid_byte | (self.ssid << AX25_SSID_SHIFT_SSID)
        data += ssid_byte.to_bytes(1, AX25_ENDIAN)
        return bytes(data)

    @classmethod
    def from_string(cls, data: str) -> Self:
        """
        Given a standard address string, create an Address. Address strings look like:
        KW6FOX
        K1LEO-3
        FOXBOX
        """
        if not data:
            raise ValueError("Empty strings are not valid addresses.")
        segments = data.split("-", 2)
        name = segments[0]
        ssid = 0
        if len(segments) == 2:
            try:
                ssid = int(segments[1])
            except ValueError as error:
                raise ValueError(f"Not a valid SSID: {repr(ssid)}") from error
        return cls(name=name, ssid=ssid)

    def __str__(self) -> str:
        """
        Form to string representation.
        """
        if self.ssid == 0:
            return self.name
        return f"{self.name}-{self.ssid}"


@dataclass(frozen=True, kw_only=True)
class Ax25AddressHeader:
    """
    Address with metadata.
    """

    address: Ax25Address
    # These reserved bits are collected, but we don't have any particular use for them.
    # They can be used by a network for whatever purpose it deems useful.
    reserved: int = 3
    command_or_repeated: bool = False

    def __len__(self) -> int:
        """
        Length, in bytes, of this structure when assembled.
        """
        return AX25_ADDR_SIZE

    def __str__(self) -> str:
        string = str(self.address)
        if self.command_or_repeated:
            string += "*"
        if self.reserved != 3:
            string += f"(R{self.reserved})"
        return string

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Instantiate an Ax25AddressHeader from bytes. Will fail if the length of
        bytes is not precisely correct.
        """
        address = Ax25Address.disassemble(data)
        flags = data[-1]
        reserved = (flags & AX25_SSID_MASK_RESERVED) >> AX25_SSID_SHIFT_RESERVED
        command = bool(flags & AX25_SSID_MASK_COMMAND)
        return cls(
            address=address,
            reserved=reserved,
            command_or_repeated=command,
        )

    def assemble(self) -> bytes:
        """
        Assemble the Ax25AddressHeader into bytes suitable for transmission.
        """
        data = self.address.assemble()
        # Add bitmask to set the ch flag as necessary on the last byte.
        ssid_byte = data[-1]
        data = data[:-1]
        ssid_byte |= self.reserved << AX25_SSID_SHIFT_RESERVED
        ssid_byte |= self.command_or_repeated and AX25_SSID_MASK_COMMAND
        data += ssid_byte.to_bytes(1, AX25_ENDIAN)
        return data


def is_last_address(byte: int) -> int:
    """
    Get the value of the ext flag from the address flags mask.
    """
    return bool(byte & AX25_SSID_MASK_LAST_ADDRESS)


@dataclass(frozen=True, kw_only=True)
class Ax25RoutePath:
    """
    Specification for a packet's intended route of traffic-- its source,
    its destination, and what digipeaters lay between.
    """

    src: Ax25AddressHeader
    dest: Ax25AddressHeader
    digipeaters: tuple[Ax25AddressHeader, ...] = tuple()

    def __len__(self) -> int:
        """
        Length, in bytes, of this structure when assembled.
        """
        return (2 + len(self.digipeaters)) * AX25_ADDR_SIZE

    def __str__(self) -> str:
        """
        Represents a route path for a frame in string form. Will add a * to the last
        repeater which has repeated the frame.
        """
        digi_section = ""
        if self.digipeaters:
            digi_section = ","
            digi_strings = []
            last_repeated_index = None
            for index, digi in enumerate(self.digipeaters):
                digi_strings.append(str(digi.address))
                if digi.command_or_repeated:
                    last_repeated_index = index
            if last_repeated_index is not None:
                digi_strings[last_repeated_index] += "*"
            digi_section += ",".join(digi_strings) + "/V"
        return "".join(
            [
                str(self.src.address),
                ">",
                str(self.dest.address),
                digi_section,
            ]
        )

    @classmethod
    def disassemble(cls, data: bytes) -> Self:
        """
        Instantiate a route path from a data byte array. If there is leftover data,
        it will be ignored.
        """
        dest_bytes = data[:AX25_ADDR_SIZE]
        dest = Ax25AddressHeader.disassemble(dest_bytes)
        data = data[AX25_ADDR_SIZE:]
        src_bytes = data[:AX25_ADDR_SIZE]
        src = Ax25AddressHeader.disassemble(src_bytes)
        last_address = is_last_address(src_bytes[-1])
        data = data[AX25_ADDR_SIZE:]
        digipeaters = []
        while len(data) and not last_address:
            digipeater_bytes = data[:AX25_ADDR_SIZE]
            digipeater = Ax25AddressHeader.disassemble(digipeater_bytes)
            last_address = is_last_address(digipeater_bytes[-1])
            digipeaters.append(digipeater)
            data = data[AX25_ADDR_SIZE:]
        if len(digipeaters) > 8:
            raise DisassemblyError(
                f"Too many digipeaters specified. Maximum is 8. Received: {digipeaters}"
            )
        return cls(src=src, dest=dest, digipeaters=tuple(digipeaters))

    def assemble(self) -> bytes:
        """
        Assemble the route path into a byte array.
        """
        data = bytearray()
        to_join = (self.dest, self.src) + self.digipeaters
        for item in to_join:
            data.extend(item.assemble())
        # The 'last_address' flag must be set on the last address in the set to indicate
        # no further addresses are forthcoming.
        ssid_byte = int(data.pop())
        ssid_byte |= 1
        return bytes(data) + ssid_byte.to_bytes(1, AX25_ENDIAN)
