"""
The frame queue takes frames from the interfaces and sends them to their intended
second_party.

Some things the frame queue may handle are:

1. Creating Connection objects and attaching them to applications
2. Message forwarding
3. Beacon processing
4. Digipeating
"""

from typing import TYPE_CHECKING, Any, Optional, Tuple, cast

from pax25.ax25.address import Ax25Address
from pax25.connection import Connection
from pax25.exceptions import ConfigurationError
from pax25.types import (
    BeaconFrame,
    ConnectFrame,
    DisconnectFrame,
    Frame,
    HeartbeatFrame,
    MessageFrame,
)

if TYPE_CHECKING:
    from pax25.interfaces import Interface
    from pax25.station import Station


class FrameQueue:
    """
    The Frame queue is a sort of router. It takes in frames from the varying interfaces
    and makes sure they go to their proper destination, whether that be an existing
    connection object or re-transcribed and sent out to another interface.
    """

    def __init__(self, *, station: "Station"):
        self.station = station
        # We map the stations we hear to the interfaces we know them to be on.
        # It is possible that we might hear a station on multiple interfaces,
        # but we're ignoring that for now.
        self.known_stations: dict[Ax25Address, set[Interface[Any]]] = {}
        self.connections: dict[Tuple[Ax25Address, Ax25Address], Connection] = {}

    async def process_frame(
        self, interface: Optional["Interface[Any]"], frame: Frame
    ) -> None:
        """
        Interfaces call this function to put a new frame in the queue.
        """
        match frame.command:
            case "connect":
                frame = cast(ConnectFrame, frame)
                assert interface, "Interface not specified for connection!"
                await self.connect_handler(interface, frame)
            case "disconnect":
                frame = cast(DisconnectFrame, frame)
                assert interface, "Interface not specified for disconnection!"
                await self.disconnect_handler(interface, frame)
            case "heartbeat":
                frame = cast(HeartbeatFrame, frame)
                await self.heartbeat_handler(frame)
            case "message":
                frame = cast(MessageFrame, frame)
                await self.message_handler(frame)
            case "beacon":
                frame = cast(BeaconFrame, frame)
                assert interface, "Beacon frame received without a source interface."
                await self.beacon_handler(interface, frame)
            case _:
                await self.not_implemented_handler(interface, frame)

    def get_connection(
        self, frame: Frame, disconnecting: bool = False
    ) -> Optional[Connection]:
        """
        Gets the connection, should it exist, for a frame.
        """
        connection = self.connections.get(
            (frame.source, frame.destination),
            self.connections.get((frame.destination, frame.source), None),
        )
        if connection and (connection.closed and not disconnecting):
            return None
        return connection

    def next_ssid(
        self,
        *,
        name: str,
        interface: "Interface[Any]",
        ssid: Optional[int] = None,
    ) -> int:
        """
        Given a station name and an interface, produces the next SSID.

        You can give an ssid you would prefer by specifying the ssid argument. If the
        ssid already exists or is invalid, throws an exception. This function is
        used primarily by the station in order to assign SSIDs to applications.
        """
        name = name.upper()
        ssids: set[int] = set()
        for address, interfaces in self.known_stations.items():
            if address.name != name:
                continue
            if interface in interfaces:
                ssids |= {address.ssid}
        if ssid is None:
            for candidate in range(16):
                if candidate not in ssids:
                    ssid = candidate
                    break
            else:
                raise ConfigurationError(
                    f"All valid SSIDs on {name}, interface {interface} are taken! "
                    "You may have at most 16 SSIDs, numbered 0-15."
                )
        if not 0 <= ssid <= 15:
            raise ConfigurationError("SSID must be between 0 and 15.")
        if ssid in ssids:
            raise ConfigurationError(
                f"SSID {repr(ssid)} already registered on {interface}!"
            )
        return ssid

    def register_station(
        self, *, interface: "Interface[Any]", address: Ax25Address
    ) -> None:
        """
        Registers an address as existing on a particular interface. It can then be
        looked up later for making connections.
        """
        self.known_stations[address] = self.known_stations.get(address, set()) | {
            interface
        }

    def interface_for_address(
        self, source_interface: "Interface[Any]", address: Ax25Address
    ) -> Optional["Interface[Any]"]:
        """
        Given a contacting interface, and an address, returns the optimal interface
        for connecting to the target station. It always tries the source interface
        first, followed by other known interfaces in priority order.
        """
        candidate_interfaces = self.known_stations.get(address, None)
        if not candidate_interfaces:
            return None
        if source_interface in candidate_interfaces:
            return source_interface
        # In recent versions of Pythons, dictionaries remember key definition order.
        # We defer to first defined interfaces as priority ones for connection.
        for interface in self.station.interfaces.values():
            if interface in candidate_interfaces:
                return interface
        return None

    async def connect_handler(
        self,
        source_interface: "Interface[Any]",
        frame: ConnectFrame,
    ) -> None:
        """Handles frames with connection requests."""
        try:
            application = self.station.application_map[source_interface.name][
                frame.destination
            ][0]
        except IndexError as exc:
            name = frame.destination.name
            interface = source_interface.name
            raise ConnectionError(
                f"Connection request made to {name} on {interface}, which has no "
                "configured application!",
            ) from exc
        connection = self.get_connection(frame)
        if connection:
            # In the future, we'll send a new acknowledgement packet.
            raise ConnectionError("Received duplicate connection request.")
        destination_interface = self.interface_for_address(
            source_interface, frame.destination
        )
        if not destination_interface:
            # We would send back some kind of error frame here, normally.
            raise ConnectionError("Received connection request for unknown station.")
        if not connection:
            connection = Connection(
                application=application,
                first_party=frame.source,
                first_party_interface=source_interface,
                second_party=frame.destination,
                second_party_interface=destination_interface,
                station=self.station,
                sudo=source_interface.sudo,
            )
            self.connections[(frame.source, frame.destination)] = connection
            await application.on_connect(connection)

    async def disconnect_handler(
        self,
        _source_interface: "Interface[Any]",
        frame: DisconnectFrame,
    ) -> None:
        """Handles frames with disconnection requests."""
        connection = self.get_connection(frame, disconnecting=True)
        if not connection:
            # May just ignore this in the future, but it's diagnostic for now.
            raise ConnectionError("Received message frame for bogus disconnection!")
        if connection.proxy_application:
            await connection.proxy_application.on_disconnect(connection)
        await connection.interface_for(frame.destination).send_frame(frame)

    async def heartbeat_handler(
        self,
        frame: HeartbeatFrame,
    ) -> None:
        """Handles frames with heartbeat instructions."""

    async def beacon_handler(
        self,
        source_interface: "Interface[Any]",
        frame: BeaconFrame,
    ) -> None:
        """Handles frames with heartbeat instructions."""
        self.register_station(interface=source_interface, address=frame.source)

    async def message_handler(
        self,
        frame: MessageFrame,
    ) -> None:
        """Handles frames that contain message bytes."""
        connection = self.get_connection(frame)
        if not connection:
            return
        if (
            connection.first_party == frame.source
            and connection.proxy_application
            and not frame.payload["outbound"]
        ):
            # We're the ones being connected to, and this message is to be handled
            # by the running application.
            await connection.proxy_application.on_bytes(
                connection,
                frame.payload["bytes"],
            )
            return
        await connection.interface_for(frame.destination).send_frame(frame)

    async def not_implemented_handler(
        self,
        source_interface: "Interface[Any]",
        frame: Frame,
    ) -> None:
        """
        Performs a default action when receiving an unrecognized command.
        """
