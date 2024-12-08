"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import Optional

import attr
from glitter_proto.ethermint.types.v1 import EthAccount as EthAccount_pb

from ....core import AccAddress
from ....util.json import JSONSerializable
from ...public_key import PublicKey
from .base_account import BaseAccount

__all__ = ["EthAccount"]


@attr.s
class EthAccount(JSONSerializable):
    """
    Stores information about an account.

    Args:
        base_account (BaseAccount): base_account
        code_hash (str): code_hash
    """

    type_amino = "cosmos-sdk/BaseAccount"
    type_url = "/ethermint.types.v1.EthAccount"

    # base_account: BaseAccount = attr.ib(converter=BaseAccount, default=None)
    base_account: BaseAccount = attr.ib()
    """"""
    code_hash: str = attr.ib(converter=str, default=None)
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "base_account": self.base_account,
                "code_hash": str(self.code_hash),
            },
        }

    @classmethod
    def from_amino(cls, amino: dict) -> EthAccount:
        amino = amino["value"] if "value" in amino else amino
        return cls(
            base_account=amino["base_account"],
            code_hash=amino["code_hash"],
        )

    def get_account_number(self) -> int:
        return self.base_account.account_number

    def get_sequence(self) -> int:
        return self.base_account.sequence

    def get_public_key(self) -> PublicKey:
        return self.base_account.public_key

    def to_data(self) -> dict:
        return {
            "base_account": self.base_account.to_data(),
            "code_hash": str(self.code_hash),
        }

    @classmethod
    def from_data(cls, data: dict) -> EthAccount:
        return cls(
            base_account=BaseAccount.from_data(data.get("base_account")),
            code_hash=data.get("code_hash")
        )

    @classmethod
    def from_proto(cls, proto: EthAccount_pb) -> EthAccount:
        return cls(
            base_account=proto.base_account,
            code_hash=proto.code_hash,
        )

    def to_proto(self) -> EthAccount_pb:
        return EthAccount_pb(
            base_account=self.base_account,
            code_hash=self.code_hash,
        )
