"""
Test file.
"""

import unittest
from quantumcrypto.utils.functions import _compress, _decompress


class TestCompressDecompress(unittest.TestCase):
    """
    Tests for compress and decompress.
    """

    def test_compress_decompress_10(self):
        """
        Decompression followed by compression should preserve the input

        For d < 12
        """
        # 2^10 == 1024
        values = [1023, 200, 765]

        d_val = 10

        result = _compress(_decompress(values, d_val), d_val)
        self.assertListEqual([1023, 200, 765], result)

    def test_compress_decompress_11(self):
        """
        Decompression followed by compression should preserve the input

        For d < 12
        """
        # 2^11 == 2048
        values = [2000, 678, 765]

        d_val = 11

        result = _compress(_decompress(values, d_val), d_val)
        self.assertListEqual([2000, 678, 765], result)

    def test_decompress_compress_10(self):
        """
        Compression followed by decompression should not significally alter the value
        """

        values = [145, 1000, 600]

        d_val = 10

        result = _decompress(_compress(values, d_val), d_val)

        # a bit unclear if this is good enough?
        self.assertListEqual([146, 1001, 601], result)
