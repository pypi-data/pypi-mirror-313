import asyncio
import logging
import time
from multiprocessing import Pipe
from threading import Thread
from typing import Callable, Coroutine, Any

import cbor2
import networkx as nx
from networkx import NodeNotFound, NetworkXNoPath
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from decentnet.consensus.blockchain_params import SKIP_SIGNATURE_VERIFICATION_DEPTH
from decentnet.consensus.cmd_enum import CMD
from decentnet.consensus.dev_constants import RUN_IN_DEBUG, METRICS
from decentnet.consensus.relay_config import RELAY_DEFAULT_SIGNING_KEY_ID, RELAY_DEFAULT_ENCRYPTION_KEY_ID, \
    RELAY_FREQUENCY_DB_ALIVE_UPDATE
from decentnet.consensus.routing_params import MAX_ROUTE_LENGTH, DEFAULT_CAPACITY
from decentnet.modules.blockchain.block import Block
from decentnet.modules.comm.beam import Beam
from decentnet.modules.comm.db_funcs import get_alive_beams
from decentnet.modules.cryptography.asymetric import AsymCrypt
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.constants import USING_ASYNC_DB
from decentnet.modules.db.models import NodeInfoTable, AliveBeam
from decentnet.modules.forwarding.flow_net import FlowNetwork
from decentnet.modules.internal_processing.blocks import ProcessingBlock
from decentnet.modules.key_util.key_manager import KeyManager
from decentnet.modules.logger.log import setup_logger

if METRICS:
    from decentnet.modules.monitoring.metric_server import ping, send_metric
from decentnet.modules.serializer.serializer import Serializer
from decentnet.modules.tasks_base.publisher import BlockPublisher
from decentnet.modules.tcp.socket_functions import recv_all
from decentnet.modules.timer.relay_counter import RelayCounter
from decentnet.modules.timer.timer import Timer
from decentnet.modules.transfer.packager import Packager

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)

AsyncCallbackType = Callable[[str, str], Coroutine[Any, Any, Any]]


