"""
The file interface. This is used mostly for testing-- we can send in predefined
commands and let the system process them this way.

It's also useful for running apps over stdin/stdout, which are the default input/output
files.
"""

import asyncio
import logging
import os
from sys import stdin, stdout
from typing import IO, TYPE_CHECKING, Literal, Optional, TextIO

from pax25.ax25.address import Ax25Address
from pax25.interfaces.types import FileSettings, Interface, TerminalSettings
from pax25.types import ConnectFrame, DisconnectFrame, Frame, MessageFrame
from pax25.utils import async_wrap

if TYPE_CHECKING:
    from pax25.station import Station

try:
    # noinspection PyUnresolvedReferences
    import termios as _termios

    # noinspection PyUnresolvedReferences
    import tty as _tty
except ImportError:
    tty = None  # pylint: disable=invalid-name
    termios = None  # pylint: disable=invalid-name
else:
    tty = _tty  # pylint: disable=invalid-name
    termios = _termios  # pylint: disable=invalid-name


logger = logging.getLogger(__name__)


class FileInterface(Interface[FileSettings]):
    """
    A file interface that will read in on a file and send the resulting
    bytes to another file. By default, input is stdin, and output is stdout.

    You may want to set the sudo settings flag to True if this is intended to be the
    administrative connection. Privileges will only be elevated if this flag is true
    AND the 'source ssid' argument matches the station name, which it will by default.
    """

    def __init__(self, name: str, settings: FileSettings, station: "Station"):
        self.name = name
        self.settings = settings
        self.station = station
        self.listening = False
        self.input: Optional[IO[bytes]] = None
        self.output: Optional[IO[bytes]] = None
        self.close_input = False
        self.close_output = False
        self.sudo = settings.get("sudo", False)
        self.old_terminal_settings: Optional[TerminalSettings] = None
        self.loop = asyncio.get_event_loop()

    def handle_for(
        self,
        file_path: Optional[str],
        mode: Literal["r", "w"],
        *,
        default_interface: TextIO,
    ) -> IO[bytes]:
        """
        Gets the file handle for a specified file path, falling back to an interface
        if the path is falsy.
        """
        handle: IO[bytes] = default_interface.buffer
        if file_path:
            # pylint: disable=consider-using-with
            handle = open(  # pylint: disable=unspecified-encoding, bad-open-mode
                file_path,
                f"{mode}b",
            )
        if termios is not None and tty is not None and os.isatty(handle.fileno()):
            # Interactive Linux terminals buffer lines locally. We need to turn this off
            # so that commands can be read in one character at a time.
            try:
                if not self.old_terminal_settings:
                    self.old_terminal_settings = termios.tcgetattr(handle.fileno())
                # Send all keystrokes at once, rather than waiting for a full line.
                # This will be more handy as we end up with control operation.
                # For later examination: In this mode, backspace shows up as characters
                # instead of going back a space. This might not be avoidable without
                # a lot more work.
                terminal_settings = termios.tcgetattr(handle.fileno())
                terminal_settings[tty.LFLAG] &= ~termios.ICANON
                terminal_settings[tty.CC][termios.VMIN] = 1
                terminal_settings[tty.CC][termios.VTIME] = 0
                termios.tcsetattr(handle.fileno(), termios.TCSAFLUSH, terminal_settings)
            except termios.error:
                # stdin is not an interactive terminal.
                self.old_terminal_settings = None
        return handle

    @property
    def address_kwargs(
        self,
    ) -> dict[Literal["source", "destination"], Ax25Address]:
        """
        Shorthand function for adding the first and second party to the frames we
        construct.
        """
        return {
            "source": Ax25Address(
                name=self.settings.get("source_name", self.station.name),
                ssid=self.settings.get("source_ssid", 0),
            ),
            "destination": Ax25Address(
                name=self.settings.get("destination_name", self.station.name),
                ssid=self.settings.get("destination_ssid", 0),
            ),
        }

    async def send_frame(self, frame: Frame) -> None:
        """
        Handles a frame from the frame queue.

        We only really care about one frame type for this interface-- the
        MessageFrame. We ignore everything else.
        """
        if frame.command == "disconnect":
            self.listening = False
            await self.conditional_shutdown()
            return
        if frame.command != "message":
            return
        if not self.output:
            raise RuntimeError(
                "Received a frame, but we don't have an open output file!",
            )
        await async_wrap(self.output.write)(frame.payload["bytes"])
        await async_wrap(self.output.flush)()

    async def conditional_shutdown(self) -> None:
        """
        If set to shut down the station automatically, go ahead and do so.
        """
        if self.settings.get("auto_shutdown", True):
            await self.station.shutdown(
                stop_loop=self.settings.get("stop_loop", True),
            )

    async def read_loop(self) -> None:
        """Reads input from the keyboard and sends it for routing."""
        self.input = self.handle_for(
            self.settings.get("input"),
            "r",
            default_interface=stdin,
        )
        self.output = self.handle_for(
            self.settings.get("output"),
            "w",
            default_interface=stdout,
        )
        self.close_input = self.input != stdin.buffer
        self.close_output = self.output != stdout.buffer
        self.listening = True
        frame_queue = self.station.frame_queue
        address_kwargs = self.address_kwargs
        await frame_queue.process_frame(
            self,
            ConnectFrame(
                source=address_kwargs["source"],
                destination=address_kwargs["destination"],
            ),
        )
        while self.listening:
            # Since we're reading from a file which can contain arbitrary data,
            # and we don't know how long it is, we process it one character at a time
            # as a full message frame. The reads block in their own thread to allow
            # other tasks to run. This prevents the application from freezing while
            # waiting for keyboard input.
            message = await async_wrap(self.input.read)(1)
            if not message:
                # The file has ended.
                await self.station.frame_queue.process_frame(
                    self,
                    DisconnectFrame(
                        source=address_kwargs["source"],
                        destination=address_kwargs["destination"],
                    ),
                )
                self.listening = False
                await self.conditional_shutdown()
                continue
            try:
                await self.station.frame_queue.process_frame(
                    self,
                    MessageFrame(
                        source=address_kwargs["source"],
                        destination=address_kwargs["destination"],
                        payload={"bytes": message, "outbound": False},
                    ),
                )
            except Exception as err:  # pylint: disable=broad-exception-caught
                logging.error("Error when processing frame.", exc_info=err)

    async def shutdown(self) -> None:
        """Closes the read loop, closes open file handles, and restores terminal."""
        self.listening = False
        if self.close_input and self.input:
            self.input.close()
        if self.output and not self.output.closed:
            await async_wrap(self.output.flush)()
            if self.close_output:
                self.output.close()
        if self.old_terminal_settings and termios:
            termios.tcsetattr(stdin, termios.TCSADRAIN, self.old_terminal_settings)
