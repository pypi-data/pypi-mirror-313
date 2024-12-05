"""
The main user facing ml-kem tool file.
"""

from quantumcrypto.utils.parameters import P512, P768, P1024
from quantumcrypto.utils.functions import ml_kem_gey_gen, ml_kem_encaps, ml_kem_decaps


class MLKEM:
    """
    ML_KEM
    """

    def __init__(self, parameter_set="1024") -> None:

        if parameter_set == "512":
            self.pm_set = P512
        elif parameter_set == "768":
            self.pm_set = P768
        else:
            self.pm_set = P1024

    def generate_keys(self) -> tuple[str, str]:
        """
        Creates the encapsulation and decapsulation keys.
        """
        ek, dk = ml_kem_gey_gen(self.pm_set.k, self.pm_set.n1)
        return ek.hex(), dk.hex()

    def encaps(self, ek: str) -> tuple[str, str]:
        """
        Creates the shared secret key and cipher
        """
        ek_bytes = bytes.fromhex(ek)
        key, cipher = ml_kem_encaps(ek_bytes, self.pm_set)
        return key.hex(), cipher.hex()

    def decaps(self, dk: str, cipher: str) -> str:
        """
        Creates the shared secret key out of cipher
        """
        dk_bytes = bytes.fromhex(dk)
        cipher_bytes = bytes.fromhex(cipher)

        key = ml_kem_decaps(dk_bytes, cipher_bytes, self.pm_set)
        return key.hex()
