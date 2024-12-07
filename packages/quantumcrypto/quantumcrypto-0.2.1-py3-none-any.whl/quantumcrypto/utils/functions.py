"""
Project functions file.
"""
import math
import hashlib
from secrets import token_bytes
from Crypto.Hash import SHAKE128, SHAKE256
import numpy as np

Q_VAL = 3329

BITREV7_NTT_MODQ = [
    1,      1729,   2580,   3289,   2642,   630,    1897,   848,
    1062,   1919,   193,    797,    2786,   3260,   569,    1746,
    296,    2447,   1339,   1476,   3046,   56,     2240,   1333,
    1426,   2094,   535,    2882,   2393,   2879,   1974,   821,
    289,    331,    3253,   1756,   1197,   2304,   2277,   2055,
    650,    1977,   2513,   632,    2865,   33,     1320,   1915,
    2319,   1435,   807,    452,    1438,   2868,   1534,   2402,
    2647,   2617,   1481,   648,    2474,   3110,   1227,   910,
    17,     2761,   583,    2649,   1637,   723,    2288,   1100,
    1409,   2662,   3281,   233,    756,    2156,   3015,   3050,
    1703,   1651,   2789,   1789,   1847,   952,    1461,   2687,
    939,    2308,   2437,   2388,   733,    2337,   268,    641,
    1584,   2298,   2037,   3220,   375,    2549,   2090,   1645,
    1063,   319,    2773,   757,    2099,   561,    2466,   2594,
    2804,   1092,   403,    1026,   1143,   2150,   2775,   886,
    1722,   1212,   1874,   1029,   2110,   2935,   885,    2154]

BITREV7_NTT_MODQ_2 = [
    17,     -17,    2761,   -2761,  583,    -583,   2649,   -2649,
    1637,   -1637,  723,    -723,   2288,   -2288,  1100,   -1100,
    1409,   -1409,  2662,   -2662,  3281,   -3281,  233,    -233,
    756,    -756,   2156,   -2156,  3015,   -3015,  3050,   -3050,
    1703,   -1703,  1651,   -1651,  2789,   -2789,  1789,   -1789,
    1847,   -1847,  952,    -952,   1461,   -1461,  2687,   -2687,
    939,    -939,   2308,   -2308,  2437,   -2437,  2388,   -2388,
    733,    -733,   2337,   -2337,  268,    -268,   641,    -641,
    1584,   -1584,  2298,   -2298,  2037,   -2037,  3220,   -3220,
    375,    -375,   2549,   -2549,  2090,   -2090,  1645,   -1645,
    1063,   -1063,  319,    -319,   2773,   -2773,  757,    -757,
    2099,   -2099,  561,    -561,   2466,   -2466,  2594,   -2594,
    2804,   -2804,  1092,   -1092,  403,    -403,   1026,   -1026,
    1143,   -1143,  2150,   -2150,  2775,   -2775,  886,    -886,
    1722,   -1722,  1212,   -1212,  1874,   -1874,  1029,   -1029,
    2110,   -2110,  2935,   -2935,  885,    -885,   2154,   -2154]


def _bits_to_bytes(bit_array: list[int]) -> list[bytes]:

    if not all(x in [0, 1] for x in bit_array):
        raise ValueError("Each bit in array need to be 0 or 1")

    if len(bit_array) % 8 != 0 or len(bit_array) == 0:
        raise ValueError("Received array of bits needs to be a multiple of 8")

    bytes_array = []

    # chunk into arrays of 8 bits
    chunked = [bit_array[i:i+8] for i in range(0, len(bit_array), 8)]

    for array in chunked:
        curr = 0

        for i, val in enumerate(array):
            # least significant on the left, little endian
            curr += val*(2 ** i)

        # casting to whatever endian should not matter as we are using only one byte
        bytes_array.append(curr.to_bytes(1, "little"))

    return bytes_array


