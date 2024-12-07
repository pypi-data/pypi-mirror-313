"""
Test file.
"""

import unittest
from quantumcrypto.utils.functions import _byte_encode, _byte_decode


class TestByteEncodeDecode(unittest.TestCase):
    """
    Tests for _byte_encode and decode.
    """

    def test_improper_int_array_length(self):
        """
        The _byte_encode expects an int_array of length 256 integers.
        """

        int_array = [1, 2, 3, 4]

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 8)

        self.assertEqual(
            "Provided array contained 4 integers. Required length is 256", str(error.exception))

    def test_improper_int_values(self):
        """
        The _byte_encode int array must contain integers.
        """

        int_array = [1, 2, 3, 4.0]*64

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 8)

        self.assertEqual(
            "int_array values must be integers", str(error.exception))

    def test_improper_d_value(self):
        """
        The _byte_encode d value must be integer.
        """

        int_array = [1, 2, 3, 4]*64

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 6.7)

        self.assertEqual(
            "Parameter d has to be integer between 1 and 12", str(error.exception))

    def test_too_high_d_value(self):
        """
        The _byte_encode d value must be integer between 1 and 12.
        """

        int_array = [1, 2, 3, 4]*64

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 13)

        self.assertEqual(
            "Parameter d has to be integer between 1 and 12", str(error.exception))

    def test_integer_value_too_high_for_8_bit_int(self):
        """
        Data will be lost if trying to encode too big integer to a too small bit space.
        """

        int_array = [1, 2, 3, 256]*64

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 8)

        self.assertEqual(
            "int_array contains an element exceeding the max value 255 for current d value 8",
            str(error.exception))

    def test_integer_value_too_high_for_12_bit_int(self):
        """
        Data will be lost if trying to encode too big integer to a too small bit space.

        The limit for 12 bit int is the q value which is 3329
        """

        int_array = [1, 2, 3, 3329]*64

        with self.assertRaises(ValueError) as error:
            _byte_encode(int_array, 12)

        self.assertEqual(
            "int_array contains an element exceeding the max value 3328 for current d value 12",
            str(error.exception))

    def test_encode_8_bit(self):
        """
        Test _byte_encode for 8 bits.
        """

        int_array = [1, 2, 3, 4]*64
        result = _byte_encode(int_array, 8)

        self.assertEqual(256, len(result))
        partial = result[:4]
        self.assertListEqual([b'\x01', b'\x02', b'\x03', b'\x04'], partial)
        self.assertEqual(1, int.from_bytes(partial[0], "little"))
        self.assertEqual(2, int.from_bytes(partial[1], "little"))
        self.assertEqual(3, int.from_bytes(partial[2], "little"))
        self.assertEqual(4, int.from_bytes(partial[3], "little"))

    def test_decode_8_bit(self):
        """
        Test _byte_decode for 8 bits.
        """

        byte_array = [b'\x01', b'\x02', b'\x03', b'\x04']*64
        result = _byte_decode(byte_array, 8)

        self.assertEqual(256, len(result))
        partial = result[:8]
        self.assertListEqual([1, 2, 3, 4, 1, 2, 3, 4], partial)

    def test_encode_12_bit(self):
        """
        Test _byte_encode for 12 bits.
        """
        int_array = [1, 2, 3, 4]*64
        result = _byte_encode(int_array, 12)

        # expected output length should be 32*d -> 32*12 == 384
        self.assertEqual(384, len(result))
        self.assertListEqual(
            [b'\x01', b' ', b'\x00', b'\x03', b'@', b'\x00']*64, result)

    def test_encode_decode_4bits(self):
        """
        Decode encode should return same values.
        """

        int_array = [10, 2, 13, 7]*64
        result = _byte_decode(_byte_encode(int_array, 4), 4)

        self.assertListEqual([10, 2, 13, 7]*64, result)

    def test_encode_decode_8bits(self):
        """
        Decode encode should return same values.
        """

        int_array = [100, 12, 213, 117]*64
        result = _byte_decode(_byte_encode(int_array, 8), 8)

        self.assertListEqual([100, 12, 213, 117]*64, result)

    def test_encode_decode_11bits(self):
        """
        Decode encode should return same values.
        """

        int_array = [2047, 12, 1000, 1]*64
        result = _byte_decode(_byte_encode(int_array, 11), 11)

        self.assertListEqual([2047, 12, 1000, 1]*64, result)

    def test_encode_decode_12bits(self):
        """
        Decode encode should return same values.
        """

        int_array = [2047, 3000, 1000, 3328]*64
        result = _byte_decode(_byte_encode(int_array, 12), 12)

        self.assertListEqual([2047, 3000, 1000, 3328]*64, result)

    def test_decode_encode(self):
        """
        Decoding bytes and encoding them back should give the same
        result as in the start
        """
        test_bytes = b"test"*96  # length has to be 32*d

        result = b"".join(_byte_encode(_byte_decode(
            [b.to_bytes(1, "little") for b in test_bytes], 12), 12))

        self.assertEqual(test_bytes, result)

    def test_decode_encode_384k(self):
        """
        Test from chapter 7.2 FIPS 203
        """
        k = 2
        start_bytes = b"test"*192  # simulate ek 384k while k=2
        test_bytes = [x.to_bytes(1, "little")
                      for x in start_bytes]

        chunked = [test_bytes[i*384:(i+1)*384] for i in range(k)]
        decoded = [_byte_decode(arr, 12) for arr in chunked]
        mid_result = [_byte_encode(arr, 12) for arr in decoded]
        bytes_arr = []
        for sublist in mid_result:
            for el in sublist:
                bytes_arr.append(el)
        result = b"".join(bytes_arr)

        self.assertEqual(start_bytes, result)
