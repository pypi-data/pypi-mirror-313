"""
Types for applications.
"""

from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar

if TYPE_CHECKING:
    from pax25.connection import Connection
    from pax25.station import Station


S = TypeVar("S")


class BaseApplication(Generic[S]):
    """
    Raw BaseApplication that implements the minimum contract that Connection and
    the FrameQueue expect. In most cases you will not want to inherit from this, but
    from Application instead.
    """

    settings: S

    def __init__(self, *, name: str, proxy: bool, station: "Station", settings: S):
        """
        Initialize a copy of this application. Usually you want to store
        the settings and whether this is being invoked as a proxy object.
        """
        raise NotImplementedError

    async def on_connect(self, connection: "Connection") -> None:
        """
        Called when a new connection is established. For instance, if we need to store
        any state for the user's session, we'd set it here. You might also send a
        welcome message.
        """

    async def on_disconnect(self, connection: "Connection") -> None:
        """
        Called when a connection is being disconnected. Perform any cleanup here.
        """

    async def on_bytes(self, connection: "Connection", bytes_received: bytes) -> None:
        """
        Called when bytes are received from a connection for this application.
        """

    async def send_bytes(self, connection: "Connection", bytes_to_send: bytes) -> None:
        """
        Call to send bytes to a particular connection.
        """


class BasicApplicationState(TypedDict):
    """
    State for the Application.
    """

    command: bytes


BasicStateTable = dict["Connection", BasicApplicationState]
