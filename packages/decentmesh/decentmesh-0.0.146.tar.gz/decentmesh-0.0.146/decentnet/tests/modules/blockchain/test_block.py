import asyncio
import os
import unittest
from random import randint

from decentnet.consensus.blockchain_params import BlockchainParams
from decentnet.modules.blockchain.block import Block
from decentnet.modules.blockchain.blockchain import Blockchain


class TestBlockSerialization(unittest.TestCase):

    def test_block_to_from_bytes(self):
        # Create a block
        b = Blockchain("test_chain")

        # Serialize to bytes
        block_bytes = asyncio.run(b.get_last().to_bytes())

        # Deserialize from bytes
        deserialized_block = Block.from_bytes(block_bytes)

        # Assert that the deserialized block matches the original block
        self.assertEqual(b.get_last().index, deserialized_block.index)
        self.assertEqual(b.get_last().previous_hash, deserialized_block.previous_hash)
        self.assertEqual(b.get_last().diff, deserialized_block.diff)
        self.assertEqual(b.get_last().data, deserialized_block.data)
        self.assertEqual(b.get_last().nonce, deserialized_block.nonce)
        self.assertEqual(b.get_last().timestamp, deserialized_block.timestamp)

    def test_block_to_from_bytes_dynamic(self):
        difficulty = BlockchainParams.seed_difficulty  # Assume a valid Difficulty object can be instantiated like this

        # Create a block
        test_blocks = int(os.getenv("TEST_BLOCKS", 500))
        for i in range(test_blocks):
            data = os.urandom(512 + i)
            non_empty_bytes_by4 = randint(1, 8)
            prev_hash = bytes.fromhex("00" * (16 - non_empty_bytes_by4)) + bytes.fromhex(
                'abcd' * non_empty_bytes_by4)

            block = Block(i, prev_hash, difficulty, data)

            # Serialize to bytes
            block_bytes = asyncio.run(block.to_bytes())

            # Deserialize from bytes
            deserialized_block = Block.from_bytes(block_bytes)

            # Assert that the deserialized block matches the original block
            self.assertEqual(block.index, deserialized_block.index)
            self.assertEqual(block.previous_hash, deserialized_block.previous_hash)
            self.assertEqual(block.diff, deserialized_block.diff)
            self.assertEqual(block.data, deserialized_block.data)
            self.assertEqual(block.nonce, deserialized_block.nonce)
            self.assertEqual(block.timestamp, deserialized_block.timestamp)


if __name__ == '__main__':
    unittest.main()
