"""
Dummy interface. No configuration, ignores everything. Used for tests.
"""

from typing import TYPE_CHECKING

from pax25.types import EmptyDict, Frame

from .types import Interface

if TYPE_CHECKING:
    from ..station import Station


class DummyInterface(Interface[EmptyDict]):
    """
    Dummy interface for testing.
    """

    def __init__(self, name: str, settings: EmptyDict, station: "Station"):
        """
        Just stash the args but don't do anything with them.
        """
        self.name = name
        self.settings = settings
        self.station = station
        self.listening = False

    async def send_frame(self, frame: Frame) -> None:
        """
        Dummy send frame function.
        """

    async def read_loop(self) -> None:
        """
        Dummy read loop function. Probably won't be an issue if it just returns
        immediately.
        """
        self.listening = True

    async def shutdown(self) -> None:
        """
        Dummy shut down function.
        """
        self.listening = False
