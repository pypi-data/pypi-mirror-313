import random
import unittest

from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.modules.comm.beacon import Beacon


class BlockProcessingCase(unittest.TestCase):
    def test_block_processing(self):
        host = 'localhost'
        port = 8888
        target_key = "Asn25jmE_EdqzpXH28-ecvGY5b05K4LF80sjtRUNjlhh"

        beacon = Beacon(host, port, pub_key_id=1, ipv=4)
        beam = beacon.create_beam(target_key, 4)

        for _ in range(500000):
            beam.send_communication_data(
                random.randint(151561, 1561551561111111156).to_bytes(8, ENDIAN_TYPE,
                                                                     signed=True))


if __name__ == '__main__':
    unittest.main()
