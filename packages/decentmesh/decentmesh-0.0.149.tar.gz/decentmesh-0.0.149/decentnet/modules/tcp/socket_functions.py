import io
import logging
import os
import socket
import threading
from typing import Optional

from decentnet.consensus.block_sizing import BLOCK_PREFIX_LENGTH_BYTES
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.tcp_params import RECV_BUFFER_SIZE, SEND_BUFFER_SIZE
from decentnet.modules.logger.log import setup_logger
from decentnet.modules.tcp.db_functions import remove_alive_beam_from_db

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


def set_sock_properties(socket_obj: socket.socket):
    socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUFFER_SIZE)
    socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)
    socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


async def recv_all(socket_obj: socket.socket, host: Optional[str] = None,
                   port: Optional[int] = None, length_prefix_size=BLOCK_PREFIX_LENGTH_BYTES) -> tuple[
    bytes, int]:
    """Receive all bytes of a message up to total_bytes from a socket."""
    logger.debug(
        f"Thread {threading.current_thread().name} in PID {os.getpid()} is reading socket {socket_obj}")

    try:
        length_prefix = socket_obj.recv(length_prefix_size)
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError,
            ConnectionRefusedError) as e:
        raise e
    finally:
        if host and port:
            await remove_alive_beam_from_db(host, port)

    total_bytes = int.from_bytes(length_prefix, ENDIAN_TYPE, signed=False)
    if total_bytes:
        logger.debug(
            f"Incoming message will have length {total_bytes} B |"
            f" prefix {length_prefix.hex()} | Thread: {threading.current_thread().name}")
    else:
        return b'', 0

    buffer = io.BytesIO()
    data_len = 0

    while data_len < total_bytes:
        # Calculate the remaining bytes to receive
        remaining_bytes = total_bytes - data_len

        # Receive up to the remaining number of bytes
        frame = socket_obj.recv(remaining_bytes)

        if not frame:
            # No more data is being sent; possibly the connection was closed
            logger.debug(
                f"Data is not being sent, closing connection... Remaining {remaining_bytes} Bytes "
                f"Thread: {threading.current_thread().name} | Buffer contained {buffer.getvalue()}")
            break

        # Write the received frame into the BytesIO buffer
        written_bytes = buffer.write(frame)
        data_len += written_bytes

    # Retrieve the accumulated data
    data = buffer.getvalue()
    # Close the buffer to free up memory
    buffer.close()
    return data, data_len
