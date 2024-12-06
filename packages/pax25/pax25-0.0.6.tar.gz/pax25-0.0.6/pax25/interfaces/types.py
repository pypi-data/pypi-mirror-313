"""
Defines types used by interfaces.
"""

from typing import TYPE_CHECKING, Any, Generic, Literal, TypedDict, TypeVar

from pax25.types import EmptyDict, Frame

if TYPE_CHECKING:
    from pax25.station import Station


S = TypeVar("S", bound=dict[str, Any] | EmptyDict)


class Interface(Generic[S]):
    """
    The interface base class, which defines the required functions for an interface.
    All the actual functions must be defined on the subclass-- this base class
    just raises NotImplementedError for all of them.

    Attributes:
        listening: bool flag to indicate whether the interface is up and
            listening for packets.
        name: str name of the interface as instantiated, for internal reference.
        settings: S, a settings dictionary for the interface.
        station: Station the interface is initialized for.
        sudo: Whether this interface can be used for superuser connections.
    """

    listening: bool = False
    name: str
    settings: S
    station: "Station"
    sudo: bool = False

    def __init__(self, name: str, settings: S, station: "Station"):
        """
        Initialize the interface. The interface will be initialized with
        its name, settings, and the station it is being initialized for.

        Under what conditions to set sudo is up to you, but it is set to False by
        default. The sudo flag indicates whether this interface can be used for
        superuser connections.

        It does not automatically mean that connections on this interface will be
        treated as superuser connections, but the base Application class will consider
        a user a superuser if they are connected to an interface while its sudo flag is
        True, and their name matches the station's default name.
        """
        raise NotImplementedError

    async def send_frame(self, frame: Frame) -> None:
        """
        Send an addressed frame through the interface.
        """
        raise NotImplementedError

    async def read_loop(self) -> None:
        """
        Interfaces should implement a read loop. The read loop is the async read
        loop that pulls in from the relevent stream, be it a socket, a file, a
        pipe, or whatever.
        """
        raise NotImplementedError

    async def shutdown(self) -> None:
        """
        This handles any cleanup needed to bring this interface offline, and then
        allows the read_loop to end. This is usually done by setting the listening
        attribute on the instance to False, so that it closes out next opportunity.

        See inheriting classes for examples.
        """
        raise NotImplementedError


class FileSettings(TypedDict, total=False):
    """
    Settings for the file input.
    """

    input: str
    output: str
    source_name: str
    source_ssid: int
    destination_name: str
    destination_ssid: int
    auto_shutdown: bool
    # If auto_shutdown is True, also closes the event loop after shutdown.
    stop_loop: bool
    sudo: bool


class FileInterfaceConfig(TypedDict):
    """
    Configuration for file interface.
    """

    type: Literal["file"]
    settings: FileSettings


class DummyInterfaceConfig(TypedDict):
    """
    Configuration for dummy interface.
    """

    type: Literal["dummy"]
    settings: FileSettings


# Type used for tracking the tty settings we manipulate when we use stdin.
TerminalSettings = list[int | list[bytes | int]]
