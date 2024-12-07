"""
Encrypt decrypt test cases.
"""

import unittest
from quantumcrypto.utils.functions import (
    _k_pke_encrypt,
    _k_pke_decrypt)
from quantumcrypto.ml_kem import MLKEM


class TestEncryptDecrypt(unittest.TestCase):
    """
    Encrypt decrypt tests.
    """

    def test_encryption_decryption512(self):
        """
        Test encryption decryption.
        """
        ml_kem = MLKEM("512")
        pm = ml_kem.pm_set
        fake_random = b"fake"*8

        ek, dk = ml_kem.generate_keys()
        ek_bytes = bytes.fromhex(ek)
        dk_bytes = bytes.fromhex(dk)
        dk_pke = dk_bytes[:384*pm.k]

        plain_msg = "testtesttesttesttesttesttesttest"

        cipher = _k_pke_encrypt(
            ek_bytes,
            bytes(plain_msg, encoding="utf-8"),
            fake_random,
            ml_kem.pm_set
        )

        decrypted_msg = _k_pke_decrypt(dk_pke, cipher, pm).decode("utf-8")

        self.assertEqual(768, len(cipher))
        self.assertEqual(decrypted_msg, "testtesttesttesttesttesttesttest")

    def test_encryption_decryption768(self):
        """
        Test encryption decryption.
        """
        ml_kem = MLKEM("768")
        pm = ml_kem.pm_set
        fake_random = b"fake"*8

        ek, dk = ml_kem.generate_keys()
        ek_bytes = bytes.fromhex(ek)
        dk_bytes = bytes.fromhex(dk)
        dk_pke = dk_bytes[:384*pm.k]

        plain_msg = "testtesttesttesttesttesttesttest"

        cipher = _k_pke_encrypt(
            ek_bytes,
            bytes(plain_msg, encoding="utf-8"),
            fake_random,
            ml_kem.pm_set
        )

        decrypted_msg = _k_pke_decrypt(dk_pke, cipher, pm).decode("utf-8")

        self.assertEqual(1088, len(cipher))
        self.assertEqual(decrypted_msg, "testtesttesttesttesttesttesttest")

    def test_encryption_decryption1024(self):
        """
        Test encryption decryption.
        """
        ml_kem = MLKEM("1024")
        pm = ml_kem.pm_set
        fake_random = b"fake"*8

        ek, dk = ml_kem.generate_keys()
        ek_bytes = bytes.fromhex(ek)
        dk_bytes = bytes.fromhex(dk)
        dk_pke = dk_bytes[:384*pm.k]

        plain_msg = "testtesttesttesttesttesttesttest"

        cipher = _k_pke_encrypt(
            ek_bytes,
            bytes(plain_msg, encoding="utf-8"),
            fake_random,
            ml_kem.pm_set
        )

        decrypted_msg = _k_pke_decrypt(dk_pke, cipher, pm).decode("utf-8")

        self.assertEqual(1568, len(cipher))
        self.assertEqual(decrypted_msg, "testtesttesttesttesttesttesttest")
