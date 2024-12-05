"""
Test file.
"""

import unittest
from quantumcrypto.utils.functions import _bits_to_bytes, _bytes_to_bits


class TestInnerFunctions(unittest.TestCase):
    """
    Tests for inner functions.
    """

    def test_bits_to_bytes_improper_length(self):
        """
        The received array of bits needs to be multiple of 8 to be converted into byte array.

        Should raise ValueError
        """
        with self.assertRaises(ValueError) as error:
            _bits_to_bytes([1, 0, 1])

        self.assertEqual(
            "Received array of bits needs to be a multiple of 8", str(error.exception))

    def test_bits_to_bytes_improper_values(self):
        """
        The received array of bits needs to consist of values 0 and 1.

        Should raise ValueError
        """

        with self.assertRaises(ValueError) as error:
            _bits_to_bytes([1, 0, 1, 0, 0, 0, 1, 2])

        self.assertEqual(
            "Each bit in array need to be 0 or 1", str(error.exception))

    def test_bits_to_bytes(self):
        """
        Converts 8 bits to byte
        """
        arr = [1, 1, 0, 1, 0, 0, 0, 1]  # 139 as little endian byte

        result = _bits_to_bytes(arr)
        self.assertEqual([b'\x8b'], result)

        self.assertEqual(139, int.from_bytes(result[0], "little"))

    def test_bits_to_bytes_larger_array(self):
        """
        Converts large bit array to byte array
        """
        arr = [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0,
               0, 0, 0]*2  # [138,10,138,10] as little endian byte

        result = _bits_to_bytes(arr)

        self.assertListEqual([b'\x8a', b'\n', b'\x8a', b'\n'], result)
        self.assertEqual(138, int.from_bytes(result[0], "little"))
        self.assertEqual(10, int.from_bytes(result[1], "little"))

    def test_bytes_to_bits(self):
        """
        Should turn byte array to array of bits.
        """
        byte_array = [b'\x8a', b'\n']  # [138,10]

        result = _bytes_to_bits(byte_array)
        self.assertEqual(16, len(result))

        # [0, 1, 0, 1, 0, 0, 0, 1] == 138 little endian
        # [0, 1, 0, 1, 0, 0, 0, 0] == 10    little endian
        self.assertListEqual(
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0], result)

    def test_bytes_to_bits_invalid_values(self):
        """
        Should raise error if receiving other values than array of bytes.
        """
        byte_array = [0, 1]

        with self.assertRaises(ValueError) as error:
            _bytes_to_bits(byte_array)
        self.assertEqual(
            "Requires an array of bytes.", str(error.exception))

    def test_bits_to_bytes_and_back(self):
        """
        Should return the same value.
        """
        # [139,11]
        arr = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0,
               0, 0, 0]

        result = _bytes_to_bits(_bits_to_bytes(arr))

        self.assertEqual([1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0,
                          0, 0, 0], result)

    def test_bytes_to_bits_and_back(self):
        """
        Should return the same value.
        """

        byte_array = [b'\x8a', b'\n']  # [138,10]

        result = _bits_to_bytes(_bytes_to_bits(byte_array))

        self.assertEqual([b'\x8a', b'\n'], result)