class Relay:

    def __init__(self, client_socket, beam_pipe_comm: dict, beam_msg_queue: dict,
                 callback: AsyncCallbackType | None = None,
                 beam: Beam | None = None):
        """
        Creates a passive relay that will listen on socket and relay incoming beams
        :param client_socket:
        :param beam_pipe_comm: Dict for beam synchronization
        :param beam_msg_queue: Dict for beam message queue
        :param callback:
        """

        BlockPublisher(beam_msg_queue)
        self.skip_verification = False

        self.do_metrics = asyncio.run(ping()) if METRICS else False
        if self.do_metrics:
            logger.debug("Metrics will be collected.. OK")
        else:
            logger.debug("Metrics in Relay will not be collected.. FAIL")

        self.alive = True
        self.beam_pipe_comm = beam_pipe_comm
        self.beam_pub_key = None
        self.socket = client_socket
        self.client_ip = client_socket.getpeername()
        self.__callback = callback
        self.public_key_id = RELAY_DEFAULT_SIGNING_KEY_ID
        self.public_key_enc_id = RELAY_DEFAULT_ENCRYPTION_KEY_ID

        logger.debug(f"Initial Connection {self.client_ip}")
        self.local_port = self.client_ip[1]

        logger.info("Waiting for genesis block from new sender...")
        request = asyncio.run(recv_all(self.socket, self.client_ip[0], self.local_port))[0]
        if not request:
            raise ConnectionError

        self.network = FlowNetwork()

        verified, unpacked_request, verified_csig = Packager.unpack(request)
        Packager.check_verified(unpacked_request, verified)

        if verified_csig is not None:
            asyncio.run(self.execute_network_cmd(unpacked_request, verified_csig))
            return

        block = Block.from_bytes(unpacked_request["data"])  # Difficulty is checked when adding to blockchain

        self.beam_pub_key = pub_key = unpacked_request["pub"]  # Key, which is received from unknown entity
        self.target_key = target_key = unpacked_request["target"]  # Key of mine or next destination

        self.init_pipes(beam_msg_queue, pub_key, target_key)

        _, self.relay_pub_key_bytes = asyncio.run(
            KeyManager.retrieve_ssh_key_pair_from_db(self.public_key_id))

        # Save key of a client
        if not beam:
            # Create a pipe for a relay beam communication between processes
            beam_pipe_comm[pub_key] = Pipe()

            self.beam = Beam(self.public_key_id, self.public_key_enc_id, target_key, self.do_metrics)
            self.beam.connect_using_socket(client_socket)
            self.beam.initialize_incoming_transmission(block)
        else:
            self.beam = beam

        self.beam.lock()

        if target_key != "NOT_KNOWN":
            asyncio.run(self.record_alive_beam(target_key, True))
            asyncio.run(self.relay_message_by_one(block, unpacked_request, request))

        _, o_pub_key = asyncio.run(KeyManager.retrieve_ssh_key_pair_from_db(self.public_key_id))
        signing_pub_key = AsymCrypt.verifying_key_to_string(o_pub_key)

        asyncio.run(self.network.add_edge(signing_pub_key,
                                          pub_key, DEFAULT_CAPACITY))
        asyncio.run(self.network.add_edge(target_key, pub_key, DEFAULT_CAPACITY))

        if block.index == 0:
            logger.info(f"Adding connected Beacon {pub_key}")
            asyncio.run(self.save_beacon(pub_key))

            Thread(
                target=lambda: self.broadcast_connected(block, pub_key, unpacked_request), daemon=True,
                name=f"Broadcasting of {pub_key}").start()
        else:
            logger.info(f"Updating beacon connection {pub_key}")
            asyncio.run(self.update_beacon_connection(pub_key))
            asyncio.run(self.network.add_edge(pub_key,
                                              KeyManager.key_to_base64(target_key), None))

        if not self.beam.alive:
            self.beam.close()
            logger.warning("INVALID BLOCK, Closed connection")
        else:
            asyncio.run(self.beam.save_new_pub_key(pub_key, False, "New Beacon"))

    @classmethod
    async def record_alive_beam(cls, pub_key, ready):
        if USING_ASYNC_DB:
            async with session_scope() as session:
                ln = len(list(await session.execute(select(AliveBeam).where(AliveBeam.pub_key == pub_key))))
                if ln:
                    return
                ab = AliveBeam(pub_key=pub_key, ready=ready)
                session.add(ab)
        else:
            with session_scope() as session:
                if len(session.get(AliveBeam).filter(pub_key=pub_key).all()):
                    return
                ab = AliveBeam(pub_key=pub_key, ready=ready)
                session.add(ab)

    @classmethod
    def init_pipes(cls, beam_msg_queue, pub_key, target_key):
        if beam_msg_queue.get(pub_key, None) is None:
            beam_msg_queue[pub_key] = Pipe()
        if beam_msg_queue.get(target_key, None) is None:
            beam_msg_queue[target_key] = Pipe()

    def broadcast_connected(self, genesis_block: Block, connected_pub_key: str,
                            unpacked_genesis: dict):
        """

        :param genesis_block:
        :param connected_pub_key: Pub key of the connected beacon needs to be base64
        :param unpacked_genesis:
        """
        if genesis_block.index == 0:
            all_alive_beams = asyncio.run(get_alive_beams())

            if len(all_alive_beams):
                _data = Packager.add_cmd(
                    unpacked_genesis, self.public_key_id, CMD.BROADCAST.value
                )
                ttl = _data.get("ttl", 0)
                logger.info(f"Broadcasting connected beacon {connected_pub_key} to connected beams TTL {ttl}")
                block_with_signature = {
                    "data": _data["data"],
                    "sig": _data["sig"],
                    "pub": _data["pub"]
                }
                # Template next connection block with broadcast block
                bb_data = cbor2.dumps(block_with_signature)
                broadcast_block = self.beam.conn_bc.template_next_block(
                    self.beam.conn_bc.difficulty,
                    bb_data
                )
                broadcast_block.mine()

                if not self.beam.conn_bc.insert(broadcast_block):
                    raise Exception("Failed to insert broadcast block")

                broadcast_block_bytes = asyncio.run(broadcast_block.to_bytes())
                broadcast_block_signature = Packager.sign_block(
                    self.public_key_id,
                    broadcast_block_bytes
                )

                serialized_broadcast = Serializer.serialize_data(
                    self.relay_pub_key_bytes,
                    broadcast_block_signature,
                    broadcast_block_bytes,
                    _data["target"],
                    _data["cmd"],
                    _data["csig"],
                    _data["cpub"],
                    ttl
                )
            else:
                logger.info(f"No one to broadcast to {connected_pub_key}")
                return
            # Broadcasting connection to other beams
            asyncio.run(self._broadcast_data(all_alive_beams, serialized_broadcast))

    @classmethod
    async def _broadcast_data(cls, all_alive_beams: list, serialized_broadcast: bytes):
        for beam in all_alive_beams:
            # TODO: Skip broadcast to current
            logger.info(f"  broadcasting connection to {beam.pub_key}")
            await BlockPublisher.publish_message(beam.pub_key, serialized_broadcast)

    async def update_beacon_connection(self, pub_key):
        await Relay.update_beacon(pub_key)
        await self.do_callback(pub_key, "ping")

    async def do_callback(self, pub_key: str, action: str):
        if self.__callback:
            await self.__callback(pub_key, action)

    async def do_relaying(self, t: Timer, relay_counter: RelayCounter):
        self.alive = True
        logger.debug(
            f"Waiting for data from {self.beam_pub_key} for relaying on {self.client_ip}...")
        request, request_size = (await recv_all(self.socket, self.client_ip[0], self.local_port))

        if not request:
            self.alive = False
            await self.network.rm_edge(self.beam.pub_key, self.beam_pub_key)
            return 0

        if self.do_metrics:
            await send_metric("prom_data_received", request_size)
        logger.info(f"Relay Connection {self.socket.getpeername()}")
        try:
            await self.relay_request(request, t, relay_counter)
        except (cbor2.CBORDecodeError, cbor2.CBORDecodeValueError):
            logger.error(f"Unable to decode: {request}")
            logger.error("Suggesting disconnect")
            self.beam.unlock()
            self.alive = False
            await self.network.rm_edge(self.beam.pub_key, self.beam_pub_key)
            return 0

        return request_size

    async def _execute_network_cmd(self, data: dict, cmd_value: int):
        await self.do_callback(data["pub"], CMD(cmd_value).name)
        if cmd_value == CMD.BROADCAST.value:
            await ProcessingBlock.proces_broadcast_block(self.network, data)
            return await ProcessingBlock.decrease_ttl_broadcast_block(data)
        elif cmd_value == CMD.SYNCHRONIZE.value:
            block = Block.from_bytes(data["data"])
            self.beam.comm_bc.insert(block)

            if not self.skip_verification:
                self.skip_verification = await self.check_if_verification_needed()
        return None

    async def check_if_verification_needed(self):
        res = len(self.beam.comm_bc) > SKIP_SIGNATURE_VERIFICATION_DEPTH
        if res:
            logger.debug(
                f"Beam {self.beam.pub_key} reached signature verification depth of "
                f"{SKIP_SIGNATURE_VERIFICATION_DEPTH}.. Skipping verification")
        return res

    async def execute_network_cmd(self, unpacked_request: dict, verified_csig: bool):
        Packager.check_verified(unpacked_request, verified_csig)
        cmd_value = unpacked_request["cmd"]
        logger.debug(f"Received verified cmd {CMD(cmd_value)}")
        changed_data = await self._execute_network_cmd(unpacked_request, cmd_value)

        if changed_data:
            await self.rebroadcast(changed_data)

    async def rebroadcast(self, changed_data):
        logger.debug(f"Rebroadcasting data TTL {changed_data.get("ttl")}")
        all_alive_beams = await get_alive_beams()
        serialized_broadcast = cbor2.dumps(changed_data)
        await self._broadcast_data(all_alive_beams, serialized_broadcast)

    async def relay_request(self, request, t: Timer, relay_counter: RelayCounter):
        t.stop()

        verified, data, verified_csig = Packager.unpack(request, self.skip_verification)

        if not self.skip_verification:
            Packager.check_verified(data, verified)

        if verified_csig is not None:
            await self.execute_network_cmd(data, verified_csig)
            return

        block = Block.from_bytes(data["data"])

        block.signature = data["sig"]
        beacon_pub_key = data["pub"]

        self.beam.comm_bc.difficulty = block.diff
        insert_res = self.beam.comm_bc.insert(block)

        if not self.skip_verification:
            self.skip_verification = await self.check_if_verification_needed()

        if relay_counter.count % RELAY_FREQUENCY_DB_ALIVE_UPDATE == 0:
            await self.update_beacon_connection(beacon_pub_key)
            relay_counter.reset()

        if not insert_res:
            logger.error(f"Failed to insert block, closing connection... {self.client_ip}")
            self.socket.close()
            self.alive = False

        if block.index > 0:
            try:
                await self.relay_message_by_one(block, data, request)
            except nx.NetworkXNoPath:
                logger.warning(f"No path between {self.beam_pub_key} => {data['target']}")

        block_process_time_timer = t.stop()
        logger.debug(f"Total block process time: {block_process_time_timer} ms")

        if self.do_metrics:
            await send_metric("prom_block_process_time", block_process_time_timer)

        relay_counter.count += 1

    async def relay_message_by_one(self, block, data, request):

        try:
            path, capacity = self.network.get_path(self.beam_pub_key, data["target"])
        except NodeNotFound:
            logger.warning(f"Node {data['target']} not found")
            self.socket.close()
            self.alive = False
            logger.debug(f"Socket closed. {self.client_ip}")
            return
        except NetworkXNoPath:
            logger.warning(f"Path to {data['target']} not found")
            self.socket.close()
            self.alive = False
            logger.debug(f"Socket closed. {self.client_ip}")
            return

        logger.debug(f"Found path {path} and capacity {capacity} for block {block.index}")
        path_len = len(path)
        if self.do_metrics:
            await send_metric("prom_block_path_len", path_len)

        if path_len == 1:
            logger.debug("Path too short")
            return

        if path and path_len > MAX_ROUTE_LENGTH:
            logger.info("Maximum path exceeded, connecting to closer relay for better latency...")
            # TODO: connect to the closer relay to make shorter path

        logger.debug(f"Publishing from {self.beam_pub_key} message to {path[1]}")

        process_uid = path[1]
        if self.beam_pipe_comm.get(process_uid, False):
            if RUN_IN_DEBUG:
                logger.debug(f"Sending {block} to PIPE {process_uid} from {self.beam_pub_key}")
            self.beam_pipe_comm[process_uid][1].send(data["data"])

        await BlockPublisher.publish_message(path[1], request)

    @classmethod
    async def update_beacon(cls, pub_key: str):
        if USING_ASYNC_DB:
            async with session_scope() as session:
                # Perform an asynchronous query to get the beacon
                result = await session.execute(
                    select(NodeInfoTable).where(NodeInfoTable.pub_key == pub_key)
                )
                beacon = result.scalar_one_or_none()

                if beacon:
                    beacon.last_ping = time.time()
        else:
            with session_scope() as session:
                # Perform a synchronous query to get the beacon
                result = session.execute(
                    select(NodeInfoTable).where(NodeInfoTable.pub_key == pub_key)
                )
                beacon = result.scalar_one_or_none()

                if beacon:
                    beacon.last_ping = time.time()

    async def disconnect_beacon(self, port: int, pub_key: str):
        # Call the disconnect callback asynchronously
        if USING_ASYNC_DB:
            # Call the disconnect callback asynchronously
            await self.do_callback(pub_key, "disconnect")

            async with session_scope() as session:
                # Perform an asynchronous query to find the record to delete
                result = await session.execute(
                    select(NodeInfoTable).where(
                        (NodeInfoTable.port == port) & (NodeInfoTable.pub_key == pub_key)
                    )
                )
                record_to_delete = result.scalar_one_or_none()

                if record_to_delete:
                    await session.delete(record_to_delete)
        else:
            # Call the disconnect callback synchronously
            self.do_callback(pub_key, "disconnect")

            with session_scope() as session:
                # Perform a synchronous query to find the record to delete
                result = session.execute(
                    select(NodeInfoTable).where(
                        (NodeInfoTable.port == port) & (NodeInfoTable.pub_key == pub_key)
                    )
                )
                record_to_delete = result.scalar_one_or_none()

                if record_to_delete:
                    session.delete(record_to_delete)

    async def save_beacon(self, pub_key: str):
        # Define a helper function to perform the database operations
        def add_beacon_to_session(session):
            client_ip = self.client_ip
            bdb = NodeInfoTable(
                ipv4=client_ip[0],
                port=client_ip[1],
                pub_key=pub_key,
            )
            session.add(bdb)

        # Define a helper function to handle commit and update
        async def commit_or_update_beacon(session):
            try:
                # Commit the transaction
                if USING_ASYNC_DB:
                    await session.commit()
                else:
                    session.commit()
            except IntegrityError:
                logger.debug(f"Updating connected node {self.client_ip[0]}:{self.client_ip[1]}")
                if USING_ASYNC_DB:
                    await session.rollback()
                    await Relay.update_beacon(pub_key)
                else:
                    session.rollback()
                    Relay.update_beacon(pub_key)

        # Perform the callback
        if USING_ASYNC_DB:
            await self.do_callback(pub_key, "connect")

            async with session_scope() as session:
                add_beacon_to_session(session)
                await commit_or_update_beacon(session)
        else:
            self.do_callback(pub_key, "connect")

            with session_scope() as session:
                add_beacon_to_session(session)
                commit_or_update_beacon(session)
