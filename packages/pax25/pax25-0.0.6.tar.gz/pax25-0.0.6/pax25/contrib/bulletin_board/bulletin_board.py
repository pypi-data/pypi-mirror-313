"""
Main application module of the contributed bulletin board system.
"""

import json
import os
import random
import string
from asyncio import Lock
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Literal, cast

from pax25 import Application
from pax25.connection import Connection
from pax25.contrib.bulletin_board.types import (
    BoardConnections,
    BoardSettings,
    BoardState,
    Message,
    ReaderState,
)
from pax25.utils import async_wrap

DEFAULT_MAX_LENGTH = 5000
DEFAULT_SLOTS = 100


def message_headers(message: Message) -> str:
    """
    Format the main headers of a message.
    """
    created_on = (
        str(datetime.fromisoformat(message["created_on"]).strftime("%d/%m/%Y %H:%M:%S"))
        + " "
    )
    to_callsign = f'{message["to_callsign"]}'.ljust(7, " ")
    from_callsign = f'{message["from_callsign"]}'.ljust(7, " ")
    return f"{created_on}{to_callsign}{from_callsign}"


def is_party(name: str, message: Message) -> bool:
    """
    Checks if a name (callsign) is party to a message.
    """
    return any(
        (
            message["from_callsign"] == name,
            message["to_callsign"] == name,
        )
    )


def message_preview(message: Message) -> str:
    """
    Create a message preview string, like what would be used in message listings.
    """
    id_text = f'{message["id"]}'.ljust(4, " ")
    status_text = "R" if message["read"] else "U"
    status_text += "!" if message["private"] else ""
    status_text = status_text.ljust(6, " ")
    message_size = len(message["body"].encode("utf-8")) + len(
        message["subject"].encode("utf-8")
    )
    size = str(f"{message_size}").ljust(5, " ")
    headers = message_headers(message)
    subject_snippet = message["subject"][:30]
    return f"{id_text}{status_text}{size}{headers}{subject_snippet}"