def _bytes_to_bits(byte_array: list[bytes]) -> list[int]:

    if not all(isinstance(x, bytes) for x in byte_array) or len(byte_array) == 0:
        raise ValueError("Requires an array of bytes.")

    bit_array = []
    for byte in byte_array:
        value = int.from_bytes(byte, "little")
        bit_values = [int(x) for x in f"{value:08b}"[::-1]]
        bit_array.extend(bit_values)

    return bit_array


def _byte_encode(int_array: list[int], d: int) -> list[bytes]:

    if len(int_array) != 256:
        raise ValueError(
            f"Provided array contained {len(int_array)} integers. Required length is 256")

    if not all(isinstance(x, int) for x in int_array):
        raise ValueError("int_array values must be integers")

    if (not d or not isinstance(d, int) or d > 12 or d < 1):
        raise ValueError(
            "Parameter d has to be integer between 1 and 12")

    m = 2**d if d < 12 else 3329    # The q param == 3329

    # check that provided int_array values are modulo of m
    if any(x >= m for x in int_array):
        raise ValueError(
            f"int_array contains an element exceeding the max value {m-1} for current d value {d}")

    bit_array = [0]*(len(int_array)*d)

    for i, val in enumerate(int_array):
        a = val
        for j in range(d):
            bit_array[i*d+j] = a % 2
            a = (a-bit_array[i*d+j]) // 2

    return _bits_to_bytes(bit_array)


def _byte_decode(bytes_array: list[bytes], d: int) -> list[int]:

    if not len(bytes_array) == 32*d:
        raise ValueError("Wrong bytes_array length")

    if not all(isinstance(x, bytes) for x in bytes_array):
        raise ValueError("bytes_array values must be bytes")

    if (not d or not isinstance(d, int) or d > 12 or d < 1):
        raise ValueError(
            "Parameter d has to be integer between 1 and 12")

    bit_array = _bytes_to_bits(bytes_array)

   # chunk into arrays of d bits
    chunked = [bit_array[i:i+d] for i in range(0, len(bit_array), d)]
    int_array = []
    for el in chunked:
        curr = 0
        for i, val in enumerate(el):
            curr += val*(2**i)
        int_array.append(curr)

    return int_array


def _compress(int_array: list[int], d: int) -> list[int]:

    compressed = []

    modifier = 2**d / Q_VAL

    for value in int_array:
        temp = modifier*value
        temp = math.ceil(
            temp) if temp % 1 == 0.5 else round(temp)

        compressed.append(temp % (2**d))

    return compressed


def _decompress(int_array: list[int], d: int) -> list[int]:

    decompressed = []

    modifier = Q_VAL/(2**d)

    for value in int_array:
        new_value = modifier*value
        new_value = math.ceil(
            new_value) if new_value % 1 == 0.5 else round(new_value)

        decompressed.append(new_value)

    return decompressed


def _prf(eta, s, b):

    if not isinstance(s, bytes) or not isinstance(b, bytes):
        raise TypeError("Both inputs of prf need to be bytes")

    if not isinstance(eta, int):
        raise TypeError("Eta needs to be of value int")

    if len(s) != 1 or len(b) != 32:
        raise ValueError(
            "The length of s needs to be 1 and the length of b needs to be 32")

    output = SHAKE256.new((s + b))
    output = output.read(64*eta)
    return [x.to_bytes(1, "little") for x in output]


