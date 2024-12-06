"""
Utility functions for working with AX.25 Frames.
"""

from dataclasses import replace

from pax25.ax25.address import Ax25Address, Ax25AddressHeader
from pax25.ax25.frame import Ax25Frame


def should_repeat_for(address: Ax25Address, frame: Ax25Frame) -> bool:
    """
    Checks if a given address is in the digipeater list and this frame requires
    repeating.
    """
    for envelope in frame.route.digipeaters:
        if envelope.address == address and not envelope.command_or_repeated:
            return True
    return False


def repeated_for(address: Ax25Address, frame: Ax25Frame) -> Ax25Frame:
    """
    Returns a revised frame with the repeat flag set for the specific address.
    Raises if this address isn't a repeater for the frame.
    """
    digipeater_list = list(frame.route.digipeaters)
    address_seen = False
    for index, envelope in enumerate(digipeater_list):
        if not envelope.address == address:
            continue
        address_seen = True
        if not envelope.command_or_repeated:
            new_envelope = replace(envelope, command_or_repeated=True)
            digipeater_list[index] = new_envelope
            new_route = replace(frame.route, digipeaters=tuple(digipeater_list))
            return replace(frame, route=new_route)
    if address_seen:
        raise ValueError(
            f"{address} is in the digipeater list, "
            f"but all occurrences are marked repeated.",
        )
    raise ValueError(f"{address} is not a digipeater for {frame}.")


def reply_digipeaters(
    digipeaters: tuple[Ax25AddressHeader, ...]
) -> tuple[Ax25AddressHeader, ...]:
    """
    Returns a revised frame that has the digipeaters in reverse order and the repeated
    flags all set to False.
    """
    revised_digipeaters = [
        replace(envelope, command_or_repeated=False)
        for envelope in reversed(digipeaters)
    ]
    if revised_digipeaters:
        revised_digipeaters[-1] = replace(revised_digipeaters[-1])
    return tuple(revised_digipeaters)


def response_frame(frame: Ax25Frame) -> Ax25Frame:
    """
    Generates the base of a response frame-- source and destination are swapped,
    digipeaters reversed, and contents emptied. The control is unchanged, as context
    for changes to it would be kept elsewhere.

    The command_or_repeated flag is swapped along with the addresses
    (if it is set at all), so bear this in mind.
    """
    route = frame.route
    route = replace(
        route,
        src=route.dest,
        dest=route.src,
        digipeaters=reply_digipeaters(route.digipeaters),
    )
    return replace(frame, route=route, info=b"")
