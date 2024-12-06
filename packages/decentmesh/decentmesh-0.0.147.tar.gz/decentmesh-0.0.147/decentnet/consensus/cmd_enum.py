from enum import Enum


class CMD(Enum):
    """Enum of commands"""
    HANDSHAKE_ENCRYPTION = 0
    BROADCAST = 1  #
    SYNCHRONIZE = 2
    UPDATE_EDGE = 3  # TODO: broadcast edge disconnect
