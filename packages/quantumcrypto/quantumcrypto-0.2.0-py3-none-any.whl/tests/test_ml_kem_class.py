"""
ML kem class test cases.
"""

import unittest
from quantumcrypto import MLKEM


class TestMLKemTestCase(unittest.TestCase):
    """
    ML_KEM tests.
    """

    def test_pm512_key_generation(self):
        """
        Test parameter set 512 creates keys
        """
        ml_kem = MLKEM("512")

        ek, dk = ml_kem.generate_keys()

        # Hex length is twice the byte length
        self.assertEqual(1600, len(ek))  # 800 * 2
        self.assertEqual(3264, len(dk))  # 1632 * 2

    def test_pm768_key_generation(self):
        """
        Test parameter set 768 creates keys
        """
        ml_kem = MLKEM("768")

        ek, dk = ml_kem.generate_keys()

        # Hex length is twice the byte length
        self.assertEqual(2368, len(ek))  # 1184 * 2
        self.assertEqual(4800, len(dk))  # 2400 * 2

    def test_pm1024_key_generation(self):
        """
        Test parameter set 1024 creates keys
        """
        ml_kem = MLKEM("1024")

        ek, dk = ml_kem.generate_keys()

        # Hex length is twice the byte length
        self.assertEqual(3136, len(ek))  # 1568 * 2
        self.assertEqual(6336, len(dk))  # 3168 * 2

    def test_encapsulate_decapsulate512(self):
        """
        Test correct process.
        """
        user_a = MLKEM("512")

        ek, dk = user_a.generate_keys()

        user_b = MLKEM("512")
        user_b_key, cipher = user_b.encaps(ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertEqual(64, len(user_a_key))
        self.assertEqual(user_a_key, user_b_key)

    def test_encapsulate_decapsulate768(self):
        """
        Test correct process.
        """
        user_a = MLKEM("768")

        ek, dk = user_a.generate_keys()

        user_b = MLKEM("768")
        user_b_key, cipher = user_b.encaps(ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertEqual(64, len(user_a_key))
        self.assertEqual(user_a_key, user_b_key)

    def test_encapsulate_decapsulate1024(self):
        """
        Test correct process.
        """
        user_a = MLKEM("1024")

        ek, dk = user_a.generate_keys()

        user_b = MLKEM("1024")
        user_b_key, cipher = user_b.encaps(ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertEqual(64, len(user_a_key))
        self.assertEqual(user_a_key, user_b_key)

    def test_incorrect_process512(self):
        """
        Test incorrect process.

        If the cipher was not created with the ek of the user a,
        the keys do not match
        """
        user_a = MLKEM("512")

        _, dk = user_a.generate_keys()

        user_b = MLKEM("512")
        wrong_ek, _ = user_b.generate_keys()
        user_b_key, cipher = user_b.encaps(wrong_ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertNotEqual(user_a_key, user_b_key)

    def test_incorrect_process768(self):
        """
        Test incorrect process.

        If the cipher was not created with the ek of the user a,
        the keys do not match
        """
        user_a = MLKEM("768")

        _, dk = user_a.generate_keys()

        user_b = MLKEM("768")
        wrong_ek, _ = user_b.generate_keys()
        user_b_key, cipher = user_b.encaps(wrong_ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertNotEqual(user_a_key, user_b_key)

    def test_incorrect_process1024(self):
        """
        Test incorrect process.

        If the cipher was not created with the ek of the user a,
        the keys do not match
        """
        user_a = MLKEM("1024")

        _, dk = user_a.generate_keys()

        user_b = MLKEM("1024")
        wrong_ek, _ = user_b.generate_keys()
        user_b_key, cipher = user_b.encaps(wrong_ek)

        user_a_key = user_a.decaps(dk, cipher)

        self.assertNotEqual(user_a_key, user_b_key)
