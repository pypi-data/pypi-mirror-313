"""
Module for the Application class, used for creating all applications.
"""

import sys
from typing import TYPE_CHECKING

from pax25.types import MessageFrame

from .types import BaseApplication, BasicStateTable, S

if TYPE_CHECKING:
    from pax25.connection import Connection
    from pax25.station import Station


class Application(BaseApplication[S]):
    """
    The Application class. You should inherit from this class to create your own custom
    pax25 apps.
    """

    def __init__(self, *, name: str, proxy: bool, station: "Station", settings: S):
        self.name = name
        self.proxy = proxy
        self.settings = settings
        self.connection_state_table: BasicStateTable = {}
        self.station = station
        self.setup()

    def setup(self) -> None:
        """
        Perform any initial state configuration for your application in this
        function.
        """

    def is_admin(self, connection: "Connection") -> bool:
        """
        Check if the current user is an admin.
        """
        return connection.sudo and connection.first_party.name == self.station.name

    async def on_connect(self, connection: "Connection") -> None:
        """
        Called when a new connection is established.
        """
        self.connection_state_table[connection] = {"command": b""}
        await self.on_startup(connection)

    async def on_startup(self, connection: "Connection") -> None:
        """
        Run right after a new connection is established. You can use this function to
        do any initial state configuration and/or send a welcome message.
        """

    async def on_disconnect(self, connection: "Connection") -> None:
        """
        Run when a connection is being dropped.
        """
        await self.on_shutdown(connection)
        del self.connection_state_table[connection]

    async def on_shutdown(self, connection: "Connection") -> None:
        """
        Called when a connection is being disconnected. Perform any cleanup here.
        """

    async def on_message(self, connection: "Connection", message: str) -> None:
        """
        Called when a message is received. By default, this is called by
        on_bytes when it detects a carriage return has been sent.
        """

    async def on_bytes(
        self,
        connection: "Connection",
        bytes_received: bytes,
    ) -> None:
        """
        Called when bytes are received from a connection for this application. You
        usually don't want to call this directly, but you might need to if you need
        to control how bytes sent from the client are handled.
        """
        # Not sure how often we'll receive packets with carriage returns in the
        # middle of them, but for most applications that should indicate the
        # end of one command and the start of another, so we break them up here.
        for raw_int in bytes_received:
            # Iterating over bytes produces ints.
            byte = raw_int.to_bytes(1, sys.byteorder)
            match byte:
                case b"\n":
                    current_message = (
                        self.connection_state_table[connection]["command"] + byte
                    ).decode("utf-8")
                    # Clear the command before sending the message in case there's an
                    # exception.
                    self.connection_state_table[connection]["command"] = b""
                    await self.on_message(
                        connection,
                        # Remove trailing newline.
                        current_message[:-1],
                    )
                # Backspace
                case b"\x7f":
                    current_string = self.connection_state_table[connection][
                        "command"
                    ].decode("utf-8")
                    self.connection_state_table[connection]["command"] = current_string[
                        :-1
                    ].encode("utf-8")
                case _:
                    self.connection_state_table[connection]["command"] += byte

    async def send_message(
        self, connection: "Connection", message: str, append_newline: bool = True
    ) -> None:
        """
        Call to send a message string to a particular connection.
        """
        if append_newline:
            message += "\n"
        await self.send_bytes(connection, message.encode("utf-8"))

    async def send_bytes(self, connection: "Connection", bytes_to_send: bytes) -> None:
        """
        Call to send bytes to a particular connection. You will usually want to call
        send_message instead. You might use this function if you need to control
        precisely what bytes are sent to the client.
        """
        await self.station.frame_queue.process_frame(
            None,
            MessageFrame(
                source=connection.second_party,
                destination=connection.first_party,
                payload={"bytes": bytes_to_send, "outbound": True},
            ),
        )
