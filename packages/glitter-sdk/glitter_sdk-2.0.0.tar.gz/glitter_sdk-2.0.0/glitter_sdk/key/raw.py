from __future__ import annotations

import hashlib

from ecdsa import SECP256k1, SigningKey
from ecdsa.util import sigencode_string_canonize

from .key import Key
from glitter_sdk.util.encrypt.eth.ethereum import HDPrivateKey
__all__ = ["RawKey"]

from ..core import PublicKey, SimplePublicKey
from ..core import PublicKey, EthSimplePublicKey
from glitter_sdk.util.encrypt.eth.ethereum import sha3
import coincurve
from coincurve._libsecp256k1 import ffi
from coincurve._libsecp256k1 import lib

class RawKey(Key):
    """RawKey directly uses a raw (plaintext) private key in memory, and provides
    the implementation for signing with ECDSA on curve Secp256k1.

    Args:
        private_key (bytes): private key in bytes
    """

    private_key: bytes
    """Private key, in bytes."""

    @classmethod
    def from_hex(cls, private_key_hex: str) -> RawKey:
        """Create a new RawKey from a hex-encoded private key string.

        Args:
            private_key_hex (str): hex-encoded private key
        """
        return cls(bytes.fromhex(private_key_hex))

    def __init__(self, private_key: HDPrivateKey):
        public_key = private_key.public_key.compressed_bytes
        super().__init__(EthSimplePublicKey(key=public_key))
        self.private_key = bytes.fromhex(private_key._key.to_hex())


    def sign(self, payload: bytes) -> bytes:
        """Signs the data payload using ECDSA and curve Secp256k1 with the private key as
        the signing key.

        Args:
            payload (bytes): data to sign
        """
        digest = sha3(payload)
        return self.evmSign(digest)

    def evmSign(self, msg: bytes) -> bytes:
        key = coincurve.PrivateKey(self.private_key)
        nonce = (lib.secp256k1_nonce_function_rfc6979, ffi.NULL)
        return key.sign_recoverable(msg, hasher=None, custom_nonce=nonce)
