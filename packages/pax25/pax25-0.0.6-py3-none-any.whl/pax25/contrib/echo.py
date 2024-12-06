"""
Echo application. Echoes back whatever you send to it.
"""

from pax25.applications import Application
from pax25.connection import Connection
from pax25.types import EmptyDict


class Echo(Application[EmptyDict]):
    """
    Echo application.
    """

    async def on_message(self, connection: "Connection", message: str) -> None:
        """
        Immediately redirect a received message back to the user.
        """
        await self.send_message(connection, message)
