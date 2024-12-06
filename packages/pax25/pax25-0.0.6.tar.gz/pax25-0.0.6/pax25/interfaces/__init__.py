"""
This module contains the different interfaces which are included with pax25.
"""

from .dummy import DummyInterface
from .file_interface import FileInterface
from .types import Interface

INTERFACE_TYPES = {
    "file": FileInterface,
    "dummy": DummyInterface,
}

__all__ = ["FileInterface", "Interface", "INTERFACE_TYPES"]
