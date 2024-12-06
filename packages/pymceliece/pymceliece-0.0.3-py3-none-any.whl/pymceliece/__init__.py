from ctypes import (
    CDLL,
    RTLD_GLOBAL,
    byref,
    c_char_p,
    c_int,
    create_string_buffer,
    util,
)
from typing import Tuple

_librb = CDLL(util.find_library("randombytes"), mode=RTLD_GLOBAL)

_lib = CDLL(util.find_library("mceliece"))

if not _lib._name:
    raise ValueError("Unable to find libmceliece")


class _McEliece:
    def __init__(self, params: str) -> None:
        self._params = params
        try:
            pklen, sklen, clen, klen = _PARAMS[params]
            self.PUBLICKEYBYTES: int = pklen
            self.SECRETKEYBYTES: int = sklen
            self.CIPHERTEXTBYTES: int = clen
            self.BYTES: int = klen

        except KeyError:
            raise

        self._c_keypair = getattr(_lib, f"mceliece_kem_{params}_keypair")
        self._c_keypair.argtypes = [c_char_p, c_char_p]
        self._c_keypair.restype = None

        self._c_enc = getattr(_lib, f"mceliece_kem_{params}_enc")
        self._c_enc.argtypes = [c_char_p, c_char_p, c_char_p]
        self._c_enc.restype = c_int

        self._c_dec = getattr(_lib, f"mceliece_kem_{params}_dec")
        self._c_dec.argtypes = [c_char_p, c_char_p, c_char_p]
        self._c_dec.restype = c_int

    def keypair(self) -> Tuple[bytes, bytes]:
        """Randomly generates a McEliece secret key and its corresponding
        public key.

        Example:
        >>> from pymceliece import mceliece6960119
        >>> pk, sk = mceliece6960119.keypair()

        """

        sk = create_string_buffer(self.SECRETKEYBYTES)
        pk = create_string_buffer(self.PUBLICKEYBYTES)
        if self._c_keypair(pk, sk):
            raise Exception("keypair failed")
        return pk.raw, sk.raw

    def enc(self, pk: bytes) -> Tuple[bytes, bytes]:
        """Randomly generates a ciphertext and the corresponding session key
        given a public key pk.

        Example:
        >>> from pymceliece import mceliece8192128f
        >>> pk, _ = mceliece8192128f.keypair()
        >>> c, k = mceliece8192128f.enc(pk)

        """
        if not isinstance(pk, bytes):
            raise TypeError("public key must be bytes")
        if len(pk) != self.PUBLICKEYBYTES:
            raise ValueError("invalid public key length")

        c = create_string_buffer(self.CIPHERTEXTBYTES)
        k = create_string_buffer(self.BYTES)
        pk_arr = create_string_buffer(pk)
        if self._c_enc(c, k, pk_arr):
            raise Exception("encapsulation failed")
        return c.raw, k.raw

    def dec(self, c: bytes, sk: bytes) -> bytes:
        """Given a McEliece secret key sk and a ciphertext c encapsulated to
        sk's corresponding public key pk, computes the session key k

        Example:
        >>> from pymceliece import mceliece348864f
        >>> pk, sk = mceliece348864f.keypair()
        >>> c, k = mceliece348864f.enc(pk)
        >>> mceliece348864f.dec(c, sk) == k
        True
        """

        if not (isinstance(c, bytes) and isinstance(sk, bytes)):
            raise TypeError("c and sk must be bytes")
        if not len(c) == self.CIPHERTEXTBYTES:
            raise ValueError("c is wrong length")
        if not len(sk) == self.SECRETKEYBYTES:
            raise ValueError("sk is wrong length")

        c_arr = create_string_buffer(c)
        sk_arr = create_string_buffer(sk)
        k = create_string_buffer(self.BYTES)
        if self._c_dec(k, c_arr, sk_arr):
            raise Exception("decapsulation failed")
        return k.raw


###############################################################################
# CONSTANTS
###############################################################################

_KLEN = 32
_PARAMS = {  # (PUBLICKEYBYTES, SECRETKEYBYTES, CIPHERTEXTBYTES, BYTES)
    "6960119": (1047319, 13948, 194, _KLEN),
    "6688128": (1044992, 13932, 208, _KLEN),
    "8192128": (1357824, 14120, 208, _KLEN),
    "460896": (524160, 13608, 156, _KLEN),
    "348864": (261120, 6492, 96, _KLEN),
    "6960119f": (1047319, 13948, 194, _KLEN),
    "6688128f": (1044992, 13932, 208, _KLEN),
    "8192128f": (1357824, 14120, 208, _KLEN),
    "460896f": (524160, 13608, 156, _KLEN),
    "348864f": (261120, 6492, 96, _KLEN),
}


mceliece8192128 = _McEliece("8192128")
mceliece6960119 = _McEliece("6960119")
mceliece6688128 = _McEliece("6688128")
mceliece8192128 = _McEliece("8192128")
mceliece460896 = _McEliece("460896")
mceliece348864 = _McEliece("348864")
mceliece6960119f = _McEliece("6960119f")
mceliece6688128f = _McEliece("6688128f")
mceliece8192128f = _McEliece("8192128f")
mceliece460896f = _McEliece("460896f")
mceliece348864f = _McEliece("348864f")
