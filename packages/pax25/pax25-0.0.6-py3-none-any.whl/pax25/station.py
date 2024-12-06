"""Station class. Defines the station parameters."""

import asyncio
from collections import defaultdict
from typing import Any, Optional, cast

from pax25.applications import BaseApplication
from pax25.applications.types import S
from pax25.ax25.address import Ax25Address
from pax25.exceptions import ConfigurationError
from pax25.frame_queue import FrameQueue
from pax25.interfaces import INTERFACE_TYPES, Interface
from pax25.types import StationConfig


class Station:
    """
    The main station class for Pax25. This class is intended to manage a physical
    station's digital affairs.
    """

    def __init__(self, *, config: StationConfig):
        self.name = config["name"].upper()
        self.interfaces: dict[str, Interface[Any]] = {}
        for key, value in config["interfaces"].items():
            interface_cls = INTERFACE_TYPES[value["type"]]
            interface_cls = cast(type[Interface[Any]], interface_cls)
            self.interfaces[key] = interface_cls(
                name=key, settings=value["settings"], station=self
            )
        self.frame_queue = FrameQueue(station=self)
        self.application_map: defaultdict[
            str, defaultdict[Ax25Address, list[BaseApplication[Any]]]
        ] = defaultdict(lambda: defaultdict(list))
        self.running = False

    def bring_up_interfaces(self) -> None:
        """
        Attempts to bring up all interfaces and queue them into the event loop.
        """
        for interface in self.interfaces.values():
            if not interface.listening:
                asyncio.ensure_future(interface.read_loop())
        self.running = True

    def register_app(  # pylint: disable=too-many-arguments
        self,
        app: type[BaseApplication[S]],
        *,
        interfaces: list[str],
        proxy: bool = False,
        application_name: Optional[str] = None,
        station_name: Optional[str] = None,
        ssid: Optional[int] = None,
        settings: S,
    ) -> None:
        """
        Registers a new application to the specified interfaces.
        """
        station_name = (station_name if station_name else self.name).upper()
        application_name = (
            application_name if application_name is not None else app.__class__.__name__
        )
        application_instance = app(
            name=application_name,
            proxy=proxy,
            settings=settings,
            station=self,
        )
        for interface in interfaces:
            if interface not in self.interfaces:
                raise ConfigurationError(
                    "Attempted to register application to non-existent "
                    f"interface, {interface}",
                )
            index = 0 if proxy else -1
            new_address = Ax25Address(
                name=station_name,
                ssid=self.frame_queue.next_ssid(
                    interface=self.interfaces[interface], name=station_name, ssid=ssid
                ),
            )
            self.application_map[interface][new_address].insert(
                index, application_instance
            )
            self.frame_queue.register_station(
                interface=self.interfaces[interface], address=new_address
            )

    async def shutdown(self, stop_loop: bool = False) -> None:
        """
        Shut down all interfaces, cutting off the station.
        """
        for interface in self.interfaces.values():
            await interface.shutdown()
        self.running = False
        if stop_loop:
            asyncio.get_event_loop().stop()