def _sample_ntt(b: bytes):

    # Verify that the seed is exactly 34 bytes (seed + j idx + i idx)
    if len(b) != 34:
        raise ValueError(
            "Received an improper length, the seed must be exactly 34 bytes.")

    # input parameter b is a 34-byte seed
    ctx = SHAKE128.new()
    ctx = ctx.update(b)
    j = 0
    a = []
    while j < 256:
        c = ctx.read(3)
        d1 = c[0] + 256 * (c[1] % 16)
        d2 = (c[1] // 16) + 16 * c[2]
        if d1 < Q_VAL:
            a.append(d1)
            j += 1
        if d2 < Q_VAL and j < 256:
            a.append(d2)
            j += 1

    return a

# Computes NTT representation 𝑓 of the given polynomial 𝑓 ∈ 𝑅𝑞.
# The input of ntt is a set of 256 coefficients (array)


def _ntt(f):

    if len(f) != 256:
        raise ValueError(
            "Received an improper length, the seed must be exactly 256.")

    if not isinstance(f, list):
        raise TypeError("The input needs to be a list.")

    i = 1
    length = 128
    start = 0

    while length >= 2:
        for start in range(0, 256, length * 2):
            zeta = BITREV7_NTT_MODQ[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f[j + length]) % Q_VAL
                f[j + length] = (f[j] - t) % Q_VAL
                f[j] = (f[j] + t) % Q_VAL
        length //= 2
    return f


def _inverse_ntt(f):
    """
    Computes ̂the polynomial 𝑓 ∈ 𝑅𝑞 that corresponds to the given NTT representation 𝑓 ∈ 𝑇𝑞.
    input (f) is an array
    """

    if len(f) != 256:
        raise ValueError(
            "Received an improper length, the array length must be exactly 256.")

    if not isinstance(f, list):
        raise TypeError("The input needs to be a list.")

    length = 2
    i = 127
    start = 0
    while length <= 128:
        for start in range(0, 256, length * 2):
            zeta = BITREV7_NTT_MODQ[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % Q_VAL
                f[j + length] = (zeta * (f[j + length] - t)) % Q_VAL
        length *= 2

    for i in range(256):
        f[i] = (f[i]*3303) % Q_VAL

    return f


def _multiply_ntt(f, g):
    """
    input is two arrays f, g
    Computes the product (in the ring 𝑇𝑞) of two NTT representations.

    """

    if not isinstance(f, list) or not isinstance(g, list):
        raise TypeError("The input needs to be a list.")

    if len(f) != 256 or len(g) != 256:
        raise ValueError(
            "The length of the input arrays need to be exactly 256.")

    # Have to initialize the list first
    h = [0] * 256

    for i in range(0, 128):
        my_tuple = _base_case_multiply(
            f[2*i], f[2*i+1], g[2*i], g[2*i+1], BITREV7_NTT_MODQ_2[i])
        h[2*i] += my_tuple[0]
        h[2*i+1] = my_tuple[1]

        # output is an array, h
        # the output consists of the coefficients of the product of the inputs
    return h


# "Computes the product of two degree-one polynomials with respect to a quadratic modulus"
def _base_case_multiply(a0, a1, b0, b1, gamma):

    if not (type(a0) or type(a1) or type(b0) or type(b1) or type(gamma)) is int:
        raise TypeError("The inputs need to be of type int")

    c0 = ((a0 * b0) + (a1 * b1 * gamma)) % Q_VAL
    c1 = ((a0 * b1) + (a1 * b0)) % Q_VAL
    return (c0, c1)


def _sample_poly_cbd(b, eta):

    bits = _bytes_to_bits(b)
    f = [0] * 256  # initialize the array to the size of the fixed output

    for i in range(0, 256):
        for j in range(0, eta - 1):
            x = bits[2*i*eta + j]
        for j in range(0, eta - 1):
            y = bits[2*i*eta + eta + j]
        f[i] = (x - y) % Q_VAL
    return f


def _j(s: bytes) -> bytes:
    """
    Function J: J(s) = SHAKE256(s, 8 * 32)
    """
    shake256 = hashlib.shake_256()
    shake256.update(s)
    return shake256.digest(32)  # Output 32 bytes


def _h(s: bytes) -> bytes:
    """
    Function H: H(s) = SHA3-256(s)
    """
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(s)
    return sha3_256.digest()  # 32 bytes


def _g(c: bytes) -> tuple[bytes, bytes]:
    """
    Function G: G(c) = SHA3-512(c), then split into two 32-byte outputs (a, b)
    """
    sha3_512 = hashlib.sha3_512()
    sha3_512.update(c)
    digest = sha3_512.digest()  # 64 bytes total
    a = digest[:32]  # First 32 bytes
    b = digest[32:]  # Last 32 bytes
    return a, b


def _encode_lists(data: list[list[int]], d: int) -> bytes:
    """
    Helper to encode and join multiple lists to bytes
    """
    mod = 2**d if d < 12 else Q_VAL

    cleaned = [[int(i) % mod for i in arr]
               for arr in data]  # remove numpy int types
    byte_lists = [_byte_encode(arr, d) for arr in cleaned]

    return b"".join([b for arr in byte_lists for b in arr])


def _k_pke_key_gen(random_bytes: bytes, k: int, n1: int) -> tuple[bytes, bytes]:  # pylint: disable=too-many-locals
    """
    Key generator.

    Args:
        random_bytes (bytes): random bytes.
        k (int): Parameter set k-value

    Returns:
        encryption_key, decryption_key (bytes,bytes)
    """
    if not len(random_bytes) == 32:
        raise ValueError("KeyGen requires 32 random bytes")

    added_random_bytes = random_bytes + k.to_bytes(1, "little")

    seed1, seed2 = _g(added_random_bytes)

    n_val = 0

    matrix_a = [[0]*k]*k
    for i in range(k):
        for j in range(k):
            matrix_a[i][j] = _sample_ntt(
                seed1+j.to_bytes(1, "little")+i.to_bytes(1, "little"))

    s_samples = [0]*k
    for i in range(k):
        s_samples[i] = _sample_poly_cbd(
            _prf(n1, n_val.to_bytes(1, "little"), seed2),
            n1
        )
        n_val += 1

    e_samples = [0]*k
    for i in range(k):
        e_samples[i] = _sample_poly_cbd(
            _prf(n1, n_val.to_bytes(1, "little"), seed2),
            n1
        )
        n_val += 1

    s_hat = [_ntt(s) for s in s_samples]
    e_hat = [_ntt(e) for e in e_samples]

    t_hat = np.einsum("ijk,ik->ik", matrix_a, s_hat) + e_hat

    encryption_key = _encode_lists(t_hat, 12) + seed1
    decryption_key = _encode_lists(s_hat, 12)

    return encryption_key, decryption_key


def _ml_kem_gey_gen_internal(d_random: bytes, z_random: bytes, k: int, n1: int):
    """
    KeyGen internal.
    """

    ek_pke, dk_pke = _k_pke_key_gen(d_random, k, n1)

    dk = dk_pke+ek_pke+_h(ek_pke)+z_random

    return ek_pke, dk


def ml_kem_gey_gen(k: int, n1: int):
    """
    KeyGen.
    """
    # TODO: check fips compliance for secrets.token_bytes for rbg
    # and change it for better if it is not appropriate
    d_random = token_bytes(32)
    z_random = token_bytes(32)

    if not d_random or not z_random or len(d_random) != 32 or len(z_random) != 32:
        raise ValueError("Random byte generation failed")

    return _ml_kem_gey_gen_internal(d_random, z_random, k, n1)


def _k_pke_encrypt(encrypt_key_bytes: bytes, message: bytes, random_bytes: bytes, pm_set) -> bytes:  # pylint: disable=too-many-locals
    """
    Encrypt.
    """
    encryption_key = [b.to_bytes(1, "little") for b in encrypt_key_bytes]
    n_val = 0
    t_hat = []
    for i in range(pm_set.k):
        t_hat.append(
            _byte_decode(encryption_key[384*i:384*(i+1)], 12)
        )
    seed = encrypt_key_bytes[384*pm_set.k:]
    matrix_a = [[0]*pm_set.k]*pm_set.k
    for i in range(pm_set.k):
        for j in range(pm_set.k):
            matrix_a[i][j] = _sample_ntt(
                seed+j.to_bytes(1, "little")+i.to_bytes(1, "little"))

    y_samples = [0]*pm_set.k
    for i in range(pm_set.k):
        y_samples[i] = _sample_poly_cbd(
            _prf(pm_set.n1, n_val.to_bytes(1, "little"), random_bytes),
            pm_set.n1
        )
        n_val += 1

    e_samples = [0]*pm_set.k
    for i in range(pm_set.k):
        e_samples[i] = _sample_poly_cbd(
            _prf(pm_set.n2, n_val.to_bytes(1, "little"), random_bytes),
            pm_set.n2
        )
        n_val += 1

    e2_sample = _sample_poly_cbd(
        _prf(pm_set.n2, n_val.to_bytes(1, "little"), random_bytes), pm_set.n2)

    y_hat = [_ntt(y) for y in y_samples]
    u_matrix = [_inverse_ntt(list(f)) for f in np.einsum(
        "ijk,ik->ik", matrix_a, y_hat)] + np.array(e_samples)

    mu = _decompress(
        _byte_decode([b.to_bytes(1, "little") for b in message], 1), 1)
    v_list = _inverse_ntt(list(np.einsum("ij,ij->j", t_hat, y_hat))) + \
        np.array(e2_sample) + np.array(mu)
    v_list = [int(x) for x in v_list]

    c1 = _encode_lists([_compress(x, pm_set.du) for x in u_matrix], pm_set.du)
    c2 = b"".join(b for b in _byte_encode(
        _compress(v_list, pm_set.dv), pm_set.dv))

    cipher = c1+c2

    return cipher


def _k_pke_decrypt(decryption_key: bytes, cipher: bytes, pm_set) -> bytes:
    """
    Decrypt.
    """
    cipher_byte_array = [b.to_bytes(1, "little") for b in cipher]
    c1 = cipher_byte_array[:32*pm_set.du*pm_set.k]
    c2 = cipher_byte_array[32*pm_set.du*pm_set.k:]

    chunk_size_c1 = len(c1) // pm_set.k
    chunked_c1 = [c1[i*chunk_size_c1:(i+1)*chunk_size_c1]
                  for i in range(pm_set.k)]
    u_list = [_decompress(_byte_decode(x, pm_set.du), pm_set.du)
              for x in chunked_c1]
    v_list = _decompress(_byte_decode(c2, pm_set.dv), pm_set.dv)

    decryption_key_byte_array = [b.to_bytes(
        1, "little") for b in decryption_key]
    s_hat = [_byte_decode(decryption_key_byte_array[i*384:(i+1)*384], 12)
             for i in range(pm_set.k)]

    u_nttd = [_ntt(x) for x in u_list]
    dot_result = [int(x) for x in np.einsum("ij,ij->j", s_hat, u_nttd)]
    w_list = np.array(v_list) - np.array(_inverse_ntt(dot_result))
    w_list = [int(x) for x in w_list]

    message = _byte_encode(_compress(w_list, 1), 1)
    joined = b"".join(message)

    return joined


def _ml_kem_encaps_internal(encryption_key: bytes, randomness: bytes, pm_set):
    """
    Encaps internal.
    """
    key, rand = _g(randomness+_h(encryption_key))

    cipher = _k_pke_encrypt(encryption_key, randomness, rand, pm_set)

    return key, cipher


def ml_kem_encaps(ek: bytes, pm_set):
    """
    Encaps.
    """
    random_bytes = token_bytes(32)

    if not random_bytes or len(random_bytes) != 32:
        raise ValueError("Random byte generation failed")

    key, cipher = _ml_kem_encaps_internal(ek, random_bytes, pm_set)
    return key, cipher


def _ml_kem_decaps_internal(dk: bytes, cipher: bytes, pm_set):
    """
    Decaps internal.
    """
    dk_pke = dk[:384*pm_set.k]
    ek_pke = dk[384*pm_set.k:(768*pm_set.k)+32]

    h_val = dk[768*pm_set.k+32:(768*pm_set.k)+64]
    z_val = dk[768*pm_set.k+64:(768*pm_set.k)+96]

    message_bytes = _k_pke_decrypt(dk_pke, cipher, pm_set)
    shared_secret_key, randomness = _g(message_bytes+h_val)

    key_check = _j(z_val+cipher)

    cipher_check = _k_pke_encrypt(ek_pke, message_bytes, randomness, pm_set)

    if cipher != cipher_check:
        # if ciphertexts do not match, “implicitly reject” (from FIPS 203)
        shared_secret_key = key_check

    return shared_secret_key


def ml_kem_decaps(dk: bytes, cipher: bytes, pm_set) -> bytes:
    """
    Decaps.
    """
    return _ml_kem_decaps_internal(dk, cipher, pm_set)
