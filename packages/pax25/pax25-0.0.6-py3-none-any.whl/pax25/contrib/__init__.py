"""
The contrib module contains premade applications and plugins that we anticipate will be
widely useful both as examples and for practical use to client developers setting up
their own station.

These allow us to eat our own dogfood, and test the breadth of capability of the library
all in one. They are NOT the only applications we expect to develop, nor the only ones
we expect to use as examples, but they are the ones that we use for testing and as
'batteries included' functionality.
"""

from .bulletin_board import BulletinBoard
from .echo import Echo

__all__ = ["BulletinBoard", "Echo"]
