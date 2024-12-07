"""
Test file.
"""

import unittest
from secrets import token_bytes
from quantumcrypto.utils.functions import (
    _sample_ntt, _ntt,
    _inverse_ntt,
    _multiply_ntt,
    _base_case_multiply,
    _prf, _sample_poly_cbd)


class TestNttFunctions(unittest.TestCase):
    """
    ######################
    ## sample_NTT tests ##
    ######################
    """

    def test_sample_ntt_improper_length(self):
        """
        Should raise ValueError if the length of the input is less than 34 bytes
        """

        improper_byte_length = token_bytes(31)
        with self.assertRaises(ValueError) as error:
            _sample_ntt(improper_byte_length)

        self.assertEqual(
            "Received an improper length, the seed must be exactly 34 bytes.", str(error.exception))

    def test_sample_ntt_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        proper_byte_length = token_bytes(34)
        output_length = 256

        output_length1 = len(_sample_ntt(proper_byte_length))

        self.assertEqual(output_length, output_length1,
                         "The output length should be 256")


#####################
##    NTT tests    ##
#####################


    def test_ntt_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        input_array = [0] * 256
        output_length = 256

        output_length1 = len(_ntt(input_array))

        self.assertEqual(output_length, output_length1,
                         "The output length should be 256")

    def test_ntt_false_input_type(self):
        """
        Test false input type.
        """

        f = (1,) * 256

        with self.assertRaises(TypeError) as error:
            _ntt(f)

        self.assertEqual(
            "The input needs to be a list.", str(error.exception))


#######################
## inverse ntt tests ##
#######################


    def test_ntt_inverse_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        f = [1] * 256
        output_length = 256

        output_length1 = len(_inverse_ntt(f))

        self.assertEqual(output_length, output_length1,
                         "Received an improper length, the array length must be exactly 256.")

    def test_inverse_ntt_false_input_type(self):
        """
        Test false input type.
        """
        f = (1,) * 256

        with self.assertRaises(TypeError) as error:
            _inverse_ntt(f)

        self.assertEqual(
            "The input needs to be a list.", str(error.exception))


#########################
## MULTIPLY_NTT tests  ##
#########################


    def test_multiply_ntt_output_length(self):
        """
        Test output lenght is expected
        """

        f = [1] * 256
        g = [2] * 256

        expected_length = 256
        h = _multiply_ntt(f, g)
        self.assertEqual(len(h), expected_length)

    def test_multiply_ntt_zero(self):
        """
        Test expected output when multiplied by zero.
        """

        expected_output = [0] * 256
        f = [0] * 256
        g = [2] * 256

        h = _multiply_ntt(f, g)
        self.assertEqual(h, expected_output)

    def test_multiply_ntt_input_len(self):
        """
        Test ntt input length
        """

        f = [0] * 250
        g = [2] * 256

        with self.assertRaises(ValueError) as error:
            _multiply_ntt(f, g)

        self.assertEqual(
            "The length of the input arrays need to be exactly 256.", str(error.exception))

    def test_multiply_ntt_input(self):
        """
        Test false input.
        """
        f = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        g = [2] * 256

        with self.assertRaises(TypeError) as error:
            _multiply_ntt(f, g)

        self.assertEqual(
            "The input needs to be a list.", str(error.exception))


class TestBaseCaseMultiply(unittest.TestCase):
    """
    ###############################
    ## BASE_CASE_MULTIPLY tests  ##
    ###############################
    """

    def test_base_case_multiply(self):
        """
        Test basic stuff with known outputs
        """

        self.assertEqual(_base_case_multiply(1, 2, 3, 4, 5), (43, 10))
        self.assertEqual(_base_case_multiply(0, 0, 0, 0, 0), (0, 0))

    def test_base_case_int_input(self):
        """
        Test _basecase_multiply inputs.
        """

        a0 = "k"
        a1 = 1
        b0 = 2
        b1 = 3
        gamma = 4

        with self.assertRaises(TypeError) as error:
            _base_case_multiply(a0, a1, b0, b1, gamma)

        self.assertEqual(
            "The inputs need to be of type int", str(error.exception))


class TestSamplePolyCBD(unittest.TestCase):
    """
    ###############################
    ##   sample_poly_cbd tests   ##
    ###############################
    """

    def test_sample_poly_cbd_outputlen(self):
        """
        Test outputlenght is correct
        """

        target_len = 256

        onebyte = token_bytes(1)
        morebytes = token_bytes(32)
        test_bytes = _prf(2, onebyte, morebytes)
        sample_poly_output = _sample_poly_cbd(test_bytes, 2)

        self.assertEqual(len(sample_poly_output), target_len,
                         "The output must be of length 256!")


class TestPRF(unittest.TestCase):
    """
    ###############################
    ##         prf tests         ##
    ###############################
    """

    def test_prf_eta_input_type(self):
        """
        Testing type of parameter eta, if different than int, raise error.
        """

        eta = "g"
        s = token_bytes(1)
        b = token_bytes(32)

        with self.assertRaises(TypeError) as error:
            _prf(eta, s, b)

        self.assertEqual(
            "Eta needs to be of value int", str(error.exception))

    def test_prf_s_input_type(self):
        """
        testing type of parameter s, if different than bytes, raise error.
        """

        eta = 2
        s = 5
        b = token_bytes(32)

        with self.assertRaises(TypeError) as error:
            _prf(eta, s, b)

        self.assertEqual(
            "Both inputs of prf need to be bytes", str(error.exception))

    def test_prf_b_input_type(self):
        """
        Testing type of parameter b, if different than bytes, return error.
        """
        eta = 2
        s = token_bytes(1)
        b = 'j'

        with self.assertRaises(TypeError) as error:
            _prf(eta, s, b)

        self.assertEqual(
            "Both inputs of prf need to be bytes", str(error.exception))

    def test_prf_s_input_length(self):
        """
        Testing input length of s parameter, should raise error if length is different than 1
        """

        eta = 2
        s = token_bytes(2)
        b = token_bytes(32)

        with self.assertRaises(ValueError) as error:
            _prf(eta, s, b)

        self.assertEqual(
            "The length of s needs to be 1 and the length of b needs to be 32",
            str(error.exception))

    def test_prf_b_input_length(self):
        """
        Testing the b parameter with incorrect length, should raise error if different than 32.
        """

        eta = 2
        s = token_bytes(1)
        b = token_bytes(2)

        with self.assertRaises(ValueError) as error:
            _prf(eta, s, b)

        self.assertEqual(
            "The length of s needs to be 1 and the length of b needs to be 32",
            str(error.exception))