class BulletinBoard(
    Application[BoardSettings]
):  # pylint: disable=too-many-public-methods
    """
    A Personal Bulletin Board System (PBBS) application.

    The bulletin board has the ability to persist its data to disk. By default,
    it will store its data in the current working directory, but the storage file can
    be customized.
    """

    version_string = "[PAX25-PBBS-0.1.0]"

    board_state: BoardState
    connections: BoardConnections
    _next_id = 1
    _save_lock: Lock

    def setup(self) -> None:
        """
        Set up the basic state of the bulletin board system.
        """
        self.connections = {}
        self._save_lock = Lock()
        self.board_state = self.load_board_state()

    @property
    def save_file_path(self) -> Path:
        """Get the path to the board's save file."""
        return Path(self.settings.get("save_file_path", "board.json"))

    @property
    def welcome_message(self) -> str:
        """Get the welcome message for the board."""
        welcome_message = self.settings.get("welcome_message") or ""
        if welcome_message:
            welcome_message += "\n"
        return welcome_message

    def load_board_state(self) -> BoardState:
        """
        Load the board's state from the file path specified in the settings.
        """
        if not self.save_file_path.is_file():
            return BoardState(messages={}, version=self.version_string)
        with open(self.save_file_path, "r", encoding="utf-8") as save_file:
            struct = json.load(save_file)
            loaded_state = cast(BoardState, struct)
            return loaded_state

    @property
    def next_id(self) -> int:
        """
        Get the next available board message ID. We recycle board IDs since
        we could be running for a very long time, and we have space to burn.
        """
        if str(self._next_id) not in self.board_state["messages"]:
            return self._next_id
        while str(self._next_id) in self.board_state["messages"]:
            self._next_id += 1
        return self._next_id

    def save_board_state(self) -> None:
        """
        Persist the board's state to disk. First write to a temporary file, then
        overwrite the original. This way we can revert to backup if we fail mid-dump.

        Don't call this directly. Await .save() instead.
        """
        cookie = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        tmp_path = self.save_file_path.with_suffix(f".{cookie}.tmp")
        with open(tmp_path, "w", encoding="utf-8") as tmp_file:
            json.dump(
                self.board_state,
                tmp_file,
                indent=2 if self.settings.get("debug", False) else None,
            )
        os.replace(tmp_path, self.save_file_path)

    async def save(self) -> None:
        """
        Locks the db for save and saves it in an awaitable manner.
        """
        async with self._save_lock:
            await async_wrap(self.save_board_state)()

    def reset_state(self, connection: Connection) -> None:
        """
        Set the user's state to a blank default-- puts them to the home mode.
        """
        self.connections[connection] = ReaderState(
            mode="home",
            body="",
            subject="",
            to_callsign="",
            private=False,
        )

    async def on_startup(self, connection: Connection) -> None:
        """Set up the user's connection state and greet them."""
        self.reset_state(connection)
        callsign = connection.first_party.name
        unread_count = len(
            [
                message
                for message in self.board_state["messages"].values()
                if message["to_callsign"] == callsign and not message["read"]
            ]
        )
        unread_segment = ""
        if unread_count:
            plural = "s" if unread_count != 1 else ""
            unread_segment = f"\nYou have {unread_count} unread message{plural}."
        slots_status = ""
        slots = self.settings.get("slots", DEFAULT_SLOTS)
        if slots is not None:
            remaining = max(0, slots - len(self.board_state["messages"]))
            plural = "s" if slots != 1 else ""
            slots_status = f"\n{remaining} of {slots} message slot{plural} available."
        greeting = (
            f"{self.version_string}{self.welcome_message}"
            f"{unread_segment}{slots_status}"
        )
        await self.send_message(connection, greeting)
        await self.send_prompt(connection)

    async def on_shutdown(self, connection: Connection) -> None:
        """Clear the user's connection state."""
        del self.connections[connection]

    async def send_prompt(self, connection: Connection) -> None:
        """
        Send the command prompt.
        """
        await self.send_message(connection, "B,L,K,R,S, H(elp) or I(nfo) >")

    async def handle_body_line(
        self, connection: Connection, state: ReaderState, message: str
    ) -> None:
        """Handle input when composing a message body."""
        # Default maximum message length is 5000 characters.
        size_limit = self.settings.get("max_message_length", DEFAULT_MAX_LENGTH)
        if message.rstrip() != "/EX":
            state.body += message + "\n"
            if size_limit is not None:
                state.body = state.body[:size_limit]
                if len(state.body) >= size_limit:
                    await self.send_message(
                        connection,
                        "Message body size limit reached. Type /EX to exit.",
                    )
                    return
            return
        self.board_state["messages"][str(self.next_id)] = Message(
            id=self.next_id,
            to_callsign=state.to_callsign,
            from_callsign=connection.first_party.name,
            subject=state.subject,
            body=state.body,
            created_on=datetime.now(timezone.utc).astimezone().isoformat(),
            read=False,
            private=state.private,
        )
        await self.save()
        self.reset_state(connection)
        await self.send_message(connection, "Message saved.")
        await self.send_prompt(connection)

    async def send_listing(
        self, connection: Connection, messages: Iterable[Message]
    ) -> None:
        """
        Given a list of messages, send all of them to the client.
        """
        # May be a generator. Resolve, in that case, so we can check for emptiness.
        messages = list(messages)
        if not messages:
            await self.send_message(connection, "No messages available.")
            return
        await self.send_message(
            connection,
            "ID# Flags Size Date        Time     To     From   Subject",
        )
        await self.send_message(
            connection,
            "\n".join([message_preview(message) for message in messages]),
        )

    async def list_mine(self, connection: Connection) -> None:
        """
        List all messages addressed to the current user.
        """
        await self.send_listing(
            connection,
            [
                message
                for message in reversed(self.board_state["messages"].values())
                if message["to_callsign"] == connection.first_party.name
            ],
        )

    def can_read(self, connection: Connection, message: Message) -> bool:
        """
        Determines if a connected user has the right to read this message.
        """
        if self.is_admin(connection):
            return True
        if not message["private"]:
            return True
        return is_party(connection.first_party.name, message)

    def readable(self, connection: Connection) -> Iterable[Message]:
        """
        Yields all messages which can be read by a connected user.
        """
        for message in reversed(self.board_state["messages"].values()):
            if self.can_read(connection, message):
                yield message

    async def list_messages(self, connection: Connection, args: list[str]) -> None:
        """
        List messages.
        """

        match args:
            case []:
                await self.send_listing(
                    connection,
                    self.readable(connection),
                )
            case [direction, callsign] if direction in ("<", ">"):
                attr: Literal["from_callsign", "to_callsign"]
                if direction == "<":
                    attr = "from_callsign"
                else:
                    attr = "to_callsign"
                await self.send_listing(
                    connection,
                    [
                        message
                        for message in self.readable(connection)
                        if message[attr] == callsign.upper()
                    ],
                )
            case _:
                await self.send_message(
                    connection,
                    "L[ist] takes either no arguments, or a direction "
                    "(> or <) and a callsign.",
                )

    async def read_mine(self, connection: Connection) -> None:
        """
        Read all messages addressed to the current user.
        """
        messages = [
            message
            for message in reversed(self.board_state["messages"].values())
            if message["to_callsign"] == connection.first_party.name
            and not message["read"]
        ]
        for message in messages:
            await self.perform_read(connection, message, save=False)
        await self.save()

    async def perform_read(
        self, connection: Connection, message: Message, save: bool = True
    ) -> None:
        """
        Send a message to a user, and mark it read.
        """
        private_prefix = "!!PRIVATE!! " if message["private"] else ""
        body = message["body"]
        # Should always have a newline at the end.
        if body and body[-1] != "\n":
            body += "\n"
        await self.send_message(
            connection,
            f"ID#{message['id']} {message_headers(message)}\n{private_prefix}SUBJECT: "
            f'{message["subject"]}\n{body}',
            append_newline=False,
        )
        if message["to_callsign"] == connection.first_party.name:
            message["read"] = True
            if save:
                await self.save()

    async def read_message(self, connection: Connection, args: list[str]) -> None:
        """
        Read a given message ID
        """
        match args:
            case []:
                await self.send_message(
                    connection, "You must specify a message number."
                )
            case [number] if (
                number not in self.board_state["messages"]
            ) or not self.can_read(connection, self.board_state["messages"][number]):
                await self.send_message(
                    connection, f"Could not find message with ID {number}"
                )
            case [number]:
                message = self.board_state["messages"][number]
                await self.perform_read(connection, message)
            case _:
                await self.send_message(
                    connection, "R[ead] takes at most one argument, a message ID."
                )

    async def bye(self, connection: Connection) -> None:
        """
        Command for closing the connection.
        """
        await self.send_message(connection, "Goodbye!")
        await connection.close()

    async def compose_message(
        self,
        connection: Connection,
        args: list[str],
        private: bool = False,
    ) -> bool:
        """
        Compose a message. We'd call this function 'send' or 'send_message', but those
        are reserved by the parent class.

        More specifically, this starts the composition by changing the mode. The rest
        of the composition work is handled in on_message.
        """
        slots = self.settings.get("slots", DEFAULT_SLOTS)
        if slots is not None:
            if slots <= len(self.board_state["messages"]):
                await self.send_message(
                    connection,
                    "The message board is full. You cannot send any more messages.",
                )
                return False
        match args:
            case []:
                await self.send_message(
                    connection, "You must specify a callsign to send your message to."
                )
            case [callsign]:
                state = self.connections[connection]
                state.to_callsign = callsign.upper()
                state.mode = "subject"
                state.private = private
                await self.send_message(connection, "SUBJECT: ", append_newline=False)
                return True
            case _:
                await self.send_message(
                    connection, "[S]end must have at most one argument, a callsign."
                )
        return False

    async def kill_mine(self, connection: Connection) -> None:
        """
        Kills all read messages addressed to the current user.
        """
        count = 0
        lowest = self._next_id
        name = connection.first_party.name
        # Iterating over a coerced list here so that we're not modifying the dictionary
        # as the key, value pairs are being generated.
        for key, message in list(self.board_state["messages"].items()):
            if message["read"] and message["to_callsign"] == name:
                lowest = min(lowest, message["id"])
                del self.board_state["messages"][key]
                count += 1
        if count:
            await self.save()
        self._next_id = lowest
        plural = "" if count == 1 else "s"
        await self.send_message(connection, f"\n{count} message{plural} deleted.")

    async def kill_message(self, connection: Connection, args: list[str]) -> None:
        """
        Delete a message from the database.
        """
        match args:
            case []:
                await self.send_message(
                    connection, "You must specify a message to kill."
                )
            case [number] if number in self.board_state["messages"]:
                # We don't have any 'real' authentication. We pretty much
                # Just have to take the client's word for it that they are us.
                message = self.board_state["messages"][number]
                if self.is_admin(connection) or is_party(
                    connection.first_party.name, message
                ):
                    del self.board_state["messages"][number]
                    await self.save()
                    self._next_id = min([self._next_id, int(number)])
                    await self.send_message(connection, f"Message {number} deleted.")
                    return
                # Do not reveal this message exists.
                if message["private"]:
                    await self.send_message(
                        connection, f"Could not find message with ID {number}."
                    )
                await self.send_message(
                    connection,
                    f"You do not have permission to kill message {number}.",
                )
            case [number]:
                await self.send_message(
                    connection, f"Could not find message with ID {number}."
                )
            case _:
                await self.send_message(
                    connection, "K[ill] takes one argument, a message ID."
                )

    async def send_info(self, connection: Connection) -> None:
        """
        Send an informational message about this board system.
        """
        info_lines = [
            "#### Pax25 PBBS ####",
            "Welcome to the Pax25 reference bulletin board implementation. Pax25 is a "
            "python library for creating packet radio applications. You are invited to "
            "join in on the fun by visiting us at: ",
            "",
            # Note: This URL is still pending moving pax25_next to pax25.
            # Also, we will probably want to make a proper intro page rather than
            # just linking the repo in the future.
            "https://git.lion.fm/radio/pax25/",
            "",
            "Pax25 was developed by KW6FOX, K1LEO, and KF0KAA. Additional contribution "
            "credit can be found on the GitLab repository homepage.",
            "###################",
        ]
        await self.send_message(connection, "\n".join(info_lines))

    async def send_help(self, connection: Connection) -> None:
        """
        Send the help text.
        """
        help_lines = [
            "B(ye)        PBBS will disconnect",
            "L(ist)       List messages you can read",
            "L <|> call   List messages to or from a callsign",
            "LM(ine)      List unread messages addressed to you",
            "K(ill) n     Delete message number n",
            "KM(ine)      Delete all read messages addressed to you",
            "R(ead) n     Display message ID n",
            "RM(ine)      Read all unread messages addressed to you"
            "S(end) call  Send message to callsign",
            "I(nfo)       Learn about his PBBS software",
        ]
        await self.send_message(connection, "\n".join(help_lines))

    async def home_commands(self, connection: Connection, message: str) -> None:
        """
        Interpret the main commands available on the home screen.
        """
        if not message.strip():
            await self.send_prompt(connection)
            return
        command, *args = message.split()
        command = command.lower()
        changed_mode = False
        match command:
            case command if "list".startswith(command):
                await self.list_messages(connection, args)
            case command if "lmine".startswith(command):
                await self.list_mine(connection)
            case command if "read".startswith(command):
                await self.read_message(connection, args)
            case command if "rmine".startswith(command):
                await self.read_mine(connection)
            case command if "send".startswith(command):
                changed_mode = await self.compose_message(connection, args)
            case command if command == "sp":
                changed_mode = await self.compose_message(
                    connection,
                    args,
                    private=True,
                )
            case command if "kill".startswith(command):
                await self.kill_message(connection, args)
            case command if "kmine".startswith(command):
                await self.kill_mine(connection)
            case command if "info".startswith(command):
                await self.send_info(connection)
            case command if "help".startswith(command):
                await self.send_help(connection)
            case command if "bye".startswith(command):
                await self.bye(connection)
        if not changed_mode:
            await self.send_prompt(connection)

    async def on_message(self, connection: Connection, message: str) -> None:
        """
        Perform the command routing.
        """
        state = self.connections[connection]
        match state.mode:
            case "home":
                await self.home_commands(connection, message)
            case "subject":
                state.subject = message[:150]
                state.mode = "body"
                response = "ENTER MESSAGE--END WITH /EX ON A SINGLE LINE"
                max_length = self.settings.get("max_message_length", DEFAULT_MAX_LENGTH)
                if max_length is not None:
                    response += f" (MAX {max_length} CHARS)"
                await self.send_message(connection, response)
            case "body":
                await self.handle_body_line(connection, state, message)
