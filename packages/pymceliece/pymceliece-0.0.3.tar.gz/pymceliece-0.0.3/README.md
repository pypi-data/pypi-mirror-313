# pymceliece
A Python wrapper for the libmceliece microlibrary

# Installation
## Dependencies
pymceliece depends only on libmceliece (which also depends on libcpucycles and
librandombytes), available [here](https://lib.mceliece.org)

# API
## Instantiated parameters
The API follows the libmceliece API. It implements the following parameter sets:

- mceliece8192128
- mceliece6960119
- mceliece6688128
- mceliece8192128
- mceliece460896
- mceliece348864
- mceliece6960119f
- mceliece6688128f
- mceliece8192128f
- mceliece460896f
- mceliece348864f

Each has the following constants defined:
- mceliecexxxxxxx.PUBLICKEYBYTES
Length of the public key
- mceliecexxxxxxx.SECRETKEYBYTES
Length of the private key
- mceliecexxxxxxx.CIPHERTEXTBYTES
Length of the ciphertext
- mceliecexxxxxxx.BYTES
Length of the session key

## Usage
For each instantiation the following functions are available:
### mcelieceXXXXXXX.keypair() -> Tuple[bytes, bytes]

Randomly generates a McEliece secret key and its corresponding public key.

Example:
```python
>>> from pymceliece import mceliece6960119
>>> pk, sk = mceliece6960119.keypair()
```

### mcelieceXXXXXXX.enc(pk: bytes) -> Tuple[bytes, bytes]
Randomly generates a ciphertext and the corresponding session key given a
public key pk.

Example:
```python
>>> from pymceliece import mceliece8192128f
>>> pk, _ = mceliece8192128f.keypair()
>>> c, k = mceliece8192128f.enc(pk)
```

### mcelieceXXXXXXX.dec(c: bytes, pk: bytes) -> bytes
Given a McEliece secret key sk and a ciphertext c encapsulated to sk's
corresponding public key pk, computes the session key k.

Example:
```python
>>> from pymceliece import mceliece348864f
>>> pk, sk = mceliece348864f.keypair()
>>> c, k = mceliece348864f.enc(pk)
>>> mceliece348864f.dec(c, sk) == k
True
```
