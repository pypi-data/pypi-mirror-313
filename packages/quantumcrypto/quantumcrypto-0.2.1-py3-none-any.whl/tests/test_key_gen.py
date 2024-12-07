"""
Keygen test cases.
"""

import unittest
from quantumcrypto.utils.functions import _k_pke_key_gen, _ml_kem_gey_gen_internal, ml_kem_gey_gen


class TestKeyGen(unittest.TestCase):
    """
    Keygen tests.
    """

    def test_tpke_key_gen_creates_right_length_keys(self):
        """
        T_pke_keygen creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        encryption_key, decryption_key = _k_pke_key_gen(
            "randbyts".encode()*4, k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(encryption_key))
        self.assertEqual(True, isinstance(encryption_key, bytes))

        # length = 384*k
        self.assertEqual(768, len(decryption_key))
        self.assertEqual(True, isinstance(decryption_key, bytes))

    def test_ml_kem_key_gen_internal_creates_right_length_keys(self):
        """
        Ml kem keygen internal creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        ek, dk = _ml_kem_gey_gen_internal(
            "randbyt1".encode()*4, "randbyt2".encode()*4, k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(ek))
        self.assertEqual(True, isinstance(ek, bytes))

        # length = 768*k+96
        self.assertEqual(768*2+96, len(dk))
        self.assertEqual(True, isinstance(dk, bytes))

    def test_ml_kem_key_gen_creates_right_length_keys(self):
        """
        Ml kem keygen creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        ek, dk = ml_kem_gey_gen(k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(ek))
        self.assertEqual(True, isinstance(ek, bytes))

        # length = 768*k+96
        self.assertEqual(768*2+96, len(dk))
        self.assertEqual(True, isinstance(dk, bytes))
