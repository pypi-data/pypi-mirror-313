"""
Types for the Personal Bulletin Board System.
"""

from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

from pax25.connection import Connection


class Message(TypedDict):
    """
    Message format for board posts.
    """

    id: int
    from_callsign: str
    to_callsign: str
    # Stored as string to be compatible with JSON, must be coerced to datetime.
    created_on: str
    subject: str
    body: str
    # Flag for indicating if the intended recipient has read the message.
    read: bool
    private: bool


@dataclass
class ReaderState:
    """
    State for tracking a connected reading user.
    """

    mode: Literal["home", "subject", "body"]
    to_callsign: str
    subject: str
    body: str
    private: bool


BoardConnections = dict[Connection, ReaderState]


class BoardState(TypedDict):
    """
    State for the bulletin board application.
    """

    # Key must be a string for JSON load and serialize compatibility,
    # but the key will be a stringified integer.
    version: str
    messages: dict[str, Message]


class BoardSettings(TypedDict, total=False):
    """
    Settings for the bulletin board application.
    """

    welcome_message: str
    save_file_path: str
    max_message_length: Optional[int]
    slots: Optional[int]
    debug: bool
