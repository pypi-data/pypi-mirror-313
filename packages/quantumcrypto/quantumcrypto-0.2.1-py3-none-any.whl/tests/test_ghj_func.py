"""
Tests for G, H and J functions.
"""

import unittest
from quantumcrypto.utils.functions import _g, _h, _j


class TestGHJTestCase(unittest.TestCase):
    """
    Tests for G, H and J functions.
    """

    @classmethod
    def setUpClass(cls):
        cls.data = "I love crypto".encode()

    def test_h(self):
        """
        Test h func.
        """
        h_result = _h(self.data)
        self.assertEqual(
            "269f810b92139241e639d888779d3ff5531f9da5d7ae7386ec61d1da8d8320ef", h_result.hex())

    def test_j(self):
        """
        Test j func.
        """
        j_result = _j(self.data)
        self.assertEqual(
            "41760f4dfdbe45522b62899e25c5ba3790257721cbb27e06cde98afebd3b2c24", j_result.hex())

    def test_g(self):
        """
        Test g func.
        """
        a, b = _g(self.data)
        self.assertEqual(
            "1a0ed86ccc0da6e3be1878c0064b272e87db7f878995ba2b423733ab197829f2", a.hex())

        self.assertEqual(
            "6968fe7c4e980f207121ec413cfd733d1e77ffaa44d17c1c6ab14f22f664be5e", b.hex())
