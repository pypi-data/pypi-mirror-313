import logging

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.consensus.routing_params import DEFAULT_CAPACITY
from decentnet.modules.forwarding.flow_net import FlowNetwork
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class ProcessingBlock:
    @staticmethod
    async def proces_broadcast_block(network: FlowNetwork, data: dict):
        logger.debug(
            f"Adding edge from broadcast data {data['pub']} => {data['target']}")
        await network.add_edge(data["pub"], data["target"], DEFAULT_CAPACITY)

    @staticmethod
    async def decrease_ttl_broadcast_block(data: dict):
        data["ttl"] -= 1
        return data
