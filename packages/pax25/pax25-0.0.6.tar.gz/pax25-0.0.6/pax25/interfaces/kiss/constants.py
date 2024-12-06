"""
Constants for the KISS protocol.
"""

import sys

KISS_FEND = b"\xC0"
KISS_FESC = b"\xDB"
KISS_TFEND = b"\xDC"
KISS_TFESC = b"\xDD"
# 0 - data frame indicator. Seems to be the only actual frame type?
KISS_CMD_DATA = b"\x00"

KISS_MIN_FRAME_LEN = 15

KISS_CMD_TXDELAY = 0x1  # 1 - TXDELAY (next byte is value in 10ms units (def 50))
KISS_CMD_PERSIST = 0x2  # 2 - PERSIST (next byte is p vaue in equation (def 63))
KISS_CMD_SLOTTIME = (
    0x3  # 3 - SLOTTIME (next byte is slot interval in 10ms units (def 10))
)
KISS_CMD_CUSTOM4 = 0x4  # 4 - UNUSED - was TXTAIL
KISS_CMD_FULLDUP = 0x5  # 5 - FULLDUPLEX (next byte > 0  FD, 0 HD (def 0))
KISS_CMD_SET_HARDWARE = 0x6  # 6 - SET-HARDWARE - user definable
KISS_CMD_CUSTOM7 = 0x7  # 7 - UNUSED

KISS_MASK_PORT = 0b11110000
KISS_SHIFT_PORT = 4
KISS_MASK_CMD = 0b00001111

KISS_ENDIAN = sys.byteorder
