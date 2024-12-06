"""
Constants used for analyzing/parsing/assembling/disassembling AX.25 frames, including
Enums.
"""

import sys
from enum import Enum

from pax25.utils import EnumReprMixin

# Platform specific
AX25_ENDIAN = sys.byteorder
AX25_CODEPAGE = "utf-8"

# Protocol limits
AX25_MIN_FRAME_LEN = 15  # per AX.25 spec (136 bits w/flags, we don't TX/RX flags)
AX25_DEFAULT_INFOMTU = 256  # per AX.25 spec
AX25_SEQ_MAX = 7  # we only do MOD8 connections
AX25_REPEATER_MAX = 7

# address bitworks
AX25_ADDR_SIZE = 7
AX25_SSID_MASK_RESERVED = 0b01100000
AX25_SSID_SHIFT_RESERVED = 5
AX25_SSID_MASK_COMMAND = 0b10000000
AX25_SSID_MASK_SSID = 0b00011110
AX25_SSID_MASK_LAST_ADDRESS = 0b00000001
AX25_SSID_SHIFT_SSID = 1

# control bitworks. Python will interpret these as integers, but they are written as
# bytes here for clarity when working with the protocol.
AX25_CTRL_I = 0b00000000
AX25_CTRL_MASK_I = 0b00000001
AX25_CTRL_MASK_RECVSEQ = 0b11100000
AX25_CTRL_INVMASK_RECVSEQ = 0b00011111
AX25_CTRL_SHIFT_RECVSEQ = 5
AX25_CTRL_MASK_SENDSEQ = 0b00001110
AX25_CTRL_SHIFT_SENDSEQ = 1
AX25_SUPERVISOR_MASK_SUBTYPE = 0b00001111
AX25_CTRL_MASK_S = 0b00000011
AX25_CTRL_S = 0b00000001
AX25_CTRL_MASK_UI = 0b00000011
AX25_CTRL_UI = 0b00000011
AX25_CTRL_MASK_PF = 0b00010000
AX25_CTRL_INVMASK_PF = 0b11101111
AX25_CTRL_SHIFT_PF = 4


class FrameType(Enum):
    """
    Enum for the different frame types.
    """

    UNNUMBERED = 0b00000011
    SUPERVISORY = 0b00000001
    INFORMATIONAL = 0b00000000


class UCommand(EnumReprMixin, Enum):
    """
    Different commands which Unnumbered frames may represent.
    """

    SET_ASYNC_BALANCED_MODE_EXTENDED = 0b01101111
    SET_ASYNC_BALANCED_MODE = 0b00101111
    DISCONNECT = 0b01000011
    DISCONNECT_MODE = 0b00001111
    UNNUMBERED_ACKNOWLEDGE = 0b01100011
    FRAME_REJECT = 0b10000111
    UNNUMBERED_INFORMATION = 0b00000011
    EXCHANGE_IDENTIFICATION = 0b10101111
    TEST = 0b11100011


UCOMMAND_DISPLAY: dict[UCommand, str] = {
    UCommand.SET_ASYNC_BALANCED_MODE_EXTENDED: "SABME",
    UCommand.SET_ASYNC_BALANCED_MODE: "SAB",
    UCommand.DISCONNECT: "DISC",
    UCommand.DISCONNECT_MODE: "DM",
    UCommand.UNNUMBERED_ACKNOWLEDGE: "UA",
    UCommand.FRAME_REJECT: "FRMR",
    UCommand.UNNUMBERED_INFORMATION: "UI",
    UCommand.EXCHANGE_IDENTIFICATION: "XID",
    UCommand.TEST: "TEST",
}


class SFrameType(EnumReprMixin, Enum):
    """
    Supervisory Frame types.
    """

    RECEIVE_READY = 0b00000001
    RECEIVE_NOT_READY = 0b00000101
    REJECT_FRAME = 0b00001001
    SELECTIVE_REJECT = 0b00001101


SFRAME_DISPLAY: dict[SFrameType, str] = {
    SFrameType.RECEIVE_READY: "RR",
    SFrameType.RECEIVE_NOT_READY: "RNR",
    SFrameType.REJECT_FRAME: "REJ",
    SFrameType.SELECTIVE_REJECT: "SREJ",
}


S_FRAME_MAP: dict[int, SFrameType] = {entry.value: entry for entry in SFrameType}
U_FRAME_MAP: dict[int, UCommand] = {entry.value: entry for entry in UCommand}

# Protocol ID types. This one is 'plain text' which almost everything uses.
AX25_PID_NONE = 0xF0

# Status and commands

AX25_STATUS_DISC = 0  # DISC - DISCONNECTED
AX25_STATUS_CONN = 1  # CONN - CONNECTED
AX25_STATUS_DREQ = 2  # DREQ - DISCONNECT REQUESTED
AX25_STATUS_CREQ = 3  # CREQ - CONNECT REQUESTED
AX25_STATUS_DISP = 4  # DISP - DISPOSE
AX25_STATUS_ERR = 5  # ERRR - ERROR
AX25_STATUS_PTX = 6  # P-TX - PAUSED TX
AX25_STATUS_PRX = 7  # P-RX - PAUSED RX
AX25_STATUS_PRTX = 8  # PRTX - PAUSED TX AND RX

AX25_CMD_CONN = 0  # ATTEMPT TO CONNECT THIS DATALINK
AX25_CMD_DISC = 0  # DISCONNECT THIS DATALINK
