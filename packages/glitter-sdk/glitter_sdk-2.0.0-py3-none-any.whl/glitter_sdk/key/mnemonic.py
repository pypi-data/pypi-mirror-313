from __future__ import annotations
from .raw import RawKey
from glitter_sdk.util.encrypt.eth.ethereum import HDKey
from glitter_sdk.util.encrypt.eth.ethereum import HDPrivateKey

__all__ = ["MnemonicKey", "GLITTER_COIN_TYPE"]

GLITTER_COIN_TYPE = 60


class MnemonicKey(RawKey):
    """A MnemonicKey derives a private key using a BIP39 mnemonic seed phrase, and provides key-derivation options based on the BIP44 HD path standard.

    .. note:: You can change ``coin_type`` to 118 to derive the key for a legacy Glitter
        wallet (shares ``coin_type`` with ATOM).

    Args:
        mnemonic (str, optional): space-separated mnemonic seed phrase. If not provided,
            a 24-word mnemonic will be generated.
        account (int, optional): HD path parameter - account number.
        index (int, optional): HD path parameter - account index.
        coin_type (int, optional): HD path parameter - coin type.
    """

    mnemonic: str
    """Mnemonic key phrase associated with the account (space-separated)."""

    account: int
    """HD path parameter: account number."""

    index: int
    """HD path parameter: account index."""

    coin_type: int
    """HD path parameter: coin type"""

    @property
    def hd_path(self) -> str:
        """Returns the BIP32 HD path for key-derivation:

        ``m/44'/COIN_TYPE'/ACCOUNT'/0/INDEX'``

        Returns:
            str: full BIP32 HD path
        """
        return f"m/44'/{self.coin_type}'/{self.account}'/0/{self.index}"

    def __init__(
        self,
        mnemonic: str = None,
        account: int = 0,
        index: int = 0,
        coin_type: int = GLITTER_COIN_TYPE,
    ):
        self.coin_type = coin_type
        self.account = account
        self.index = index

        master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
        root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
        acct_priv_key = root_keys[-1]
        acct_pub_key = HDKey.from_b58check(acct_priv_key.to_b58check())
        keys = HDKey.from_path(acct_pub_key, f'{0}/{index}')

        # eth_address = keys[-1].public_key.address()
        # self.private_key = bytes.fromhex(keys[-1]._key.to_hex())
        # self.evmos_address = eth_to_evmos(eth_address)
        # self.public_key = keys[-1].public_key.compressed_bytes
        super().__init__(keys[-1])

        self.mnemonic = mnemonic
