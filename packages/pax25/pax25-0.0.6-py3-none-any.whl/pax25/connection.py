"""
Connections handle state and method for connections between two stations (or,
in some cases, one part of a station to another part of itself). They are
instantiated by the frame queue, and then handed to applications for
manipulation.
"""

from io import BytesIO
from typing import TYPE_CHECKING, Any, List, Optional

from pax25.ax25.address import Ax25Address
from pax25.types import ConnectionStats, DisconnectFrame

if TYPE_CHECKING:
    from pax25.applications import BaseApplication
    from pax25.interfaces import Interface
    from pax25.station import Station


class Connection:
    """
    Connections handle state and configuration for a virtual circuit between
    stations.

    It is important to note that a connection could be loopback, which informs
    some design here.

    If sudo is True, signals to applications that this connection is safe to assume
    as a superuser if the connected name matches the station name.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        first_party: Ax25Address,
        first_party_interface: "Interface[Any]",
        second_party: Ax25Address,
        second_party_interface: "Interface[Any]",
        application: Optional["BaseApplication[Any]"],
        station: "Station",
        sudo: bool = False,
    ):
        # The party that initializes the connection is the first party.
        self.first_party = first_party
        self.first_party_interface = first_party_interface
        # The party that receives the initial connection request is the second party.
        self.second_party = second_party
        self.second_party_interface = second_party_interface
        self.receive_buffer = BytesIO()
        self.send_buffer = BytesIO()
        self.application_stack: List[BaseApplication[Any]] = (
            [application] if application else []
        )
        self.sudo = sudo
        self.proxy_application = application
        self.station = station
        self.closed = False
        self.counters = {
            "tx_bytes": 0,
            "rx_bytes": 0,
        }

    def __hash__(self) -> int:
        """
        There should only ever be one connection between two parties on one station.
        So, we can use these properties as the hash for this object, allowing us to
        safely use it as a dictionary key or in a set.
        """
        return hash(
            (hash(self.first_party), hash(self.second_party), hash(self.station))
        )

    def interface_for(self, party: Ax25Address) -> "Interface[Any]":
        """
        Given one of the parties, return the interface they are listening on.
        """
        if party == self.first_party:
            return self.first_party_interface
        if party == self.second_party:
            return self.second_party_interface
        raise RuntimeError(f"{party} is not party to this connection!")

    async def close(self) -> None:
        """
        Sends a disconnection frame.
        """
        self.closed = True
        await self.station.frame_queue.process_frame(
            self.second_party_interface,
            DisconnectFrame(
                source=self.second_party,
                destination=self.first_party,
            ),
        )

    @property
    def stats(self) -> ConnectionStats:
        """
        Produces metrics about this connection.

        These metrics are currently empty and not used, but when the functions
        which enable them to be used are implemented, they will be populated,
        and this property should be added to the documentation.
        """
        return {
            "transmitted_bytes": self.counters["tx_bytes"],
            "received_bytes": self.counters["rx_bytes"],
            "receive_buffer_length": self.receive_buffer.getbuffer().nbytes,
            "send_buffer_length": self.send_buffer.getbuffer().nbytes,
        }
