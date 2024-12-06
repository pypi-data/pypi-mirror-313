import logging

from decentnet.consensus.dev_constants import R2R_LOG_LEVEL
from decentnet.modules.blockchain.block import Block
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(R2R_LOG_LEVEL, logger)


class R2RComm:
    def __init__(self, relay):
        self.relay = relay
        logger.debug(f"Current pipes {relay.beam_pipe_comm.keys()}")
        process_uid = relay.beam_pub_key

        while relay.alive:
            self.relay_key = process_uid
            if process_uid in relay.beam_pipe_comm.keys():
                logger.debug(f"Receiving PIPE on {process_uid} for sync")
                data = relay.beam_pipe_comm[process_uid][0].recv()
                logger.debug("Received data from PIPE %s B" % (len(data)))
                block = Block.from_bytes(data)

                if block.index == 0:
                    logger.debug(f"Overwriting blockchain with new genesis R2R")
                    relay.beam.comm_bc.clear()

                relay.beam.comm_bc.difficulty = block.diff
                relay.beam.comm_bc.insert(block)

        logger.debug(f"Closing blockchain sync pipes for  {process_uid}")
        self.close_relay_pipe()

    def close_relay_pipe(self):
        self.relay.beam_pipe_comm[self.relay_key][0].close()
        self.relay.beam_pipe_comm[self.relay_key][1].close()
        self.relay.beam_pipe_comm.pop(self.relay_key)
