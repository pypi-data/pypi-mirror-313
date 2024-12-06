from _typeshed import Incomplete
from ctypes import byref as byref
from typing import Tuple

class _McEliece:
    PUBLICKEYBYTES: Incomplete
    SECRETKEYBYTES: Incomplete
    CIPHERTEXTBYTES: Incomplete
    BYTES: Incomplete
    def __init__(self, params: str) -> None: ...
    def keypair(self) -> Tuple[bytes, bytes]: ...
    def enc(self, pk: bytes) -> Tuple[bytes, bytes]: ...
    def dec(self, c: bytes, sk: bytes) -> bytes: ...

mceliece8192128: Incomplete
mceliece6960119: Incomplete
mceliece6688128: Incomplete
mceliece460896: Incomplete
mceliece348864: Incomplete
mceliece6960119f: Incomplete
mceliece6688128f: Incomplete
mceliece8192128f: Incomplete
mceliece460896f: Incomplete
mceliece348864f: Incomplete
