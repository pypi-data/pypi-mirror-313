import logging

import cbor2
import click
import rich
from rich.panel import Panel

from decentnet.consensus.blockchain_params import BlockchainParams
from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.interface.basic import BasicInterface
from decentnet.modules.comm.beacon import Beacon
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


@click.group()
def client():
    pass


@client.command()
@click.argument("owner_key_id")
@click.argument("host", type=str)
@click.argument("port", type=int)
@click.argument("target-key", type=str, required=False,
                default="Ah70wYetFbhu9X/nrFQsFXTW/3kE4GKeRfhQ+1os1rcL")  # "Target public signing key"
@click.argument("target-enc-key", type=str, required=False, default=None)  # "Target encryption key"
@click.option("--wait", "-w", is_flag=True, default=False)
def start(owner_key_id, host: str, port: int, target_key: str, target_enc_key: str, wait: bool) -> None:
    beacon = Beacon(host, port, owner_key_id)
    client_str = f"Identity {beacon.pub_key}\nConnecting to:\nHost: {host}\nPort: {port}\nTargeting: {target_key}"
    rich.print(Panel(client_str, title="Client Info"))
    beam = beacon.create_beam(target_key, 4, False)
    if beam is None:
        logger.error("No connection could be made, is relay running ?")
        return

    # Todo: it looks like that client gets genesis block and then it gets broadcast block which results in broadcast block not able to insert
    if not wait:
        # Get target enc pub key

        # This is used for the second layer of security between client and client as a last encryption layer
        # Client is expecting the first block to be handshake block
        # enc_target_key = session.query(ForeignKeys).where(
        #    ForeignKeys.description == f"Key from {target_key}").first()
        if target_enc_key is None:
            logger.error("No public key for encryption")
            exit(1)
        logger.debug("> Communication genesis block is \n%s" % (beam.comm_bc.get_last()))
        # Set lower difficulty for handshake block
        beam.comm_bc.difficulty = BlockchainParams.low_diff_sha256
        block, pwd = beam.comm_bc.create_handshake_encryption_block_dict(
            target_enc_key)
        # Send handshake block for direct communication without relay being able to decrypt
        handshake_block_bytes = beam.comm_bc.convert_handshake_block_dict_to_bytes(block)
        beam.send_communication_data(handshake_block_bytes, False)
        beam.process_handshake_block(block, False, False)
        logger.debug("Waiting for ack handshake")
        data = beam.fetch_message()[0].data
        logger.debug("MSG: %s" % beam.encryptor_beacon.decrypt(bytes(data)))
        if not beam.send_communication_data(f"Hello :) incom".encode("ascii")):
            logger.error("Failed to send message with response")

    if wait:
        logger.info("Waiting for incoming beams")
        for _ in range(3):
            incoming_block = beam.fetch_message()[0]

            logger.debug(f"Block data {incoming_block}")


@client.command()
@click.argument("owner_key_id")
@click.argument("owner_key_enc_id")
@click.argument("target-key", type=str, required=False,
                default="Ah70wYetFbhu9X/nrFQsFXTW/3kE4GKeRfhQ+1os1rcL")  # "Target public signing key"
@click.argument("target-enc-key", type=str, required=False, default=None)  # "Target encryption key"
def testsend(owner_key_id, owner_key_enc_id, target_key: str, target_enc_key: str) -> None:
    bi = BasicInterface(target_key, target_enc_key)
    bi.init_sending(owner_key_id, owner_key_enc_id)
    print(bi.encrypted_send)
    bi.send(cbor2.dumps({"data": "Hello"}))


@client.command()
@click.argument("owner_key_id")
@click.argument("owner_key_enc_id")
@click.argument("target-key", type=str, required=False,
                default="Ah70wYetFbhu9X/nrFQsFXTW/3kE4GKeRfhQ+1os1rcL")  # "Target public signing key"
@click.argument("target-enc-key", type=str, required=True)  # "Target encryption key"
def testrec(owner_key_id, owner_key_enc_id, target_key: str, target_enc_key: str) -> None:
    bi = BasicInterface(target_key, target_enc_key)
    bi.init_receiving(owner_key_id, owner_key_enc_id)

    print(bi.fetch())
